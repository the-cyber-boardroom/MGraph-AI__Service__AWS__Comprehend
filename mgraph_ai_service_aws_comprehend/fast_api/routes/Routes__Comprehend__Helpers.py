from fastapi                                                                                        import HTTPException
from osbot_aws.aws.comprehend.Comprehend                                                            import Comprehend
from osbot_utils.decorators.methods.cache_on_self                                                   import cache_on_self
from osbot_utils.helpers.duration.decorators.capture_duration                                       import capture_duration
from osbot_utils.type_safe.primitives.core.Safe_Float                                               import Safe_Float
from osbot_fast_api.api.routes.Fast_API__Routes                                                     import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                             import Safe_Str__Fast_API__Route__Tag
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Probability_Score    import Safe_Float__Probability_Score
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                        import Safe_Str__Text
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Threshold_Request         import Schema__Comprehend__Threshold_Request
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Request                   import Schema__Comprehend__Request
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Boolean_Response         import Schema__Comprehend__Boolean_Response
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Sentiment_Score_Response import Schema__Comprehend__Sentiment_Score_Response
from mgraph_ai_service_aws_comprehend.schemas.response.Schema__Comprehend__Toxicity_Score_Response  import Schema__Comprehend__Toxicity_Score_Response
from mgraph_ai_service_aws_comprehend.service.Comprehend__Service                                   import Comprehend__Service


TAG__ROUTES_COMPREHEND_HELPERS   = 'comprehend-helpers'
ROUTES_PATHS__COMPREHEND_HELPERS = [f'/{TAG__ROUTES_COMPREHEND_HELPERS}' + '/is-positive'      ,  # Helper endpoints
                                    f'/{TAG__ROUTES_COMPREHEND_HELPERS}' + '/is-negative'      ,
                                    f'/{TAG__ROUTES_COMPREHEND_HELPERS}' + '/is-neutral'       ,
                                    f'/{TAG__ROUTES_COMPREHEND_HELPERS}' + '/is-toxic'         ,
                                    f'/{TAG__ROUTES_COMPREHEND_HELPERS}' + '/sentiment-score'  ,
                                    f'/{TAG__ROUTES_COMPREHEND_HELPERS}' + '/toxicity-score'   ]


