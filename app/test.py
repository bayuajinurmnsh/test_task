from logging import error
import unittest
from requests.api import request
from app import app
import technical


class Test(unittest.TestCase):
    
    #UNIT TEST FOR app.py
    URL = "http://127.0.0.1:5000/test_task/api/distance_address"

    data_valid = {"address": "Moscow"}
    key_invalid = {"adres": "Moscow"}
    invalid_address_1 ={"address": "@5-!&*a"}
    invalid_address_2 ={"address": "-1@1 jgstuo2"}
    outside_mkad = {"address": "Jakarta, Indonesia"}

    error_1 = b'{"message":"You have to send data in json format"}\n'
    error_2 = b'{"message":"make sure you have key address in your JSON data"}\n'
    error_3 = b'{"message":"Invalid address!"}\n'
    error_4 = b'{"message":"Can not find your address!"}\n'
    error_5 = b'{"message":"Server do not have access to yandex API"}\n'
    inside_mkad =  b'{"message":"area inside MKAD"}\n'

    # Test for index function
    # Test to check the index function if it run properly or not
    def test_index(self):
        test = app.test_client(self)
        response = test.get('/', content_type = 'html/text')
        self.assertEqual(response.status_code, 200)
    
    # Test for distance_address function
    # Test to check if address is inside Moscow ring road
    def test_inside_mkad(self):
        tester = app.test_client(self)
        response = tester.post(self.URL, json = self.data_valid,
                              content_type = 'application/json')
        self.assertEqual(self.inside_mkad,response.data)
        self.assertEqual(response.status_code, 200)
    
    # Test to check if address is outside Moscow ring road
    def test_outside_mkad(self):
        tester = app.test_client(self)
        response = tester.post(self.URL, json = self.outside_mkad,
                              content_type = 'application/json')
        self.assertNotEqual(response.data, self.inside_mkad)
        self.assertEqual(response.status_code, 200)
    
    # Test to check if client not post a json file type
    # In this case i try to use xml
    def test_content_type_not_json(self):
        test = app.test_client(self)
        response = test.post(self.URL, data = self.data_valid, 
                             content_type='application/xml')
        self.assertEqual(response.data, self.error_1)
        self.assertEqual(response.status_code, 415)
    
    # Test to check if key not is json file
    # valid key is 'address' but in this test used 'adres'
    def test_content_key_invalid(self):
        test = app.test_client(self)
        response = test.post(self.URL, json = self.key_invalid,
                             content_type = 'application/json')
        self.assertEqual(response.data, self.error_2)
        self.assertEqual(response.status_code, 400)
        
    # Invalid address type 1
    # This test check if client only send one letter in address or
    # maybe a number with single value like only "5"
    def test_invalid_addres_1(self):
        tester = app.test_client(self)
        response = tester.post(self.URL, json = self.invalid_address_1,
                              content_type = 'application/json')
        self.assertEqual(response.data, self.error_3)
        self.assertEqual(response.status_code, 422)
        
    # Invalid address type 2
    # If address have passed the invalid type 1 but yandex can not find
    # latitude and longitude from specific address
    def test_invalid_addres_2(self):
        tester = app.test_client(self)
        response = tester.post(self.URL, json = self.invalid_address_2,
                              content_type = 'application/json')
        self.assertEqual(response.data, self.error_4)
        self.assertEqual(response.status_code, 404)

    # Test if our server have access to Yandex API
    # Error occurs when our server do not have valid API Key
    def test_access(self):
        tester = app.test_client(self)
        response = tester.post(self.URL, json = self.data_valid,
                              content_type = 'application/json')
        self.assertNotEqual(response.data, self.error_5)
        self.assertNotEqual(response.status_code, 500)
    
    #UNIT TEST FOR technical.py
    # Test if address inside mkad  [test class CheckDistance]
    def test_count_distance_1(self):
        lat = 55.753220 #lat for Moscow, Russia
        long = 37.622513 #long for Moscow, Russia
        obj_check_distance = technical.CheckDistance(lat,long)
        count_distance = obj_check_distance.count_distance()
        self.assertEqual('area inside MKAD', count_distance)
    
    # Test if address outside  mkad [test class CheckDistance]
    # And test if count_distance return a value in float type
    def test_count_distance_2(self):
        lat = -6.175391 #lat for Jakarta, Indonesia
        long =  106.826261 #long for Jakarta, Indonesia
        obj_check_distance = technical.CheckDistance(lat,long)
        count_distance = obj_check_distance.count_distance()
        self.assertNotEqual('area inside MKAD', count_distance)
        self.assertIs(type(count_distance), float)
    
    # Test if lat, and long not in float type [test class CheckDistance]
    def test_count_distance_3(self):
        lat_1 = "-6.175391"
        long_1 =  106.826261
        lat_2 = "Moscow, Russia"
        long_2 = "Jakarta, Indonesia"
        obj_check_distance_1 = technical.CheckDistance(lat_1,long_1)
        count_distance_1 = obj_check_distance_1.count_distance()
        self.assertEqual("latitude and longitude must be in float type", 
                        count_distance_1)

        obj_check_distance_2 = technical.CheckDistance(lat_2,long_2)
        count_distance_2 = obj_check_distance_2.count_distance()
        self.assertEqual("latitude and longitude must be in float type", 
                        count_distance_2)
    
    # Test haversine function if lat and long in float type
    # And check if result not in string type [test class CheckDistance]
    def test_haversine_1(self):
        lat_1 = 55.898947 #lat for MKAD, 88th kilometre, inner side
        long_1 = 37.632206 # long for MKAD, 88th kilometre, inner side
        lat_2 = 38.231572
        long_2 = 25.192846
        obj_check_distance = technical.CheckDistance(lat_2,long_2)
        haversine = obj_check_distance.haversine(lat_1, long_1, 
                                                 lat_2, long_2)
        self.assertIsNot(type(haversine), str)
        self.assertIs(type(haversine), float)
    
    # Test haversine function if lat and lon in integer 
    def test_haversine_2(self):
        lat_1 = int(55)
        long_1 = int(37)
        lat_2 = int(38)
        long_2 = int(-25)
        obj_check_distance = technical.CheckDistance(lat_2,long_2)
        haversine = obj_check_distance.haversine(lat_1, long_1, 
                                                 lat_2, long_2)
        self.assertIsNot(type(haversine), str)
    
    # Test if lat or long in string type
    def test_haversine_3(self):
        lat_1 = str(55) #lat for MKAD, 88th kilometre, inner side
        long_1 = 37 # long for MKAD, 88th kilometre, inner side
        lat_2 = 38.0098
        long_2 = "15"
        obj_check_distance = technical.CheckDistance(lat_2,long_2)
        haversine = obj_check_distance.haversine(lat_1, long_1, 
                                                 lat_2, long_2)
        self.assertEqual("latitude and longitude can not be string", 
                         haversine)
        
    # Test check_address function to check address is valid or not
    # Test valid if (address is a letter, length addres >=2)
    # Test valid if (address is number, length address >=2)
    def test_check_address_valid_1(self):
        address = "Moscow, Russia"
        obj_check_address = technical.TextPreprocessing(address)
        check_address = obj_check_address.check_address()
        self.assertEqual("valid", check_address)
    
    # Test if lat and long value in string type
    def test_check_address_valid_2(self):
        address = "55.2333, 25.444221"
        obj_check_address = technical.TextPreprocessing(address)
        check_address = obj_check_address.check_address()
        self.assertEqual("valid", check_address)
    
    # Test if address not in string type
    def test_check_address_valid_2(self):
        address = 55.233325
        obj_check_address = technical.TextPreprocessing(address)
        check_address = obj_check_address.check_address()
        self.assertEqual("address must be in string type", check_address)


if __name__ == "__main__":
    unittest.main()