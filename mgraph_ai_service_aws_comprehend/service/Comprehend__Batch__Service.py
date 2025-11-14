from typing                                                                             import Dict
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                    import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash      import Safe_Str__Hash
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Sentiment       import Schema__Comprehend__Detect_Sentiment
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content   import Schema__Comprehend__Detect_Toxic_Content
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code             import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text           import Safe_Str__Comprehend__Text
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                       import Comprehend__Service


class Comprehend__Batch__Service(Type_Safe):                                   # Batch processing service for multiple texts
    comprehend_service : Comprehend__Service                                   # Main Comprehend service

    # ============================================================================
    # BATCH SENTIMENT DETECTION
    # ============================================================================

    @type_safe
    def batch_detect_sentiment(self                                                ,   # Process multiple texts for sentiment
                              texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text],
                              language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                              use_cache     : bool                            = False
                         ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Detect_Sentiment]:

        results        = {}
        cached_count   = Safe_UInt(0)

        for hash_key, text in texts.items():
            result = self.comprehend_service.detect_sentiment(text          = text         ,
                                                              language_code = language_code,
                                                              use_cache     = use_cache    )
            results[hash_key] = result

        return results

    # ============================================================================
    # BATCH TOXIC CONTENT DETECTION
    # ============================================================================

    @type_safe
    def batch_detect_toxic_content(self                                            ,   # Process multiple texts for toxicity
                                  texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text],
                                  language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                                  use_cache     : bool                            = False
                             ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Detect_Toxic_Content]:

        results = {}

        for hash_key, text in texts.items():
            result = self.comprehend_service.detect_toxic_content(text          = text         ,
                                                                  language_code = language_code,
                                                                  use_cache     = use_cache    )
            results[hash_key] = result

        return results
