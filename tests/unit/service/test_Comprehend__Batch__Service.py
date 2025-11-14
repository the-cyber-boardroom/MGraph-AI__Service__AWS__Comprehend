from unittest                                                                                import TestCase
from osbot_aws.aws.comprehend.Comprehend__Batch                                              import Comprehend__Batch
from osbot_aws.aws.comprehend.Comprehend__IAM__Temp_Role                                     import Comprehend__with_temp_role
from osbot_aws.aws.comprehend.schemas.batch.Schema__Comprehend__Batch_Item__Detect_Sentiment import Schema__Comprehend__Batch_Item__Detect_Sentiment
from osbot_utils.testing.__                                                                  import __, __SKIP__, __LESS_THAN__, __GREATER_THAN__
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash           import Safe_Str__Hash
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content        import Schema__Comprehend__Detect_Toxic_Content
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code                  import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                import Safe_Str__Comprehend__Text
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                        import Type_Safe__Dict
from mgraph_ai_service_aws_comprehend.service.Comprehend__Cache__Service                     import Comprehend__Cache__Service
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                            import Comprehend__Service
from mgraph_ai_service_aws_comprehend.service.Comprehend__Batch__Service                     import Comprehend__Batch__Service


class test_Comprehend__Batch__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.comprehend          = Comprehend__with_temp_role()
        cls.comprehend_detect   = cls.comprehend.detect()
        cls.comprehend_batch    = cls.comprehend.batch()
        cls.comprehend_service  = Comprehend__Service       (comprehend_detect  = cls.comprehend_detect )
        cls.batch_service       = Comprehend__Batch__Service(comprehend_service = cls.comprehend_service,
                                                             comprehend_batch   = cls.comprehend_batch  )

    def test__init__(self):                                                    # Test batch service initialization
        with self.batch_service as _:
            assert type(_)                    is Comprehend__Batch__Service
            assert type(_.comprehend_batch  ) is Comprehend__Batch
            assert type(_.comprehend_service) is Comprehend__Service
            assert type(_.cache_service     ) is Comprehend__Cache__Service


    # ========================================
    # batch_detect_sentiment Tests
    # ========================================

    def test__batch_detect_sentiment__single_text(self):                       # Test batch sentiment with single text
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test text")}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 1
        assert Safe_Str__Hash("abc1234567") in results
        assert type(results[Safe_Str__Hash("abc1234567")]) is Schema__Comprehend__Batch_Item__Detect_Sentiment

        assert results.obj() == __(abc1234567=__(index     = 0                                                                                   ,
                                                 sentiment = 'Neutral'                                                                          ,
                                                 score     = __(mixed    = __LESS_THAN__   (0.04)  ,    # e.g. 0.022231953218579292
                                                                negative = __LESS_THAN__   (0.03)  ,    # e.g. 0.009739890694618225
                                                                neutral  = __GREATER_THAN__(0.9 )  ,    # e.g. 0.9545490145683289
                                                                positive = __LESS_THAN__   (0.05)) ,    # e.g. 0.013479218818247318
                                                 duration  = __SKIP__                              ))


    def test__batch_detect_sentiment__multiple_texts(self):                    # Test batch sentiment with multiple texts
        texts = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Positive text")   ,
                 Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Negative text")   ,
                 Safe_Str__Hash("ccc1234567"): Safe_Str__Comprehend__Text("Neutral text")    }

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results)  is Type_Safe__Dict
        assert len(results)   == 3
        assert results.obj()  == __(aaa1234567 = __(index     = 0                                                                                   ,
                                                    sentiment = 'Positive'                                                                         ,
                                                    score     = __(mixed    = __LESS_THAN__   (0.01)  ,    # e.g. 0.0008680016617290676
                                                                   negative = __LESS_THAN__   (0.01)  ,    # e.g. 0.0009610106935724616
                                                                   neutral  = __LESS_THAN__   (0.02)  ,    # e.g. 0.007862226106226444
                                                                   positive = __GREATER_THAN__(0.9 ))),   # e.g. 0.9903088212013245

                                    bbb1234567 = __(index     = 1                                                                                   ,
                                                    sentiment = 'Negative'                                                                         ,
                                                    score     = __(mixed    = __LESS_THAN__   (0.01)  ,    # e.g. 0.0009992261184379458
                                                                   negative = __GREATER_THAN__(0.9 )  ,    # e.g. 0.9965705871582031
                                                                   neutral  = __LESS_THAN__   (0.01)  ,    # e.g. 0.0022562050726264715
                                                                   positive = __LESS_THAN__   (0.01))),   # e.g. 0.0001739517174428329

                                    ccc1234567 = __(index     = 2                                                                                   ,
                                                    sentiment = 'Neutral'                                                                          ,
                                                    score     = __(mixed    = __LESS_THAN__   (0.04)  ,    # e.g. 0.03354164958000183
                                                                   negative = __LESS_THAN__   (0.2 )  ,    # e.g. 0.11283839493989944
                                                                   neutral  = __GREATER_THAN__(0.6 )  ,    # e.g. 0.6909114718437195
                                                                   positive = __LESS_THAN__   (0.3 ))))    # e.g. 0.16270844638347626

        # assert all(hash_key in results for hash_key in texts.keys())
        # assert all(type(result) is Schema__Comprehend__Detect_Sentiment for result in results.values())

    def test__batch_detect_sentiment__empty(self):                             # Test batch sentiment with empty dict
        texts = {}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 0

    def test__batch_detect_sentiment__with_cache(self):                        # Test batch sentiment with caching enabled
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test")}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = True                                   )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 1
        assert results.obj() == __(abc1234567 = __(index     = 0                                                                                 ,
                                                   sentiment = 'Neutral'                                                                        ,
                                                   score     = __(mixed    = __LESS_THAN__   (0.01) ,    # e.g. 0.0005342626827768981
                                                                  negative = __LESS_THAN__   (0.01) ,    # e.g. 0.0017269368981942534
                                                                  neutral  = __GREATER_THAN__(0.9 ) ,    # e.g. 0.9953723549842834
                                                                  positive = __LESS_THAN__   (0.01))))    # e.g. 0.002366372849792242


    # ========================================
    # batch_detect_toxic_content Tests
    # ========================================

    def test__batch_detect_toxic_content__single_text(self):                   # Test batch toxicity with single text
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test text")}

        results = self.batch_service.batch_detect_toxic_content(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 1
        assert Safe_Str__Hash("abc1234567") in results
        assert type(results[Safe_Str__Hash("abc1234567")]) is Schema__Comprehend__Detect_Toxic_Content

        assert results.obj() == __(abc1234567 = __(labels = [ __(name = 'PROFANITY'           , score = __LESS_THAN__(0.1)) ,   # e.g. 0.046799998730421066
                                                              __(name = 'HATE_SPEECH'         , score = __LESS_THAN__(0.1)) ,   # e.g. 0.08839999884366989
                                                              __(name = 'INSULT'              , score = __LESS_THAN__(0.2)) ,   # e.g. 0.11400000005960464
                                                              __(name = 'GRAPHIC'             , score = __LESS_THAN__(0.05)),   # e.g. 0.019500000402331352
                                                              __(name = 'HARASSMENT_OR_ABUSE' , score = __LESS_THAN__(0.1)) ,   # e.g. 0.07940000295639038
                                                              __(name = 'SEXUAL'              , score = __LESS_THAN__(0.1)) ,   # e.g. 0.05260000005364418
                                                              __(name = 'VIOLENCE_OR_THREAT'  , score = __LESS_THAN__(0.1))],   # e.g. 0.04410000145435333
                                              duration = __SKIP__   ))  # e.g. 0.49


    def test__batch_detect_toxic_content__multiple_texts(self):                # Test batch toxicity with multiple texts
        texts = { "aaa1234567": "Clean text"   ,
                  "bbb1234567": "Rude text"    ,
                  "ccc1234567": "Normal text"  }

        results = self.batch_service.batch_detect_toxic_content(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = False                                  )

        assert type(results)    is Type_Safe__Dict
        assert len(results)     == 3
        assert all(hash_key     in results for hash_key in texts.keys())
        assert all(type(result) is Schema__Comprehend__Detect_Toxic_Content for result in results.values())

        assert results.obj()    == __(aaa1234567 = __(labels  = [__(name = 'PROFANITY'           , score = __LESS_THAN__(0.1)) ,    # e.g. 0.04780000075697899
                                                                 __(name = 'HATE_SPEECH'         , score = __LESS_THAN__(0.1)) ,    # e.g. 0.08839999884366989
                                                                 __(name = 'INSULT'              , score = __LESS_THAN__(0.15)),    # e.g. 0.1273999959230423
                                                                 __(name = 'GRAPHIC'             , score = __LESS_THAN__(0.05)),    # e.g. 0.019500000402331352
                                                                 __(name = 'HARASSMENT_OR_ABUSE' , score = __LESS_THAN__(0.1)) ,    # e.g. 0.07940000295639038
                                                                 __(name = 'SEXUAL'              , score = __LESS_THAN__(0.1)) ,    # e.g. 0.07029999792575836
                                                                 __(name = 'VIOLENCE_OR_THREAT'  , score = __LESS_THAN__(0.05))],   # e.g. 0.03970000147819519
                                                duration = __SKIP__                                                                ),  # e.g. 0.158

                                      bbb1234567 = __(labels  = [__(name = 'PROFANITY'           , score = __LESS_THAN__(0.1)) ,    # e.g. 0.08630000054836273
                                                                 __(name = 'HATE_SPEECH'         , score = __LESS_THAN__(0.1)) ,    # e.g. 0.07970000058412552
                                                                 __(name = 'INSULT'              , score = __LESS_THAN__(0.2)) ,    # e.g. 0.1785999983549118
                                                                 __(name = 'GRAPHIC'             , score = __LESS_THAN__(0.05)),    # e.g. 0.01860000006854534
                                                                 __(name = 'HARASSMENT_OR_ABUSE' , score = __LESS_THAN__(0.1)) ,    # e.g. 0.07450000196695328
                                                                 __(name = 'SEXUAL'              , score = __LESS_THAN__(0.1)) ,    # e.g. 0.0835999995470047
                                                                 __(name = 'VIOLENCE_OR_THREAT'  , score = __LESS_THAN__(0.05))],   # e.g. 0.027699999511241913
                                                duration = __SKIP__                                                                ),  # e.g. 0.061

                                      ccc1234567 = __(labels  = [__(name = 'PROFANITY'           , score = __LESS_THAN__(0.1)) ,    # e.g. 0.046799998730421066
                                                                 __(name = 'HATE_SPEECH'         , score = __LESS_THAN__(0.1)) ,    # e.g. 0.08839999884366989
                                                                 __(name = 'INSULT'              , score = __LESS_THAN__(0.15)),    # e.g. 0.12219999730587006
                                                                 __(name = 'GRAPHIC'             , score = __LESS_THAN__(0.05)),    # e.g. 0.019500000402331352
                                                                 __(name = 'HARASSMENT_OR_ABUSE' , score = __LESS_THAN__(0.1)) ,    # e.g. 0.07569999992847443
                                                                 __(name = 'SEXUAL'              , score = __LESS_THAN__(0.1)) ,    # e.g. 0.05260000005364418
                                                                 __(name = 'VIOLENCE_OR_THREAT'  , score = __LESS_THAN__(0.05))],   # e.g. 0.03970000147819519
                                                duration = __SKIP__                                                                ))  # e.g. 0.059


    def test__batch_detect_toxic_content__empty(self):                         # Test batch toxicity with empty dict
        texts = {}

        results = self.batch_service.batch_detect_toxic_content(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 0

    def test__batch_detect_toxic_content__with_cache(self):                    # Test batch toxicity with caching enabled
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test")}

        results = self.batch_service.batch_detect_toxic_content(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = True                                   )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 1

        assert results.obj() == __(abc1234567 = __(labels  = [__(name = 'PROFANITY'           , score = __LESS_THAN__(0.1 )) ,   # e.g. 0.09719999879598618
                                                              __(name = 'HATE_SPEECH'         , score = __LESS_THAN__(0.2 )) ,   # e.g. 0.10610000044107437
                                                              __(name = 'INSULT'              , score = __LESS_THAN__(0.2 )) ,   # e.g. 0.16179999709129333
                                                              __(name = 'GRAPHIC'             , score = __LESS_THAN__(0.1 )) ,   # e.g. 0.0551999993622303
                                                              __(name = 'HARASSMENT_OR_ABUSE' , score = __LESS_THAN__(0.2 )) ,   # e.g. 0.09000000357627869
                                                              __(name = 'SEXUAL'              , score = __LESS_THAN__(0.2 )) ,   # e.g. 0.13009999692440033
                                                              __(name = 'VIOLENCE_OR_THREAT'  , score = __LESS_THAN__(0.1 ))],   # e.g. 0.06669999659061432
                                           duration = __SKIP__                                                                ))  # e.g. 3.489

