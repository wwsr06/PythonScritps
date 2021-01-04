#coding=utf-8
import sys
import time
import json
import requests
import hmac
import hashlib

accessKey = b'b904b335-01b90d85-vqgdf4gsga-ef9e3'
secKey = b'e272153c-8e2f8e09-ae09a28b-8dc96'

def get_sitestatus():
    r = requests.get("https://status.huobigroup.com/api/v2/summary.json")
    print (r.status_code)
    print (r.text)

def get_servertime():
    reqstr = 'https://api.binance.com/api/v3/time'
    #print (reqstr)

    headers = {"X-MBX-APIKEY":apikey}
    r = requests.get(reqstr)
    
    #print (r.status_code)
    #print (r.text)
    resd = json.loads(r.text)
    return resd.get("serverTime")

def get_accountinfo():
    ts = str(int((time.time()*1000)))
    tmpstr = 'timestamp='
    tmpstr += ts
    #print (tmpstr)

    msg = bytes(tmpstr,encoding='utf-8')
    h = hmac.new(key,msg,digestmod='SHA256')
    sign = h.hexdigest()
    #print (sign)

    reqstr = 'https://api.binance.com/api/v3/account'
    reqstr += '?timestamp='
    reqstr += ts
    reqstr += '&signature='
    reqstr += sign
    #print (reqstr)
    
    headers = {"X-MBX-APIKEY":apikey}
    
    RdOK = 0
    while RdOK!=200:
        r = requests.get(reqstr,headers=headers)
        print (r.status_code)
        RdOK = r.status_code
        #print (r.text)

   
    resd = json.loads(r.text)
    bal_all = resd["balances"]
    for ba in bal_all:
        if (ba.get("asset")=="BTC" or ba.get("asset")=="USDT" or ba.get("asset")=="TRX"):
            print (str(ba.get("asset"))+'|'+str(ba.get("free")))

def get_24hrPriceChangeStatistics(symbol):
    reqstr = 'https://api.huobi.pro/market/detail'
    reqstr += '?symbol='
    reqstr += symbol
    #print (reqstr)
    
    
    try:
        r = requests.get(reqstr)
    except Exception:
        print ("Error:")
        return -1
         
    #print (r.status_code)
    #print (r.text)
    resd = json.loads(r.text)
    ptstr = "Last/H/L : " 
    ptstr += str(int(resd.get("tick").get("close"))) + '|'
    ptstr += str(int(resd.get("tick").get("high"))) + '|'
    ptstr += str(int(resd.get("tick").get("low"))) + '|\n'
    print (ptstr)

    
def get_CurrentOpenOrders():
    shastr = 'symbol=BTCUSDT'
    ts = str(int((time.time()*1000))-300) 
    shastr+= '&timestamp='
    shastr+= ts
    #print (shastr)

    msg = bytes(shastr,encoding='utf-8')
    h = hmac.new(key,msg,digestmod='SHA256')
    sign = h.hexdigest()
    #print (sign)
    

    reqstr = 'https://api.binance.com/api/v3/openOrders?'
    reqstr += shastr
    reqstr += '&signature='
    reqstr += sign
    #print (reqstr)
    
    headers = {"X-MBX-APIKEY":apikey}
    r = requests.get(reqstr,headers=headers)
    #print (r.status_code)
    print (r.text)
    resd = json.loads(r.text)
    oID = (resd[0].get("orderId"))
    
    return oID
    
def set_NewOrder(): 
    ts = str(int((time.time()*1000)))
    '''
    data = {
        "symbol":"BTCUSDT",
        "side":"BUY",
        "type":"LIMIT",
        "timeInForce":"GTC",
        "quantity":"0.0001",
        "price":"50000",
        "recvWindow":"5000",
        "timestamp" : ts,
    }
    
    url = "https://api.binance.com/api/v3/order/test"
    r = requests.post(url=url,data=data)
    print (r.status_code)
    print (r.text)
    '''

    shastr = 'symbol=BTCUSDT'
    shastr+= '&side=BUY'
    shastr+= '&type=LIMIT'
    shastr+= '&timeInForce=GTC'
    shastr+= '&quantity=0.0011'
    shastr+= '&price=23000'
    shastr+= '&recvWindow=5000'
    ts = str(int((time.time()*1000)))
    shastr+= '&timestamp='
    shastr+= ts
    print (shastr)
    #input()

    msg = bytes(shastr,encoding='utf-8')
    h = hmac.new(key,msg,digestmod='SHA256')
    sign = h.hexdigest()
    #print (sign)

    reqstr = 'https://api.binance.com/api/v3/order?'
    reqstr += shastr
    reqstr += '&signature='
    reqstr += sign
    print (reqstr)
    #input()
    
    print (get_server_time())



    headers = {"X-MBX-APIKEY":apikey}
    r = requests.post(url=reqstr,headers=headers)
    print (r.status_code)
    print (r.text)

    
def cancel_order(orderID):
    
    shastr = 'symbol=BTCUSDT'
    shastr+= '&orderId=' + str(orderID)
    ts = str(int((time.time()*1000))-300) 
    shastr+= '&timestamp='
    shastr+= ts
    #print (shastr)

    msg = bytes(shastr,encoding='utf-8')
    h = hmac.new(key,msg,digestmod='SHA256')
    sign = h.hexdigest()
    #print (sign)
    

    reqstr = 'https://api.binance.com/api/v3/order?'
    reqstr += shastr
    reqstr += '&signature='
    reqstr += sign
    #print (reqstr)
    
    headers = {"X-MBX-APIKEY":apikey}
    r = requests.delete(reqstr,headers=headers)
    print (r.status_code)
    print (r.text)

    



#Main Flow
#get_sitestatus()
while 1:
    get_24hrPriceChangeStatistics('btcusdt')
    time.sleep(1)
