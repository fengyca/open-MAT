# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import startappium
import time, os
from .tasks import build_job
import UIAutomationView
# import DHSQL

# Create your views here.

# AppiumTrHTML = '<tr><td>%s</td><td>%s</td><td>%s</td><td style="color:%s">%s <span style="color:%s">%s</span></td><td id=%s><input type="button" class="btn btn-primary btn-xs" value="启动">  <input type="button" class="btn btn-warning btn-xs" value="终止"> </td><td id=%s>  <input type="button" class="btn btn-default btn-xs" value="投屏">  <input type="button" class="btn btn-danger btn-xs" value="关屏"></td></tr>'
AppiumTrHTML = '<tr><td>%s</td><td style="color:%s">%s <span style="color:%s">%s</span></td><td id=%s><input type="button" class="btn btn-primary btn-xs" value="启动">  <input type="button" class="btn btn-warning btn-xs" value="终止"> </td><td id=%s>  <input type="button" class="btn btn-default btn-xs" value="投屏">  <input type="button" class="btn btn-danger btn-xs" value="关屏"></td></tr>'


def getHTML(request):
    fileName = os.listdir(
        os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'appcrawler', 'crawlerServer'))
    for i in fileName:
        if i == 'appcrawler-2.1.3.jar':
            fileName.remove(i)
        else:
            pass
    return render(request, 'app_c.html', locals())


def getAppiumList(request):
    requestDevices = request.GET.get('devices')

    devicesJsonInfor, statusList = startappium.startDevicesJson()  # get devices of online information Json
    AppiumHTML = []
    mobleList = []
    for k, v in devicesJsonInfor.items():
        for i in statusList:
            if i[0] == k:
                if i[-1] == 'device':
                    minicap = startappium.minicap_is_runner(str(v['socketPort']))
                    if minicap == 'True':
                        minicapStatus = '投屏'
                        minicapColor = 'red'
                    elif minicap == 'False':
                        minicapStatus = '可投'
                        minicapColor = 'green'
                    else:
                        minicapStatus = '错误'
                        minicapColor = '#F75000'
                    if startappium.Appium_is_runner(str(v['port'])) == 'True':
                        status = '运行'
                        color = 'red'
                    else:
                        status = '空闲'
                        color = 'green'
                    # AppiumHTML.append(
                    #     AppiumTrHTML % (
                    #         str(v['name']), k, str(v['port']), color, status, minicapColor, minicapStatus, k, k))
                    if requestDevices == 'web':
                        AppiumHTML.append(
                            AppiumTrHTML % (
                                str(v['name']), color, status, minicapColor, minicapStatus, k, k))
                    elif requestDevices == 'mobiles':  # 移动端获取设备列表
                        mobleList.append({'devices': str(v['name']), 'status': minicapStatus, 'udid': k, 'port': str(v['socketPort']), 'mtsp':str(v['mtsp'])})
                    else:
                        pass
                else:
                    if requestDevices == 'web':
                        AppiumHTML.append(
                            AppiumTrHTML % (str(v['name']),  'red', '设备掉线了！！', '', '', k, k))
                    elif requestDevices == 'mobiles':
                        mobleList.append({'devices': str(v['name']), 'status': '设备掉线了！！', 'udid': k})
    data = startappium.is_runnnig(devicesJsonInfor)
    if requestDevices == 'web':
        return JsonResponse({'dataList': ''.join(AppiumHTML), 'dataServer': data})
    elif requestDevices == 'mobiles':
        return JsonResponse({'datas': mobleList})
    else:
        return JsonResponse({'data': False})


def startServer(request):
    """
    start all AppiumServer for online devices，A connection failed to return to False
    :param request: 
    :return: 
    """
    try:
        devicesJsonInfor, statusList = startappium.startDevicesJson()  # get devices of online information Json
        # startappium.startAppium(devicesJsonInfor)
        for k, v in devicesJsonInfor.items():
            build_job.delay(v["config"])
            time.sleep(1)
        return JsonResponse({'data': 'True'})
    except:
        return JsonResponse({'data': 'False'})


def stopServer(request):
    """
    Terminate all appium services
    :param request: 
    :return: something
    """
    try:
        startappium.stop_server()
        return JsonResponse({'data': 'True'})
    except:
        return JsonResponse({'data': 'False'})


