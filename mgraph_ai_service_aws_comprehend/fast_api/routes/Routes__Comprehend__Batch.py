from typing                                                                                         import Dict
from fastapi                                                                                        import HTTPException
from osbot_utils.helpers.duration.decorators.capture_duration                                       import capture_duration
from osbot_utils.type_safe.primitives.core.Safe_Float                                               import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                  import Safe_Str__Hash
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                        import Safe_Str__Text
from osbot_fast_api.api.routes.Fast_API__Routes                                                     import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                             import Safe_Str__Fast_API__Route__Tag
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Sentiment                   import Schema__Comprehend__Detect_Sentiment
from osbot_aws.aws.comprehend.schemas.detect.Schema__Comprehend__Detect_Toxic_Content               import Schema__Comprehend__Detect_Toxic_Content
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Batch_Request             import Schema__Comprehend__Batch_Request
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Batch_Threshold_Request   import Schema__Comprehend__Batch_Threshold_Request
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Batch_Boolean_Response   import Schema__Comprehend__Batch_Boolean_Response
from mgraph_ai_service_aws_comprehend.service.Comprehend__Batch__Service                            import Comprehend__Batch__Service


TAG__ROUTES_COMPREHEND_BATCH   = 'comprehend-batch'
ROUTES_PATHS__COMPREHEND_BATCH = [f'/{TAG__ROUTES_COMPREHEND_BATCH}' + '/detect-sentiment'  ,  # Batch endpoints
                                  f'/{TAG__ROUTES_COMPREHEND_BATCH}' + '/detect-toxic'      ,
                                  f'/{TAG__ROUTES_COMPREHEND_BATCH}' + '/is-positive'       ,
                                  f'/{TAG__ROUTES_COMPREHEND_BATCH}' + '/is-negative'       ,
                                  f'/{TAG__ROUTES_COMPREHEND_BATCH}' + '/is-toxic'          ]


class Routes__Comprehend__Batch(Fast_API__Routes):                                  # Batch routes - process multiple texts at once
    tag           : Safe_Str__Fast_API__Route__Tag = TAG__ROUTES_COMPREHEND_BATCH   # OpenAPI tag
    batch_service : Comprehend__Batch__Service                                      # Batch processing service

    # ========================================
    # BATCH DETECTION
    # ========================================

    def detect_sentiment(self,                                                       # Batch sentiment detection
                        request: Schema__Comprehend__Batch_Request                   # Batch request
                   ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Detect_Sentiment]:  # Hash → sentiment mapping

        try:
            results = self.batch_service.batch_detect_sentiment(texts         = request.texts        ,
                                                                language_code = request.language_code,
                                                                use_cache     = request.use_cache    )
            return results

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch sentiment detection failed: {str(e)}")

    def detect_toxic(self,                                                           # Batch toxicity detection
                    request: Schema__Comprehend__Batch_Request                       # Batch request
               ) -> Dict[Safe_Str__Hash, Schema__Comprehend__Detect_Toxic_Content]:  # Hash → toxicity mapping

        try:
            results = self.batch_service.batch_detect_toxic_content(texts         = request.texts        ,
                                                                    language_code = request.language_code,
                                                                    use_cache     = request.use_cache    )
            return results

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch toxic detection failed: {str(e)}")

    # ========================================
    # BATCH BOOLEAN HELPERS
    # ========================================

    def is_positive(self,                                                       # Batch check if texts are positive
                   request: Schema__Comprehend__Batch_Threshold_Request         # Batch threshold request
              ) -> Schema__Comprehend__Batch_Boolean_Response:                  # Batch boolean response

        try:
            with capture_duration() as duration:
                sentiment_results = self.batch_service.batch_detect_sentiment(texts         = request.texts        ,
                                                                              language_code = request.language_code,
                                                                              use_cache     = request.use_cache    )

                results = {}
                scores  = {}

                for hash_key, sentiment_result in sentiment_results.items():
                    positive_score        = sentiment_result.score.positive
                    results[hash_key]     = float(positive_score) > float(request.threshold)
                    scores[hash_key]      = Safe_Float(positive_score)

            return Schema__Comprehend__Batch_Boolean_Response(results   = results                        ,
                                                              scores    = scores                         ,
                                                              threshold = request.threshold              ,
                                                              operation = Safe_Str__Text('is_positive')  ,
                                                              total     = Safe_UInt(len(request.texts))  ,
                                                              cached    = Safe_UInt(0)                   ,  # TODO: Track cache hits
                                                              duration  = Safe_Float(duration.seconds)   )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch is_positive check failed: {str(e)}")

    def is_negative(self,                                                       # Batch check if texts are negative
                   request: Schema__Comprehend__Batch_Threshold_Request         # Batch threshold request
              ) -> Schema__Comprehend__Batch_Boolean_Response:                  # Batch boolean response

        try:
            with capture_duration() as duration:
                sentiment_results = self.batch_service.batch_detect_sentiment(texts         = request.texts        ,
                                                                              language_code = request.language_code,
                                                                              use_cache     = request.use_cache    )

                results = {}
                scores  = {}

                for hash_key, sentiment_result in sentiment_results.items():
                    negative_score        = sentiment_result.score.negative
                    results[hash_key]     = float(negative_score) > float(request.threshold)
                    scores[hash_key]      = Safe_Float(negative_score)

            return Schema__Comprehend__Batch_Boolean_Response(results   = results                        ,
                                                              scores    = scores                         ,
                                                              threshold = request.threshold              ,
                                                              operation = Safe_Str__Text('is_negative')  ,
                                                              total     = Safe_UInt(len(request.texts))  ,
                                                              cached    = Safe_UInt(0)                   ,
                                                              duration  = Safe_Float(duration.seconds)   )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch is_negative check failed: {str(e)}")

    def is_toxic(self,                                                          # Batch check if texts are toxic
                request: Schema__Comprehend__Batch_Threshold_Request            # Batch threshold request
           ) -> Schema__Comprehend__Batch_Boolean_Response:                     # Batch boolean response

        try:
            with capture_duration() as duration:
                toxic_results = self.batch_service.batch_detect_toxic_content(texts         = request.texts        ,
                                                                             language_code = request.language_code,
                                                                             use_cache     = request.use_cache    )

                results = {}
                scores  = {}

                for hash_key, toxic_result in toxic_results.items():
                    # Get max toxicity score
                    max_score = 0.0
                    if toxic_result.labels:
                        label_scores = [float(label.score) for label in toxic_result.labels]
                        max_score    = max(label_scores) if label_scores else 0.0

                    results[hash_key] = max_score > float(request.threshold)
                    scores[hash_key]  = Safe_Float(max_score)

            return Schema__Comprehend__Batch_Boolean_Response(results   = results                      ,
                                                              scores    = scores                       ,
                                                              threshold = request.threshold            ,
                                                              operation = Safe_Str__Text('is_toxic')   ,
                                                              total     = Safe_UInt(len(request.texts)),
                                                              cached    = Safe_UInt(0)                 ,
                                                              duration  = Safe_Float(duration.seconds) )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch is_toxic check failed: {str(e)}")

    # ========================================
    # ROUTE SETUP
    # ========================================

    def setup_routes(self):                                                     # Register all route handlers
        self.add_route_post(self.detect_sentiment)                             # Batch sentiment endpoint
        self.add_route_post(self.detect_toxic    )                             # Batch toxicity endpoint
        self.add_route_post(self.is_positive     )                             # Batch is_positive endpoint
        self.add_route_post(self.is_negative     )                             # Batch is_negative endpoint
        self.add_route_post(self.is_toxic        )                             # Batch is_toxic endpoint
