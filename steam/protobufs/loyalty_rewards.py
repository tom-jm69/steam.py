# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: steammessages_clientserver_login.proto
# plugin: python-betterproto
# Last updated 19/04/2022

from dataclasses import dataclass
from typing import List

import betterproto


@dataclass(eq=False, repr=False)
class DefinitionBadgeData(betterproto.Message):
    level: int = betterproto.int32_field(1)
    image: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class CommunityItemData(betterproto.Message):
    item_name: str = betterproto.string_field(1)
    item_title: str = betterproto.string_field(2)
    item_description: str = betterproto.string_field(3)
    item_image_small: str = betterproto.string_field(4)
    item_image_large: str = betterproto.string_field(5)
    item_movie_webm: str = betterproto.string_field(6)
    item_movie_mp4: str = betterproto.string_field(7)
    animated: bool = betterproto.bool_field(8)
    badge_data: List[DefinitionBadgeData] = betterproto.message_field(9)
    item_movie_webm_small: str = betterproto.string_field(10)
    item_movie_mp4_small: str = betterproto.string_field(11)
    profile_theme_id: str = betterproto.string_field(12)


@dataclass(eq=False, repr=False)
class Definition(betterproto.Message):
    appid: int = betterproto.uint32_field(1)
    defid: int = betterproto.uint32_field(2)
    type: int = betterproto.int32_field(3)
    community_item_class: int = betterproto.int32_field(4)
    community_item_type: int = betterproto.uint32_field(5)
    point_cost: int = betterproto.int64_field(6)
    timestamp_created: int = betterproto.uint32_field(7)
    timestamp_updated: int = betterproto.uint32_field(8)
    timestamp_available: int = betterproto.uint32_field(9)
    quantity: int = betterproto.int64_field(10)
    internal_description: str = betterproto.string_field(11)
    active: bool = betterproto.bool_field(12)
    community_item_data: CommunityItemData = betterproto.message_field(13)
    timestamp_available_end: int = betterproto.uint32_field(14)
    bundle_defids: List[int] = betterproto.uint32_field(15)
    usable_duration: int = betterproto.uint32_field(16)
    bundle_discount: int = betterproto.uint32_field(17)


