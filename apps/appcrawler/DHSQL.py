# coding:utf-8
import base64
import commands
import hashlib
import random
import time

import MySQLdb
import rsa
import os

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'appcrawler', 'RSApem')


# 云贷越过身份证扫描以及扫脸认证的阶段，使用插入数据库的方式搞定

def getIDcard():
    """随机生产身份证号码"""
    ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    pro = {
        0: '11',
        1: '12',
        2: '13',
        3: '14',
        4: '15',
        5: '21',
        6: '22',
        7: '23',
        8: '31',
        9: '32',
        10: '33',
        11: '34',
        12: '35',
        13: '36',
        14: '37',
        15: '41',
        16: '42',
        17: '43',
        18: '44',
        19: '45',
        20: '46',
        21: '50',
        22: '51',
        23: '52',
        24: '53',
        25: '54',
        26: '61',
        27: '62',
        28: '63',
        29: '64',
        30: '65',
    }
    LAST = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
            '10': '2'}
    t = time.localtime()[0]
    x = '%02s%02s%02s%04s%02s%02s%03s' % (pro[random.randint(0, 30)],
                                          random.randint(10, 99),
                                          random.randint(10, 99),
                                          random.randint(t - 80, t - 18),
                                          random.randint(01, 12),
                                          random.randint(01, 28),
                                          random.randint(001, 999))
    x = x.replace(' ', '0')
    y = 0
    for i in range(17):
        y += int(x[i]) * ARR[i]
    b = y % 11
    return '%s%s' % (str(x), LAST[str(b)])


def MD5Safe(string):
    """MD5加密"""
    hash = hashlib.md5()
    hash.update(bytes(string))
    return hash.hexdigest()

def getName():
    a1 = ['张', '金', '李', '王', '赵', '冯', '杨', '薛', '王', '李', '钱', '孙', '李', '刘', '周', '邓', '胡', '段', '陈']
    a2 = ['玉', '明', '龙', '芳', '军', '玲', '溢', '秀', '娅', '可', '到', '是', '在', '哥', '呃', '无', '投', '好', '天', '另', '领', '包',
          '吧']
    a3 = ['', '立', '玲', '靠', '国', '', '超', '哦', '好', '卡', '里', '量', '零', '笆', '与', '值', '因', '大', '二', '斯', '乐', '无',
          '爱', '搜', '神']
    name = random.choice(a1) + random.choice(a2) + random.choice(a3)
    return name

def RSASafe(string):
    # RSA加密解密，按照长度来区分，长度超过20即是解密，小于就是加密
    publicPath = os.path.join(path, 'public.pem')
    with open(publicPath, 'r+') as f:  # 公钥加密
        publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(f.read().encode())
    privatePath = os.path.join(path, 'private.pem')
    with open(privatePath, 'r+') as f:  # 私钥解密
        privateKey = rsa.PrivateKey.load_pkcs1(f.read().encode())

    if len(string) >= 20:
        cryptedMessage = rsa.decrypt(base64.b64decode(string), privateKey)  # 解密
        cryptedMessage = cryptedMessage.decode()
    else:
        message = string.encode()  # 加密
        cryptedMessage = base64.b64encode(rsa.encrypt(message, publicKey))
    return cryptedMessage


def Myconnect(ip, port, username, password, db):
    # 连接mysql数据库
    PTparams = dict(
        host=ip,
        port=int(port),
        db=db,
        user=username,
        passwd=password,
        charset='utf8mb4',  # 编码要加上，否则可能出现中文乱码问题
    )
    cnx = MySQLdb.connect(**PTparams)
    return cnx


