# -*-coding=utf-8-*-

from django.conf.urls import url
from views import *


urlpatterns = {
    url(r'startServer', startServer, name='start appiumServer and appcrawlerServer'),
    url(r'stopServer', stopServer, name='stop appiumServer'),
    url(r'stopServer', stopServer, name='stop all serveices'),
    url(r'runTest', runTest, name='start appcrawlerServer'),
    url(r'getAppiumList', getAppiumList, name='get AppiumServer information'),
    url(r'runAppiumSigle', runAppiumSigle, name='start appium for someone'),
    url(r'stopAppiumSigle', stopAppiumSigle, name='stop appium for someome'),
    url(r'startMinicap', startMinicap, name='start minicap server'),
    url(r'minicapView', minicapView, name='return minicap view'),
    url(r'stopMinicap', stopMinicap, name='stop minicap view'),
    # url(r'minitouchSocket', minitouchSocket, name='do minitouch action'),
    url(r'ctrlMobilePhone', ctrlMobilePhone, name='ctrl Mobile Phone'),
    url(r'sendkey', sendkey, name='send key to phone'),
    url(r'getDevicesXML', getDevicesXML, name='get xml and return html'),
    url(r'liDetail', liDetail, name='get xml li detail'),
    url(r'deleYml', deleYml, name='dele yaml'),
    url(r'uploadFile', uploadFile, name='uploadFile'),
    url(r'getXY', getXY, name='getXY'),
    url(r'getUDID', getUDID, name='getUDID'),
    url(r'getUDID', getUDID, name='getUDID')
    # url(r'testhtml', testhtml),
    # url(r'mytest', mytest, name='mytest'),
    # url(r'testStop', testStop),
}
