import pytest
import requests
from unittest                           import TestCase
from osbot_utils.testing.__             import __, __LESS_THAN__, __GREATER_THAN__
from osbot_utils.testing.__helpers      import obj
from osbot_utils.utils.Env              import get_env, load_dotenv
from osbot_utils.utils.Http             import url_join_safe

from tests.integration.Integration_Helper__Html_Service import SAMPLE__HTML__SIMPLE, SAMPLE__HTML__ARTICLE

ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL  = "AUTH__SERVICE__AWS__COMPREHEND__BASE_URL"
ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME  = "AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME"
ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE = "AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE"

ENV_NAME__AUTH__SERVICE__HTML__BASE_URL             = "AUTH__SERVICE__HTML__BASE_URL"
ENV_NAME__AUTH__SERVICE__HTML__KEY_NAME             = "AUTH__SERVICE__HTML__KEY_NAME"
ENV_NAME__AUTH__SERVICE__HTML__KEY_VALUE            = "AUTH__SERVICE__HTML__KEY_VALUE"

class test_qa_routes__Comprehend__Batch(TestCase):

    @classmethod
    def setup_class(cls):
        load_dotenv()

    def helper__make_request(self, url, json=None, method="GET", headers=None):
        response = requests.request(method=method, url=url, headers=headers, json=json)
        return response.json()

    def helper__html_service__request(self, path, json=None, method="GET"):
        server    = get_env(ENV_NAME__AUTH__SERVICE__HTML__BASE_URL)
        key_name  = get_env(ENV_NAME__AUTH__SERVICE__HTML__KEY_NAME)
        key_value = get_env(ENV_NAME__AUTH__SERVICE__HTML__KEY_VALUE)
        headers   = { key_name: key_value }
        url       = url_join_safe(server, path)
        return self.helper__make_request(url=url, json=json, method=method, headers=headers)

    def helper__html_service__html_to_hashes(self, html):
        path = "/html/to/text/hashes"
        response = self.helper__html_service__request(path=path, json=dict(html=html), method="POST")
        return response.get('hash_mapping')


    def helper__aws_comprehend__request(self, path, json=None, method="GET"):
        server    = get_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL)
        key_name  = get_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME)
        key_value = get_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE)
        headers   = { key_name: key_value }
        url       = url_join_safe(server, path)
        return self.helper__make_request(url=url, json=json, method=method, headers=headers)

    def helper__aws_comprehend__detect_sentiment(self, texts):
        path = "/comprehend-batch/detect-sentiment"
        return self.helper__aws_comprehend__request(path=path, json=dict(texts=texts), method="POST")

    def helper__detect_sentiment(self, html):
        texts      = self.helper__html_service__html_to_hashes(html)
        sentiment  = self.helper__aws_comprehend__detect_sentiment(texts)
        return sentiment

    def helper__detect_sentiment__from_url(self, url):
        html = requests.get(url).text
        return self.helper__detect_sentiment(html)

    # TESTS

    def test_helper__html_service__request(self):
        assert self.helper__html_service__request('/info/version') == {'version': 'v1.24.0'}

    def test_helper__aws_comprehend__request(self):
        assert self.helper__aws_comprehend__request('/info/health') == {'status': 'ok'}

    def test_helper__html_service__html_to_hashes(self):
        assert self.helper__html_service__html_to_hashes(SAMPLE__HTML__SIMPLE) == {'b10a8db164': 'Hello World'}

    def test_helper__aws_comprehend__detect_sentiment(self):
        texts    = {"0123456789": "it's 42"}
        response = self.helper__aws_comprehend__detect_sentiment(texts)
        assert response['0123456789'].get('sentiment') == "Neutral"

    def test__detect_sentiment__html_simple(self):
        response = self.helper__detect_sentiment(SAMPLE__HTML__SIMPLE)
        assert obj(response) == __(b10a8db164 = __(index     = 0                                                                                  ,
                                          sentiment = 'Positive'                                                                         ,
                                          score     = __(mixed    = __LESS_THAN__   (0.01) ,    # e.g. 0.0010159355588257313
                                                         negative = __LESS_THAN__   (0.01) ,    # e.g. 0.0015335445059463382
                                                         neutral  = __LESS_THAN__   (0.5 ) ,    # e.g. 0.42408183217048645
                                                         positive = __GREATER_THAN__(0.5 ))))   # e.g. 0.5733687281608582
    def test__detect_sentiment__html_article(self):
        assert len(self.helper__detect_sentiment(SAMPLE__HTML__ARTICLE)) == 12

    def test__detect_sentiment__www_google_co_uk(self):
        assert len(self.helper__detect_sentiment__from_url("https://www.google.co.uk")) == 24

    def test__detect_sentiment__docs_diniscruz_ai(self):
        for i in range(1):                  # change range to experiment (values above 20 will trigger ThrottlingException
            #with print_duration():
                assert len(self.helper__detect_sentiment__from_url("https://docs.diniscruz.ai")) == 148

    def test__detect_sentiment__news_bbc_co_uk(self):
        for i in range(1):
            assert len(self.helper__detect_sentiment__from_url("https://news.bbc.co.uk")) > 320


    def test__detect_sentiment__docs_diniscruz_ai__using__thread_pool(self):
        pytest.skip("trigger manually")
        from concurrent.futures import ThreadPoolExecutor, as_completed

        NUM_CALLS = 40
        MAX_CONCURRENCY = 3     # 10 will trigger ThrottlingException, 3 seems to be a good balance

        def task():
            #with print_duration():
                result = self.helper__detect_sentiment__from_url("https://docs.diniscruz.ai")
                if len(result) != 148:
                    print(f"ERROR: {result}")
                # else:
                #     print(f"SUCCESS: {result}")
                #assert len(result) == 148

        with ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as executor:
            futures = [executor.submit(task) for _ in range(NUM_CALLS)]
            for f in as_completed(futures):
                f.result()   # propagate assertion errors