def insertMYSQL(phone, udid):
    # 平台8511查询uid
    cnx = Myconnect('172.30.3.78', '3310', 'yjsdata', 'PtSjKmMkFwY666', 'yyfax_user')  # 连接
    con = cnx.cursor()  # 游标
    try:
        UIDsql = "SELECT user_id FROM user_info WHERE phone = '%s'" % phone
        con.execute(UIDsql)
        uid = con.fetchall()[-1][-1]
    except:
        return '输入的电话号码误！', '0'
    finally:
        con.close()
        cnx.close()

    # 查询mac地址
    MAC = commands.getoutput('adb -s %s shell cat /sys/class/net/wlan0/address' % udid)
    if MAC.split(' ')[0] == 'error:':
        return '输入的udid有误', '0'
    else:
        MACid = MAC.replace(':', '')

    # 插入扫描身份证
    try:
        idcnx = Myconnect('172.29.2.15', '3306', 'yylendingdata', 'Aa!123456', 'lasdb')
        idcon = idcnx.cursor()  # 游标
        imageID = '10004207228' + str(random.randint(000000001, 791426686))

        imagePath = os.path.join(path, 'image.txt')
        with open(imagePath, 'r+') as f:
            image = f.read().encode()
        newtime = time.strftime('%Y-%m-%d %H:%M:%S')


        # 数据
        user_name = getName()
        idcard = getIDcard()
        identity = RSASafe(idcard)
        sign_identity = MD5Safe(idcard)


        idsql3 = """INSERT INTO l_customer_image_info (image_id, platform_user_id, image, image_source, create_time, last_update_time, image_system_id)
                    VALUES( '%s', '%s', '%s', '0', '%s', '%s', '')""" % (
            imageID, uid, image, str(newtime), str(newtime))
        idcon.execute(idsql3)

        idsql4 = """INSERT INTO l_customer_sface_info (sface_id,platform_user_id,is_passed,face_verify_time,net_photo_id,id_score, face_score,verify_count,device_id,create_time,last_update_time) 
                    VALUES ('%s', '%s','1', '%s', '%s', '90','50','1','%s', '%s','%s')""" % (
            imageID, uid, str(int(round(time.time() * 1000))), imageID, MACid, str(newtime), str(newtime))
        idcon.execute(idsql4)

        idsql2 = """UPDATE l_customer_info SET identity='%s', sface_id='%s', sign_identity='%s',user_name='%s',idcard_office='南山区公安局',idcard_start_date='20110806',idcard_end_date='20210806' 
                    WHERE platform_user_id='%s'""" % (identity, imageID, sign_identity, user_name, uid)
        idcon.execute(idsql2)

        idcnx.commit()  # 提交

        idcnx.close()
        idcon.close()
        return '越过成功！！', '1'
    except:
        return '系统执行错误，请联系管理员！', '0'


if __name__ == '__main__':

    cnx = Myconnect('172.30.3.78', '3310', 'yjsdata', 'PtSjKmMkFwY666', 'yyfax_user')  # 连接
    con = cnx.cursor()  # 游标

    UIDsql = "SELECT user_id FROM user_info WHERE phone = '%s'" % '13245678901'
    con.execute(UIDsql)
    uid = con.fetchall()[-1][-1]
    print uid
    con.close()
    cnx.close()

    idRSA = RSASafe('6222980537530885')
    print idRSA
    phone = RSASafe('13245678901')
    print phone


    sql6 = """INSERT INTO authentication_info (user_id,
                                               business_id,
                                               fuiou_id,
                                               cert_type,
                                               bank_code,
                                               bank_name,
                                               card_no,
                                               card_no_cip,
                                               bank_phone,
                                               bank_phone_cip,
                                               fuiou_phone,
                                               fuiou_phone_cip,
                                               auth_state,
                                               card_state,
                                               frozen_state,
                                               frozen_time,
                                               remark,
                                               auth_time,
                                               update_time) 
                                      VALUES ('U020033609',
                                              'RE0720000000000000000009999173',
                                              '15800099214', '0', '1001', '中国工商银行',
                                              '', '%s', 'null', '%s',
                                              'null', '%s', '1', '1', '0', 'null',
                                              'null', '2017-10-06 08:43:20', '2017-10-06 08:46:24')""" % (idRSA, phone, phone)

    sql7 = "SELECT * FROM yyfax_user.authentication_info WHERE user_id= 'U020033609'"


    # 银行卡验证数据库
    cnx = Myconnect('172.30.3.78', '3306', 'yjsdata', 'PtSjKmMkFwY666', 'yyfax_user')  # 连接
    con = cnx.cursor()  # 游标

    con.execute(sql7)
    print con.fetchall()
    cnx.commit()
    con.close()
    cnx.close()



