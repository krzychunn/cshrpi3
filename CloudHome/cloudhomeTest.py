# -*- coding: utf-8 -*-
import time
import grovepi
import math

import requests
import thread

from grovepi import *
from grove_rgb_lcd import *

sound_sensor = 0        
light_sensor = 1         
dht_sensor_port = 7	
dht_sensor_type = 0     
ultrasonic_ranger = 4
led_green = 2
led_red = 3
heating = 8
airCondition = 6
buzzer = 5

pinMode(led_green,"OUTPUT")
pinMode(led_red,"OUTPUT")
digitalWrite(led_green,1)

mainAppPath='https://arcane-escarpment-70375.herokuapp.com'
login='knn'
password='nnk'

def checkDistance(distance1, distance2):
        minimumDistance = httpGet('/minimumDistance/getLast')
        if(abs(distance1-distance2)==0):
                digitalWrite(buzzer, 0)
                httpPost('/buzzer/add', {'state':'false'})
        if(abs(distance1-distance2)!=0):
                digitalWrite(buzzer, 1)
                httpPost('/buzzer/add', {'state':'true'})
                time.sleep(5)

def security():
        try:
                distance1 = ultrasonicRead(ultrasonic_ranger)
                #print("distance1=", distance1)
                        
                time.sleep(0.1)

                distance2 = ultrasonicRead(ultrasonic_ranger)
                #print("distance2=", distance2)

                checkDistance(distance1, distance2)                      
                
        except KeyboardInterrupt:
                digitalWrite(buzzer, 0)
        except (IOError,TypeError) as e:
                print('---------------------------------------')

def main():
        counter = 0
        while True:
                try:
        
                        digitalWrite(led_red,0)

                        light_intensity = grovepi.analogRead(light_sensor)

                        sound_level = grovepi.analogRead(sound_sensor)

                        [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)

                        distant = ultrasonicRead(ultrasonic_ranger)

                        #print('---------------------------------------')
                        #print('Light intensity: ', light_intensity)
                        #print('Sound level: ', sound_level)
                        #print('Temperature: ',temp)
                        #print('Humidity: ',hum)
                        #print('Distant: ',distant)

                        #optimalTemperature = httpGet('/optimalTemperature/getLast')
                        #if(temp>(float)(optimalTemperature["minimumTemperature"])):
                                #digitalWrite(heating, 0)
                                #httpPost('/heating/add', {'state':'false'})
                        #if(temp<(float)(optimalTemperature["minimumTemperature"])):
                                #digitalWrite(heating, 1)
                                #httpPost('/heating/add', {'state':'true'})
                        #if(temp>(float)(optimalTemperature["maximumTemperature"])):
                                #digitalWrite(airCondition, 1)
                                #httpPost('/airCondition/add', {'state':'true'})
                        #if(temp<(float)(optimalTemperature["maximumTemperature"])):
                                #digitalWrite(airCondition, 0)
                                #httpPost('/airCondition/add', {'state':'false'})

                        security()

                        digitalWrite(led_red,1)
                        if(counter%10==0):
                                query_args = {'lightIntensity':light_intensity,'soundLevel':sound_level,'temperature':temp,'humidity':hum,'distance':distant}
                                #httpPost('/measurements/add', query_args)

                        counter +=1
                        #time.sleep(0.1)
                except KeyboardInterrupt:
                        digitalWrite(led_green,0)
                        digitalWrite(led_red,0)
                        digitalWrite(buzzer, 0)
                        digitalWrite(heating, 0)
                        digitalWrite(airCondition, 0)
                        break
                except (IOError,TypeError) as e:
                        print('---------------------------------------')

def httpGet(path):
        r = requests.get(mainAppPath+path, auth=(login, password))
        body = r.json()
        return body;

def httpPost(path, toPost):
        r = requests.post(mainAppPath+path, auth=(login, password), json=toPost)
        headers = {'Content-type': 'application/json'}
        return

def display(t, h):
        setRGB(0,128,64)
	setRGB(0,64,64)
	setText("Temp. :" + t + "'C   " + "Hum.  :" + h + "%")
	return

main()
