from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                  import Safe_Float
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text          import Safe_Str__Comprehend__Text
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code            import Enum__Comprehend__Language_Code


class Schema__Comprehend__Threshold_Request(Type_Safe):                        # Request with threshold for boolean helper endpoints
    text          : Safe_Str__Comprehend__Text                                 # Text to analyze
    threshold     : Safe_Float                                  = 0.7          # Threshold for boolean decision (0.0-1.0)
    language_code : Enum__Comprehend__Language_Code             = Enum__Comprehend__Language_Code.ENGLISH  # Language of the text
    use_cache     : bool                                        = False        # Whether to use caching
