from unittest                                                                                import TestCase
from osbot_aws.aws.comprehend.Comprehend                                                     import Comprehend
from osbot_aws.aws.comprehend.schemas.batch.Schema__Comprehend__Batch_Item__Detect_Sentiment import Schema__Comprehend__Batch_Item__Detect_Sentiment
from osbot_utils.type_safe.primitives.core.Safe_UInt                                         import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash           import Safe_Str__Hash
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code                  import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                import Safe_Str__Comprehend__Text
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                        import Type_Safe__Dict
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                            import Comprehend__Service
from mgraph_ai_service_aws_comprehend.service.Comprehend__Batch__Service                     import Comprehend__Batch__Service


class test_Comprehend__Batch__Service__concurrent_requests(TestCase):            # Tests for concurrent batch processing implementation (Phase 2)

    @classmethod
    def setUpClass(cls):
        cls.comprehend          = Comprehend()
        cls.comprehend_detect   = cls.comprehend.detect()
        cls.comprehend_batch    = cls.comprehend.batch()
        cls.comprehend_service  = Comprehend__Service       (comprehend_detect  = cls.comprehend_detect )
        cls.batch_service       = Comprehend__Batch__Service(comprehend_service = cls.comprehend_service,
                                                             comprehend_batch   = cls.comprehend_batch  )

    def test__init__with_max_concurrent_batches(self):                                         # Test initialization with default max_concurrent_batches
        with self.batch_service as _:
            assert type(_)                       is Comprehend__Batch__Service
            assert type(_.max_concurrent_batches) is Safe_UInt
            assert _.max_concurrent_batches       == 5                                         # Default value

    def test__init__with_custom_max_workers(self):                                             # Test initialization with custom max_concurrent_batches
        custom_service = Comprehend__Batch__Service(comprehend_service      = self.comprehend_service,
                                                    comprehend_batch        = self.comprehend_batch  ,
                                                    max_concurrent_batches  = Safe_UInt(10)          )

        assert type(custom_service.max_concurrent_batches) is Safe_UInt
        assert custom_service.max_concurrent_batches       == 10

    # ========================================
    # Helper Method Tests: _chunk_texts
    # ========================================

    def test___chunk_texts__empty_dict(self):                                                  # Test chunking with empty input
        texts   = {}
        chunks  = self.batch_service._chunk_texts(texts, chunk_size=25)

        assert type(chunks) is list
        assert len(chunks)  == 0

    def test___chunk_texts__single_text(self):                                                 # Test chunking with single text
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Test text")}
        chunks = self.batch_service._chunk_texts(texts, chunk_size=25)

        assert type(chunks) is list
        assert len(chunks)  == 1
        assert len(chunks[0]) == 1
        assert Safe_Str__Hash("abc1234567") in chunks[0]

    def test___chunk_texts__exactly_25_texts(self):                                            # Test chunking with exactly 25 texts (AWS limit)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(25)}

        chunks = self.batch_service._chunk_texts(texts, chunk_size=25)

        assert len(chunks)    == 1                                                             # Single chunk
        assert len(chunks[0]) == 25                                                            # All texts in one chunk

    def test___chunk_texts__26_texts(self):                                                    # Test chunking with 26 texts (just over limit)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(26)}

        chunks = self.batch_service._chunk_texts(texts, chunk_size=25)

        assert len(chunks)    == 2                                                             # Two chunks
        assert len(chunks[0]) == 25                                                            # First chunk full
        assert len(chunks[1]) == 1                                                             # Second chunk with remainder

    def test___chunk_texts__50_texts(self):                                                    # Test chunking with 50 texts (2 full chunks)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(50)}

        chunks = self.batch_service._chunk_texts(texts, chunk_size=25)

        assert len(chunks)    == 2
        assert len(chunks[0]) == 25
        assert len(chunks[1]) == 25

    def test___chunk_texts__100_texts(self):                                                   # Test chunking with 100 texts (4 full chunks)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(100)}

        chunks = self.batch_service._chunk_texts(texts, chunk_size=25)

        assert len(chunks)    == 4
        assert all(len(chunk) == 25 for chunk in chunks)

    def test___chunk_texts__127_texts(self):                                                   # Test chunking with 127 texts (5 chunks + partial)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(127)}

        chunks = self.batch_service._chunk_texts(texts, chunk_size=25)
        assert len(texts    ) == 127
        assert len(chunks   ) == 6                                                             # 5 full + 1 partial
        assert len(chunks[0]) == 25                                                            # First chunk full
        assert len(chunks[4]) == 25                                                            # Fifth chunk full
        assert len(chunks[5]) == 2                                                             # Last chunk has remainder (127 % 25 = 2)

    def test___chunk_texts__custom_chunk_size(self):                                           # Test chunking with custom chunk size
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(15)}

        chunks = self.batch_service._chunk_texts(texts, chunk_size=10)

        assert len(chunks)    == 2
        assert len(chunks[0]) == 10
        assert len(chunks[1]) == 5

    # ========================================
    # Helper Method Tests: _process_sentiment_chunk
    # ========================================

    def test___process_sentiment_chunk__single_text(self):                                     # Test processing single text chunk
        chunk = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Happy text")}

        result = self.batch_service._process_sentiment_chunk(chunk         = chunk                                    ,
                                                             language_code = Enum__Comprehend__Language_Code.ENGLISH)

        assert type(result) is Type_Safe__Dict
        assert len(result)  == 1
        assert Safe_Str__Hash("abc1234567") in result
        assert type(result[Safe_Str__Hash("abc1234567")]) is Schema__Comprehend__Batch_Item__Detect_Sentiment

    def test___process_sentiment_chunk__multiple_texts(self):                                  # Test processing multiple text chunk
        chunk = {Safe_Str__Hash("aaa1234567"): Safe_Str__Comprehend__Text("Positive text") ,
                 Safe_Str__Hash("bbb1234567"): Safe_Str__Comprehend__Text("Negative text") ,
                 Safe_Str__Hash("ccc1234567"): Safe_Str__Comprehend__Text("Neutral text")  }

        result = self.batch_service._process_sentiment_chunk(chunk         = chunk                                    ,
                                                             language_code = Enum__Comprehend__Language_Code.ENGLISH)

        assert type(result) is Type_Safe__Dict
        assert len(result)  == 3
        assert all(hash_key in result for hash_key in chunk.keys())
        assert all(type(item) is Schema__Comprehend__Batch_Item__Detect_Sentiment for item in result.values())

    def test___process_sentiment_chunk__25_texts(self):                                        # Test processing full chunk (25 texts - AWS limit)
        chunk = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(25)}

        result = self.batch_service._process_sentiment_chunk(chunk         = chunk                                    ,
                                                             language_code = Enum__Comprehend__Language_Code.ENGLISH)

        assert type(result) is Type_Safe__Dict
        assert len(result)  == 25
        assert all(hash_key in result for hash_key in chunk.keys())

    def test___process_sentiment_chunk__empty_chunk(self):                                     # Test processing empty chunk
        chunk  = {}
        result = self.batch_service._process_sentiment_chunk(chunk         = chunk                                    ,
                                                             language_code = Enum__Comprehend__Language_Code.ENGLISH)

        assert type(result) is Type_Safe__Dict
        assert len(result)  == 0

    # ========================================
    # Concurrent batch_detect_sentiment Tests
    # ========================================

    def test__batch_detect_sentiment__empty_dict(self):                                        # Test with empty input (early return)
        texts   = {}
        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 0

    def test__batch_detect_sentiment__single_text__no_threading(self):                         # Test single text (single chunk - no threading overhead)
        texts = {Safe_Str__Hash("abc1234567"): Safe_Str__Comprehend__Text("Happy text")}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 1
        assert Safe_Str__Hash("abc1234567") in results

    def test__batch_detect_sentiment__25_texts__no_threading(self):                            # Test exactly 25 texts (single chunk - no threading)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(25)}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 25
        assert all(hash_key in results for hash_key in texts.keys())

    def test__batch_detect_sentiment__50_texts__concurrent(self):                              # Test 50 texts (2 chunks - concurrent execution)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text {i}")
                 for i in range(50)}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 50                                                             # All texts processed
        assert all(hash_key in results for hash_key in texts.keys())                          # All hashes present
        assert all(type(item) is Schema__Comprehend__Batch_Item__Detect_Sentiment             # All items correct type
                   for item in results.values())

    def test__batch_detect_sentiment__100_texts__concurrent(self):                             # Test 100 texts (4 chunks - concurrent execution)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Text number {i}")
                 for i in range(100)}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 100
        assert all(hash_key in results for hash_key in texts.keys())

    def test__batch_detect_sentiment__127_texts__concurrent(self):                             # Test 127 texts (6 chunks - mixed full and partial)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Comment {i}")
                 for i in range(127)}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 127
        assert all(hash_key in results for hash_key in texts.keys())

    def test__batch_detect_sentiment__200_texts__concurrent(self):                             # Test 200 texts (8 chunks - testing higher concurrency)
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"User comment {i}")
                 for i in range(200)}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 200
        assert all(hash_key in results for hash_key in texts.keys())

    def test__batch_detect_sentiment__mixed_sentiments__concurrent(self):                      # Test concurrent processing preserves sentiment accuracy
        texts = {}

        # Create 30 positive texts
        for i in range(30):
            texts[Safe_Str__Hash(f"a{i:09d}")] = Safe_Str__Comprehend__Text(f"I love this wonderful product - {i}")

        # Create 30 negative texts
        for i in range(30):
            texts[Safe_Str__Hash(f"b{i:09d}")] = Safe_Str__Comprehend__Text(f"This is terrible and awful - {i}")

        # Create 30 neutral texts
        for i in range(30):
            texts[Safe_Str__Hash(f"c{i:09d}")] = Safe_Str__Comprehend__Text(f"The sky is blue - {i}")


        results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                            language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                            use_cache     = False                                  )
        assert len(texts  ) == 90
        assert len(results) == 90

        # Check positive texts
        positive_results = {k: v for k, v in results.items() if k.startswith("a")}
        assert len(positive_results) == 30
        assert all(item.sentiment in ['Positive', 'Neutral'] for item in positive_results.values())

        # Check negative texts
        negative_results = {k: v for k, v in results.items() if k.startswith("b")}
        assert len(negative_results) == 30
        assert all(item.sentiment in ['Negative', 'Mixed'] for item in negative_results.values())

    def test__batch_detect_sentiment__with_spanish__concurrent(self):                          # Test concurrent processing with non-English language
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text("Hola mundo")
                 for i in range(50)}

        results = self.batch_service.batch_detect_sentiment(texts         = texts                                   ,
                                                            language_code = Enum__Comprehend__Language_Code.SPANISH,
                                                            use_cache     = False                                  )

        assert type(results) is Type_Safe__Dict
        assert len(results)  == 50

    # ========================================
    # Performance/Throttling Detection Tests
    # ========================================

    def test__batch_detect_sentiment__400_texts__stress_test(self):                            # Test 400 texts (16 chunks - near max expected load)
        # This test is designed to detect throttling issues
        # Watch for ThrottlingException or TooManyRequestsException
        size  = 400     # 1000 seems to work ok      # 1500 or 2000 start to hit ThrottlingException
        texts = {Safe_Str__Hash(f"{i:010d}"): Safe_Str__Comprehend__Text(f"Article comment {i}")
                 for i in range(size)}

        try:
            results = self.batch_service.batch_detect_sentiment(texts         = texts                                    ,
                                                                language_code = Enum__Comprehend__Language_Code.ENGLISH,
                                                                use_cache     = False                                  )

            assert type(results) is Type_Safe__Dict
            assert len(results)  == size
            assert all(hash_key in results for hash_key in texts.keys())

            # If we get here without throttling, log success
            #print(f"✓ Successfully processed {size} texts with max_workers={self.batch_service.max_concurrent_batches}")

        except Exception as e:
            # If we hit throttling, document it
            error_msg = str(e)
            if 'Throttling' in error_msg or 'TooManyRequests' in error_msg or '429' in error_msg:
                print(f"⚠ Hit throttling with {size} texts and max_workers={self.batch_service.max_concurrent_batches}")
                print(f"   Error: {error_msg}")
                # Re-raise to fail the test (so we can tune max_concurrent_batches)
                raise
            else:
                # Different error - re-raise
                raise