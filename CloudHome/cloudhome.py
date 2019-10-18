# -*- coding: utf-8 -*-
import time
import grovepi
import math

import requests

from grovepi import *
from grove_rgb_lcd import *
      
light_sensor = 1         
dht_sensor_port = 2	
dht_sensor_type = 0     
gas_sensor = 0
light = 7
humidifier = 8
heating = 3
airCondition = 4
buzzer = 5

timeSleep = 60

pinMode(gas_sensor,"INPUT")

mainAppPath='https://csh-rpi-3.herokuapp.com'
login='knn'
password='nnk'

def httpGet(path):
        r = requests.get(mainAppPath+path, auth=(login, password))
        body = r.json()
        return body;

def httpPost(path, toPost):
        r = requests.post(mainAppPath+path, auth=(login, password), json=toPost)
        headers = {'Content-type': 'application/json'}
        return

def display(temperature, humidity, light, gas):
        setRGB(0,128,64)
	setRGB(0,64,64)
	setText("T" + temperature + " H" + humidity + "\nL" + light + " G" + gas)
	return

while True:
	try:                

                light_intensity = grovepi.analogRead(light_sensor)

                gas_level = grovepi.analogRead(gas_sensor)

		[ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)

                optimalTemperature = httpGet('/optimalTemperature/getLast')
                if(temp>(float)(optimalTemperature["minimumTemperature"])):
                        digitalWrite(heating, 0)
                        httpPost('/heating/add', {'state':'false'})
                if(temp<(float)(optimalTemperature["minimumTemperature"])):
                        digitalWrite(heating, 1)
                        httpPost('/heating/add', {'state':'true'})
                if(temp>(float)(optimalTemperature["maximumTemperature"])):
                        digitalWrite(airCondition, 1)
                        httpPost('/airCondition/add', {'state':'true'})
                if(temp<(float)(optimalTemperature["maximumTemperature"])):
                        digitalWrite(airCondition, 0)
                        httpPost('/airCondition/add', {'state':'false'})
                if(temp==(float)(optimalTemperature["maximumTemperature"]) or temp==(float)(optimalTemperature["minimumTemperature"])):
                        digitalWrite(airCondition, 0)
                        httpPost('/airCondition/add', {'state':'false'})
                        digitalWrite(heating, 0)
                        httpPost('/heating/add', {'state':'false'})
                     
                maximumGas = httpGet('/maximumGas/getLast')
                if(gas_level<(float)(maximumGas["maximumGas"])):
                        digitalWrite(buzzer, 0)
                        httpPost('/buzzer/add', {'state':'false'})
                if(gas_level>(float)(maximumGas["maximumGas"])):
                        digitalWrite(buzzer, 1)
                        httpPost('/buzzer/add', {'state':'true'})

                minimumHumidity = httpGet('/minimumHumidity/getLast')
                if(hum>(float)(minimumHumidity["minimumHumidity"])):
                        digitalWrite(humidifier, 0)
                        httpPost('/humidifier/add', {'state':'false'})
                if(hum<(float)(minimumHumidity["minimumHumidity"])):
                        digitalWrite(humidifier, 1)
                        httpPost('/humidifier/add', {'state':'true'})

                minimumLight = httpGet('/minimumLight/getLast')
                if(light_intensity>(float)(minimumLight["minimumLight"])):
                        digitalWrite(light, 0)
                        httpPost('/light/add', {'state':'false'})
                if(light_intensity<(float)(minimumLight["minimumLight"])):
                        digitalWrite(light, 1)
                        httpPost('/light/add', {'state':'true'})

		display(str(temp), str(hum), str(light_intensity), str(gas_level))

                query_args = {'lightIntensity':light_intensity,'gasDensity':gas_level,'temperature':temp,'humidity':hum}
                httpPost('/measurements/add', query_args)

                time.sleep(timeSleep)

        except KeyboardInterrupt:
                digitalWrite(light,0)
                digitalWrite(humidifier,0)
                digitalWrite(buzzer, 0)
                digitalWrite(heating, 0)
                digitalWrite(airCondition, 0)
                break
	except (IOError,TypeError) as e:
		print('---------------------------------------')
