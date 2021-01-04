#coding=utf-8
import sys
import time
import json
import binance as ba
import huobi as hb


def show_help():
    print ("Usage: Demo [-h] [ba/hb] [instruction]\n")

    print ("instruction:\n")
    print ("\tGetSiteStatus or gss\n")
    print ("\tGetServerTime or gst\n")
    print ("\tGetAccountSnap or gas\n")
    print ("\tGet24hPriceInfo [-t] or gpi\n")
    print ("\tGetCurrentOpenOrders or gco\n")
    print ("\tSetNewOrder or sno [Buy/Sell] [Price] [Quantity(in USDT]\n")
    print ("\tCancelOrder or co\n")

def ba_process(argv):
    cmd = argv[2]
    
    if cmd=="GetSiteStatus" or cmd=="gss":
        ba.gn_get_site_status()
    elif cmd=="GetServerTime" or cmd=="gst":
        ba.gn_get_server_time()
    elif cmd=="GetAccountSnap" or cmd=="gas":
        ba.acnt_get_acountinfo()
    elif cmd=="Get24hPriceInfo" or cmd=="gpi":
        ba.md_get_24hrPriceChangeStatistics('BTCUSDT')
        if len(argv)==4 and argv[3]=="-t":
            while 1:
                ba.md_get_24hrPriceChangeStatistics('BTCUSDT')
                time.sleep(1)
    elif cmd=="SetNewOrder" or cmd=="sno":
        if len(argv)<6:
            print ("Lack of parameters Eg, SetNewOrder [Buy/Sell] [Price] [Quantity(in BTC]\n")
        else :
            #print ("Set Order\n")
            ba.trade_set_neworder(argv[3],argv[4],argv[5])
    elif cmd=="CancelOrder" or cmd=="co":
        if len(argv)<4:
            print ("Lack of parameters Eg, CancelOrder orderID\n")
        else:
            ba.trade_cancel_order(argv[3])
    elif cmd=="GetCurrentOpenOrders" or cmd=="gco":
        ba.trade_get_CurrentOpenOrders()
    else :
        print ("Invalid Command")

def hb_process(argv):
    print ("huobi")
    print (argv[2])

#Main Flow
#print ("Input arg numer is :", len(sys.argv))
#print ('Input arg is :', str(sys.argv))

if len(sys.argv)<2:
    print ("Wrong input, please use -h to get help info")
elif sys.argv[1] == "-h":
    show_help()
elif sys.argv[1] == "ba":
    ba_process(sys.argv)
elif sys.argv[1] == "hb":
    hb_process(sys.argv)



while 0:
    hb.get_24hrPriceChangeStatistics('btcusdt')
    ba.md_get_24hrPriceChangeStatistics('BTCUSDT')
    time.sleep(1)


#acnt_get_acountinfo(apikey,key)
#orderID = trade_get_CurrentOpenOrders(apikey,key)
#trade_cancel_order(apikey,key,orderID)
#set_new_order(apikey,key)

while 0:
    #curt = time.localtime(time.time())
    #ptstr = str(curt.tm_year)+'-'+str(curt.tm_mon)+'-'+str(curt.tm_mday)+' '+str(curt.tm_hour)+':'+str(curt.tm_min)+':'+str(curt.tm_sec)
    #print (ptstr)
    
    ba.md_get_24hrPriceChangeStatistics('BTCUSDT')
    #ba.gn_get_accountSnapshot()
    time.sleep(5)
    

