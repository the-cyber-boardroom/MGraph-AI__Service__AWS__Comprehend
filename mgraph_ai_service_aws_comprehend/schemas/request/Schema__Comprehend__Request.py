from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text          import Safe_Str__Comprehend__Text
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code            import Enum__Comprehend__Language_Code


class Schema__Comprehend__Request(Type_Safe):                                  # Base request for Comprehend operations
    text          : Safe_Str__Comprehend__Text                                 # Text to analyze (5000 char limit enforced by Safe_Str)
    language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH  # Language of the text
    use_cache     : bool                            = False                    # Whether to use caching for this request
