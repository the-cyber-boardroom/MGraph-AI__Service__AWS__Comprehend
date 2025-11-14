from unittest                                                                                 import TestCase
from fastapi                                                                                  import FastAPI
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
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend                      import Routes__Comprehend
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Request             import Schema__Comprehend__Request
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                             import Comprehend__Service


class test_Routes__Comprehend(TestCase):

    @classmethod
    def setUpClass(cls):
        # if in_github_action():
        #     pytest.skip("Skipping this test on GitHub Actions (since it needs AWS Auth")
        #cls.app                = FastAPI()
        # cls.comprehend         = Comprehend__with_temp_role()
        # cls.comprehend_detect  = cls.comprehend.detect()
        # cls.comprehend_service = Comprehend__Service(comprehend_detect  = cls.comprehend_detect )
        # cls.routes             = Routes__Comprehend (app                = cls.app               ,
        #                                              comprehend_service = cls.comprehend_service).setup()
        # when using the AWS credentials, this all we need
        cls.routes = Routes__Comprehend(app=FastAPI()).setup()

    def test__setUpClass(self):                                                # Test routes setup
        with self.routes as _:
            assert type(_)                       is Routes__Comprehend
            assert _.tag                         == 'comprehend'
            assert type(_.comprehend          )  is Comprehend
            assert type(_.comprehend_service())  is Comprehend__Service
            assert _.routes_paths()              == [ '/detect-dominant-language',          # the .routes_paths don't have the TAG__ROUTES_COMPREHEND prefix
                                                      '/detect-entities'         ,
                                                      '/detect-key-phrases'      ,
                                                      '/detect-pii-entities'     ,
                                                      '/detect-sentiment'        ,
                                                      '/detect-syntax'           ,
                                                      '/detect-toxic-content'    ]

    # ========================================
    # detect_sentiment Tests
    # ========================================

    def test__detect_sentiment__basic(self):                                   # Test basic sentiment detection endpoint
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("This is a test"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH     ,
                                              use_cache     = False                                       )

        response = self.routes.detect_sentiment(request)

        assert type(response)   is Schema__Comprehend__Detect_Sentiment
        assert response.sentiment in ['Positive', 'Negative', 'Neutral', 'Mixed']
        assert 0.0 <= response.score.positive <= 1.0

    def test__detect_sentiment__positive_text(self):                            # Test sentiment with clearly positive text
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("This is amazing and wonderful!"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH                     ,
                                              use_cache     = False                                                       )

        response = self.routes.detect_sentiment(request)

        assert type(response) is Schema__Comprehend__Detect_Sentiment
        assert response.score.positive > response.score.negative                # Should be more positive

    def test__detect_sentiment__negative_text(self):                            # Test sentiment with clearly negative text
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("This is terrible and awful"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH                ,
                                              use_cache     = False                                                  )

        response = self.routes.detect_sentiment(request)

        assert type(response) is Schema__Comprehend__Detect_Sentiment
        assert response.score.negative > response.score.positive                # Should be more negative

    # ========================================
    # detect_key_phrases Tests
    # ========================================

    def test__detect_key_phrases__basic(self):                                 # Test basic key phrase extraction
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("AWS Lambda is a serverless service"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH                        ,
                                              use_cache     = False                                                          )

        response = self.routes.detect_key_phrases(request)

        assert type(response)           is Schema__Comprehend__Detect_Key_Phrases
        assert len(response.key_phrases) > 0

    def test__detect_key_phrases__simple_text(self):                            # Test key phrases with simple text
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("Hello World"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH ,
                                              use_cache     = False                                   )

        response = self.routes.detect_key_phrases(request)

        assert type(response) is Schema__Comprehend__Detect_Key_Phrases

    # ========================================
    # detect_entities Tests
    # ========================================

    def test__detect_entities__with_entities(self):                            # Test entity detection with clear entities
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("Amazon was founded by Jeff Bezos"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH                       ,
                                              use_cache     = False                                                         )

        response = self.routes.detect_entities(request)

        assert type(response)       is Schema__Comprehend__Detect_Entities
        assert len(response.entities) > 0

    def test__detect_entities__no_entities(self):                              # Test entity detection with no entities
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("It was nice"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH   ,
                                              use_cache     = False                                     )

        response = self.routes.detect_entities(request)

        assert type(response) is Schema__Comprehend__Detect_Entities

    # ========================================
    # detect_dominant_language Tests
    # ========================================

    def test__detect_dominant_language__english(self):                         # Test language detection for English
        request = Schema__Comprehend__Request(text      = Safe_Str__Comprehend__Text("This is English"),
                                              use_cache = False                                         )

        response = self.routes.detect_dominant_language(request)

        assert type(response)           is Schema__Comprehend__Detect_Dominant_Language
        assert len(response.languages)  > 0
        assert response.languages[0].language_code == 'en'

    def test__detect_dominant_language__spanish(self):                         # Test language detection for Spanish
        request = Schema__Comprehend__Request(text      = Safe_Str__Comprehend__Text("Hola mundo"),
                                              use_cache = False                                    )

        response = self.routes.detect_dominant_language(request)

        assert type(response)          is Schema__Comprehend__Detect_Dominant_Language
        assert len(response.languages) > 0

    # ========================================
    # detect_pii_entities Tests
    # ========================================

    def test__detect_pii_entities__with_email(self):                           # Test PII detection with email
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("Email: test@example.com"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH               ,
                                              use_cache     = False                                                 )

        response = self.routes.detect_pii_entities(request)

        assert type(response) is Schema__Comprehend__Detect_Pii_Entities

    def test__detect_pii_entities__clean_text(self):                           # Test PII detection with clean text
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("The weather is nice"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH            ,
                                              use_cache     = False                                              )

        response = self.routes.detect_pii_entities(request)

        assert type(response)           is Schema__Comprehend__Detect_Pii_Entities
        assert len(response.entities)   == 0

    # ========================================
    # detect_syntax Tests
    # ========================================

    def test__detect_syntax__basic(self):                                      # Test syntax detection
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("The quick fox"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH   ,
                                              use_cache     = False                                     )

        response = self.routes.detect_syntax(request)

        assert type(response)               is Schema__Comprehend__Detect_Syntax
        assert len(response.syntax_tokens)  > 0

    # ========================================
    # detect_toxic_content Tests
    # ========================================

    def test__detect_toxic_content__clean(self):                               # Test toxicity with clean text
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("Have a nice day"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH       ,
                                              use_cache     = False                                         )

        response = self.routes.detect_toxic_content(request)

        assert type(response)       is Schema__Comprehend__Detect_Toxic_Content
        assert len(response.labels) > 0

    def test__detect_toxic_content__rude(self):                                # Test toxicity with rude text
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("You are stupid"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH      ,
                                              use_cache     = False                                        )

        response = self.routes.detect_toxic_content(request)

        assert type(response)       is Schema__Comprehend__Detect_Toxic_Content
        assert len(response.labels) > 0
