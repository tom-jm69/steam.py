# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: steammessages_clientserver_2.proto
# plugin: python-betterproto
# Last updated 09/09/2021

from dataclasses import dataclass
from typing import List

import betterproto


@dataclass(eq=False, repr=False)
class CMsgClientUpdateUserGameInfo(betterproto.Message):
    steamid_idgs: int = betterproto.fixed64_field(1)
    gameid: int = betterproto.fixed64_field(2)
    game_ip: int = betterproto.uint32_field(3)
    game_port: int = betterproto.uint32_field(4)
    token: bytes = betterproto.bytes_field(5)


@dataclass(eq=False, repr=False)
class CMsgClientRichPresenceUpload(betterproto.Message):
    rich_presence_kv: bytes = betterproto.bytes_field(1)
    steamid_broadcast: List[int] = betterproto.fixed64_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientRichPresenceRequest(betterproto.Message):
    steamid_request: List[int] = betterproto.fixed64_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientRichPresenceInfo(betterproto.Message):
    rich_presence: List["CMsgClientRichPresenceInfoRichPresence"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientRichPresenceInfoRichPresence(betterproto.Message):
    steamid_user: int = betterproto.fixed64_field(1)
    rich_presence_kv: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientCheckFileSignature(betterproto.Message):
    app_id: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientCheckFileSignatureResponse(betterproto.Message):
    app_id: int = betterproto.uint32_field(1)
    pid: int = betterproto.uint32_field(2)
    eresult: int = betterproto.uint32_field(3)
    filename: str = betterproto.string_field(4)
    esignatureresult: int = betterproto.uint32_field(5)
    sha_file: bytes = betterproto.bytes_field(6)
    signatureheader: bytes = betterproto.bytes_field(7)
    filesize: int = betterproto.uint32_field(8)
    getlasterror: int = betterproto.uint32_field(9)
    evalvesignaturecheckdetail: int = betterproto.uint32_field(10)


@dataclass(eq=False, repr=False)
class CMsgClientReadMachineAuth(betterproto.Message):
    filename: str = betterproto.string_field(1)
    offset: int = betterproto.uint32_field(2)
    cubtoread: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientReadMachineAuthResponse(betterproto.Message):
    filename: str = betterproto.string_field(1)
    eresult: int = betterproto.uint32_field(2)
    filesize: int = betterproto.uint32_field(3)
    sha_file: bytes = betterproto.bytes_field(4)
    getlasterror: int = betterproto.uint32_field(5)
    offset: int = betterproto.uint32_field(6)
    cubread: int = betterproto.uint32_field(7)
    bytes_read: bytes = betterproto.bytes_field(8)
    filename_sentry: str = betterproto.string_field(9)


@dataclass(eq=False, repr=False)
class CMsgClientUpdateMachineAuth(betterproto.Message):
    filename: str = betterproto.string_field(1)
    offset: int = betterproto.uint32_field(2)
    cubtowrite: int = betterproto.uint32_field(3)
    bytes_: bytes = betterproto.bytes_field(4)
    otp_type: int = betterproto.uint32_field(5)
    otp_identifier: str = betterproto.string_field(6)
    otp_sharedsecret: bytes = betterproto.bytes_field(7)
    otp_timedrift: int = betterproto.uint32_field(8)


@dataclass(eq=False, repr=False)
class CMsgClientUpdateMachineAuthResponse(betterproto.Message):
    filename: str = betterproto.string_field(1)
    eresult: int = betterproto.uint32_field(2)
    filesize: int = betterproto.uint32_field(3)
    sha_file: bytes = betterproto.bytes_field(4)
    getlasterror: int = betterproto.uint32_field(5)
    offset: int = betterproto.uint32_field(6)
    cubwrote: int = betterproto.uint32_field(7)
    otp_type: int = betterproto.int32_field(8)
    otp_value: int = betterproto.uint32_field(9)
    otp_identifier: str = betterproto.string_field(10)


@dataclass(eq=False, repr=False)
class CMsgClientRequestMachineAuth(betterproto.Message):
    filename: str = betterproto.string_field(1)
    eresult_sentryfile: int = betterproto.uint32_field(2)
    filesize: int = betterproto.uint32_field(3)
    sha_sentryfile: bytes = betterproto.bytes_field(4)
    lock_account_action: int = betterproto.int32_field(6)
    otp_type: int = betterproto.uint32_field(7)
    otp_identifier: str = betterproto.string_field(8)
    otp_sharedsecret: bytes = betterproto.bytes_field(9)
    otp_value: int = betterproto.uint32_field(10)
    machine_name: str = betterproto.string_field(11)
    machine_name_userchosen: str = betterproto.string_field(12)


@dataclass(eq=False, repr=False)
class CMsgClientRequestMachineAuthResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientRegisterKey(betterproto.Message):
    key: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientPurchaseResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    purchaseresult_details: int = betterproto.int32_field(2)
    purchase_receipt_info: bytes = betterproto.bytes_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientActivateOemLicense(betterproto.Message):
    bios_manufacturer: str = betterproto.string_field(1)
    bios_serialnumber: str = betterproto.string_field(2)
    license_file: bytes = betterproto.bytes_field(3)
    mainboard_manufacturer: str = betterproto.string_field(4)
    mainboard_product: str = betterproto.string_field(5)
    mainboard_serialnumber: str = betterproto.string_field(6)


@dataclass(eq=False, repr=False)
class CMsgClientRegisterOemMachine(betterproto.Message):
    oem_register_file: bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientRegisterOemMachineResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientPurchaseWithMachineId(betterproto.Message):
    package_id: int = betterproto.uint32_field(1)
    machine_info: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class CMsgTradingInitiateTradeRequest(betterproto.Message):
    trade_request_id: int = betterproto.uint32_field(1)
    other_steamid: int = betterproto.uint64_field(2)
    other_name: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class CMsgTradingInitiateTradeResponse(betterproto.Message):
    response: int = betterproto.uint32_field(1)
    trade_request_id: int = betterproto.uint32_field(2)
    other_steamid: int = betterproto.uint64_field(3)
    steamguard_required_days: int = betterproto.uint32_field(4)
    new_device_cooldown_days: int = betterproto.uint32_field(5)
    default_password_reset_probation_days: int = betterproto.uint32_field(6)
    password_reset_probation_days: int = betterproto.uint32_field(7)
    default_email_change_probation_days: int = betterproto.uint32_field(8)
    email_change_probation_days: int = betterproto.uint32_field(9)


@dataclass(eq=False, repr=False)
class CMsgTradingCancelTradeRequest(betterproto.Message):
    other_steamid: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class CMsgTradingStartSession(betterproto.Message):
    other_steamid: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientGetCdnAuthToken(betterproto.Message):
    depot_id: int = betterproto.uint32_field(1)
    host_name: str = betterproto.string_field(2)
    app_id: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientGetDepotDecryptionKey(betterproto.Message):
    depot_id: int = betterproto.uint32_field(1)
    app_id: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientGetDepotDecryptionKeyResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    depot_id: int = betterproto.uint32_field(2)
    depot_encryption_key: bytes = betterproto.bytes_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientCheckAppBetaPassword(betterproto.Message):
    app_id: int = betterproto.uint32_field(1)
    betapassword: str = betterproto.string_field(2)
    language: int = betterproto.int32_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientCheckAppBetaPasswordResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    betapasswords: List["CMsgClientCheckAppBetaPasswordResponseBetaPassword"] = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class CMsgClientCheckAppBetaPasswordResponseBetaPassword(betterproto.Message):
    betaname: str = betterproto.string_field(1)
    betapassword: str = betterproto.string_field(2)
    betadescription: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientUpdateAppJobReport(betterproto.Message):
    app_id: int = betterproto.uint32_field(1)
    depot_ids: List[int] = betterproto.uint32_field(2)
    app_state: int = betterproto.uint32_field(3)
    job_app_error: int = betterproto.uint32_field(4)
    error_details: str = betterproto.string_field(5)
    job_duration: int = betterproto.uint32_field(6)
    files_validation_failed: int = betterproto.uint32_field(7)
    job_bytes_downloaded: int = betterproto.uint64_field(8)
    job_bytes_staged: int = betterproto.uint64_field(9)
    bytes_comitted: int = betterproto.uint64_field(10)
    start_app_state: int = betterproto.uint32_field(11)
    stats_machine_id: int = betterproto.fixed64_field(12)
    branch_name: str = betterproto.string_field(13)
    total_bytes_downloaded: int = betterproto.uint64_field(14)
    total_bytes_staged: int = betterproto.uint64_field(15)
    total_bytes_restored: int = betterproto.uint64_field(16)
    is_borrowed: bool = betterproto.bool_field(17)
    is_free_weekend: bool = betterproto.bool_field(18)
    total_bytes_legacy: int = betterproto.uint64_field(19)
    total_bytes_patched: int = betterproto.uint64_field(20)
    total_bytes_saved: int = betterproto.uint64_field(21)
    cell_id: int = betterproto.uint32_field(22)


@dataclass(eq=False, repr=False)
class CMsgClientDpContentStatsReport(betterproto.Message):
    stats_machine_id: int = betterproto.fixed64_field(1)
    country_code: str = betterproto.string_field(2)
    os_type: int = betterproto.int32_field(3)
    language: int = betterproto.int32_field(4)
    num_install_folders: int = betterproto.uint32_field(5)
    num_installed_games: int = betterproto.uint32_field(6)
    size_installed_games: int = betterproto.uint64_field(7)


@dataclass(eq=False, repr=False)
class CMsgClientGetCdnAuthTokenResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)
    token: str = betterproto.string_field(2)
    expiration_time: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class CMsgDownloadRateStatistics(betterproto.Message):
    cell_id: int = betterproto.uint32_field(1)
    stats: List["CMsgDownloadRateStatisticsStatsInfo"] = betterproto.message_field(2)
    throttling_kbps: int = betterproto.uint32_field(3)
    steam_realm: int = betterproto.uint32_field(4)


