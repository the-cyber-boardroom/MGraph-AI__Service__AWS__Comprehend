from osbot_utils.type_safe.Type_Safe                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                      import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text import Safe_Str__Text


class Schema__Comprehend__Cache_Info(Type_Safe):                               # Cache information response
    namespace     : Safe_Str__Text                                              # Cache namespace being used
    total_entries : Safe_UInt                                                   # Total number of cached entries
    size_bytes    : Safe_UInt                                                   # Total size of cache in bytes
