import requests
import re
import datetime
import time

adminuser = "useradmin"
adminpwd = "******"
url = "http://192.168.1.1/cgi-bin/luci"
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"

#凌晨四点
nRefresTime = 4

class TimeMgr:
    #是否新的一天
    bIsNowDay = False
    #今天的日期
    nCurDay = 0

    def __init__(self):
        self.bIsNowDay = True
        self.nCurDay = datetime.datetime.now().day

    def Check(self):
        if self.bIsNowDay:
            if datetime.datetime.now().hour == nRefresTime:
                self.bIsNowDay = False
                return True
        else:
            if datetime.datetime.now().day != self.nCurDay:
                self.nCurDay = datetime.datetime.now().day
                self.bIsNowDay = True

        return False

def RestartRouter():
    session = requests.Session()
    respons = session.post(url, data={"username":adminuser,"psd":adminpwd}, headers={"User-Agent":agent, "Referer":url},)

    rtoken = re.search("token: \'([a-z0-9]*)\'", respons.content.decode(), re.I)
    if rtoken == None:
        return False

    token = rtoken.group(1)
    print("token="+token)

    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    if cookies.get("sysauth") == None:
        return False

    sysauth="sysauth="+cookies["sysauth"]
    print(sysauth)

    restart_url = "http://192.168.1.1/cgi-bin/luci/admin/reboot"
    print(session.post(restart_url, data={"token":token}, headers={"User-Agent":agent, "Referer":url,"Cookie":sysauth},))

    return True

timemgr = TimeMgr()
print("启动=>"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
while True:
    if timemgr.Check():
        RestartRouter()
        print("重启=>"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print("检测=>"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    time.sleep(600)
