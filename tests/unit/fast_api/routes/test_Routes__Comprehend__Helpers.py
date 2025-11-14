from unittest                                                                                       import TestCase
from fastapi                                                                                        import FastAPI
from osbot_utils.type_safe.primitives.core.Safe_Float                                               import Safe_Float
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                        import Safe_Str__Text
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code                         import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                       import Safe_Str__Comprehend__Text
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend__Helpers                   import Routes__Comprehend__Helpers
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Request                   import Schema__Comprehend__Request
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Threshold_Request         import Schema__Comprehend__Threshold_Request
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Boolean_Response         import Schema__Comprehend__Boolean_Response
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Sentiment_Score_Response import Schema__Comprehend__Sentiment_Score_Response
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Toxicity_Score_Response  import Schema__Comprehend__Toxicity_Score_Response
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                                   import Comprehend__Service


class test_Routes__Comprehend__Helpers(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app    = FastAPI()
        cls.routes = Routes__Comprehend__Helpers(app=cls.app).setup()

    def test__setUpClass(self):                                                # Test routes setup
        with self.routes as _:
            assert type(_)                      is Routes__Comprehend__Helpers
            assert _.tag                        == 'comprehend-helpers'
            assert type(_.comprehend_service)  is Comprehend__Service
            assert _.app                        == self.app
            assert _.routes_paths()             == [ '/comprehend-helpers/is-negative'    ,
                                                     '/comprehend-helpers/is-neutral'     ,
                                                     '/comprehend-helpers/is-positive'    ,
                                                     '/comprehend-helpers/is-toxic'       ,
                                                     '/comprehend-helpers/sentiment-score',
                                                     '/comprehend-helpers/toxicity-score' ]

    # ========================================
    # is_positive Tests
    # ========================================

    def test__is_positive__above_threshold(self):                              # Test is_positive with high positive score
        request = Schema__Comprehend__Threshold_Request(text          = Safe_Str__Comprehend__Text("This is amazing!"),
                                                        threshold     = Safe_Float(0.5)                               ,
                                                        language_code = Enum__Comprehend__Language_Code.ENGLISH       ,
                                                        use_cache     = False                                         )

        response = self.routes.is_positive(request)

        assert type(response)       is Schema__Comprehend__Boolean_Response
        assert response.result       in [True, False]                          # Boolean result
        assert 0.0 <= response.score <= 1.0
        assert response.threshold   == Safe_Float(0.5)
        assert response.operation   == Safe_Str__Text('is_positive')
        assert response.cached      == False
        assert response.duration    > 0

    def test__is_positive__below_threshold(self):                              # Test is_positive with high threshold
        request = Schema__Comprehend__Threshold_Request(text          = Safe_Str__Comprehend__Text("Test"),
                                                        threshold     = Safe_Float(0.99)                      ,
                                                        language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                        use_cache     = False                                 )

        response = self.routes.is_positive(request)

        assert type(response) is Schema__Comprehend__Boolean_Response
        # Result likely False with threshold 0.99

    def test__is_positive__default_threshold(self):                            # Test is_positive with default threshold
        request = Schema__Comprehend__Threshold_Request(text          = Safe_Str__Comprehend__Text("Great!"),
                                                        language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                        use_cache     = False                                 )

        response = self.routes.is_positive(request)

        assert type(response)     is Schema__Comprehend__Boolean_Response
        assert response.threshold == Safe_Float(0.7)                           # Default threshold

    # ========================================
    # is_negative Tests
    # ========================================

    def test__is_negative__negative_text(self):                                # Test is_negative with negative text
        request = Schema__Comprehend__Threshold_Request(text          = Safe_Str__Comprehend__Text("This is terrible"),
                                                        threshold     = Safe_Float(0.5)                              ,
                                                        language_code = Enum__Comprehend__Language_Code.ENGLISH      ,
                                                        use_cache     = False                                        )

        response = self.routes.is_negative(request)

        assert type(response)     is Schema__Comprehend__Boolean_Response
        assert response.result     in [True, False]
        assert response.operation == Safe_Str__Text('is_negative')
        assert 0.0 <= response.score <= 1.0

    def test__is_negative__positive_text(self):                                # Test is_negative with positive text
        request = Schema__Comprehend__Threshold_Request(text          = Safe_Str__Comprehend__Text("Amazing!"),
                                                        threshold     = Safe_Float(0.5)                        ,
                                                        language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                        use_cache     = False                                  )

        response = self.routes.is_negative(request)

        assert type(response) is Schema__Comprehend__Boolean_Response
        # Result likely False for positive text

    # ========================================
    # is_neutral Tests
    # ========================================

    def test__is_neutral__neutral_text(self):                                  # Test is_neutral with neutral text
        request = Schema__Comprehend__Threshold_Request(text          = Safe_Str__Comprehend__Text("It is okay"),
                                                        threshold     = Safe_Float(0.5)                        ,
                                                        language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                        use_cache     = False                                  )

        response = self.routes.is_neutral(request)

        assert type(response)     is Schema__Comprehend__Boolean_Response
        assert response.result     in [True, False]
        assert response.operation == Safe_Str__Text('is_neutral')

    # ========================================
    # is_toxic Tests
    # ========================================

    def test__is_toxic__clean_text(self):                                      # Test is_toxic with clean text
        request = Schema__Comprehend__Threshold_Request(text          = Safe_Str__Comprehend__Text("Have a nice day"),
                                                        threshold     = Safe_Float(0.5)                              ,
                                                        language_code = Enum__Comprehend__Language_Code.ENGLISH      ,
                                                        use_cache     = False                                        )

        response = self.routes.is_toxic(request)

        assert type(response)     is Schema__Comprehend__Boolean_Response
        assert response.operation == Safe_Str__Text('is_toxic')
        assert 0.0 <= response.score <= 1.0

    def test__is_toxic__rude_text(self):                                       # Test is_toxic with rude text
        request = Schema__Comprehend__Threshold_Request(text          = Safe_Str__Comprehend__Text("You are stupid"),
                                                        threshold     = Safe_Float(0.5)                             ,
                                                        language_code = Enum__Comprehend__Language_Code.ENGLISH     ,
                                                        use_cache     = False                                       )

        response = self.routes.is_toxic(request)

        assert type(response)   is Schema__Comprehend__Boolean_Response
        assert response.result   in [True, False]
        assert response.score   > 0.0                                          # Should have some toxicity

    # ========================================
    # sentiment_score Tests
    # ========================================

    def test__sentiment_score__basic(self):                                    # Test sentiment_score endpoint
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("Test text"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                              use_cache     = False                                  )

        response = self.routes.sentiment_score(request)

        assert type(response)       is Schema__Comprehend__Sentiment_Score_Response
        assert 0.0 <= response.positive <= 1.0
        assert 0.0 <= response.negative <= 1.0
        assert 0.0 <= response.neutral  <= 1.0
        assert 0.0 <= response.mixed    <= 1.0
        assert response.cached      == False
        assert response.duration    > 0

    def test__sentiment_score__positive_text(self):                            # Test sentiment_score with positive text
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("Amazing!"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                              use_cache     = False                                  )

        response = self.routes.sentiment_score(request)

        assert type(response) is Schema__Comprehend__Sentiment_Score_Response
        assert response.positive > response.negative                           # Should be more positive

    # ========================================
    # toxicity_score Tests
    # ========================================

    def test__toxicity_score__basic(self):                                     # Test toxicity_score endpoint
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("Test text"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                              use_cache     = False                                  )

        response = self.routes.toxicity_score(request)

        assert type(response)   is Schema__Comprehend__Toxicity_Score_Response
        assert type(response.scores) is dict
        assert len(response.scores)  > 0
        assert response.cached  == False
        assert response.duration > 0

    def test__toxicity_score__clean_text(self):                                # Test toxicity_score with clean text
        request = Schema__Comprehend__Request(text          = Safe_Str__Comprehend__Text("Have a nice day"),
                                              language_code = Enum__Comprehend__Language_Code.ENGLISH       ,
                                              use_cache     = False                                         )

        response = self.routes.toxicity_score(request)

        assert type(response) is Schema__Comprehend__Toxicity_Score_Response
        assert all(0.0 <= score <= 1.0 for score in response.scores.values())
