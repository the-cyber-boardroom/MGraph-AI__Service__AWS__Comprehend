from typing                                                                             import Dict
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                   import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash      import Safe_Str__Hash
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text           import Safe_Str__Comprehend__Text
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code             import Enum__Comprehend__Language_Code


class Schema__Comprehend__Batch_Threshold_Request(Type_Safe):                                               # Batch processing request with threshold
    texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]                                        # Hash → text mapping
    threshold     : Safe_Float                                  = 0.7                                       # Threshold for boolean decisions
    language_code : Enum__Comprehend__Language_Code             = Enum__Comprehend__Language_Code.ENGLISH   # Language of the texts
    use_cache     : bool                                        = False                                     # Whether to use caching
