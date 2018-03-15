import urllib
import urllib2
import os
import time
import traceback

REQUEST_FILE_NAME = "request_ip.txt"
RESULT_FILE_NAME = "result.txt"

def getIpList():
    ipList = []
    listFile = None
    
    try:
        if os.path.isfile(REQUEST_FILE_NAME):
            listFile = open(REQUEST_FILE_NAME, "r")
            while True:
                readLine = listFile.readline()
                if not readLine:
                    break
                
                ipList.append(readLine.replace("\n", ""))
        else:
            listFile = open(REQUEST_FILE_NAME, "w")
    except:
        traceback.print_exc()
    finally:
        listFile.close()
    
    return ipList

def getWhoisInfo(ipAddress):
    # IPv4 Address    Organization Name    Service Name    Address    Zip Code    Registration Date
    whoisInfo = {
        "ipAddress": ipAddress, 
        "orgName": "", 
        "serviceName": "", 
        "address": "",  
        "zipCode": "", 
        "regDate": "", 
    }
    url = "https://whois.kisa.or.kr/kor/whois/whois.jsc"
    data = urllib.urlencode({
        'query' : ipAddress, 
        'ip' : '163.152.126.248'
    })
    httpRequest = urllib2.Request(url=url, data=data)
    httpRequest.get_method = lambda: 'POST'
    connection = None
    try:
        connection = urllib2.urlopen(httpRequest, timeout=None)
        while True:
            readLine = connection.readline()
            if not readLine:
                break
            if readLine.find("IPv4 Address") >= 0:
                if whoisInfo["ipAddress"].__len__() > 0:
                    whoisInfo["ipAddress"] += ', '
                whoisInfo["ipAddress"] += readLine[readLine.find(": ")+2:-1]
            if readLine.find("Organization Name") >= 0:
                if whoisInfo["orgName"].__len__() > 0:
                    whoisInfo["orgName"] += ', '
                whoisInfo["orgName"] += readLine[readLine.find(": ")+2:-1]
            if readLine.find("Service Name") >= 0:
                if whoisInfo["serviceName"].__len__() > 0:
                    whoisInfo["serviceName"] += ', '
                whoisInfo["serviceName"] += readLine[readLine.find(": ")+2:-1]
            if readLine.find("Address") >= 0:
                if whoisInfo["address"].__len__() > 0:
                    whoisInfo["address"] += ', '
                whoisInfo["address"] += readLine[readLine.find(": ")+2:-1]
            if readLine.find("Zip Code") >= 0:
                if whoisInfo["zipCode"].__len__() > 0:
                    whoisInfo["zipCode"] += ', '
                whoisInfo["zipCode"] += readLine[readLine.find(": ")+2:-1]
            if readLine.find("Registration Date") >= 0:
                if whoisInfo["regDate"].__len__() > 0:
                    whoisInfo["regDate"] += ', '
                whoisInfo["regDate"] += readLine[readLine.find(": ")+2:-1]
    except:
        traceback.print_exc()
    finally:
        if connection != None:
            connection.close()
    return whoisInfo

if __name__ == '__main__':
    resultFile = None

    try:
        resultFile = open(RESULT_FILE_NAME, "w")
        
        resultFile.write("IPv4 Address\tOrganization Name\tService Name\tAddress\tZip Code\tRegistration Date\n")
        print "IPv4 Address\tOrganization Name\tService Name\tAddress\tZip Code\tRegistration Date\n"
        ipList = getIpList()
        for ipAddress in ipList:
            whoisInfo = getWhoisInfo(ipAddress)
            
            resultFile.write(
                whoisInfo["ipAddress"] + "$" + 
                whoisInfo["orgName"] + "$" +
                whoisInfo["serviceName"] + "$" +
                whoisInfo["address"] + "$" + 
                whoisInfo["zipCode"] + "$" +
                whoisInfo["regDate"] + "\n"
            )
            print(
                whoisInfo["ipAddress"] + "\t" + 
                whoisInfo["orgName"] + "\t" +
                whoisInfo["serviceName"] + "\t" +
                whoisInfo["address"] + "\t" + 
                whoisInfo["zipCode"] + "\t" +
                whoisInfo["regDate"] + "\n"
            )
            time.sleep(1)
    except:
        traceback.print_exc()
    finally:
        resultFile.close()