@dataclass(eq=False, repr=False)
class CMsgDownloadRateStatisticsStatsInfo(betterproto.Message):
    source_type: int = betterproto.uint32_field(1)
    source_id: int = betterproto.uint32_field(2)
    seconds: int = betterproto.uint32_field(3)
    bytes_: int = betterproto.uint64_field(4)
    host_name: str = betterproto.string_field(5)
    microseconds: int = betterproto.uint64_field(6)
    used_ipv6: bool = betterproto.bool_field(7)
    proxied: bool = betterproto.bool_field(8)


@dataclass(eq=False, repr=False)
class CMsgClientRequestAccountData(betterproto.Message):
    account_or_email: str = betterproto.string_field(1)
    action: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientRequestAccountDataResponse(betterproto.Message):
    action: int = betterproto.uint32_field(1)
    eresult: int = betterproto.uint32_field(2)
    account_name: str = betterproto.string_field(3)
    ct_matches: int = betterproto.uint32_field(4)
    account_name_suggestion1: str = betterproto.string_field(5)
    account_name_suggestion2: str = betterproto.string_field(6)
    account_name_suggestion3: str = betterproto.string_field(7)


@dataclass(eq=False, repr=False)
class CMsgClientUgsGetGlobalStats(betterproto.Message):
    gameid: int = betterproto.uint64_field(1)
    history_days_requested: int = betterproto.uint32_field(2)
    time_last_requested: int = betterproto.fixed32_field(3)
    first_day_cached: int = betterproto.uint32_field(4)
    days_cached: int = betterproto.uint32_field(5)


