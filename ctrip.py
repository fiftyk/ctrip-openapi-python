# -*- coding: utf-8 -*-
import time
import hashlib

'''
md5 算法
'''
def md5(str):
  m = hashlib.md5()   
  m.update(str)
  return m.hexdigest()

print md5('asd')
'''
ctrip openapi signature 算法
'''
def signature(requesttype, allianceid, apikey, sid):
  timestamp = str(int(round(time.time())))
  return md5(timestamp + allianceid + md5(apikey).upper() + sid + requesttype).upper()

'''
ctrip openapi request header template
'''
HEADER_TPL = '<Header AllianceID="%s" SID="%s" TimeStamp="%d" Signature="%s" RequestType="%s"/>'

'''
ctrip openapi request header function
'''
def header(requesttype, allianceid, apikey, sid):
  timestamp = int(round(time.time()))
  return HEADER_TPL%(allianceid, sid, timestamp, signature(requesttype, allianceid, apikey, sid), requesttype)

from suds.client import Client
url = "http://openapi.ctrip.com/Hotel/OTA_Ping.asmx?WSDL"
client = Client(url)

_header = header('OTA_Ping', allianceid='26610', apikey='B7B9C84A-5EBD-4A26-93E5-9851E3479A54', sid='462597')

print client.service.Request(
  requestXML='<Request>%s<HotelRequest><RequestBody xmlns:ns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><ns:OTA_PingRQ><ns:EchoData>sdf</ns:EchoData></ns:OTA_PingRQ></RequestBody></HotelRequest></Request>'%_header
)
