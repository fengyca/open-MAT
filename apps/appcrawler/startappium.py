# coding:utf-8
from multiprocessing import Pool
import os
import yaml
import requests
import commands
import time


def Foo(cmd):
    os.system(cmd)
    return cmd


def getOutput(cmd):
    return commands.getoutput(cmd)


def Bar(arg):
    print arg


# def startAppium(deviceJson):
#     pool = Pool(len(deviceJson))  # 进程池
#     for k, v in deviceJson.items():
#         pool.apply_async(func=Foo, args=(v["config"],),
#                          callback=Bar)  # func子进程执行完后，才会执行callback，否则callback不执行（而且callback是由父进程来执行了）
#     pool.close()
#     pool.join()  # 主进程等待所有子进程执行完毕。必须在close()或terminate()之后。


def stop_server():
    """stop the appium server
    selenium_appium: appium selenium
    :return:
    """
    os.system("kill -9 $(ps -ef|grep node |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')")
    os.system("kill -9 $(ps -ef|grep adb |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')")


def Appium_is_runner(port):
    """
    check only one port AppiumServer
    :param port: Appium port
    :return: string True or False
    """
    response = None
    url = " http://127.0.0.1:" + str(port) + "/wd/hub" + "/status"
    try:
        response = requests.get(url, timeout=5)

        if str(response.status_code).startswith("2"):
            return 'True'
        else:
            return 'False'
    except:
        return 'False'
    finally:
        if response:
            response.close()


def is_runnnig(deviceJson):
    """
    Determine whether server is running
    check all online devices
    :return:True or False
    """
    response = None
    # no online devices return false
    if deviceJson == {}:
        return 'False'
    # online devices if has one error return false  when all pass return true
    for k, v in deviceJson.items():
        url = " http://127.0.0.1:" + str(v["port"]) + "/wd/hub" + "/status"
        try:
            response = requests.get(url, timeout=5)

            if str(response.status_code).startswith("2"):
                pass
            else:
                return 'False'
        except:
            return 'False'
        finally:
            if response:
                response.close()
    return 'True'


def getYaml():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'appcrawler', 'deviceYaml.yml')
    with open(path, 'r') as t:
        deviceJson = yaml.load(t)
    return deviceJson


def returnPath(cpu, level):
    cpuPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'appcrawler/minicap/bin', cpu,
                           'minicap')
    minitouchPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'appcrawler/minitouch',
                                 cpu,
                                 'minitouch')
    levelPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                             'appcrawler/minicap/libs', 'android-%s' % level, cpu, 'minicap.so')
    appPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                           'appcrawler/minicap/example/app.js')
    touchJsPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'appcrawler/minitouch',
                               'minitouch.js')
    return cpuPath, levelPath, appPath, minitouchPath, touchJsPath


def getDevices():
    """
    get devices list
    :return: devices list
    """

    device = commands.getoutput('adb devices')
    s = device.replace('List of devices attached', '').split('\n')
    deviceList = []
    statusList = []
    for i in s:
        if i == '':
            pass
        else:
            deviceList.append(i.split('\t')[0])
            # eg:[['LE67A06310079608', 'offline'],['LE67A06310079608', 'offline']]
            statusList.append(i.split('\t'))

    return deviceList, statusList


def startDevicesJson():
    """
    get onLine devices information, and return json
    :return: SDJ
    """
    deviceJson = getYaml()
    onLineDevices, statusList = getDevices()
    SDJ = {}
    if onLineDevices != []:
        for k, v in deviceJson.items():
            for i in onLineDevices:
                if k == i:
                    SDJ.__setitem__(k, v)
                else:
                    pass
    return SDJ, statusList


# def runApp(project, deviceJson):
#     path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'appcrawler', 'crawlerServer')
#     appcrawlerPATH = os.path.join(path, 'appcrawler-2.1.3.jar')
#     yamlPATH = os.path.join(path, project, 'config.yml')
#     pool = Pool(len(deviceJson))
#     for k, v in deviceJson.items():
#         reportPATH = os.path.join(path, project, 'report',
#                                   'log%s%s' % (str(time.strftime("%Y-%m-%d-%H-%M-%S")), str(v["port"])))
#         os.makedirs(reportPATH)  # 创建文件夹
#         cmd = 'java -jar %s -u %s -c %s -o %s'  # 命令行启动
#         pool.apply_async(func=Foo, args=(cmd % (appcrawlerPATH, str(v["port"]), yamlPATH, reportPATH),), callback=Bar)
#     pool.close()
#     pool.join()


def killPortPID(port):
    try:
        commands.getoutput("lsof -n -i:%s | grep LISTEN | awk '{print $2}' | xargs kill" % port)
        return "True"
    except:
        return "False"


def removeForward(udid, port):
    try:
        commands.getoutput('adb -s %s forward --remove tcp:%s' % (udid, port))
        return 'True'
    except:
        return 'False'


def stopShellPID(udid, tap):
    try:
        output = commands.getoutput('adb -s %s shell ps|grep /data/local/tmp/%s' % (udid, tap))
        pid = ''
        if output:
            l = output.split(' ')
            for i in l:
                if i:
                    pass
                else:
                    l.remove(i)
            pid = l[1]
        if pid:
            commands.getoutput('adb -s %s shell kill %s' % (udid, pid))
            return 'True'
        else:
            return 'False'
    except:
        return 'False'


def isExist(udid, tap):
    output = commands.getoutput('adb -s %s shell ls /data/local/tmp/%s' % (udid, tap))
    l = output.split('/')
    if tap + '\r' in l:
        # 存在返回False
        return False
    else:
        # 不存在返回True
        return True


def minicap_is_runner(port):
    """
    check minicap is running or not
    :param port: app.js port
    :return: True is running, Error is port be occupied, False is no running
    """
    a = commands.getoutput('lsof -i:%s' % port)
    if a:
        # b = a.split('\n')[-1].split(' ')
        # if b[0] == 'node':
        #     return 'True'
        # else:
        #     return 'Error'
        return 'True'
    else:
        return 'False'


if __name__ == '__main__':
    name = 'sss_()'
    if '(' in name:
        name = name.replace('(', '')
        print name