@dataclass(eq=False, repr=False)
class CMsgClientUgsGetGlobalStatsResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    timestamp: int = betterproto.fixed32_field(2)
    day_current: int = betterproto.int32_field(3)
    days: List["CMsgClientUgsGetGlobalStatsResponseDay"] = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class CMsgClientUgsGetGlobalStatsResponseDay(betterproto.Message):
    day_id: int = betterproto.uint32_field(1)
    stats: List["CMsgClientUgsGetGlobalStatsResponseDayStat"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientUgsGetGlobalStatsResponseDayStat(betterproto.Message):
    stat_id: int = betterproto.int32_field(1)
    data: int = betterproto.int64_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientRedeemGuestPass(betterproto.Message):
    guest_pass_id: int = betterproto.fixed64_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientRedeemGuestPassResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)
    package_id: int = betterproto.uint32_field(2)
    must_own_appid: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientGetClanActivityCounts(betterproto.Message):
    steamid_clans: List[int] = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientGetClanActivityCountsResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientOgsReportString(betterproto.Message):
    accumulated: bool = betterproto.bool_field(1)
    sessionid: int = betterproto.uint64_field(2)
    severity: int = betterproto.int32_field(3)
    formatter: str = betterproto.string_field(4)
    varargs: bytes = betterproto.bytes_field(5)


