import requests
from unittest                                                                           import TestCase
from fastapi                                                                            import FastAPI
from osbot_utils.helpers.duration.decorators.print_duration                             import print_duration
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend__Batch         import Routes__Comprehend__Batch
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Batch_Request import Schema__Comprehend__Batch_Request
from tests.integration.Integration_Helper__Html_Service                                 import Integration_Helper__Html_Service, SAMPLE__HTML__SIMPLE, SAMPLE__HTML__PARAGRAPH, SAMPLE__HTML__COMPLEX, SAMPLE__HTML__ARTICLE

class test__int__Routes__Comprehend__Batch(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client__html_service = Integration_Helper__Html_Service()
        cls.routes__comprehend_batch    = Routes__Comprehend__Batch(app=FastAPI()).setup()

    def helper__detect_sentiment(self, html):
        texts               = self.client__html_service.html_to_hashes(html)
        request             = Schema__Comprehend__Batch_Request(texts=texts)
        sentiment           = self.routes__comprehend_batch.detect_sentiment(request)
        return sentiment

    def helper__detect_sentiment__from_url(self, url):
        with print_duration(action_name="get html"):
            response = requests.get(url)
            html     = response.text
        with print_duration(action_name="get sentiment"):
            return self.helper__detect_sentiment(html)


    def test__000__warm_up(self):
        self.helper__detect_sentiment(SAMPLE__HTML__SIMPLE)

    def test__process__hashes__html_simple(self):
        sentiment = self.helper__detect_sentiment(SAMPLE__HTML__SIMPLE)
        assert len(sentiment)                    == 1
        assert sentiment['b10a8db164'].sentiment == 'Positive'

    def test__process__hashes__html_paragraph(self):
        sentiment = self.helper__detect_sentiment(SAMPLE__HTML__PARAGRAPH)
        assert len(sentiment)                    == 1
        assert sentiment['f8485ab0cd'].sentiment == 'Neutral'

    def test__process__hashes__html_complex(self):
        sentiment = self.helper__detect_sentiment(SAMPLE__HTML__COMPLEX)
        assert len(sentiment)                    == 12
        assert sentiment['030c5b6d1e'].sentiment == 'Neutral'
        assert sentiment['14c3c2854c'].sentiment == 'Negative'

    def test__process__hashes__html_article(self):
        sentiment = self.helper__detect_sentiment(SAMPLE__HTML__ARTICLE)
        assert len(sentiment)                    == 12
        sentiment.print()
        assert sentiment['02e2c97c77'].sentiment == 'Neutral'
        assert sentiment['2bc16ecc1d'].sentiment == 'Positive'

    def test__process__hashes__google_com(self):
        sentiment = self.helper__detect_sentiment__from_url("https://www.google.com")
        assert len(sentiment)                    == 24
        sentiment.print()
        assert sentiment['13348442cc'].sentiment == 'Neutral'
        assert sentiment['1834a46420'].sentiment == 'Neutral'

    # this needs splitting
    # def test__process__hashes__docs_diniscruz_ai(self):
    #     sentiment = self.helper__detect_sentiment__from_url("https://docs.diniscruz.ai")
    #     assert len(sentiment)                    == 24
    #     sentiment.print()
    #     assert sentiment['13348442cc'].sentiment == 'Neutral'
    #     assert sentiment['1834a46420'].sentiment == 'Neutral'



