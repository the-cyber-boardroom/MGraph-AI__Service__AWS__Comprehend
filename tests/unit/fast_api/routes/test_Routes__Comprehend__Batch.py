import pytest
from unittest                                                                                     import TestCase
from fastapi                                                                                      import FastAPI
from osbot_aws.aws.comprehend.schemas.batch.Schema__Comprehend__Batch_Item__Detect_Sentiment      import Schema__Comprehend__Batch_Item__Detect_Sentiment
from osbot_utils.type_safe.primitives.core.Safe_Float                                             import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                              import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                import Safe_Str__Hash
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                      import Safe_Str__Text
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content             import Schema__Comprehend__Detect_Toxic_Content
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code                       import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                     import Safe_Str__Comprehend__Text
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                             import Type_Safe__Dict
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend__Batch                   import Routes__Comprehend__Batch
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Batch_Request           import Schema__Comprehend__Batch_Request
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Batch_Threshold_Request import Schema__Comprehend__Batch_Threshold_Request
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Batch_Boolean_Response import Schema__Comprehend__Batch_Boolean_Response
from mgraph_ai_service_aws_comprehend.service.Comprehend__Batch__Service                          import Comprehend__Batch__Service


class test_Routes__Comprehend__Batch(TestCase):

    @classmethod
    def setUpClass(cls):
        # if in_github_action():
        #     pytest.skip("Skipping this test on GitHub Actions (since it needs AWS Auth")
        #
        # cls.app    = FastAPI()
        # cls.comprehend         = Comprehend__with_temp_role()
        # cls.comprehend_detect  = cls.comprehend.detect()
        # cls.comprehend_service = Comprehend__Service(comprehend_detect  = cls.comprehend_detect )
        # cls.comprehend_batch   = cls.comprehend.batch()
        # cls.batch_service      = Comprehend__Batch__Service(comprehend_batch   = cls.comprehend_batch  ,
        #                                                     comprehend_service = cls.comprehend_service)
        # cls.routes             = Routes__Comprehend__Batch (app           = cls.app          ,
        #                                                     batch_service = cls.batch_service).setup()

        cls.routes = Routes__Comprehend__Batch(app=FastAPI()).setup()

    def test__setUpClass(self):                                                # Test routes setup
        with self.routes as _:
            assert type(_)                  is Routes__Comprehend__Batch
            assert _.tag                    == 'comprehend-batch'
            assert type(_.batch_service())  is Comprehend__Batch__Service
            assert _.routes_paths()         == [ '/detect-sentiment',
                                                 '/detect-toxic'    ,
                                                 '/is-negative'     ,
                                                 '/is-positive'     ,
                                                 '/is-toxic'        ]

    # ========================================
    # detect_sentiment Tests
    # ========================================

    def test__detect_sentiment__single_text(self):                             # Test batch sentiment with single text
        texts   = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test text")}
        request = Schema__Comprehend__Batch_Request(texts         = texts                                    ,
                                                    language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                    use_cache     = False                                  )

        response = self.routes.detect_sentiment(request)

        assert type(response) is Type_Safe__Dict
        assert len(response)  == 1
        assert Safe_Str__Hash("abc1234567") in response
        assert type(response[Safe_Str__Hash("abc1234567")]) is Schema__Comprehend__Batch_Item__Detect_Sentiment

    def test__detect_sentiment__multiple_texts(self):                          # Test batch sentiment with multiple texts
        texts   = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Positive"),
                   Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Negative"),
                   Safe_Str__Hash("ccc1234567"): Safe_Str__Comprehend__Text("Neutral") }
        request = Schema__Comprehend__Batch_Request(texts         = texts                                    ,
                                                    language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                    use_cache     = False                                  )

        response = self.routes.detect_sentiment(request)

        assert type(response) is Type_Safe__Dict
        assert len(response)  == 3
        assert all(hash_key in response for hash_key in texts.keys())
        assert all(type(result) is Schema__Comprehend__Batch_Item__Detect_Sentiment for result in response.values())

    def test__detect_sentiment__empty(self):                                   # Test batch sentiment with empty dict
        texts   = {}
        request = Schema__Comprehend__Batch_Request(texts         = texts                                    ,
                                                    language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                    use_cache     = False                                  )

        response = self.routes.detect_sentiment(request)

        assert type(response) is Type_Safe__Dict
        assert len(response)  == 0

    # ========================================
    # detect_toxic Tests
    # ========================================

    def test__detect_toxic__single_text(self):                                 # Test batch toxicity with single text
        pytest.skip("Toxic content detection - not available on eu-west-2 (London) ")
        texts   = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test text")}
        request = Schema__Comprehend__Batch_Request(texts         = texts                                    ,
                                                    language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                    use_cache     = False                                  )

        response = self.routes.detect_toxic(request)

        assert type(response) is Type_Safe__Dict
        assert len(response)  == 1
        assert Safe_Str__Hash("abc1234567") in response
        assert type(response[Safe_Str__Hash("abc1234567")]) is Schema__Comprehend__Detect_Toxic_Content

    def test__detect_toxic__multiple_texts(self):                              # Test batch toxicity with multiple texts
        pytest.skip("Toxic content detection - not available on eu-west-2 (London) ")
        texts   = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Clean"),
                   Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Rude") ,
                   Safe_Str__Hash("ccc1234567"): Safe_Str__Comprehend__Text("Normal")}
        request = Schema__Comprehend__Batch_Request(texts         = texts                                    ,
                                                    language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                    use_cache     = False                                  )

        response = self.routes.detect_toxic(request)

        assert type(response) is Type_Safe__Dict
        assert len(response)  == 3
        assert all(type(result) is Schema__Comprehend__Detect_Toxic_Content for result in response.values())

    # ========================================
    # is_positive Tests
    # ========================================

    def test__is_positive__single_text(self):                                  # Test batch is_positive with single text
        texts   = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Great!")}
        request = Schema__Comprehend__Batch_Threshold_Request(texts         = texts                                    ,
                                                              threshold     = Safe_Float(0.5)                        ,
                                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                              use_cache     = False                                  )

        response = self.routes.is_positive(request)

        assert type(response)       is Schema__Comprehend__Batch_Boolean_Response
        assert len(response.results) == 1
        assert len(response.scores)  == 1
        assert response.threshold   == Safe_Float(0.5)
        assert response.operation   == Safe_Str__Text('is_positive')
        assert response.total       == Safe_UInt(1)

    def test__is_positive__multiple_texts(self):                               # Test batch is_positive with multiple texts
        texts   = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Amazing!"),
                   Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Terrible"),
                   Safe_Str__Hash("ccc1234567"): Safe_Str__Comprehend__Text("Okay")    }
        request = Schema__Comprehend__Batch_Threshold_Request(texts         = texts                                    ,
                                                              threshold     = Safe_Float(0.5)                        ,
                                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                              use_cache     = False                                  )

        response = self.routes.is_positive(request)

        assert type(response)       is Schema__Comprehend__Batch_Boolean_Response
        assert len(response.results) == 3
        assert len(response.scores)  == 3
        assert response.total       == Safe_UInt(3)
        assert all(isinstance(result, bool) for result in response.results.values())

    # ========================================
    # is_negative Tests
    # ========================================

    def test__is_negative__single_text(self):                                  # Test batch is_negative with single text
        texts   = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Terrible!")}
        request = Schema__Comprehend__Batch_Threshold_Request(texts         = texts                                    ,
                                                              threshold     = Safe_Float(0.5)                        ,
                                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                              use_cache     = False                                  )

        response = self.routes.is_negative(request)

        assert type(response)     is Schema__Comprehend__Batch_Boolean_Response
        assert response.operation == Safe_Str__Text('is_negative')

    def test__is_negative__multiple_texts(self):                               # Test batch is_negative with multiple texts
        texts   = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Bad"),
                   Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Awful")}
        request = Schema__Comprehend__Batch_Threshold_Request(texts         = texts                                    ,
                                                              threshold     = Safe_Float(0.5)                        ,
                                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                              use_cache     = False                                  )

        response = self.routes.is_negative(request)

        assert type(response)       is Schema__Comprehend__Batch_Boolean_Response
        assert len(response.results) == 2

    # ========================================
    # is_toxic Tests
    # ========================================

    def test__is_toxic__single_text(self):                                     # Test batch is_toxic with single text
        pytest.skip("Toxic content detection - not available on eu-west-2 (London) ")
        texts   = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("You are an idiot")}
        request = Schema__Comprehend__Batch_Threshold_Request(texts         = texts                                    ,
                                                              threshold     = Safe_Float(0.5)                        ,
                                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                              use_cache     = False                                  )

        response = self.routes.is_toxic(request)

        assert type(response)     is Schema__Comprehend__Batch_Boolean_Response
        assert response.operation == Safe_Str__Text('is_toxic')

    def test__is_toxic__multiple_texts(self):                                  # Test batch is_toxic with multiple texts
        pytest.skip("Toxic content detection - not available on eu-west-2 (London) ")
        texts   = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Clean text"),
                   Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Rude text") }
        request = Schema__Comprehend__Batch_Threshold_Request(texts         = texts                                    ,
                                                              threshold     = Safe_Float(0.5)                        ,
                                                              language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                              use_cache     = False                                  )

        response = self.routes.is_toxic(request)

        assert type(response)       is Schema__Comprehend__Batch_Boolean_Response
        assert len(response.results) == 2
        assert len(response.scores)  == 2
        assert response.total       == Safe_UInt(2)
