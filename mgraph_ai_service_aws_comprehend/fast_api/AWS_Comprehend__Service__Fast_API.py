from osbot_fast_api.api.routes.Routes__Set_Cookie                                       import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API                            import Serverless__Fast_API
from osbot_fast_api_serverless.fast_api.routes.Routes__Info                             import Routes__Info
from mgraph_ai_service_aws_comprehend.config                                            import FAST_API__TITLE
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend                import Routes__Comprehend
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend__Helpers       import Routes__Comprehend__Helpers
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend__Batch         import Routes__Comprehend__Batch
from mgraph_ai_service_aws_comprehend.fast_api.routes.Routes__Comprehend__Cache         import Routes__Comprehend__Cache
from mgraph_ai_service_aws_comprehend.utils.Version                                     import version__mgraph_ai_service_aws_comprehend


class AWS_Comprehend__Service__Fast_API(Serverless__Fast_API):
    enable_api_key = False                                                      # todo: update to new version of Serverless__Fast_API and use the new config object

    def fast_api__title(self):                                                  # todo: move this to the Fast_API class
        return FAST_API__TITLE

    def setup(self):
        super().setup()
        self.setup_fast_api_title_and_version()
        return self

    def setup_fast_api_title_and_version(self):                                # todo: move this to the Fast_API class
        app       = self.app()
        app.title = self.fast_api__title()
        app.version = version__mgraph_ai_service_aws_comprehend
        return self

    def setup_routes(self):
        self.add_routes(Routes__Info                )                          # Info routes
        self.add_routes(Routes__Comprehend          )                          # Main Comprehend routes
        self.add_routes(Routes__Comprehend__Helpers )                          # Helper routes
        self.add_routes(Routes__Comprehend__Batch   )                          # Batch routes
        self.add_routes(Routes__Comprehend__Cache   )                          # Cache routes
        self.add_routes(Routes__Set_Cookie          )                          # Set cookie routes
