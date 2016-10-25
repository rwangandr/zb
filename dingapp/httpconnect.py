#  -*- coding:utf-8 -*-
#Does not work on Mac as Apple disable the SSLV3

__author__ = 'rwang'

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("../")

import logging
import logging.config
import time
from publiclib import myglobal
from publiclib import monkey_ssl
from publiclib import configuration
import ssl

ssl.wrap_socket = monkey_ssl.getssl()
import urllib2

__GET__ = 0
__POST__ = 1

class httpconnect:
    def __init__(self):
        logging.config.fileConfig(myglobal.LOGGINGINI)
        self.__logger = logging.getLogger('httpconnect')
        c = configuration.configuration()
        c.fileConfig(myglobal.CONFIGURATONINI)
        self.__RETRY_TIMES__ = int(c.getValue("Runtime","retry_times"))
        self.__PAGE_INTERVAL__ = int(c.getValue("Runtime","page_interval"))

    def __http_post(self,url,body,header):
        #jdata = json.dumps(body)             # 对数据进行JSON格式化编码
        #print jdata
        strResult = "{}"
        tried = 1
        #print body.decode('utf-8')
        req = urllib2.Request(url, body)
        if header != "":
            req.add_header(header.split(":")[0],header.split(":")[1])
        while True:
            try:
                response = urllib2.urlopen(req)
                strResult = response.read()
                break
            except urllib2.URLError,e:
                self.__logger.error(e.reason)
                tried = tried + 1
                if tried > self.__RETRY_TIMES__:
                    break
                time.sleep(self.__PAGE_INTERVAL__)
                self.__logger.warn("Retry %i" %tried)
        return strResult

    def __http_get(self,url):
        strResult = "{}"
        tried = 1
        req = urllib2.Request(url)
        while True:
            try:
                response = urllib2.urlopen(req)
                strResult = response.read()
                break
            except urllib2.URLError,e:
                self.__logger.error(e.reason)
                tried = tried + 1
                if tried > self.__RETRY_TIMES__:
                    break
                time.sleep(self.__PAGE_INTERVAL__)
                self.__logger.warn("Retry %i" %tried)
        return strResult

    def apiGet(self,url):
        data =  self.__http_get(url)
        #print data
        return data

    def apiPost(self,url,body,header):
        data =  self.__http_post(url,body,header)
        return data

#url = "https://oapi.dingtalk.com/user/list?access_token=e4a4d59e12aa31f0b75738eb8dbbc22a&department_id=20139001"
#h = httpconnect()
#print h.apiGet(url)