def runTest(request):
    """
    Start compatibility test, start appcrawler service connection Appium
    :param request: 
    :return: 
    """
    try:
        project = request.GET.get('project')
        devicesJsonInfor, statusList = startappium.startDevicesJson()  # get devices of online information Json
        # startappium.runApp(project, devicesJsonInfor)

        path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'appcrawler', 'crawlerServer')
        appcrawlerPATH = os.path.join(path, 'appcrawler-2.1.3.jar')
        yamlPATH = os.path.join(path, project, 'config.yml')
        for k, v in devicesJsonInfor.items():
            reportPATH = os.path.join(path, project, 'report',
                                      'log%s%s' % (str(time.strftime("%Y-%m-%d-%H-%M-%S")), str(v["port"])))
            os.makedirs(reportPATH)  # 创建文件夹
            cmd = 'java -jar %s -u %s -c %s -o %s'  # 命令行启动
            build_job.delay(cmd % (appcrawlerPATH, str(v["port"]), yamlPATH, reportPATH))
            time.sleep(1)
        return JsonResponse({'data': 'True'})
    except:
        return JsonResponse({'data': 'False'})


def runAppiumSigle(request):
    udid = request.GET.get('udid')
    devicesList = startappium.getYaml()
    config = devicesList[udid]['config']
    status = startappium.Appium_is_runner(devicesList[udid]['port'])
    if status == 'True':
        return JsonResponse({'data': 'False'})
    else:
        try:
            build_job.delay(config)
        except Exception as e:
            print str(e)
            return JsonResponse({'data': 'False'})
        return JsonResponse({'data': 'True'})


def stopAppiumSigle(request):
    udid = request.GET.get('udid')
    devicesList = startappium.getYaml()
    port = devicesList[udid]['port']
    status = startappium.killPortPID(port)
    return JsonResponse({'data': status})


def startMinicap(request):
    udid = request.GET.get('udid')
    test = request.GET.get('test')
    devicesList = startappium.getYaml()

    devicesName = devicesList[udid]['name']

    pcPort = devicesList[udid]['pcPort']
    socketPort = devicesList[udid]['socketPort']
    # 本地端口映射minitouch
    minitouchPort = devicesList[udid]['minitouchPort']
    mtsp = devicesList[udid]['mtsp']
    if test == 'True':
        minicap = startappium.minicap_is_runner(socketPort)
        if minicap == 'True':
            return JsonResponse({'data': 'False'})
        else:
            return JsonResponse({'data': 'True'})
    else:
        windowSize = startappium.getOutput(
            "adb -s %s shell dumpsys window | grep -Eo 'init=\d+x\d+' | head -1 | cut -d= -f 2" % udid)

        cpu = startappium.getOutput("adb -s %s shell getprop ro.product.cpu.abi | tr -d '\r'" % udid)
        level = startappium.getOutput("adb -s %s shell getprop ro.build.version.sdk | tr -d '\r'" % udid)
        cpuPath, levelPath, appPath, minitouchPath, touchJsPath = startappium.returnPath(cpu, level)
        try:
            # 先判断文件是否存在，不存在则push文件入手机
            if startappium.isExist(udid, 'minicap'):
                startappium.Foo("adb -s %s push %s /data/local/tmp" % (udid, cpuPath))
                startappium.Foo("adb -s %s push %s /data/local/tmp" % (udid, levelPath))
            if startappium.isExist(udid, 'minitouch'):
                startappium.Foo("adb -s %s push %s /data/local/tmp" % (udid, minitouchPath))
            # 异步启动minicap
            build_job.delay("adb -s %s shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P %s@%s/0" % (
                udid, windowSize, windowSize))
            startappium.Foo("adb -s %s forward tcp:%s localabstract:minicap" % (udid, pcPort))  # 端口映射
            build_job.delay("adb -s %s shell /data/local/tmp/minitouch" % (udid))
            startappium.Foo("adb -s %s forward tcp:%s localabstract:minitouch" % (udid, minitouchPort))  # 端口映射
            build_job.delay("node %s %s %s" % (appPath, socketPort, pcPort))
            build_job.delay("node %s %s %s" % (touchJsPath, minitouchPort, mtsp))
            time.sleep(4)
        except Exception as e:
            print str(e)
            return JsonResponse({'data': 'Error'})
        return JsonResponse(
            {'data': 'True', 'port': str(socketPort), 'udid': str(udid), 'name': str(devicesName), 'touchPort': str(minitouchPort),
             'mtsp': str(mtsp)})


