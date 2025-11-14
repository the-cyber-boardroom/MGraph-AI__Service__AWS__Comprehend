from typing                                                                                     import Dict
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                            import Safe_UInt
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                           import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                  import type_safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash              import Safe_Str__Hash
from osbot_aws.aws.comprehend.Comprehend__Batch                                                 import Comprehend__Batch
from osbot_aws.aws.comprehend.schemas.batch.Schema__Comprehend__Batch_Item__Detect_Sentiment    import Schema__Comprehend__Batch_Item__Detect_Sentiment
from osbot_aws.aws.comprehend.schemas.batch.Schema__Comprehend__Batch_Item__Detect_Entities     import Schema__Comprehend__Batch_Item__Detect_Entities
from osbot_aws.aws.comprehend.schemas.batch.Schema__Comprehend__Batch_Item__Detect_Key_Phrases  import Schema__Comprehend__Batch_Item__Detect_Key_Phrases
from osbot_aws.aws.comprehend.schemas.batch.Schema__Comprehend__Batch_Item__Detect_Syntax       import Schema__Comprehend__Batch_Item__Detect_Syntax
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content           import Schema__Comprehend__Detect_Toxic_Content
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code                     import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                   import Safe_Str__Comprehend__Text
from mgraph_ai_service_aws_comprehend.service.Comprehend__Cache__Service                        import Comprehend__Cache__Service
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                               import Comprehend__Service


class Comprehend__Batch__Service(Type_Safe):                                                               # Batch processing service using native AWS Comprehend batch APIs
    comprehend_batch   : Comprehend__Batch                                                                 # Native OSBot-AWS batch client
    comprehend_service : Comprehend__Service                                                               # Single-text service (for operations without batch API)
    cache_service      : Comprehend__Cache__Service                                                        # Caching service (future integration)

    # ============================================================================
    # BATCH SENTIMENT DETECTION (Native AWS Batch API)
    # ============================================================================

    @type_safe
    def batch_detect_sentiment(self                                                                 ,      # Process multiple texts for sentiment using native batch API
                               texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]     ,      # Hash → text mapping for batch processing
                               language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                               use_cache     : bool                            = False
                          ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Batch_Item__Detect_Sentiment]:

        hash_to_index = Type_Safe__Dict(expected_key_type   = Safe_UInt     ,
                                        expected_value_type = Safe_Str__Hash)                                                                                 # Maps hash → list index for result mapping
        text_list     = []

        for i, (hash_key, text) in enumerate(texts.items()):                                              # Convert hash-keyed dict to list for AWS API
            hash_to_index[i] = hash_key
            text_list.append(text)

        results = Type_Safe__Dict(expected_key_type   = Safe_Str__Hash                                  ,
                                  expected_value_type = Schema__Comprehend__Batch_Item__Detect_Sentiment)                                                                                 # Maps hash → list index for result mapping                                                                                       # Map results back to hash keys

        if text_list:
            batch_result = self.comprehend_batch.batch_detect_sentiment(text_list     = text_list    ,       # Single AWS API call for up to 25 documents
                                                                        language_code = language_code)

            for result_item in batch_result.result_list:
                hash_key          = hash_to_index[result_item.index]
                results[hash_key] = result_item

        # TODO: Handle batch_result.error_list items
        # TODO: Implement cache integration when use_cache=True

        return results

    # ============================================================================
    # BATCH ENTITIES DETECTION (Native AWS Batch API)
    # ============================================================================

    @type_safe
    def batch_detect_entities(self                                                                  ,      # Process multiple texts for entities using native batch API
                              texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]      ,      # Hash → text mapping for batch processing
                              language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                              use_cache     : bool                            = False
                         ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Batch_Item__Detect_Entities]:

        hash_to_index = {}
        text_list     = []

        for i, (hash_key, text) in enumerate(texts.items()):
            hash_to_index[i] = hash_key
            text_list.append(text)

        batch_result = self.comprehend_batch.batch_detect_entities(text_list     = text_list    ,
                                                                   language_code = language_code)

        results = Type_Safe__Dict(expected_key_type   = Safe_Str__Hash                          ,
                                  expected_value_type = Schema__Comprehend__Batch_Item__Detect_Entities)    # Maps hash → list index for result mapping

        for result_item in batch_result.result_list:
            hash_key          = hash_to_index[result_item.index]
            results[hash_key] = result_item

        return results

    # ============================================================================
    # BATCH KEY PHRASES DETECTION (Native AWS Batch API)
    # ============================================================================

    @type_safe
    def batch_detect_key_phrases(self                                                               ,      # Process multiple texts for key phrases using native batch API
                                 texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]   ,      # Hash → text mapping for batch processing
                                 language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                                 use_cache     : bool                            = False
                            ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Batch_Item__Detect_Key_Phrases]:

        hash_to_index = {}
        text_list     = []

        for i, (hash_key, text) in enumerate(texts.items()):
            hash_to_index[i] = hash_key
            text_list.append(text)

        batch_result = self.comprehend_batch.batch_detect_key_phrases(text_list     = text_list    ,
                                                                      language_code = language_code)

        results = Type_Safe__Dict(expected_key_type   = Safe_Str__Hash                          ,
                                  expected_value_type = Schema__Comprehend__Batch_Item__Detect_Key_Phrases)    # Maps hash → list index for result mapping

        for result_item in batch_result.result_list:
            hash_key          = hash_to_index[result_item.index]
            results[hash_key] = result_item

        return results

    # ============================================================================
    # BATCH SYNTAX DETECTION (Native AWS Batch API)
    # ============================================================================

    @type_safe
    def batch_detect_syntax(self                                                                    ,      # Process multiple texts for syntax using native batch API
                           texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]         ,      # Hash → text mapping for batch processing
                           language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                           use_cache     : bool                            = False
                      ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Batch_Item__Detect_Syntax]:

        hash_to_index = {}
        text_list     = []

        for i, (hash_key, text) in enumerate(texts.items()):
            hash_to_index[i] = hash_key
            text_list.append(text)

        batch_result = self.comprehend_batch.batch_detect_syntax(text_list     = text_list    ,
                                                                 language_code = language_code)

        results = Type_Safe__Dict(expected_key_type   = Safe_Str__Hash                          ,
                          expected_value_type = Schema__Comprehend__Batch_Item__Detect_Syntax)    # Maps hash → list index for result mapping

        for result_item in batch_result.result_list:
            hash_key          = hash_to_index[result_item.index]
            results[hash_key] = result_item

        return results

    # ============================================================================
    # BATCH TOXIC CONTENT DETECTION (NO Native Batch API - Manual Iteration)
    # ============================================================================

    @type_safe
    def batch_detect_toxic_content(self                                                             ,      # Process multiple texts for toxicity (NO native batch API available)
                                   texts         : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]  ,      # Hash → text mapping for batch processing
                                   language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                                  use_cache     : bool                            = False
                             ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Detect_Toxic_Content]:

        # AWS Comprehend does NOT provide batch_detect_toxic_content API
        # We must fall back to individual calls per text

        results = Type_Safe__Dict(expected_key_type   = Safe_Str__Hash                          ,
                                  expected_value_type = Schema__Comprehend__Detect_Toxic_Content)    # Maps hash → list index for result mapping


        for hash_key, text in texts.items():
            result = self.comprehend_service.detect_toxic_content(text          = text         ,
                                                                  language_code = language_code,
                                                                  use_cache     = use_cache    )
            results[hash_key] = result

        return results