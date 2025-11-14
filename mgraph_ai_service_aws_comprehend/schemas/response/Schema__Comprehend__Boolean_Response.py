from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                               import Safe_Float
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text


class Schema__Comprehend__Boolean_Response(Type_Safe):                         # Boolean response for helper endpoints (is_positive, is_negative, etc.)
    result    : bool                                                            # True/False based on threshold comparison
    score     : Safe_Float                                                      # Actual score from AWS Comprehend
    threshold : Safe_Float                                                      # Threshold used for comparison
    operation : Safe_Str__Text                                                  # Operation name (e.g., 'is_positive', 'is_toxic')
    cached    : bool                                                            # Whether result was retrieved from cache
    duration  : Safe_Float                                                      # Processing time in seconds