def minicapView(request):
    port = request.GET.get('PORT')
    touch = request.GET.get('touch')
    udid = request.GET.get('udid')
    mtsp = request.GET.get('mtsp')
    return render(request, 'myframe.html', locals())


def stopMinicap(request):
    udid = request.GET.get('udid')
    devicesList = startappium.getYaml()

    pcPort = devicesList[udid]['pcPort']
    socketPort = devicesList[udid]['socketPort']
    mtsp = devicesList[udid]['mtsp']
    minitouchPort = devicesList[udid]['minitouchPort']

    try:
        # startappium.killPortPID(pcPort)
        # startappium.killPortPID(minitouchPort)

        startappium.killPortPID(socketPort)
        startappium.killPortPID(mtsp)
        # 杀掉minicap，minitouch
        startappium.stopShellPID(udid, 'minicap')
        startappium.stopShellPID(udid, 'minitouch')

        startappium.removeForward(udid, pcPort)
        startappium.removeForward(udid, minitouchPort)
        pc = startappium.getOutput('lsof -i:%s' % pcPort)
        socket = startappium.getOutput('lsof -i:%s' % socketPort)
        if pc == '' and socket == '':
            return JsonResponse({'data': 'True'})
        else:
            # startappium.killPortPID(pcPort)
            # startappium.killPortPID(minitouchPort)

            startappium.killPortPID(socketPort)
            startappium.killPortPID(mtsp)
            # 杀掉minicap，minitouch
            startappium.stopShellPID(udid, 'minicap')
            startappium.stopShellPID(udid, 'minitouch')

            startappium.removeForward(udid, pcPort)
            startappium.removeForward(udid, minitouchPort)
            socket = startappium.getOutput('lsof -i:%s' % socketPort)
            if socket == '':
                return JsonResponse({'data': 'True'})
            else:
                return JsonResponse({'data': 'False'})
    except Exception as e:
        print e
        return JsonResponse({'data': 'Error'})


# def minitouchSocket(request):
#     tag = request.GET.get('tag')
#     port = request.GET.get('port')
#     sx = request.GET.get('sx')
#     sy = request.GET.get('sy')
#     ex = request.GET.get('ex')
#     ey = request.GET.get('ey')
#
#     # 声明协议类型,同时生成socket连接对象
#     client = socket.socket()
#     client.connect(('localhost', int(port)))
#
#     msg = '%s 0 %s %s 50\n' % ('d', sx, sy)
#     client.send(msg.encode('utf-8'))
#     client.send('c\n'.encode('utf-8'))
#
#     if tag == 'click':
#         pass
#     elif tag == 'swipe':
#         linex, liney = startappium.make_swipe_line(int(sx), int(sy), int(ex), int(ey))
#         for i in range(10, len(linex)):
#             x = linex[i]
#             y = liney[i]
#             msg = 'm 0 %s %s 50\n' % (int(x), int(y))
#             client.send(msg.encode('utf-8'))
#             client.send('c\n'.encode('utf-8'))
#     client.send('u 0\n'.encode('utf-8'))
#     client.send('c\n'.encode('utf-8'))
#
#     client.close()
#     return JsonResponse({'data': 'True'})


def ctrlMobilePhone(request):
    tag = request.GET.get('tag')
    udid = request.GET.get('udid')

    if tag == 'caidan':
        key = '1'
    elif tag == 'home':
        key = '3'
    elif tag == 'fanhui':
        key = '4'
    elif tag == 'dianyuan':
        key = '26'
    else:
        key = None

    if key:
        startappium.Foo('adb -s %s shell input keyevent %s' % (udid, key))
        return JsonResponse({'data': 'True'})
    else:
        return JsonResponse({'data': 'False'})


def sendkey(request):
    key = request.GET.get('key')
    udid = request.GET.get('udid')
    if key == '67' or key == '66' or key == '62':
        build_job.delay('adb -s %s shell input keyevent %s' % (udid, key))
    else:
        build_job.delay('adb -s %s shell input text %s' % (udid, key))
    return JsonResponse({'data': 'True'})


