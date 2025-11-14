from unittest                                                                            import TestCase
from fastapi                                                                             import FastAPI
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend__Cache          import Routes__Comprehend__Cache
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Cache_Info    import Schema__Comprehend__Cache_Info
from mgraph_ai_service_aws_comprehend.service.Comprehend__Cache__Service                 import Comprehend__Cache__Service


class test_Routes__Comprehend__Cache(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app    = FastAPI()
        cls.routes = Routes__Comprehend__Cache(app=cls.app).setup()

    def test__setUpClass(self):                                                # Test routes setup
        with self.routes as _:
            assert type(_)                  is Routes__Comprehend__Cache
            assert _.tag                    == 'comprehend-cache'
            assert type(_.cache_service)   is Comprehend__Cache__Service
            assert _.app                    == self.app
            assert _.routes_paths()         == [ '/clear',
                                                 '/info'  ]

    # ========================================
    # info Tests
    # ========================================

    def test__info__basic(self):                                               # Test cache info endpoint
        response = self.routes.info()

        assert type(response)           is Schema__Comprehend__Cache_Info
        assert response.namespace       == 'aws-comprehend'
        assert type(response.total_entries) is Safe_UInt                       # Placeholder returns 0
        assert type(response.size_bytes)    is Safe_UInt                       # Placeholder returns 0

    def test__info__returns_placeholder_values(self):                          # Test that info returns placeholder values
        response = self.routes.info()

        assert response.total_entries == 0                                     # Placeholder value
        assert response.size_bytes    == 0                                     # Placeholder value

    # ========================================
    # clear Tests
    # ========================================

    def test__clear__basic(self):                                              # Test cache clear endpoint
        response = self.routes.clear()

        assert type(response) is dict
        assert "success" in response
        assert "message" in response

    def test__clear__returns_success(self):                                    # Test that clear returns success
        response = self.routes.clear()

        assert response["success"] is True
        assert "placeholder" in response["message"].lower()                    # Indicates placeholder implementation
