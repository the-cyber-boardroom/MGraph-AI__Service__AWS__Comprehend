import requests
from unittest                                                           import TestCase
from mgraph_ai_service_html.html__fast_api.Html_Service__Fast_API       import Html_Service__Fast_API
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config    import Serverless__Fast_API__Config
from osbot_utils.decorators.methods.cache_on_self                       import cache_on_self
from osbot_utils.helpers.duration.decorators.print_duration             import print_duration
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from starlette.testclient                                               import TestClient

# needs: pip install mgraph_ai_service_html

class Integration_Helper__Html_Service(Type_Safe):

    @cache_on_self
    def client__html_service(self):
        config       = Serverless__Fast_API__Config(enable_api_key=False)        # note: see if we need to add a singleton here, since this runs in 0.08 seconds :)
        html_service = Html_Service__Fast_API(config=config).setup()
        return html_service.client()

    def html_to_hashes(self, html):
        response = self.client__html_service().post('/html/to/text/hashes', json=dict(html=html))
        return response.json().get('hash_mapping')

    def url_to_hashes(self, url):
        response = requests.get(url)
        html     = response.text
        return self.html_to_hashes(html)

    def hashes__html_simple(self):
        return self.html_to_hashes(SAMPLE__HTML__SIMPLE)

class test_Integration_Helper__Html_Service(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.integration_helper__html_service = Integration_Helper__Html_Service()

    def test_client__html_service(self):
        with self.integration_helper__html_service.client__html_service()  as _:
            assert type(_) is TestClient
            assert _.get('/docs').status_code == 200
            assert _.post('/html/to/tree/view', json = dict(html=SAMPLE__HTML__SIMPLE)).text == 'html\n    └── body\n        └── TEXT: Hello World'

    def test_html_to_hashes(self):
        with self.integration_helper__html_service as _:

            assert _.html_to_hashes(SAMPLE__HTML__SIMPLE   ) == {'b10a8db164': 'Hello World'}
            assert _.html_to_hashes(SAMPLE__HTML__PARAGRAPH) == {'f8485ab0cd': 'This is a test paragraph.'}
            assert _.html_to_hashes(SAMPLE__HTML__COMPLEX  ) == {'030c5b6d1e': 'italic',
                                                                 '094cf2ae96': 'Test Page',
                                                                 '1267f9f89a': 'Third item',
                                                                 '14c3c2854c': 'Some nested content',
                                                                 '2d99d326cd': ' text.',
                                                                 '4e864ad0c1': 'Second item',
                                                                 '658bbd823c': 'This is a ',
                                                                 '69dcab4a73': 'bold',
                                                                 '78aa26e3ec': ' statement with ',
                                                                 '936ccdb971': 'Click here',
                                                                 '9f6c1a3ffc': 'Welcome to MGraph',
                                                                 'f1ef59ee34': 'First item'}

            assert _.html_to_hashes(SAMPLE__HTML__ARTICLE  ) == { '02e2c97c77': 'Privacy-preserving transformations',
                                                                  '0b3fbc0b52': 'Key Benefits',
                                                                  '0b79795d3e': 'Introduction',
                                                                  '2bc16ecc1d': 'A comprehensive guide to text transformation',
                                                                  '35b7bfadde': 'It allows us to transform and ',
                                                                  '3844cc6967': ' in meaningful ways.',
                                                                  '50c6c2f41b': 'Understanding Semantic Text Analysis',
                                                                  '60f1913af6': 'Copyright 2025 MGraph AI',
                                                                  '7364a26cf2': 'Scalable processing',
                                                                  'bb5b3b6bc8': 'Semantic text analysis is a powerful tool for understanding '
                                                                                'content.',
                                                                  'c89d6c27b1': 'analyze text',
                                                                  'db357b6e52': 'Structure-aware analysis'}

    def test_url_to_hashes(self):
        with self.integration_helper__html_service as _:
            with print_duration():
                assert _.url_to_hashes("https://www.google.co.uk/404") == {'140e11e173': 'Error 404 (Not Found)!!1',
                                                                           '37d6303d23': ' was not found on this server.  ',
                                                                           '820afc1600': 'That’s an error.',
                                                                           'ae915fae68': '404.',
                                                                           'bdc592a6bc': 'The requested URL ',
                                                                           'c02548476b': '/404',
                                                                           'c82c79685a': 'That’s all we know.'}
            with print_duration():
                assert _.url_to_hashes("https://www.google.co.uk"    ) == {'13348442cc': 'Search',
                                                                           '1834a46420': ' »',
                                                                           '2ce5fc2898': 'Advertising',
                                                                           '384470d10f': 'Web History',
                                                                           '6f1bf85c9e': 'Terms',
                                                                           '7cb8ad4656': 'Advanced search',
                                                                           '7d53cbd3f0': 'Gmail',
                                                                           '8b36e9207c': 'Google',
                                                                           '8dd1bae8da': 'YouTube',
                                                                           'a33ca90318': 'About Google',
                                                                           'a43b6a8b7d': 'Google.co.uk',
                                                                           'acb46671b0': '© 2025 - ',
                                                                           'af51fdf94a': 'Maps',
                                                                           'b6d4223e60': 'Sign in',
                                                                           'c02f226ecf': ' | ',
                                                                           'c5f29bb36f': 'Privacy',
                                                                           'd3da97e2d9': 'More',
                                                                           'dd1ba1872d': 'News',
                                                                           'de3c731be5': 'Play',
                                                                           'e476a22329': 'Business Solutions',
                                                                           'f2c6151d6c': 'Drive',
                                                                           'f4f70727dc': 'Settings',
                                                                           'f574aa2039': ' - ',
                                                                           'fff0d600f8': 'Images'}

        with print_duration():
            assert len(_.url_to_hashes("https://docs.diniscruz.ai"           )) == 148

        with print_duration():
            assert len(_.url_to_hashes("https://docs.diniscruz.ai/about.html")) == 130

        with print_duration():
            assert len(_.url_to_hashes("https://www.bbc.co.uk"               )) == 354
        with print_duration():
            assert len(_.url_to_hashes("https://text.npr.org/"               )) == 33


SAMPLE__HTML__SIMPLE    = "<html><body>Hello World</body></html>"
SAMPLE__HTML__PARAGRAPH = "<html><body><p>This is a test paragraph.</p></body></html>"
SAMPLE__HTML__COMPLEX   = """
                             <html>
                                 <head><title>Test Page</title></head>
                                 <body>
                                     <h1>Welcome to MGraph</h1>
                                     <p>This is a <b>bold</b> statement with <i>italic</i> text.</p>
                                     <ul>
                                         <li>First item</li>
                                         <li>Second item</li>
                                         <li>Third item</li>
                                     </ul>
                                     <div>
                                         <span>Some nested content</span>
                                         <a href="#">Click here</a>
                                     </div>
                                 </body>
                             </html>
                        """
SAMPLE__HTML__ARTICLE = """
                            <article>
                                <header>
                                    <h1>Understanding Semantic Text Analysis</h1>
                                    <p class="subtitle">A comprehensive guide to text transformation</p>
                                </header>
                                <section>
                                    <h2>Introduction</h2>
                                    <p>Semantic text analysis is a powerful tool for understanding content.</p>
                                    <p>It allows us to transform and <b>analyze text<b> in meaningful ways.</p>
                                </section>
                                <section>
                                    <h2>Key Benefits</h2>
                                    <ul>
                                        <li>Privacy-preserving transformations</li>
                                        <li>Structure-aware analysis</li>
                                        <li>Scalable processing</li>
                                    </ul>
                                </section>
                                <footer>
                                    <p>Copyright 2025 MGraph AI</p>
                                </footer>
                            </article>
                        """