def getDevicesXML(request):
    udid = request.GET.get('udid')
    oldname = request.GET.get('name')
    if oldname == '':  # 删除老旧的yml文件
        pass
    else:
        try:
            oldPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                                   'appcrawler/UIxml/%s.yml' % str(oldname))
            os.remove(oldPath)
        except Exception as e:
            print e
    # 生产新的文件
    name = int(time.time())
    file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                             'appcrawler/UIxml/%s.xml' % str(name))
    startappium.getOutput('adb -s %s shell rm -r /sdcard/window_dump.xml' % (udid))  # 删除旧文件
    startappium.getOutput('adb -s %s shell uiautomator dump /sdcard/window_dump.xml' % (udid))
    startappium.getOutput('adb -s %s pull %s %s' % (udid, '/sdcard/window_dump.xml', file_name))
    data = UIAutomationView.getXmlData(file_name, name)
    return JsonResponse({'data': data, 'name': name})


def liDetail(request):
    id = request.GET.get('id')
    name = request.GET.get('name')
    bit = request.GET.get('bit')
    file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                             'appcrawler/UIxml/%s.yml' % str(name))

    detailDict = UIAutomationView.getXmlDetail(id, file_name)
    tbList = []
    tbHTML = "<tr><td>%s</td><td>%s</td></tr>"
    for k, v in detailDict.items():
        tbList.append(tbHTML % (k, v))
    try:
        string = detailDict['bounds']
        sx, sy, ex, ey = UIAutomationView.getXY(string)
        sx = int(int(sx) / int(bit))
        sy = int(int(sy) / int(bit))
        ex = int(int(ex) / int(bit))
        ey = int(int(ey) / int(bit))
        lenx = ex - sx
        leny = ey - sy
    except Exception as e:
        sx = sy = lenx = leny = 0
        print e

    return JsonResponse({'data': ''.join(tbList), 'id': id, 'x': sx, 'y': sy, 'lenx': lenx, 'leny': leny})


def deleYml(request):
    try:
        name = request.GET.get('name')
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                            'appcrawler/UIxml/%s.yml' % str(name))
        os.remove(path)
        return JsonResponse({'data': 'True'})
    except:
        return JsonResponse({'data': 'Error'})


def uploadFile(request):
    upFile = request.FILES.get('file')
    udid = request.POST.get('udid')
    if str(upFile.name).split('.')[-1] != 'apk':
        return JsonResponse({'data': 'False'})
    else:
        name = str(upFile.name).split('.')[0]
        if '(' in name:
            name = name.replace('(', '')
        if ')' in name:
            name = name.replace(')', '')

    path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                        'appcrawler/UIapp/%s' % str('%s.apk' % (name)))

    with open(path, 'wb') as new_file:
        for chunk in upFile.chunks():
            new_file.write(chunk)

    time.sleep(1)

    # build_job.delay('adb -s %s install %s' % (udid, path))

    os.system('adb -s %s install -r %s' % (udid, path))
    time.sleep(3)
    # os.remove(path)
    return JsonResponse({'data': 'True'})


# def testhtml(request):
#     return render(request, 'post_result.html')
#
#
# def mytest(request):
#     a = request.GET.get('a')
#     # b = request.GET.get('b')
#     res = build_job.delay(a)
#     data = res.id
#     status = res.status
#     return JsonResponse({'data': data, 'status': status})
#
#
# def testStop(request):
#     task_id = request.GET.get('id')
#     the_task = build_job.AsyncResult(task_id)
#     the_task.revoke(terminate=True, signal='SIGKILL')
#     return JsonResponse({'data': ''})

def getXY(request):
    udid = request.GET.get('udid')
    windowSize = startappium.getOutput(
        "adb -s %s shell dumpsys window | grep -Eo 'init=\d+x\d+' | head -1 | cut -d= -f 2" % udid)
    return JsonResponse({'data': windowSize})

def getUDID(request):
    udid = request.GET.get('udid')
    devicesList = startappium.getYaml()

    AppiumPort = devicesList[udid]['port']
    return JsonResponse({'data': AppiumPort})


# def YDover(request):
#     """越过云贷扫脸扫身份证"""
#     udid = request.GET.get('udid')
#     phone = request.GET.get('phoneNum')
#
#     reslut, tag = DHSQL.insertMYSQL(phone=phone, udid=udid)
#     return JsonResponse({'data': reslut, 'tag': tag})
