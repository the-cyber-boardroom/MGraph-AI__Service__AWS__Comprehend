from typing                                                                            import Dict
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash     import Safe_Str__Hash
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text          import Safe_Str__Comprehend__Text
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code            import Enum__Comprehend__Language_Code


class Schema__Comprehend__Batch_Request(Type_Safe):                                            # Batch processing request for multiple texts
    texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]                           # Hash → text mapping for batch processing
    language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH  # Language of the texts
    use_cache     : bool                            = False                                    # Whether to use caching for batch results