@dataclass(eq=False, repr=False)
class CMsgClientOgsReportBug(betterproto.Message):
    sessionid: int = betterproto.uint64_field(1)
    bugtext: str = betterproto.string_field(2)
    screenshot: bytes = betterproto.bytes_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientSentLogs(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class CMsgGcClient(betterproto.Message):
    appid: int = betterproto.uint32_field(1)
    msgtype: int = betterproto.uint32_field(2)
    payload: bytes = betterproto.bytes_field(3)
    steamid: int = betterproto.fixed64_field(4)
    gcname: str = betterproto.string_field(5)
    ip: int = betterproto.uint32_field(6)


@dataclass(eq=False, repr=False)
class CMsgClientRequestFreeLicense(betterproto.Message):
    appids: List[int] = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientRequestFreeLicenseResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)
    granted_packageids: List[int] = betterproto.uint32_field(2)
    granted_appids: List[int] = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class CMsgDrmDownloadRequestWithCrashData(betterproto.Message):
    download_flags: int = betterproto.uint32_field(1)
    download_types_known: int = betterproto.uint32_field(2)
    guid_drm: bytes = betterproto.bytes_field(3)
    guid_split: bytes = betterproto.bytes_field(4)
    guid_merge: bytes = betterproto.bytes_field(5)
    module_name: str = betterproto.string_field(6)
    module_path: str = betterproto.string_field(7)
    crash_data: bytes = betterproto.bytes_field(8)


@dataclass(eq=False, repr=False)
class CMsgDrmDownloadResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)
    app_id: int = betterproto.uint32_field(2)
    blob_download_type: int = betterproto.uint32_field(3)
    merge_guid: bytes = betterproto.bytes_field(4)
    download_file_dfs_ip: int = betterproto.uint32_field(5)
    download_file_dfs_port: int = betterproto.uint32_field(6)
    download_file_url: str = betterproto.string_field(7)
    module_path: str = betterproto.string_field(8)


@dataclass(eq=False, repr=False)
class CMsgDrmFinalResult(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)
    app_id: int = betterproto.uint32_field(2)
    blob_download_type: int = betterproto.uint32_field(3)
    error_detail: int = betterproto.uint32_field(4)
    merge_guid: bytes = betterproto.bytes_field(5)
    download_file_dfs_ip: int = betterproto.uint32_field(6)
    download_file_dfs_port: int = betterproto.uint32_field(7)
    download_file_url: str = betterproto.string_field(8)


@dataclass(eq=False, repr=False)
class CMsgClientDpCheckSpecialSurvey(betterproto.Message):
    survey_id: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientDpCheckSpecialSurveyResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)
    state: int = betterproto.uint32_field(2)
    name: str = betterproto.string_field(3)
    custom_url: str = betterproto.string_field(4)
    include_software: bool = betterproto.bool_field(5)
    token: bytes = betterproto.bytes_field(6)


