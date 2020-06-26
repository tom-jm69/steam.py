# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2020 James

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import json
import logging
import re
from base64 import b64encode
from sys import version_info
from time import time
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    List,
    Optional,
    Tuple,
    Union,
)

import aiohttp
import rsa
from bs4 import BeautifulSoup
from yarl import URL as _URL

from . import __version__, errors
from .models import URL
from .user import ClientUser

if TYPE_CHECKING:
    from .client import Client
    from .image import Image

log = logging.getLogger(__name__)


async def json_or_text(r: aiohttp.ClientResponse) -> Optional[Any]:
    try:
        return await r.json()
    except aiohttp.ContentTypeError:  # steam is too inconsistent to do this properly
        return await r.text()


class Route:
    def __init__(self, path):
        self.url = _URL(f'{self.BASE}{path}')

    def __str__(self):
        return str(self.url)


class APIRoute(Route):
    def __init__(self, path):
        self.url = _URL(f'{URL.API}{path}{"/v1" if not path.endswith("v2") else ""}')


class CRoute(Route):
    BASE = URL.COMMUNITY


class HTTPClient:
    """The HTTP Client that interacts with the Steam web API."""

    SUCCESS_LOG = '{method} {url} has received {text}'
    REQUEST_LOG = '{method} {url} with {payload} has returned {status}'

    def __init__(self,
                 loop: asyncio.AbstractEventLoop,
                 session: aiohttp.ClientSession,
                 client: 'Client'):
        self._loop = loop
        self._session = session
        self._client = client
        self._lock = asyncio.Lock()

        self.username = None
        self.password = None
        self.api_key = None
        self.shared_secret = None
        self._one_time_code = None

        self.session_id = None
        self.user = None
        self.logged_in = False
        self._steam_id = None
        self.user_agent = f'steam.py/{__version__} client (https://github.com/Gobot1234/steam.py), ' \
                          f'Python/{version_info[0]}.{version_info[1]}, aiohttp/{aiohttp.__version__}'

    def recreate(self) -> None:
        if self._session.closed:
            self._session = aiohttp.ClientSession(loop=self._loop)

    async def request(self, method: str, url: Union[APIRoute, CRoute, str],
                      **kwargs) -> Optional[Any]:  # adapted from d.py
        kwargs['headers'] = {
            "User-Agent": self.user_agent,
            **kwargs.get('headers', {})
        }

        async with self._lock:
            for tries in range(5):
                async with self._session.request(method, str(url), **kwargs) as r:
                    payload = kwargs.get('json')
                    log.debug(self.REQUEST_LOG.format(
                        method=method,
                        url=url,
                        payload=f'PAYLOAD: {payload}',
                        status=r.status)
                    )

                    # even errors have text involved in them so this is safe to call
                    data = await json_or_text(r)

                    # the request was successful so just return the text/json
                    if 300 > r.status >= 200:
                        log.debug(f'{method} {url} has received {data}')
                        return data

                    # we are being rate limited
                    if r.status == 429:
                        # I haven't been able to get any X-Retry-After headers
                        # from the API but we should probably still handle it
                        try:
                            await asyncio.sleep(float(r.headers['X-Retry-After']))
                        except KeyError:  # steam being un-helpful as usual
                            await asyncio.sleep(2 ** tries)
                        continue

                    # we've received a 500 or 502, an unconditional retry
                    if r.status in {500, 502}:
                        await asyncio.sleep(1 + tries * 3)
                        continue

                    if r.status == 401:
                        # api key either got revoked or it was never valid
                        if not data:
                            raise errors.HTTPException(r, data)
                        if 'Access is denied. Retrying will not help. Please verify your <pre>key=</pre>' in data:
                            # time to fetch a new key
                            self.api_key = kwargs['key'] = await self.get_api_key()
                            continue
                            # retry with our new key

                    # the usual error cases
                    if r.status == 403:
                        raise errors.Forbidden(r, data)
                    if r.status == 404:
                        raise errors.NotFound(r, data)
                    else:
                        raise errors.HTTPException(r, data)

            # we've run out of retries, raise
            raise errors.HTTPException(r, data)

    def connect_to_cm(self, cm: str) -> Awaitable:
        headers = {
            "User-Agent": self.user_agent
        }
        return self._session.ws_connect(f'wss://{cm}/cmsocket/', timeout=60, headers=headers)

    async def login(self, username: str, password: str, api_key: str, shared_secret: str = None) -> None:
        self.username = username
        self.password = password
        self.shared_secret = shared_secret

        login_response = await self._send_login_request()

        if 'captcha_needed' in login_response:
            raise errors.LoginError('A captcha code is required, please try again later')
        if not login_response['success']:
            raise errors.InvalidCredentials(login_response['message'])

        data = login_response.get('transfer_parameters')
        if data is None:
            raise errors.LoginError('Cannot perform redirects after login, no parameters fetched. '
                                    'The Steam API likely is down, please try again later.')

        for url in login_response['transfer_urls']:
            await self.request('POST', url=url, data=data)
        self.logged_in = True

        if api_key is None:
            self.api_key = self._client.api_key = await self.get_api_key()
        else:
            self.api_key = self._client.api_key = api_key
        cookies = self._session.cookie_jar.filter_cookies(_URL(URL.COMMUNITY))
        self.session_id = cookies['sessionid'].value

        id64 = login_response['transfer_parameters']['steamid']
        resp = await self.get_user(id64)
        data = resp['response']['players'][0]
        self.user = ClientUser(state=self._client._connection, data=data)
        self._client._connection._users[self.user.id64] = self.user
        self._client.dispatch('login')

    async def logout(self) -> None:
        log.debug('Logging out of session')
        payload = {
            "sessionid": self.session_id
        }
        await self.request('POST', CRoute('/login/logout'), data=payload)
        self.logged_in = False
        self._client.dispatch('logout')

    async def _get_rsa_params(self, current_repetitions: int = 0) -> Tuple[rsa.PublicKey, int]:
        payload = {
            "username": self.username,
            "donotcache": int(time() * 1000)
        }
        try:
            key_response = await self.request('POST', CRoute('/login/getrsakey'), data=payload)
        except Exception as e:
            raise errors.LoginError from e
        try:
            rsa_mod = int(key_response['publickey_mod'], 16)
            rsa_exp = int(key_response['publickey_exp'], 16)
            rsa_timestamp = key_response['timestamp']
        except KeyError:
            if current_repetitions < 5:
                return await self._get_rsa_params(current_repetitions + 1)
            raise ValueError('could not obtain rsa-key')
        else:
            return rsa.PublicKey(rsa_mod, rsa_exp), rsa_timestamp

    async def _send_login_request(self) -> dict:
        rsa_key, timestamp = await self._get_rsa_params()
        encrypted_password = b64encode(rsa.encrypt(self.password.encode('utf-8'), rsa_key))
        payload = {
            "username": self.username,
            "password": encrypted_password.decode(),
            "emailauth": '',
            "emailsteamid": '',
            "twofactorcode": self._one_time_code or '',
            "captchagid": '-1',
            "captcha_text": '',
            "loginfriendlyname": self.user_agent,
            "rsatimestamp": timestamp,
            "remember_login": True,
            "donotcache": int(time() * 1000),
        }
        try:
            login_response = await self.request('POST', CRoute('/login/dologin'), data=payload)
            if login_response['requires_twofactor']:
                self._one_time_code = await self._client.code()
                return await self._send_login_request()
            return login_response
        except Exception as e:
            raise errors.LoginError from e

    def get_user(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamids": user_id64
        }
        return self.request('GET', APIRoute('/ISteamUser/GetPlayerSummaries/v2'), params=params)

    async def get_users(self, user_id64s: List[int]) -> List[dict]:
        ret = []

        def chunk():  # chunk the list into 100 element sub-lists for the requests
            for i in range(0, len(user_id64s), 100):
                yield user_id64s[i:i + 100]

        for sublist in chunk():
            for _ in sublist:
                params = {
                    "key": self.api_key,
                    "steamids": ','.join(map(str, sublist))
                }

            full_resp = await self.request('GET', APIRoute('/ISteamUser/GetPlayerSummaries/v2'), params=params)
            ret.extend(full_resp['response']['players'])
        return ret

    def add_user(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "accept_invite": 0
        }
        return self.request('POST', CRoute('/actions/AddFriendAjax'), data=payload)

    def remove_user(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
        }
        return self.request('POST', CRoute('/actions/RemoveFriendAjax'), data=payload)

    def block_user(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "block": 1
        }
        return self.request('POST', CRoute('/actions/BlockUserAjax'), data=payload)

    def unblock_user(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "block": 0
        }
        return self.request('POST', CRoute('/actions/BlockUserAjax'), data=payload)

    def accept_user_invite(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "accept_invite": 1
        }
        return self.request('POST', CRoute('/actions/AddFriendAjax'), data=payload)

    def decline_user_invite(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "accept_invite": 0
        }
        return self.request('POST', CRoute('/actions/IgnoreFriendInviteAjax'), data=payload)

    def get_user_games(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid": user_id64,
            "include_appinfo": 1,
            "include_played_free_games": 1
        }
        return self.request('GET', APIRoute('/IPlayerService/GetOwnedGames'), params=params)

    def get_user_inventory(self, user_id64: int, app_id: int, context_id: int) -> Awaitable:
        params = {
            "count": 5000,
        }
        return self.request('GET', CRoute(f'/inventory/{user_id64}/{app_id}/{context_id}'), params=params)

    def get_user_escrow(self, user_id64: int, token: Optional[str]) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid_target": user_id64,
            "trade_offer_access_token": token if token is not None else ''
        }
        return self.request('GET', APIRoute('/IEconService/GetTradeHoldDurations'), params=params)

    async def get_friends(self, user_id64: int) -> List[dict]:
        params = {
            "key": self.api_key,
            "steamid": user_id64,
            "relationship": 'friend'
        }
        friends = await self.request('GET', APIRoute('/ISteamUser/GetFriendList'), params=params)
        return await self.get_users([friend['steamid'] for friend in friends['friendslist']['friends']])

    def get_trade_offers(self, active_only: bool = True,
                         sent: bool = True, received: bool = True) -> Awaitable:
        params = {
            "key": self.api_key,
            "active_only": int(active_only),
            "get_sent_offers": int(sent),
            "get_descriptions": 1,
            "get_received_offers": int(received)
        }
        return self.request('GET', APIRoute('/IEconService/GetTradeOffers'), params=params)

    def get_trade_history(self, limit: int, previous_time: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "max_trades": limit,
            "get_descriptions": 1,
            "include_total": 1,
            "start_after_time": previous_time or 0
        }
        return self.request('GET', APIRoute('/IEconService/GetTradeHistory'), params=params)

    def get_trade(self, trade_id: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "tradeofferid": trade_id,
            "get_descriptions": 1
        }
        return self.request('GET', APIRoute('/IEconService/GetTradeOffer'), params=params)

    def accept_user_trade(self, user_id64: int, trade_id: int) -> Awaitable:
        payload = {
            'sessionid': self.session_id,
            'tradeofferid': trade_id,
            'serverid': 1,
            'partner': user_id64,
            'captcha': ''
        }
        headers = {'Referer': f'{URL.COMMUNITY}/tradeoffer/{trade_id}'}
        return self.request('POST', CRoute(f'/tradeoffer/{trade_id}/accept'), data=payload, headers=headers)

    def decline_user_trade(self, trade_id: int) -> Awaitable:
        payload = {
            "key": self.api_key,
            "tradeofferid": trade_id
        }
        return self.request('POST', APIRoute('/IEconService/DeclineTradeOffer'), data=payload)

    def cancel_user_trade(self, trade_id: int) -> Awaitable:
        payload = {
            "key": self.api_key,
            "tradeofferid": trade_id
        }
        return self.request('POST', APIRoute('/IEconService/CancelTradeOffer'), data=payload)

    def send_trade_offer(self, user_id64: int, user_id: int,
                         to_send: List[dict], to_receive: List[dict],
                         token: Optional[str], offer_message: str,
                         **kwargs) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "serverid": 1,
            "partner": user_id64,
            "tradeoffermessage": offer_message,
            "json_tradeoffer": json.dumps({
                "newversion": True,
                "version": 4,
                "me": {
                    "assets": to_send,
                    "currency": [],
                    "ready": False
                },
                "them": {
                    "assets": to_receive,
                    "currency": [],
                    "ready": False
                }
            }),
            "captcha": '',
            "trade_offer_create_params": json.dumps({
                'trade_offer_access_token': token
            }) if token is not None else {}
        }
        payload.update(**kwargs)
        headers = {'Referer': f'{URL.COMMUNITY}/tradeoffer/new/?partner={user_id}'}
        return self.request('POST', CRoute('/tradeoffer/new/send'), data=payload, headers=headers)

    def send_counter_trade_offer(self, trade_id: int, user_id64: int, user_id: int,
                                 to_send: List[dict], to_receive: List[dict],
                                 token: Optional[str], offer_message: str) -> Awaitable:
        return self.send_trade_offer(user_id64, user_id, to_send, to_receive,
                                     token, offer_message, trade_id=trade_id)

    def get_cm_list(self, cell_id: int) -> Awaitable:
        params = {
            "cellid": cell_id
        }
        return self.request('GET', APIRoute('/ISteamDirectory/GetCMList'), params=params)

    def get_comments(self, id64: int, comment_type: str, limit: int = None) -> Awaitable:
        params = {
            "start": 0,
            "totalcount": 9999999999
        }
        if limit is None:
            params["count"] = 9999999999
        else:
            params["count"] = limit
        return self.request('GET', CRoute(f'/comment/{comment_type}/render/{id64}'), params=params)

    def post_comment(self, id64: int, comment_type: str, content: str) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "comment": content,
        }
        return self.request('POST', CRoute(f'/comment/{comment_type}/post/{id64}'), data=payload)

    def delete_comment(self, id64: int, comment_id: int, comment_type: str) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "gidcomment": comment_id,
        }
        return self.request('POST', CRoute(f'/comment/{comment_type}/delete/{id64}'), data=payload)

    def report_comment(self, id64: int, comment_id: int, comment_type: str) -> Awaitable:
        payload = {
            "gidcomment": comment_id,
            "hide": 1
        }
        return self.request('POST', CRoute(f'/comment/{comment_type}/hideandreport/{id64}'), data=payload)

    def accept_clan_invite(self, clan_id: int) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "steamid": self.user.id64,
            "ajax": '1',
            "action": 'group_accept',
            "steamids[]": clan_id
        }
        return self.request('POST', CRoute('/my/friends/action'), data=payload)

    def decline_clan_invite(self, clan_id: int) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "steamid": self.user.id64,
            "ajax": '1',
            "action": 'group_ignore',
            "steamids[]": clan_id
        }
        return self.request('POST', CRoute('/my/friends/action'), data=payload)

    def join_clan(self, clan_id: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "action": 'join',
        }
        return self.request('POST',  CRoute(f'/gid/{clan_id}'), data=payload)

    def leave_clan(self, clan_id: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "action": 'leaveGroup',
            "groupId": clan_id
        }
        return self.request('POST', CRoute('/my/home_process'), data=payload)

    def invite_user_to_clan(self, user_id64: int, clan_id: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "group": clan_id,
            "invitee": user_id64,
            "type": 'groupInvite',
        }
        return self.request('POST', CRoute('/actions/GroupInvite'), data=payload)

    def get_user_clans(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid": user_id64
        }
        return self.request('GET', APIRoute('/ISteamUser/GetUserGroupList'), params=params)

    def get_user_bans(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamids": user_id64
        }
        return self.request('GET', APIRoute('/ISteamUser/GetPlayerBans'), params=params)

    def get_user_level(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid": user_id64
        }
        return self.request('GET', APIRoute('/IPlayerService/GetSteamLevel'), params=params)

    def get_user_badges(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid": user_id64
        }
        return self.request('GET', APIRoute('/IPlayerService/GetBadges'), params=params)

    def clear_nickname_history(self) -> Awaitable:
        payload = {
            "sessionid": self.session_id
        }
        return self.request('POST', CRoute('/my/ajaxclearaliashistory'), data=payload)

    def clear_notifications(self) -> Awaitable:
        return self.request('GET', CRoute('/my/inventory'))

    async def edit_profile(self, nick: str, real_name: str,
                           summary: str, clan_id: int, avatar: 'Image') -> None:
        resp = await self.request('GET', url=f'{self.user.community_url}/edit')
        soup = BeautifulSoup(resp, 'html.parser')
        editable = ['personaName', 'real_name', 'customURL', 'primary_group_steamid']
        current_values = {i['name']: i['value'] for i in soup.find_all('input') if i['name'] in editable}

        payload = {
            "sessionID": self.session_id,
            "type": 'profileSave',
            "personaName": nick or current_values['personaName'],
            "real_name": real_name or current_values['real_name'],
            "summary": summary or soup.find('textarea').text,
            "primary_group_steamid": clan_id or current_values['primary_group_steamid']
        }

        await self.request('POST', CRoute('/my/edit'), data=payload)
        if avatar is not None:
            payload = {
                "MAX_FILE_SIZE": len(avatar),
                "type": 'player_avatar_image',
                "sId": self.user.id64,
                "sessionid": self.session_id,
                "doSub": 1,
                "avatar": {
                    "value": avatar.read(),
                    "options": {
                        "filename": avatar.name,
                        "contentType": f'image/{avatar.type}'
                    }
                }
            }
            await self.request('POST', CRoute('/actions/FileUploader'), data=payload)

    async def send_user_image(self, user_id64: int, image: 'Image') -> None:
        payload = {
            "sessionid": self.session_id,
            "l": 'english',
            "file_size": len(image),
            "file_name": image.name,
            "file_sha": image.hash,
            "file_image_width": image.width,
            "file_image_height": image.height,
            "file_type": f'image/{image.type}',
        }
        resp = await self.request('POST', CRoute('/chat/beginfileupload'), data=payload)

        result = resp['result']
        url = f'{"https" if result["use_https"] else "http"}://{result["url_host"]}{result["url_path"]}'
        headers = {header['name']: header['value'] for header in result['request_headers']}
        await self.request('PUT', url=url, headers=headers, data=image.read())

        payload.update({
            'success': 1,
            'ugcid': result['ugcid'],
            'timestamp': resp['timestamp'],
            'hmac': resp['hmac'],
            'friend_steamid': user_id64,
            'spoiler': int(image.spoiler)
        })
        await self.request('POST', CRoute('/chat/commitfileupload'), data=payload)

    async def send_group_image(self, chat_id: int, channel_id: int, image: 'Image') -> None:
        payload = {
            "sessionid": self.session_id,
            "l": 'english',
            "file_size": len(image),
            "file_name": image.name,
            "file_sha": image.hash,
            "file_image_width": image.width,
            "file_image_height": image.height,
            "file_type": f'image/{image.type}',
        }
        resp = await self.request('POST', CRoute('/chat/beginfileupload'), data=payload)

        result = resp['result']
        url = f'{"https" if result["use_https"] else "http"}://{result["url_host"]}{result["url_path"]}'
        headers = {header['name']: header['value'] for header in result['request_headers']}
        await self.request('PUT', url=url, headers=headers, data=image.read())

        payload.update({
            'success': 1,
            'ugcid': result['ugcid'],
            'timestamp': resp['timestamp'],
            'hmac': resp['hmac'],
            'chat_group_id': channel_id,
            'chat_id': chat_id,
            'spoiler': int(image.spoiler)
        })
        await self.request('POST', CRoute('/chat/commitfileupload'), data=payload)

    async def get_api_key(self) -> str:
        resp = await self.request('GET', CRoute('/dev/apikey'))
        if '<h2>Access Denied</h2>' in resp:
            raise errors.LoginError('Access denied, you will need to generate a key yourself: '
                                    'https://steamcommunity.com/dev/apikey')
        error = 'You must have a validated email address to create a Steam Web API key'
        if error in resp:
            raise errors.LoginError(error)

        match = re.findall(r'<p>Key: ([0-9A-F]+)</p>', resp)
        if match:
            return match[0]

        self.session_id = re.findall(r'g_sessionID = "(.*?)";', resp)[0]
        payload = {
            "domain": 'steam.py',
            "agreeToTerms": 'agreed',
            "sessionid": self.session_id,
            "Submit": 'Register'
        }
        resp = await self.request('POST', CRoute('/dev/registerkey'), data=payload)
        return re.findall(r'<p>Key: ([0-9A-F]+)</p>', resp)[0]
