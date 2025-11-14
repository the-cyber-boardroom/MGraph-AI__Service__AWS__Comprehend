from unittest                                                                          import TestCase
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash     import Safe_Str__Hash
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Sentiment      import Schema__Comprehend__Detect_Sentiment
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content  import Schema__Comprehend__Detect_Toxic_Content
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code            import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text          import Safe_Str__Comprehend__Text
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                      import Comprehend__Service
from mgraph_ai_service_aws_comprehend.service.Comprehend__Batch__Service               import Comprehend__Batch__Service


class test_Comprehend__Batch__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        comprehend_service  = Comprehend__Service()
        cls.batch_service   = Comprehend__Batch__Service(comprehend_service=comprehend_service)

    def test__init__(self):                                                    # Test batch service initialization
        with self.batch_service as _:
            assert type(_)                    is Comprehend__Batch__Service
            assert type(_.comprehend_service) is Comprehend__Service

    # ========================================
    # batch_detect_sentiment Tests
    # ========================================

    def test__batch_detect_sentiment__single_text(self):                       # Test batch sentiment with single text
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test text")}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is dict
        assert len(results)  == 1
        assert Safe_Str__Hash("abc1234567") in results
        assert type(results[Safe_Str__Hash("abc1234567")]) is Schema__Comprehend__Detect_Sentiment

    def test__batch_detect_sentiment__multiple_texts(self):                    # Test batch sentiment with multiple texts
        texts = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Positive text")   ,
                 Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Negative text")   ,
                 Safe_Str__Hash("ccc1234567"): Safe_Str__Comprehend__Text("Neutral text")    }

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is dict
        assert len(results)  == 3
        assert all(hash_key in results for hash_key in texts.keys())
        assert all(type(result) is Schema__Comprehend__Detect_Sentiment for result in results.values())

    def test__batch_detect_sentiment__empty(self):                             # Test batch sentiment with empty dict
        texts = {}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is dict
        assert len(results)  == 0

    def test__batch_detect_sentiment__with_cache(self):                        # Test batch sentiment with caching enabled
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test")}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = True                                   )

        assert type(results) is dict
        assert len(results)  == 1

    # ========================================
    # batch_detect_toxic_content Tests
    # ========================================

    def test__batch_detect_toxic_content__single_text(self):                   # Test batch toxicity with single text
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test text")}

        results = self.batch_service.batch_detect_toxic_content(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = False                                  )

        assert type(results) is dict
        assert len(results)  == 1
        assert Safe_Str__Hash("abc1234567") in results
        assert type(results[Safe_Str__Hash("abc1234567")]) is Schema__Comprehend__Detect_Toxic_Content

    def test__batch_detect_toxic_content__multiple_texts(self):                # Test batch toxicity with multiple texts
        texts = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Clean text")   ,
                 Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Rude text")    ,
                 Safe_Str__Hash("ccc1234567"): Safe_Str__Comprehend__Text("Normal text")  }

        results = self.batch_service.batch_detect_toxic_content(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = False                                  )

        assert type(results) is dict
        assert len(results)  == 3
        assert all(hash_key in results for hash_key in texts.keys())
        assert all(type(result) is Schema__Comprehend__Detect_Toxic_Content for result in results.values())

    def test__batch_detect_toxic_content__empty(self):                         # Test batch toxicity with empty dict
        texts = {}

        results = self.batch_service.batch_detect_toxic_content(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = False                                  )

        assert type(results) is dict
        assert len(results)  == 0

    def test__batch_detect_toxic_content__with_cache(self):                    # Test batch toxicity with caching enabled
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test")}

        results = self.batch_service.batch_detect_toxic_content(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = True                                   )

        assert type(results) is dict
        assert len(results)  == 1