@dataclass(eq=False, repr=False)
class AddReactionRequest(betterproto.Message):
    target_type: int = betterproto.int32_field(1)
    targetid: int = betterproto.uint64_field(2)
    reactionid: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class AddReactionResponse(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class BatchedQueryRewardItemsRequest(betterproto.Message):
    requests: List["QueryRewardItemsRequest"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class BatchedQueryRewardItemsResponse(betterproto.Message):
    responses: List["BatchedQueryRewardItemsResponseResponse"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class BatchedQueryRewardItemsResponseResponse(betterproto.Message):
    eresult: int = betterproto.int32_field(1)
    response: "QueryRewardItemsResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class GetActivePurchaseBonusesRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetActivePurchaseBonusesResponse(betterproto.Message):
    bonuses: List["PurchaseBonus"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class GetEligibleAppsRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetEligibleAppsResponse(betterproto.Message):
    apps: List["GetEligibleAppsResponseEligibleApp"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class GetEligibleAppsResponseEligibleApp(betterproto.Message):
    appid: int = betterproto.uint32_field(1)
    has_items_anyone_can_purchase: bool = betterproto.bool_field(2)
    event_app: bool = betterproto.bool_field(3)
    hero_carousel_image: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class GetPointsForSpendResponse(betterproto.Message):
    points: int = betterproto.int64_field(1)


@dataclass(eq=False, repr=False)
class GetProfileCustomizationsConfigResponse(betterproto.Message):
    points_cost: int = betterproto.uint32_field(1)
    upgrade_points_cost: int = betterproto.uint32_field(2)
    purchasable_customization_types: List[int] = betterproto.int32_field(3)
    upgradable_customization_types: List[int] = betterproto.int32_field(4)
    max_slots_per_type: int = betterproto.uint32_field(5)
    max_upgradable_level: int = betterproto.uint32_field(6)


@dataclass(eq=False, repr=False)
class GetReactionConfigRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetReactionConfigResponse(betterproto.Message):
    reactions: List["GetReactionConfigResponseReactionConfig"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class GetReactionConfigResponseReactionConfig(betterproto.Message):
    reactionid: int = betterproto.int32_field(1)
    points_cost: int = betterproto.uint32_field(2)
    points_transferred: int = betterproto.uint32_field(3)
    valid_target_types: List[int] = betterproto.int32_field(4)
    valid_ugc_types: List[int] = betterproto.uint32_field(5)


@dataclass(eq=False, repr=False)
class GetReactionsRequest(betterproto.Message):
    target_type: int = betterproto.int32_field(1)
    targetid: int = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class GetReactionsResponse(betterproto.Message):
    reactionids: List[int] = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class GetReactionsSummaryForUserResponse(betterproto.Message):
    total: List["GetReactionsSummaryForUserResponseBreakdown"] = betterproto.message_field(1)
    user_reviews: List["GetReactionsSummaryForUserResponseBreakdown"] = betterproto.message_field(2)
    ugc: List["GetReactionsSummaryForUserResponseBreakdown"] = betterproto.message_field(3)
    profile: List["GetReactionsSummaryForUserResponseBreakdown"] = betterproto.message_field(4)
    forum_topics: List["GetReactionsSummaryForUserResponseBreakdown"] = betterproto.message_field(5)
    comments: List["GetReactionsSummaryForUserResponseBreakdown"] = betterproto.message_field(6)
    total_points_given: int = betterproto.int64_field(7)
    total_points_received: int = betterproto.int64_field(8)
    total_points_given: int = betterproto.int64_field(9)
    total_points_received: int = betterproto.int64_field(10)


@dataclass(eq=False, repr=False)
class GetReactionsSummaryForUserResponseBreakdown(betterproto.Message):
    reactionid: int = betterproto.int32_field(1)
    given: int = betterproto.uint32_field(2)
    received: int = betterproto.uint32_field(3)
    points_given: int = betterproto.int64_field(4)
    points_received: int = betterproto.int64_field(5)


@dataclass(eq=False, repr=False)
class GetSummaryRequest(betterproto.Message):
    steamid: int = betterproto.fixed64_field(1)


@dataclass(eq=False, repr=False)
class GetSummaryResponse(betterproto.Message):
    summary: "GetSummaryResponseSummary" = betterproto.message_field(1)
    timestamp_updated: int = betterproto.uint32_field(2)
    auditid_highwater: int = betterproto.uint64_field(3)


@dataclass(eq=False, repr=False)
class GetSummaryResponseSummary(betterproto.Message):
    points: int = betterproto.int64_field(1)
    points_earned: int = betterproto.int64_field(2)
    points_spent: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class QueryRewardItemsRequest(betterproto.Message):
    appids: List[int] = betterproto.uint32_field(1)
    time_available: int = betterproto.uint32_field(2)
    community_item_classes: List[int] = betterproto.int32_field(3)
    language: str = betterproto.string_field(4)
    count: int = betterproto.int32_field(5)
    cursor: str = betterproto.string_field(6)
    sort: int = betterproto.int32_field(7)
    sort_descending: bool = betterproto.bool_field(8)
    reward_types: List[int] = betterproto.int32_field(9)
    excluded_community_item_classes: List[int] = betterproto.int32_field(10)
    definitionids: List[int] = betterproto.uint32_field(11)
    filters: List[int] = betterproto.int32_field(12)
    filter_match_all_category_tags: List[str] = betterproto.string_field(13)
    filter_match_any_category_tags: List[str] = betterproto.string_field(14)
    contains_definitionids: List[int] = betterproto.uint32_field(15)
    include_direct_purchase_disabled: bool = betterproto.bool_field(16)
    excluded_content_descriptors: List[int] = betterproto.uint32_field(17)
    excluded_appids: List[int] = betterproto.uint32_field(18)


@dataclass(eq=False, repr=False)
class QueryRewardItemsResponse(betterproto.Message):
    definitions: List["Definition"] = betterproto.message_field(1)
    total_count: int = betterproto.int32_field(2)
    count: int = betterproto.int32_field(3)
    next_cursor: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class RedeemPointsRequest(betterproto.Message):
    defid: int = betterproto.uint32_field(1)
    expected_points_cost: int = betterproto.int64_field(2)


@dataclass(eq=False, repr=False)
class RedeemPointsResponse(betterproto.Message):
    communityitemid: int = betterproto.uint64_field(1)
    bundle_community_item_ids: List[int] = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class RedeemPointsForBadgeLevelRequest(betterproto.Message):
    defid: int = betterproto.uint32_field(1)
    num_levels: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class RedeemPointsForProfileCustomizationRequest(betterproto.Message):
    customization_type: int = betterproto.int32_field(1)


@dataclass(eq=False, repr=False)
class RedeemPointsForProfileCustomizationResponse(betterproto.Message):
    purchaseid: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class RedeemPointsForProfileCustomizationUpgradeRequest(betterproto.Message):
    customization_type: int = betterproto.int32_field(1)
    new_level: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class RedeemPointsForProfileCustomizationUpgradeResponse(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class RegisterForSteamDeckRewardsRequest(betterproto.Message):
    serial_number: str = betterproto.string_field(1)
    controller_code: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class RegisterForSteamDeckRewardsResponse(betterproto.Message):
    granted_profile_modifier: bool = betterproto.bool_field(1)


@dataclass(eq=False, repr=False)
class PurchaseBonus(betterproto.Message):
    bonusid: int = betterproto.uint64_field(1)
    appid: int = betterproto.uint32_field(2)
    active: bool = betterproto.bool_field(3)
    points: int = betterproto.int32_field(4)
    timestamp_start: int = betterproto.uint32_field(5)
    timestamp_end: int = betterproto.uint32_field(6)
    internal_description: str = betterproto.string_field(7)