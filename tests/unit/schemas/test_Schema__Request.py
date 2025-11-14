from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                       import Safe_Float
from osbot_aws.aws.comprehend.schemas.enums.Enum__Comprehend__Language_Code                 import Enum__Comprehend__Language_Code
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text               import Safe_Str__Comprehend__Text
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Request           import Schema__Comprehend__Request
from mgraph_ai_service_aws_comprehend.schemas.request.Schema__Comprehend__Threshold_Request import Schema__Comprehend__Threshold_Request


class test_Schema__Comprehend__Request(TestCase):

    def test__init__(self):                                                    # Test schema initialization
        with Schema__Comprehend__Request() as _:
            assert type(_) is Schema__Comprehend__Request
            assert _.language_code == Enum__Comprehend__Language_Code.ENGLISH  # Default value
            assert _.use_cache     == False                                    # Default value
            assert _.obj()         == __(text          = ''       ,            # Empty Safe_Str__Comprehend__Text
                                        language_code = 'en'     ,
                                        use_cache     = False    )

    def test__init__with_values(self):                                         # Test schema with provided values
        text = Safe_Str__Comprehend__Text("Test text")

        with Schema__Comprehend__Request(text          = text                                    ,
                                         language_code = Enum__Comprehend__Language_Code.SPANISH,
                                         use_cache     = True                                   ) as _:
            assert _.text          == text
            assert _.language_code == Enum__Comprehend__Language_Code.SPANISH
            assert _.use_cache     == True
            assert _.obj()         == __(text          = 'Test text',
                                        language_code = 'es'      ,
                                        use_cache     = True      )

    def test__init__type_conversion(self):                                     # Test auto-conversion from raw types
        with Schema__Comprehend__Request(text          = "Raw string"  ,       # Auto-converts to Safe_Str__Comprehend__Text
                                         language_code = "en"          ,       # Auto-converts to Enum
                                         use_cache     = False         ) as _:
            assert type(_.text)          is Safe_Str__Comprehend__Text
            assert type(_.language_code) is Enum__Comprehend__Language_Code
            assert _.language_code       == Enum__Comprehend__Language_Code.ENGLISH


class test_Schema__Comprehend__Threshold_Request(TestCase):

    def test__init__(self):                                                    # Test threshold request initialization
        with Schema__Comprehend__Threshold_Request() as _:
            assert type(_)          is Schema__Comprehend__Threshold_Request
            assert _.threshold      == Safe_Float(0.7)                         # Default threshold
            assert _.language_code  == Enum__Comprehend__Language_Code.ENGLISH
            assert _.use_cache      == False
            assert _.obj()          == __(text          = ''     ,
                                         threshold     = 0.7    ,
                                         language_code = 'en'   ,
                                         use_cache     = False  )

    def test__init__with_values(self):                                         # Test threshold request with values
        text = Safe_Str__Comprehend__Text("Test")

        with Schema__Comprehend__Threshold_Request(text          = text                                    ,
                                                   threshold     = Safe_Float(0.8)                        ,
                                                   language_code = Enum__Comprehend__Language_Code.FRENCH,
                                                   use_cache     = True                                   ) as _:
            assert _.text          == text
            assert _.threshold     == Safe_Float(0.8)
            assert _.language_code == Enum__Comprehend__Language_Code.FRENCH
            assert _.use_cache     == True
            assert _.obj()         == __(text          = 'Test',
                                        threshold     = 0.8   ,
                                        language_code = 'fr'  ,
                                        use_cache     = True  )

    def test__threshold__range_validation(self):                               # Test that threshold is a Safe_Float (0.0-1.0)
        with Schema__Comprehend__Threshold_Request(threshold=Safe_Float(0.5)) as _:
            assert 0.0 <= float(_.threshold) <= 1.0
