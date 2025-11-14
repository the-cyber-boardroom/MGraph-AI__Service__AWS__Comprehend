from typing                                                                          import Dict
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                               import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text


class Schema__Comprehend__Batch_Boolean_Response(Type_Safe):                   # Batch boolean response for helper endpoints
    results   : Dict[Safe_Str__Hash, bool]                                      # Hash → boolean result mapping
    scores    : Dict[Safe_Str__Hash, Safe_Float]                                # Hash → actual score mapping
    threshold : Safe_Float                                                      # Threshold used for all comparisons
    operation : Safe_Str__Text                                                  # Operation name (e.g., 'is_positive')
    total     : Safe_UInt                                                       # Total number of texts processed
    cached    : Safe_UInt                                                       # Number of results from cache
    duration  : Safe_Float                                                      # Total processing time in seconds
