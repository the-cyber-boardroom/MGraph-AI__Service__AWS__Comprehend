from osbot_aws.aws.comprehend.Comprehend__Detect import Comprehend__Detect
from osbot_utils.decorators.methods.cache_on_self                                             import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                import type_safe
from osbot_aws.aws.comprehend.Comprehend                                                      import Comprehend
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Sentiment             import Schema__Comprehend__Detect_Sentiment
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Key_Phrases           import Schema__Comprehend__Detect_Key_Phrases
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Entities              import Schema__Comprehend__Detect_Entities
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Dominant_Language     import Schema__Comprehend__Detect_Dominant_Language
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Pii_Entities          import Schema__Comprehend__Detect_Pii_Entities
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Syntax                import Schema__Comprehend__Detect_Syntax
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content         import Schema__Comprehend__Detect_Toxic_Content
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code                   import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                 import Safe_Str__Comprehend__Text
from mgraph_ai_service_aws_comprehend.service.Comprehend__Cache__Service                      import Comprehend__Cache__Service


class Comprehend__Service(Type_Safe):                                          # Main orchestrator for AWS Comprehend operations with caching support
    comprehend     : Comprehend                                                # OSBot-AWS Comprehend instance
    cache_service  : Comprehend__Cache__Service                                # Caching service

    # ============================================================================
    # SENTIMENT DETECTION
    # ============================================================================

    @cache_on_self
    def comprehend_detect(self) -> Comprehend__Detect:
        return self.comprehend.detect()

    @type_safe
    def detect_sentiment(self                                                         ,  # Detect sentiment with optional caching
                        text          : Safe_Str__Comprehend__Text                    ,
                        language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                        use_cache     : bool                            = False
                   ) -> Schema__Comprehend__Detect_Sentiment:

        if use_cache:
            cached_result = self.cache_service.get_sentiment(text, language_code)
            if cached_result:
                return cached_result

        result = self.comprehend_detect().detect_sentiment(text, language_code)

        if use_cache:
            self.cache_service.store_sentiment(text, language_code, result)

        return result

    # ============================================================================
    # KEY PHRASES DETECTION
    # ============================================================================

    @type_safe
    def detect_key_phrases(self                                                       ,  # Detect key phrases with optional caching
                          text          : Safe_Str__Comprehend__Text                  ,
                          language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                          use_cache     : bool                            = False
                     ) -> Schema__Comprehend__Detect_Key_Phrases:

        if use_cache:
            cached_result = self.cache_service.get_key_phrases(text, language_code)
            if cached_result:
                return cached_result

        result = self.comprehend_detect().detect_key_phrases(text, language_code)

        if use_cache:
            self.cache_service.store_key_phrases(text, language_code, result)

        return result

    # ============================================================================
    # ENTITY DETECTION
    # ============================================================================

    @type_safe
    def detect_entities(self                                                          ,  # Detect entities with optional caching
                       text          : Safe_Str__Comprehend__Text                     ,
                       language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                       use_cache     : bool                            = False
                  ) -> Schema__Comprehend__Detect_Entities:

        if use_cache:
            cached_result = self.cache_service.get_entities(text, language_code)
            if cached_result:
                return cached_result

        result = self.comprehend_detect().detect_entities(text, language_code)

        if use_cache:
            self.cache_service.store_entities(text, language_code, result)

        return result

    # ============================================================================
    # DOMINANT LANGUAGE DETECTION
    # ============================================================================

    @type_safe
    def detect_dominant_language(self                            ,                     # Detect dominant language with optional caching
                                text      : Safe_Str__Comprehend__Text                 ,
                                use_cache : bool                   = False
                           ) -> Schema__Comprehend__Detect_Dominant_Language:

        if use_cache:
            cached_result = self.cache_service.get_dominant_language(text)
            if cached_result:
                return cached_result

        result = self.comprehend_detect().detect_dominant_language(text)

        if use_cache:
            self.cache_service.store_dominant_language(text, result)

        return result

    # ============================================================================
    # PII DETECTION
    # ============================================================================

    @type_safe
    def detect_pii_entities(self                                                      ,  # Detect PII entities with optional caching
                           text          : Safe_Str__Comprehend__Text                 ,
                           language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                           use_cache     : bool                            = False
                      ) -> Schema__Comprehend__Detect_Pii_Entities:

        if use_cache:
            cached_result = self.cache_service.get_pii_entities(text, language_code)
            if cached_result:
                return cached_result

        result = self.comprehend_detect().detect_pii_entities(text, language_code)

        if use_cache:
            self.cache_service.store_pii_entities(text, language_code, result)

        return result

    # ============================================================================
    # SYNTAX DETECTION
    # ============================================================================

    @type_safe
    def detect_syntax(self                                                            ,  # Detect syntax with optional caching
                     text          : Safe_Str__Comprehend__Text                       ,
                     language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                     use_cache     : bool                            = False
                ) -> Schema__Comprehend__Detect_Syntax:

        if use_cache:
            cached_result = self.cache_service.get_syntax(text, language_code)
            if cached_result:
                return cached_result

        result = self.comprehend_detect().detect_syntax(text, language_code)

        if use_cache:
            self.cache_service.store_syntax(text, language_code, result)

        return result

    # ============================================================================
    # TOXIC CONTENT DETECTION
    # ============================================================================

    @type_safe
    def detect_toxic_content(self                                                     ,  # Detect toxic content with optional caching
                            text          : Safe_Str__Comprehend__Text                ,
                            language_code : Enum__Comprehend__Language_Code = Enum__Comprehend__Language_Code.ENGLISH,
                            use_cache     : bool                            = False
                       ) -> Schema__Comprehend__Detect_Toxic_Content:

        if use_cache:
            cached_result = self.cache_service.get_toxic_content(text, language_code)
            if cached_result:
                return cached_result

        result = self.comprehend_detect().detect_toxic_content(text, language_code)

        if use_cache:
            self.cache_service.store_toxic_content(text, language_code, result)

        return result
