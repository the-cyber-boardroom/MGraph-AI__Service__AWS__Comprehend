import pytest
from unittest                                                                                 import TestCase
from osbot_aws.aws.comprehend.Comprehend__Detect                                              import Comprehend__Detect
from osbot_aws.aws.comprehend.Comprehend__IAM__Temp_Role                                      import Comprehend__with_temp_role
from osbot_utils.testing.__                                                                   import __, __SKIP__, __GREATER_THAN__, __LESS_THAN__
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Sentiment             import Schema__Comprehend__Detect_Sentiment
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Key_Phrases           import Schema__Comprehend__Detect_Key_Phrases
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Entities              import Schema__Comprehend__Detect_Entities
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Dominant_Language     import Schema__Comprehend__Detect_Dominant_Language
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Pii_Entities          import Schema__Comprehend__Detect_Pii_Entities
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Syntax                import Schema__Comprehend__Detect_Syntax
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content         import Schema__Comprehend__Detect_Toxic_Content
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code                   import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                 import Safe_Str__Comprehend__Text
from osbot_utils.utils.Env                                                                    import in_github_action
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                             import Comprehend__Service
from mgraph_ai_service_aws_comprehend.service.Comprehend__Cache__Service                      import Comprehend__Cache__Service


class test_Comprehend__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        if in_github_action():
            pytest.skip("Skipping this test on GitHub Actions (since it needs AWS Auth")
        cls.comprehend        = Comprehend__with_temp_role()                          # use this version which has a dedicated role for the Comprehend service
        cls.comprehend_detect = cls.comprehend.detect()
        cls.service           = Comprehend__Service(comprehend_detect=cls.comprehend_detect)

    def test__init__(self):                                                    # Test service initialization
        with self.service as _:
            assert type(_)                   is Comprehend__Service
            assert type(_.comprehend_detect) is Comprehend__Detect
            assert type(_.cache_service    ) is Comprehend__Cache__Service

    # ========================================
    # detect_sentiment Tests
    # ========================================

    def test__detect_sentiment__basic(self):                                   # Test basic sentiment detection without cache
        text   = Safe_Str__Comprehend__Text("This is a test")
        result = self.service.detect_sentiment(text, use_cache=False)

        assert type(result)     is Schema__Comprehend__Detect_Sentiment
        assert result.sentiment in ['Positive', 'Negative', 'Neutral', 'Mixed']
        assert 0.0 <= result.score.positive <= 1.0
        assert 0.0 <= result.score.negative <= 1.0
        assert 0.0 <= result.score.neutral  <= 1.0
        assert 0.0 <= result.score.mixed    <= 1.0
        assert result.obj() == __( sentiment = 'Neutral'                                                                                             ,
                                   score     = __(mixed    = __LESS_THAN__   (0.04) ,    # 0.03025072067975998
                                                  negative = __LESS_THAN__   (0.03) ,    # 0.023267695680260658
                                                  neutral  = __GREATER_THAN__(0.8 )  ,    # 0.8832748532295227
                                                  positive = __LESS_THAN__   (0.07)) ,    # 0.0632067397236824
                                   duration  = __SKIP__   )

    def test__detect_sentiment__with_language_code(self):                      # Test sentiment detection with explicit language
        text   = Safe_Str__Comprehend__Text("Test text")
        result = self.service.detect_sentiment(text                          = text                                    ,
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                              use_cache     = False                                  )

        assert type(result) is Schema__Comprehend__Detect_Sentiment

    def test__detect_sentiment__with_cache(self):                              # Test sentiment detection with caching enabled
        text   = Safe_Str__Comprehend__Text("Test")
        result = self.service.detect_sentiment(text, use_cache=True)

        assert type(result) is Schema__Comprehend__Detect_Sentiment
        # Note: Cache is placeholder, so this just tests interface

    # ========================================
    # detect_key_phrases Tests
    # ========================================

    def test__detect_key_phrases__basic(self):                                 # Test basic key phrase detection
        text   = Safe_Str__Comprehend__Text("AWS Lambda is a serverless compute service")
        result = self.service.detect_key_phrases(text, use_cache=False)

        assert type(result)         is Schema__Comprehend__Detect_Key_Phrases
        assert len(result.key_phrases) > 0
        assert result.duration       > 0

    def test__detect_key_phrases__empty_result(self):                          # Test key phrase detection with minimal text
        text   = Safe_Str__Comprehend__Text("Hi")
        result = self.service.detect_key_phrases(text, use_cache=False)

        assert type(result) is Schema__Comprehend__Detect_Key_Phrases

    # ========================================
    # detect_entities Tests
    # ========================================

    def test__detect_entities__basic(self):                                    # Test basic entity detection
        text   = Safe_Str__Comprehend__Text("Amazon was founded by Jeff Bezos in Seattle")
        result = self.service.detect_entities(text, use_cache=False)

        assert type(result)      is Schema__Comprehend__Detect_Entities
        assert len(result.entities) > 0
        assert result.duration   > 0

    def test__detect_entities__no_entities(self):                              # Test entity detection with no entities
        text   = Safe_Str__Comprehend__Text("It was nice")
        result = self.service.detect_entities(text, use_cache=False)

        assert type(result) is Schema__Comprehend__Detect_Entities

    # ========================================
    # detect_dominant_language Tests
    # ========================================

    def test__detect_dominant_language__english(self):                         # Test language detection for English
        text   = Safe_Str__Comprehend__Text("This is English text")
        result = self.service.detect_dominant_language(text, use_cache=False)

        assert type(result)         is Schema__Comprehend__Detect_Dominant_Language
        assert len(result.languages) > 0
        assert result.languages[0].language_code == 'en'

    def test__detect_dominant_language__spanish(self):                         # Test language detection for Spanish
        text   = Safe_Str__Comprehend__Text("Hola mundo")
        result = self.service.detect_dominant_language(text, use_cache=False)

        assert type(result)         is Schema__Comprehend__Detect_Dominant_Language
        assert len(result.languages) > 0

    # ========================================
    # detect_pii_entities Tests
    # ========================================

    def test__detect_pii_entities__with_email(self):                           # Test PII detection with email
        text   = Safe_Str__Comprehend__Text("My email is test@example.com")
        result = self.service.detect_pii_entities(text, use_cache=False)

        assert type(result) is Schema__Comprehend__Detect_Pii_Entities

    def test__detect_pii_entities__no_pii(self):                               # Test PII detection with no PII
        text   = Safe_Str__Comprehend__Text("The weather is nice")
        result = self.service.detect_pii_entities(text, use_cache=False)

        assert type(result)         is Schema__Comprehend__Detect_Pii_Entities
        assert len(result.entities) == 0

    # ========================================
    # detect_syntax Tests
    # ========================================

    def test__detect_syntax__basic(self):                                      # Test basic syntax detection
        text   = Safe_Str__Comprehend__Text("The quick brown fox")
        result = self.service.detect_syntax(text, use_cache=False)

        assert type(result)             is Schema__Comprehend__Detect_Syntax
        assert len(result.syntax_tokens) > 0

    # ========================================
    # detect_toxic_content Tests
    # ========================================

    def test__detect_toxic_content__clean(self):                               # Test toxicity detection with clean text
        text   = Safe_Str__Comprehend__Text("Have a great day")
        result = self.service.detect_toxic_content(text, use_cache=False)

        assert type(result)     is Schema__Comprehend__Detect_Toxic_Content
        assert len(result.labels) > 0

    def test__detect_toxic_content__rude(self):                                # Test toxicity detection with rude text
        text   = Safe_Str__Comprehend__Text("You are an idiot")
        result = self.service.detect_toxic_content(text, use_cache=False)

        assert type(result)     is Schema__Comprehend__Detect_Toxic_Content
        assert len(result.labels) > 0
