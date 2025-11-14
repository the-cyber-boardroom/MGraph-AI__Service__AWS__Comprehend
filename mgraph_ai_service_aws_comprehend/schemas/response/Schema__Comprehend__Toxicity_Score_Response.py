from typing                                                                                      import Dict
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                            import Safe_Float
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Probability_Score import Safe_Float__Probability_Score
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Toxic_Content_Label                import Enum__Comprehend__Toxic_Content_Label


class Schema__Comprehend__Toxicity_Score_Response(Type_Safe):                  # Simplified toxicity score response
    scores   : Dict[Enum__Comprehend__Toxic_Content_Label, Safe_Float__Probability_Score]  # Label → score mapping
    cached   : bool                                                             # Whether result was from cache
    duration : Safe_Float                                                       # Processing time in seconds
