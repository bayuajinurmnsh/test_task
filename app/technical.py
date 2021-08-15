from logging import error
from math import radians, cos, sin, asin, sqrt


class CheckDistance:
    
    def __init__(self, address_lat, address_long):
      self.address_lat = address_lat
      self.address_long = address_long
      
      # Set center point in a few area inside MKAD and set a radius area 
      self.center_point = [
              {'lat':55.753220, 'long':37.622513, 'radius':13.708}, 
              {'lat':55.80357, 'long':37.55673, 'radius':10.484},
              {'lat':55.84250, 'long':37.46568, 'radius':4.709}, 
              {'lat':55.76929, 'long':37.49548, 'radius':8.086},
              {'lat':55.85389, 'long':37.57094, 'radius':6.378}, 
              {'lat':55.83005, 'long':37.65742, 'radius':7.661},
              {'lat':55.80288, 'long':37.78037, 'radius':3.824}, 
              {'lat':55.82753, 'long':37.73952, 'radius':4.160},
              {'lat':55.81697, 'long':37.80511, 'radius':2.149}, 
              {'lat':55.83139, 'long':37.79135, 'radius':1.689},
              {'lat':55.76542, 'long':37.79374, 'radius':3.286}, 
              {'lat':55.78687, 'long':37.81664, 'radius':1.628},
              {'lat':55.68828, 'long':37.63789, 'radius':12.452}, 
              {'lat':55.74438, 'long':37.44958, 'radius':4.957},
              {'lat':55.72315, 'long':37.43767, 'radius':3.503}, 
              {'lat':55.69380, 'long':37.51139, 'radius':6.034},
              {'lat':55.66398, 'long':37.81106, 'radius':1.779}, 
              {'lat':55.66024, 'long':37.82557, 'radius':0.93514},
              {'lat':55.65617, 'long':37.82159, 'radius':1.071}, 
              {'lat':55.64990, 'long':37.82241, 'radius':0.60358},
              {'lat':55.64677, 'long':37.81213, 'radius':0.91403}, 
              {'lat':55.62192, 'long':37.54877, 'radius':3.764},
              {'lat':55.64735, 'long':37.63765, 'radius':8.371}
              ]

      #this is default start point for Moscow Ring Road      
      self.start_point = [{'lat': 55.898947, 'long': 37.632206}]

    def haversine(self,lat_1, long_1, lat_2, long_2):
      """
      This function is useful for calculating the distance between 
      the start point and a specific address using the haversine formula
      lat_1 is latitude from start_point / center point
      long_1 is longitude from start_point / center point
      lat_2 is latitude from address point
      long_2 is longitude from address point
      """
      #check if lat and long not in float type
      if isinstance(lat_1, str) or isinstance(long_1, str) or isinstance(
          lat_2, str) or isinstance(long_2, str):
        return "latitude and longitude can not be string"

      # Convert decimal degrees to radians 
      lat_1, long_1, lat_2, long_2 = map(radians, [lat_1, long_1, 
                                       lat_2, long_2])

      # Haversine formula to count distance
      delta_long = long_2 - long_1 
      delta_lat = lat_2 - lat_1 
      earth_radius = 6371 # Radius of earth in kilometers.
      result = 2 * asin(sqrt(sin(delta_lat/2)**2 + cos(lat_1) 
          * cos(lat_2) * sin(delta_long/2)**2)) * earth_radius
      return result

    def count_distance(self):
      inside_area = 0
      lat_2 = self.address_lat
      long_2 = self.address_long
      
      if isinstance(lat_2, str) or isinstance(long_2, str):
        return "latitude and longitude must be in float type"

      # Check if the point from specific address is inside MKAD or not
      for item in self.center_point:
        lat_center = item['lat']
        long_center = item['long']
        radius_area_center = item['radius']
        distance_center_to_address = self.haversine(lat_center, long_center,
                                  lat_2, long_2)
        
        # If distance from center point to address point is less than
        # or equal the radius area of center point, it means 
        # specific address is inside MKAD
        if distance_center_to_address <= radius_area_center:
          inside_area +=1
      
      # Count the distance between start poin to address point if 
      # variable inside_area equal to 0
      if inside_area == 0:
        lat_1 = self.start_point[0]['lat']
        long_1 = self.start_point[0]['long']
        result = self.haversine(lat_1, long_1, lat_2, long_2)
        return result
      else: 
        return "area inside MKAD" 
      

class TextPreprocessing:

    def __init__(self,text):
        self.text = text
    
    def check_address(self):
      """ 
      In yandex API we can find the location even though it only 
      contains 2 letters like CA (california) and UK (united kingdom), 
      so if the address contains less than 2 letters it is an invalid 
      address And also we can find a location with latitude and 
      longitude with only 2 value like 5,5
      """
      txt = self.text
      if not isinstance(txt, str):
        return "address must be in string type"

      count_alphabet = 0
      count_number = 0
      for alphabet in txt:
        if alphabet.isalpha():
          count_alphabet += 1
        
      for number in txt:
        if number.isnumeric():
          count_number += 1

      if count_alphabet >= 2 or count_number >=2:
        return "valid"
      else:
        return "invalid"