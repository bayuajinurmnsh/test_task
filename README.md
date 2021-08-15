# test_task
This is an application to check distance from moscow ring road to a specific address using Yandex API Geocoder and Haversine Formula



## System Requirement
### If you have docker , clone this repository to your docker

### If you do not have docker , you install manually this library : 
* Python version 3.9.6 or at least Python version 3.8
* certifi==2021.5.30
* charset-normalizer==2.0.4
* click==8.0.1
* colorama==0.4.4
* Flask==2.0.1
* idna==3.2
* itsdangerous==2.0.1
* Jinja2==3.0.1
* MarkupSafe==2.0.1
* requests==2.26.0
* toml==0.10.2
* urllib3==1.26.6
* utils==1.0.1
* Werkzeug==2.0.1

# How to use this program

## A. If you are using Postman

![alt text](https://github.com/bayuajinurmnsh/test_task/blob/main/documentation/postman.png)

* start the program: using **docker** ->  docker run -p 5000:5000 -d "your docker image name"
* start the program: using **app.py** ->  "your path to app.py" python app.py

1. Open your postman
2. Type in url "http://127.0.0.1:5000/test_task/api/distance_address"
3. Change your method to "POST"
4. In tab "body" choose JSON
5. Send your data with json syntax

**NOTES**
- start point has set to default from MKAD at latitude:55.898947, longitude:37.632206
- Make sure you send "**address**" : "your address"
- If you send "**adres**" : "your address" program will send response that your json file do not have **address** key
- You can send address with specific address like "Odintsovo-1 Residential Complex Odintsovo, Moscow Region, Russia"
  Or you can send latitude and longitude from the specific address, "latitude, longitude". Example "55.641974, 37.231171"
- Do not send a single word like "a" , "b" or program will send a response that your address is invalid. But if you send "ca" it is valid and program will count the distance from MKAD to California, America , or
- Do not send a number with single value like "5" or "1" or program will send a response that your address is invalid. But if you send "5, 5" it is valid and program will count the distance from mkad to Gulf of Guinea at latitude 5.000000 and longitude 5.000000
- If your specific address is in the Moscow ring road then the program will not calculate the distance from the default point to the intended address

## B. If you are using Web Browser

![alt text](https://github.com/bayuajinurmnsh/test_task/blob/main/documentation/gui_1.png)

* start the program: using **docker** ->  docker run -p 5000:5000 -d "your docker image name"
* start the program: using **app.py** ->  "your path to app.py" python app.py

1. Open your browser
2. Type url http://127.0.0.1:5000/
3. Type your specific address

**NOTES**
- start point has set to default from MKAD at latitude:55.898947, longitude:37.632206
- You can send address with specific address like "Odintsovo-1 Residential Complex Odintsovo, Moscow Region, Russia"
  Or you can send latitude and longitude from the specific address, "latitude, longitude". Example "55.641974, 37.231171"
- Do not send a single word like "a" , "b" or program will send a response that your address is invalid. But if you send "ca" it is valid and program will count the distance from MKAD to California, America , or
- Do not send a number with single value like "5" or "1" or program will send a response that your address is invalid. But if you send "5, 5" it is valid and program will count the distance from mkad to Gulf of Guinea at latitude 5.000000 and longitude 5.000000
- If your specific address is in the Moscow ring road then the program will not calculate the distance from the default point to the intended address