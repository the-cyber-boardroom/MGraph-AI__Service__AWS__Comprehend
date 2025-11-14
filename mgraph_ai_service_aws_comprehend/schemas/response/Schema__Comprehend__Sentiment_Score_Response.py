from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                               import Safe_Float
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Probability_Score import Safe_Float__Probability_Score


class Schema__Comprehend__Sentiment_Score_Response(Type_Safe):                 # Simplified sentiment score response
    positive : Safe_Float__Probability_Score                                    # Positive sentiment score (0.0-1.0)
    negative : Safe_Float__Probability_Score                                    # Negative sentiment score (0.0-1.0)
    neutral  : Safe_Float__Probability_Score                                    # Neutral sentiment score (0.0-1.0)
    mixed    : Safe_Float__Probability_Score                                    # Mixed sentiment score (0.0-1.0)
    cached   : bool                                                             # Whether result was from cache
    duration : Safe_Float                                                       # Processing time in seconds