@dataclass(eq=False, repr=False)
class CMsgClientDpSendSpecialSurveyResponse(betterproto.Message):
    survey_id: int = betterproto.uint32_field(1)
    data: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientDpSendSpecialSurveyResponseReply(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)
    token: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientRequestForgottenPasswordEmail(betterproto.Message):
    account_name: str = betterproto.string_field(1)
    password_tried: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientRequestForgottenPasswordEmailResponse(betterproto.Message):
    eresult: int = betterproto.uint32_field(1)
    use_secret_question: bool = betterproto.bool_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientItemAnnouncements(betterproto.Message):
    count_new_items: int = betterproto.uint32_field(1)
    unseen_items: List["CMsgClientItemAnnouncementsUnseenItem"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientItemAnnouncementsUnseenItem(betterproto.Message):
    appid: int = betterproto.uint32_field(1)
    context_id: int = betterproto.uint64_field(2)
    asset_id: int = betterproto.uint64_field(3)
    amount: int = betterproto.uint64_field(4)
    rtime32_gained: int = betterproto.fixed32_field(5)
    source_appid: int = betterproto.uint32_field(6)


@dataclass(eq=False, repr=False)
class CMsgClientRequestItemAnnouncements(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class CMsgClientUserNotifications(betterproto.Message):
    notifications: List["CMsgClientUserNotificationsNotification"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientUserNotificationsNotification(betterproto.Message):
    user_notification_type: int = betterproto.uint32_field(1)
    count: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientCommentNotifications(betterproto.Message):
    count_new_comments: int = betterproto.uint32_field(1)
    count_new_comments_owner: int = betterproto.uint32_field(2)
    count_new_comments_subscriptions: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientRequestCommentNotifications(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class CMsgClientOfflineMessageNotification(betterproto.Message):
    offline_messages: int = betterproto.uint32_field(1)
    friends_with_offline_messages: List[int] = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientRequestOfflineMessageCount(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class CMsgClientChatGetFriendMessageHistory(betterproto.Message):
    steamid: int = betterproto.fixed64_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientChatGetFriendMessageHistoryResponse(betterproto.Message):
    steamid: int = betterproto.fixed64_field(1)
    success: int = betterproto.uint32_field(2)
    messages: List["CMsgClientChatGetFriendMessageHistoryResponseFriendMessage"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientChatGetFriendMessageHistoryResponseFriendMessage(betterproto.Message):
    accountid: int = betterproto.uint32_field(1)
    timestamp: int = betterproto.uint32_field(2)
    message: str = betterproto.string_field(3)
    unread: bool = betterproto.bool_field(4)


@dataclass(eq=False, repr=False)
class CMsgClientChatGetFriendMessageHistoryForOfflineMessages(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class CMsgClientFsGetFriendsSteamLevels(betterproto.Message):
    accountids: List[int] = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientFsGetFriendsSteamLevelsResponse(betterproto.Message):
    friends: List["CMsgClientFsGetFriendsSteamLevelsResponseFriend"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientFsGetFriendsSteamLevelsResponseFriend(betterproto.Message):
    accountid: int = betterproto.uint32_field(1)
    level: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientEmailAddrInfo(betterproto.Message):
    email_address: str = betterproto.string_field(1)
    email_is_validated: bool = betterproto.bool_field(2)
    email_validation_changed: bool = betterproto.bool_field(3)
    credential_change_requires_code: bool = betterproto.bool_field(4)
    password_or_secretqa_change_requires_code: bool = betterproto.bool_field(5)
    remind_user_about_email: bool = betterproto.bool_field(6)


@dataclass(eq=False, repr=False)
class CMsgCreItemVoteSummary(betterproto.Message):
    published_file_ids: List["CMsgCreItemVoteSummaryPublishedFileId"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class CMsgCreItemVoteSummaryPublishedFileId(betterproto.Message):
    published_file_id: int = betterproto.fixed64_field(1)


@dataclass(eq=False, repr=False)
class CMsgCreItemVoteSummaryResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    item_vote_summaries: List["CMsgCreItemVoteSummaryResponseItemVoteSummary"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class CMsgCreItemVoteSummaryResponseItemVoteSummary(betterproto.Message):
    published_file_id: int = betterproto.fixed64_field(1)
    votes_for: int = betterproto.int32_field(2)
    votes_against: int = betterproto.int32_field(3)
    reports: int = betterproto.int32_field(4)
    score: float = betterproto.float_field(5)


@dataclass(eq=False, repr=False)
class CMsgCreUpdateUserPublishedItemVote(betterproto.Message):
    published_file_id: int = betterproto.fixed64_field(1)
    vote_up: bool = betterproto.bool_field(2)


@dataclass(eq=False, repr=False)
class CMsgCreUpdateUserPublishedItemVoteResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)


@dataclass(eq=False, repr=False)
class CMsgCreGetUserPublishedItemVoteDetails(betterproto.Message):
    published_file_ids: List["CMsgCreGetUserPublishedItemVoteDetailsPublishedFileId"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class CMsgCreGetUserPublishedItemVoteDetailsPublishedFileId(betterproto.Message):
    published_file_id: int = betterproto.fixed64_field(1)


@dataclass(eq=False, repr=False)
class CMsgCreGetUserPublishedItemVoteDetailsResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    user_item_vote_details: List[
        "CMsgCreGetUserPublishedItemVoteDetailsResponseUserItemVoteDetail"
    ] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class CMsgCreGetUserPublishedItemVoteDetailsResponseUserItemVoteDetail(betterproto.Message):
    published_file_id: int = betterproto.fixed64_field(1)
    vote: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class CMsgFsGetFollowerCount(betterproto.Message):
    steam_id: int = betterproto.fixed64_field(1)


@dataclass(eq=False, repr=False)
class CMsgFsGetFollowerCountResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    count: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class CMsgFsGetIsFollowing(betterproto.Message):
    steam_id: int = betterproto.fixed64_field(1)


@dataclass(eq=False, repr=False)
class CMsgFsGetIsFollowingResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    is_following: bool = betterproto.bool_field(2)


@dataclass(eq=False, repr=False)
class CMsgFsEnumerateFollowingList(betterproto.Message):
    start_index: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class CMsgFsEnumerateFollowingListResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    total_results: int = betterproto.int32_field(2)
    steam_ids: List[int] = betterproto.fixed64_field(3)


@dataclass(eq=False, repr=False)
class CMsgDpGetNumberOfCurrentPlayers(betterproto.Message):
    appid: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class CMsgDpGetNumberOfCurrentPlayersResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    player_count: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientFriendUserStatusPublished(betterproto.Message):
    friend_steamid: int = betterproto.fixed64_field(1)
    appid: int = betterproto.uint32_field(2)
    status_text: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientServiceMethodLegacy(betterproto.Message):
    method_name: str = betterproto.string_field(1)
    serialized_method: bytes = betterproto.bytes_field(2)
    is_notification: bool = betterproto.bool_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientServiceMethodLegacyResponse(betterproto.Message):
    method_name: str = betterproto.string_field(1)
    serialized_method_response: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientUiMode(betterproto.Message):
    uimode: int = betterproto.uint32_field(1)
    chat_mode: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientVanityUrlChangedNotification(betterproto.Message):
    vanity_url: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientAuthorizeLocalDeviceRequest(betterproto.Message):
    device_description: str = betterproto.string_field(1)
    owner_account_id: int = betterproto.uint32_field(2)
    local_device_token: int = betterproto.uint64_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientAuthorizeLocalDevice(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    owner_account_id: int = betterproto.uint32_field(2)
    authed_device_token: int = betterproto.uint64_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientAuthorizeLocalDeviceNotification(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    owner_account_id: int = betterproto.uint32_field(2)
    local_device_token: int = betterproto.uint64_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientDeauthorizeDeviceRequest(betterproto.Message):
    deauthorization_account_id: int = betterproto.uint32_field(1)
    deauthorization_device_token: int = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientDeauthorizeDevice(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    deauthorization_account_id: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientUseLocalDeviceAuthorizations(betterproto.Message):
    authorization_account_id: List[int] = betterproto.uint32_field(1)
    device_tokens: List["CMsgClientUseLocalDeviceAuthorizationsDeviceToken"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientUseLocalDeviceAuthorizationsDeviceToken(betterproto.Message):
    owner_account_id: int = betterproto.uint32_field(1)
    token_id: int = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientGetAuthorizedDevices(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class CMsgClientGetAuthorizedDevicesResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    authorized_device: List["CMsgClientGetAuthorizedDevicesResponseAuthorizedDevice"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientGetAuthorizedDevicesResponseAuthorizedDevice(betterproto.Message):
    auth_device_token: int = betterproto.uint64_field(1)
    device_name: str = betterproto.string_field(2)
    last_access_time: int = betterproto.uint32_field(3)
    borrower_id: int = betterproto.uint32_field(4)
    is_pending: bool = betterproto.bool_field(5)
    app_played: int = betterproto.uint32_field(6)


@dataclass(eq=False, repr=False)
class CMsgClientSharedLibraryLockStatus(betterproto.Message):
    locked_library: List["CMsgClientSharedLibraryLockStatusLockedLibrary"] = betterproto.message_field(1)
    own_library_locked_by: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientSharedLibraryLockStatusLockedLibrary(betterproto.Message):
    owner_id: int = betterproto.uint32_field(1)
    locked_by: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientSharedLibraryStopPlaying(betterproto.Message):
    seconds_left: int = betterproto.int32_field(1)
    stop_apps: List["CMsgClientSharedLibraryStopPlayingStopApp"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientSharedLibraryStopPlayingStopApp(betterproto.Message):
    app_id: int = betterproto.uint32_field(1)
    owner_id: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class CMsgClientServiceCall(betterproto.Message):
    sysid_routing: bytes = betterproto.bytes_field(1)
    call_handle: int = betterproto.uint32_field(2)
    module_crc: int = betterproto.uint32_field(3)
    module_hash: bytes = betterproto.bytes_field(4)
    function_id: int = betterproto.uint32_field(5)
    cub_output_max: int = betterproto.uint32_field(6)
    flags: int = betterproto.uint32_field(7)
    callparameter: bytes = betterproto.bytes_field(8)
    ping_only: bool = betterproto.bool_field(9)
    max_outstanding_calls: int = betterproto.uint32_field(10)


@dataclass(eq=False, repr=False)
class CMsgClientServiceModule(betterproto.Message):
    module_crc: int = betterproto.uint32_field(1)
    module_hash: bytes = betterproto.bytes_field(2)
    module_content: bytes = betterproto.bytes_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientServiceCallResponse(betterproto.Message):
    sysid_routing: bytes = betterproto.bytes_field(1)
    call_handle: int = betterproto.uint32_field(2)
    module_crc: int = betterproto.uint32_field(3)
    module_hash: bytes = betterproto.bytes_field(4)
    ecallresult: int = betterproto.uint32_field(5)
    result_content: bytes = betterproto.bytes_field(6)
    os_version_info: bytes = betterproto.bytes_field(7)
    system_info: bytes = betterproto.bytes_field(8)
    load_address: int = betterproto.fixed64_field(9)
    exception_record: bytes = betterproto.bytes_field(10)
    portable_os_version_info: bytes = betterproto.bytes_field(11)
    portable_system_info: bytes = betterproto.bytes_field(12)
    was_converted: bool = betterproto.bool_field(13)
    internal_result: int = betterproto.uint32_field(14)
    current_count: int = betterproto.uint32_field(15)
    last_call_handle: int = betterproto.uint32_field(16)
    last_call_module_crc: int = betterproto.uint32_field(17)
    last_call_sysid_routing: bytes = betterproto.bytes_field(18)
    last_ecallresult: int = betterproto.uint32_field(19)
    last_callissue_delta: int = betterproto.uint32_field(20)
    last_callcomplete_delta: int = betterproto.uint32_field(21)


@dataclass(eq=False, repr=False)
class CMsgAmUnlockStreaming(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class CMsgAmUnlockStreamingResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    encryption_key: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class CMsgAmUnlockHevc(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class CMsgAmUnlockHevcResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientPlayingSessionState(betterproto.Message):
    playing_blocked: bool = betterproto.bool_field(2)
    playing_app: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class CMsgClientKickPlayingSession(betterproto.Message):
    only_stop_game: bool = betterproto.bool_field(1)


@dataclass(eq=False, repr=False)
class CMsgClientVoiceCallPreAuthorize(betterproto.Message):
    caller_steamid: int = betterproto.fixed64_field(1)
    receiver_steamid: int = betterproto.fixed64_field(2)
    caller_id: int = betterproto.int32_field(3)
    hangup: bool = betterproto.bool_field(4)


@dataclass(eq=False, repr=False)
class CMsgClientVoiceCallPreAuthorizeResponse(betterproto.Message):
    caller_steamid: int = betterproto.fixed64_field(1)
    receiver_steamid: int = betterproto.fixed64_field(2)
    eresult: int = betterproto.int32_field(3)
    caller_id: int = betterproto.int32_field(4)


@dataclass(eq=False, repr=False)
class CMsgBadgeCraftedNotification(betterproto.Message):
    appid: int = betterproto.uint32_field(1)
    badge_level: int = betterproto.uint32_field(2)