class Routes__Comprehend__Helpers(Fast_API__Routes):                           # Helper routes - simplified boolean/threshold-based endpoints
    tag        : Safe_Str__Fast_API__Route__Tag = TAG__ROUTES_COMPREHEND_HELPERS  # OpenAPI tag
    comprehend : Comprehend     
    
    
    @cache_on_self
    def comprehend_service(self) -> Comprehend__Service:
        comprehend_detect  = self.comprehend.detect()
        comprehend_service = Comprehend__Service(comprehend_detect=comprehend_detect)
        return comprehend_service

    # ========================================
    # SENTIMENT HELPERS
    # ========================================

    def is_positive(self,                                                       # Check if text is positive (score > threshold)
                   request: Schema__Comprehend__Threshold_Request               # Threshold request
              ) -> Schema__Comprehend__Boolean_Response:                        # Boolean response

        try:
            with capture_duration() as duration:
                sentiment_result = self.comprehend_service().detect_sentiment(text          = request.text         ,
                                                                             language_code = request.language_code,
                                                                             use_cache     = request.use_cache    )

                positive_score = sentiment_result.score.positive
                result         = float(positive_score) > float(request.threshold)

            return Schema__Comprehend__Boolean_Response(result    = result                         ,
                                                        score     = Safe_Float(positive_score)     ,
                                                        threshold = request.threshold              ,
                                                        operation = Safe_Str__Text('is_positive')  ,
                                                        cached    = False                          ,  # TODO: Track if from cache
                                                        duration  = Safe_Float(duration.seconds)   )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"is_positive check failed: {str(e)}")

    def is_negative(self,                                                       # Check if text is negative (score > threshold)
                   request: Schema__Comprehend__Threshold_Request               # Threshold request
              ) -> Schema__Comprehend__Boolean_Response:                        # Boolean response

        try:
            with capture_duration() as duration:
                sentiment_result = self.comprehend_service().detect_sentiment(text          = request.text         ,
                                                                              language_code = request.language_code,
                                                                              use_cache     = request.use_cache    )

                negative_score = sentiment_result.score.negative
                result         = float(negative_score) > float(request.threshold)

            return Schema__Comprehend__Boolean_Response(result    = result                         ,
                                                        score     = Safe_Float(negative_score)     ,
                                                        threshold = request.threshold              ,
                                                        operation = Safe_Str__Text('is_negative')  ,
                                                        cached    = False                          ,
                                                        duration  = Safe_Float(duration.seconds)   )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"is_negative check failed: {str(e)}")

    def is_neutral(self,                                                        # Check if text is neutral (score > threshold)
                  request: Schema__Comprehend__Threshold_Request                # Threshold request
             ) -> Schema__Comprehend__Boolean_Response:                         # Boolean response

        try:
            with capture_duration() as duration:
                sentiment_result = self.comprehend_service().detect_sentiment(text          = request.text         ,
                                                                             language_code = request.language_code,
                                                                             use_cache     = request.use_cache    )

                neutral_score = sentiment_result.score.neutral
                result        = float(neutral_score) > float(request.threshold)

            return Schema__Comprehend__Boolean_Response(result    = result                        ,
                                                        score     = Safe_Float(neutral_score)     ,
                                                        threshold = request.threshold             ,
                                                        operation = Safe_Str__Text('is_neutral')  ,
                                                        cached    = False                         ,
                                                        duration  = Safe_Float(duration.seconds)  )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"is_neutral check failed: {str(e)}")

    # ========================================
    # TOXICITY HELPERS
    # ========================================

    def is_toxic(self,                                                          # Check if text is toxic (any score > threshold)
                request: Schema__Comprehend__Threshold_Request                  # Threshold request
           ) -> Schema__Comprehend__Boolean_Response:                           # Boolean response

        try:
            with capture_duration() as duration:
                toxic_result = self.comprehend_service().detect_toxic_content(text          = request.text         ,
                                                                             language_code = request.language_code,
                                                                             use_cache     = request.use_cache    )

                # Check if any toxicity label exceeds threshold
                max_score = Safe_Float(0.0)
                if toxic_result.labels:
                    scores    = [float(label.score) for label in toxic_result.labels]
                    max_score = Safe_Float(max(scores)) if scores else Safe_Float(0.0)

                result = float(max_score) > float(request.threshold)

            return Schema__Comprehend__Boolean_Response(result    = result                      ,
                                                        score     = max_score                   ,
                                                        threshold = request.threshold           ,
                                                        operation = Safe_Str__Text('is_toxic')  ,
                                                        cached    = False                       ,
                                                        duration  = Safe_Float(duration.seconds))

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"is_toxic check failed: {str(e)}")

    # ========================================
    # SCORE HELPERS
    # ========================================

    def sentiment_score(self,                                                   # Get just sentiment scores without full response
                       request: Schema__Comprehend__Request                     # Comprehend request
                  ) -> Schema__Comprehend__Sentiment_Score_Response:            # Simplified sentiment scores

        try:
            with capture_duration() as duration:
                sentiment_result = self.comprehend_service().detect_sentiment(text          = request.text         ,
                                                                             language_code = request.language_code,
                                                                             use_cache     = request.use_cache    )

            return Schema__Comprehend__Sentiment_Score_Response(
                positive = sentiment_result.score.positive,
                negative = sentiment_result.score.negative,
                neutral  = sentiment_result.score.neutral ,
                mixed    = sentiment_result.score.mixed   ,
                cached   = False                          ,  # TODO: Track if from cache
                duration = Safe_Float(duration.seconds)
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"sentiment_score failed: {str(e)}")

    def toxicity_score(self,                                                    # Get just toxicity scores without full response
                      request: Schema__Comprehend__Request                      # Comprehend request
                 ) -> Schema__Comprehend__Toxicity_Score_Response:              # Simplified toxicity scores

        try:
            with capture_duration() as duration:
                toxic_result = self.comprehend_service().detect_toxic_content(text          = request.text         ,
                                                                             language_code = request.language_code,
                                                                             use_cache     = request.use_cache    )

                # Convert labels list to scores dict
                scores = {}
                for label in toxic_result.labels:
                    scores[label.name] = Safe_Float__Probability_Score(label.score)

            return Schema__Comprehend__Toxicity_Score_Response(scores   = scores                       ,
                                                               cached   = False                        ,
                                                               duration = Safe_Float(duration.seconds) )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"toxicity_score failed: {str(e)}")

    # ========================================
    # ROUTE SETUP
    # ========================================

    def setup_routes(self):                                                     # Register all route handlers
        self.add_route_post(self.is_positive    )                              # is_positive endpoint
        self.add_route_post(self.is_negative    )                              # is_negative endpoint
        self.add_route_post(self.is_neutral     )                              # is_neutral endpoint
        self.add_route_post(self.is_toxic       )                              # is_toxic endpoint
        self.add_route_post(self.sentiment_score)                              # sentiment_score endpoint
        self.add_route_post(self.toxicity_score )                              # toxicity_score endpoint
