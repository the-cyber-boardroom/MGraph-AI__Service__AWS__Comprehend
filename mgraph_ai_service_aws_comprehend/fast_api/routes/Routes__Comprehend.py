from fastapi                                                                                  import HTTPException
from osbot_fast_api.api.routes.Fast_API__Routes                                               import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                       import Safe_Str__Fast_API__Route__Tag
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Sentiment             import Schema__Comprehend__Detect_Sentiment
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Key_Phrases           import Schema__Comprehend__Detect_Key_Phrases
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Entities              import Schema__Comprehend__Detect_Entities
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Dominant_Language     import Schema__Comprehend__Detect_Dominant_Language
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Pii_Entities          import Schema__Comprehend__Detect_Pii_Entities
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Syntax                import Schema__Comprehend__Detect_Syntax
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content         import Schema__Comprehend__Detect_Toxic_Content
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Request             import Schema__Comprehend__Request
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                             import Comprehend__Service


TAG__ROUTES_COMPREHEND   = 'comprehend'
ROUTES_PATHS__COMPREHEND = [f'/{TAG__ROUTES_COMPREHEND}' + '/detect-sentiment'        ,  # Main AWS Comprehend endpoints
                            f'/{TAG__ROUTES_COMPREHEND}' + '/detect-key-phrases'       ,
                            f'/{TAG__ROUTES_COMPREHEND}' + '/detect-entities'          ,
                            f'/{TAG__ROUTES_COMPREHEND}' + '/detect-dominant-language' ,
                            f'/{TAG__ROUTES_COMPREHEND}' + '/detect-pii-entities'      ,
                            f'/{TAG__ROUTES_COMPREHEND}' + '/detect-syntax'            ,
                            f'/{TAG__ROUTES_COMPREHEND}' + '/detect-toxic-content'     ]


class Routes__Comprehend(Fast_API__Routes):                                    # Main FastAPI routes - direct AWS Comprehend API wrappers
    tag                 : Safe_Str__Fast_API__Route__Tag = TAG__ROUTES_COMPREHEND  # OpenAPI tag
    comprehend_service  : Comprehend__Service                                   # Main Comprehend service

    # ========================================
    # SENTIMENT DETECTION
    # ========================================

    def detect_sentiment(self,                                                  # Detect sentiment in text
                        request: Schema__Comprehend__Request                    # Comprehend request
                   ) -> Schema__Comprehend__Detect_Sentiment:                   # Sentiment detection result

        try:
            result = self.comprehend_service.detect_sentiment(text          = request.text         ,
                                                              language_code = request.language_code,
                                                              use_cache     = request.use_cache    )
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Sentiment detection failed: {str(e)}")

    # ========================================
    # KEY PHRASES DETECTION
    # ========================================

    def detect_key_phrases(self,                                                # Extract key phrases from text
                          request: Schema__Comprehend__Request                  # Comprehend request
                     ) -> Schema__Comprehend__Detect_Key_Phrases:               # Key phrases detection result

        try:
            result = self.comprehend_service.detect_key_phrases(text          = request.text         ,
                                                                language_code = request.language_code,
                                                                use_cache     = request.use_cache    )
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Key phrases detection failed: {str(e)}")

    # ========================================
    # ENTITY DETECTION
    # ========================================

    def detect_entities(self,                                                   # Detect named entities in text
                       request: Schema__Comprehend__Request                     # Comprehend request
                  ) -> Schema__Comprehend__Detect_Entities:                     # Entity detection result

        try:
            result = self.comprehend_service.detect_entities(text          = request.text         ,
                                                             language_code = request.language_code,
                                                             use_cache     = request.use_cache    )
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Entity detection failed: {str(e)}")

    # ========================================
    # DOMINANT LANGUAGE DETECTION
    # ========================================

    def detect_dominant_language(self,                                          # Detect dominant language in text
                                request: Schema__Comprehend__Request            # Comprehend request (language_code ignored)
                           ) -> Schema__Comprehend__Detect_Dominant_Language:   # Language detection result

        try:
            result = self.comprehend_service.detect_dominant_language(text      = request.text     ,
                                                                      use_cache = request.use_cache)
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Language detection failed: {str(e)}")

    # ========================================
    # PII ENTITY DETECTION
    # ========================================

    def detect_pii_entities(self,                                               # Detect PII entities in text
                           request: Schema__Comprehend__Request                 # Comprehend request
                      ) -> Schema__Comprehend__Detect_Pii_Entities:             # PII entity detection result

        try:
            result = self.comprehend_service.detect_pii_entities(text          = request.text         ,
                                                                 language_code = request.language_code,
                                                                 use_cache     = request.use_cache    )
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PII entity detection failed: {str(e)}")

    # ========================================
    # SYNTAX DETECTION
    # ========================================

    def detect_syntax(self,                                                     # Detect syntax/POS tags in text
                     request: Schema__Comprehend__Request                       # Comprehend request
                ) -> Schema__Comprehend__Detect_Syntax:                         # Syntax detection result

        try:
            result = self.comprehend_service.detect_syntax(text          = request.text         ,
                                                           language_code = request.language_code,
                                                           use_cache     = request.use_cache    )
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Syntax detection failed: {str(e)}")

    # ========================================
    # TOXIC CONTENT DETECTION
    # ========================================

    def detect_toxic_content(self,                                              # Detect toxic content in text
                            request: Schema__Comprehend__Request                # Comprehend request
                       ) -> Schema__Comprehend__Detect_Toxic_Content:           # Toxic content detection result

        try:
            result = self.comprehend_service.detect_toxic_content(text          = request.text         ,
                                                                  language_code = request.language_code,
                                                                  use_cache     = request.use_cache    )
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Toxic content detection failed: {str(e)}")

    # ========================================
    # ROUTE SETUP
    # ========================================

    def setup_routes(self):                                                     # Register all route handlers
        self.add_route_post(self.detect_sentiment        )                     # Sentiment endpoint
        self.add_route_post(self.detect_key_phrases      )                     # Key phrases endpoint
        self.add_route_post(self.detect_entities         )                     # Entities endpoint
        self.add_route_post(self.detect_dominant_language)                     # Language endpoint
        self.add_route_post(self.detect_pii_entities     )                     # PII entities endpoint
        self.add_route_post(self.detect_syntax           )                     # Syntax endpoint
        self.add_route_post(self.detect_toxic_content    )                     # Toxic content endpoint
