#  -*- coding:utf-8 -*-
#Does not work on Mac as Apple disable the SSLV3
__author__ = 'rwang'

import json
import logging
import logging.config

from publiclib import monkey_ssl
from publiclib import configuration
from publiclib import myglobal
#import configuration
import httpconnect
import ssl

ssl.wrap_socket = monkey_ssl.getssl()


class dingapi:
    def __init__(self):
        logging.config.fileConfig(myglobal.LOGGINGINI)
        self.__logger = logging.getLogger('dingapi')
        self.__c = configuration.configuration()
        self.__c.fileConfig(myglobal.CONFIGURATONINI)
        self.__h = httpconnect.httpconnect()
        self.__token = self.__genToken(self.__c.getValue("Ding","corpid"),self.__c.getValue("Ding","corpsecret"))


    def __genToken(self,corpID, corpSecret):
        url = "https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s" % (corpID, corpSecret)
        resp = self.__h.apiGet(url)
        return json.loads(resp)['access_token']

    def __listDepartment(self,accessToken):
        url = "https://oapi.dingtalk.com/department/list?access_token=%s" % (accessToken)
        return self.__h.apiGet(url)

    def __listUserInfo(self,accessToken):
        url = "https://oapi.dingtalk.com/user/list?access_token=%s" % (accessToken)
        return self.__h.apiGet(url)

    def __sendMsg(self,accessToken,jsonBody):
        url = "https://oapi.dingtalk.com/message/send?access_token=%s" % (accessToken)
        header = "Content-Type:application/json"
        resp =  self.__h.apiPost(url,jsonBody,header)
        return json.loads(resp)

    def dingMsg(self,msgContent,renew=False):
        #msgContent = u'中国ss'
        if renew:
           self.__token = self.__genToken(self.__c.getValue("Ding","corpid"),self.__c.getValue("Ding","corpsecret"))
        ISOTIMEFORMAT= '%Y-%m-%d %X'
        #content = time.strftime(ISOTIMEFORMAT, time.localtime())
        post_body = {"touser": "", \
                     "toparty": self.__c.getValue("Ding","partyid"), \
                     "agentid": self.__c.getValue("Ding","agentid"), \
                     "msgtype": "text", \
                     "text": {"content": msgContent}}

        resp =  self.__sendMsg(self.__token,json.dumps(post_body))
        #print resp
        #print resp['errcode']
        if resp['errcode'] == 40014:
            self.__logger.warn("AccessToken is expired")
            return self.dingMsg(msgContent,True)
        self.__logger.info(resp)
        if resp['errmsg'] == "ok":
            #print "True"
            return True
        else:
            return False
        #print resp['errmsg']
        #print resp

#d = dingapi()
#d.dingMsg("")