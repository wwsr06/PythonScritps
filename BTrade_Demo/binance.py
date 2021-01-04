#coding=utf-8
import sys
import time
import json
import requests
import hmac
import hashlib

key = b'MKkyxdhn2oPoHDKg4WIiIeOeOiz4LdFGBZCCwIpyj87MGG7ZAbAKPn0IWcCO2zaf' #sec key
apikey = b'XNm2yp6zfhDQ6ULqPtSZhFNzjsOz1pmOnSNOXhpta16yKuGKpRkzblgyg1zz37yi' #apikey

def gn_get_site_status():
    r = requests.get("https://api.binance.com/wapi/v3/systemStatus.html")
    print (r.status_code)
    resd = json.loads(r.text)
    print (resd.get("msg"))

def gn_get_server_time():
    r = requests.get("https://api.binance.com/api/v3/time")
    #print (r.status_code)
    resd = json.loads(r.text)
    #print (resd.get("msg"))
    print (resd["serverTime"])
    return resd["serverTime"]

def gn_get_accountSnapshot():
    ts = str(int((time.time()*1000))-300)
    tmpstr = 'type=SPOT&'
    tmpstr += 'recvWindow=5000&'
    tmpstr += 'timestamp='
    tmpstr += ts
    #print (tmpstr)

    msg = bytes(tmpstr,encoding='utf-8')
    h = hmac.new(key,msg,digestmod='SHA256')
    sign = h.hexdigest()
    #print (sign)

    reqstr = 'https://api.binance.com/sapi/v1/accountSnapshot'
    reqstr += '?type=SPOT&recvWindow=5000&timestamp='
    reqstr += ts
    reqstr += '&signature='
    reqstr += sign
    #print (reqstr)

    headers = {"X-MBX-APIKEY":apikey}
    r = requests.get(reqstr,headers=headers)
    
    print (r.status_code)
    print (r.text)


def md_get_ExchangeInformation():
    reqstr = 'https://api.binance.com/api/v3/exchangeInfo'
    #print (reqstr)

    headers = {"X-MBX-APIKEY":apikey}
    r = requests.get(reqstr)
    
    #print (r.status_code)
    print (r.text)
    resd = json.loads(r.text)
    #return resd.get("serverTime")

def md_get_OrderBook(symbol):
    reqstr = 'https://api.binance.com/api/v3/depth'
    reqstr += '?symbol='
    reqstr += symbol
    reqstr += '&limit=5'
    #print (reqstr)
    
    r = requests.get(reqstr)
    #print (r.status_code)
    print (r.text)
    resd = json.loads(r.text)
    #return resd.get("serverTime")

def md_get_24hrPriceChangeStatistics(symbol):
    reqstr = 'https://api.binance.com/api/v3/ticker/24hr'
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
    
    last = int(float(resd.get("lastPrice")))
    high = int(float(resd.get("highPrice")))
    low = int(float(resd.get("lowPrice")))
    
    ptstr = "Last/H/L: " 
    ptstr += str(last) + '|'
    ptstr += str(high) + '|'
    ptstr += str(low) + '|\n'
    print (ptstr)
    
def acnt_get_acountinfo():
    ts = str(int((time.time()*1000))-3000)
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

    
def trade_get_CurrentOpenOrders():
    shastr = 'symbol=BTCUSDT'
    ts = str(int((time.time()*1000))-3000) 
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
    #print (r.text)
    resd = json.loads(r.text)
    
    if resd==[]:
        print ("No open orders!\n")
    
    for elm in resd:
        print ("Symbol  : " + elm.get("symbol"))
        print ("OrderID : " + str(elm.get("orderId")))
        print ("side    : " + elm.get("side"))
        print ("Price   : " + elm.get("price"))
        print ("origQty : " + elm.get("origQty"))
        print ("execQty : " + elm.get("executedQty"))
        print ("\n")
    
def trade_set_neworder(buysell,price,quantity):
    
    print ("Get Order Command : "+ buysell + "|" + price + "|" + quantity)
    print ("Confirm???!!!")
    input()

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
    if buysell=="Buy":
        shastr+= '&side=BUY'
    elif buysell=="Sell": 
        shastr+= '&side=SELL'
        
    shastr+= '&type=LIMIT'
    shastr+= '&timeInForce=GTC' 
    shastr+= '&quantity='
    shastr+= quantity
    shastr+= '&price='
    shastr+= price
    shastr+= '&recvWindow=5000'
    ts = str(int((time.time()*1000))-3000)
    shastr+= '&timestamp='
    shastr+= ts
    #print (shastr)
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
    
    print (ts)
    gn_get_server_time()



    headers = {"X-MBX-APIKEY":apikey}
    r = requests.post(url=reqstr,headers=headers)
    print (r.status_code)
    print (r.text)

    
def trade_cancel_order(orderID):  
    shastr = 'symbol=BTCUSDT'
    shastr+= '&orderId=' + (orderID)
    ts = str(int((time.time()*1000))-3000) 
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

    

'''

#Main Flow
key = b'MKkyxdhn2oPoHDKg4WIiIeOeOiz4LdFGBZCCwIpyj87MGG7ZAbAKPn0IWcCO2zaf' #sec key
apikey = b'XNm2yp6zfhDQ6ULqPtSZhFNzjsOz1pmOnSNOXhpta16yKuGKpRkzblgyg1zz37yi' #apikey

#acnt_get_acountinfo(apikey,key)
#orderID = trade_get_CurrentOpenOrders(apikey,key)
#trade_cancel_order(apikey,key,orderID)
#set_new_order(apikey,key)

while 1:
    #curt = time.localtime(time.time())
    #ptstr = str(curt.tm_year)+'-'+str(curt.tm_mon)+'-'+str(curt.tm_mday)+' '+str(curt.tm_hour)+':'+str(curt.tm_min)+':'+str(curt.tm_sec)
    #print (ptstr)
    
    md_get_24hrPriceChangeStatistics('BTCUSDT')
    time.sleep(1)
'''    

