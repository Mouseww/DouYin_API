# from playwright.sync_api import sync_playwright, TimeoutError
import requests
import time
import json
import hashlib
import base64
import re
import random

# msedge_exe_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
# msedge_exe_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def get_ua():
    # 常见浏览器名称和引擎
    browsers = ["Mozilla", "Chrome","Firefox", "Edge"]
    # 随机选择浏览器和引擎
    browser = random.choice(browsers)
    # 生成随机版本号
    major_version = random.randint(1, 99)
    minor_version = random.randint(0, 9)
    patch_version = random.randint(0, 9)
    version = f"{major_version}.{minor_version}.{patch_version}"
    # 生成User-Agent字符串
    def ran1(): return random.choice(['7.0', '10.0', '11.0'])
    def ran2(): return random.randint(500, 600)
    def ran3(): return random.randint(111,120)
    def ran4(): return random.randint(0,99)
    def ran5(): return random.randint(0,9)
    def ran6(): return random.choice(["Win32", "Win64", "x86_64"])
    user_agent = f'Mozilla/{ran1()} (Windows NT 10.0; {ran6()}; x64) AppleWebKit/{ran2()}.{ran4()}  Chrome/{ran3()}.{ran4()}.{ran4()}.{ran4()} Safari/{ran2()}.{ran4()}'
    print(user_agent)
    return user_agent
# playwright 得到cookie
# def get_cookie(ua):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(executable_path=msedge_exe_path, headless=False)
#         # 隐藏headless
        
#         with browser.new_context(user_agent=ua) as context:
#             page = context.new_page()           
            
#             page.goto('https://www.douyin.com')
#             # page.goto('https://www.douyin.com/user/MS4wLjABAAAAtHTi3Xy4jS-A3cnFBi8cGF_kUxEWIns3_Ge4JuklXpA')
#             try:
#                 # 键盘下键
#                 page.wait_for_selector('//div[@class = "dy-account-close"]')
#                 page.click('//div[@class="dy-account-close"]')
#                 time.sleep(1)
#                 page.keyboard.press('ArrowDown')
#                 time.sleep(0.5)
#                 page.keyboard.press('ArrowDown')
#                 time.sleep(0.5)
#                 page.keyboard.press('ArrowDown')
#                 # page.wait_for_selector('//*[@id="douyin-right-container"]//ul/li[1]/div/a/div', timeout=100000)
#                 # element = page.query_selector('//*[@id="douyin-right-container"]//ul/li[2]/div/a/div')
#                 # element.click()
#                 page.wait_for_selector('//a/a/a', timeout=30000)
#             except TimeoutError:
#                 pass

#             cookie = context.cookies()
#             # 只需要 ttwid, msToken,带上其他参数会更稳定
#             cookie_keys = ['__ac_nonce', '__ac_signature', 'ttwid', 's_v_web_id', 'passport_csrf_token','passport_csrf_token_default', 'msToken', 'ttcid', 'tt_scid']
#             needed_cookies = {}

#             for item in cookie:
#                 if item['name']in cookie_keys:
#                     needed_cookies[item['name']] = item['value']
#             print(needed_cookies)
#             return needed_cookies

# 直接生成cookie
def get_cookie(ua):
    def generate_random_str(randomlength=107):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def getttwid(headers): 
        d = '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":true}'
        res = requests.post('https://ttwid.bytedance.com/ttwid/union/register/',data=d,headers=headers)
        cookie = res.headers.get('Set-Cookie')
        ttwid:str = re.findall('ttwid=(.*?);', cookie)[0]
        return ttwid
    
    def get_s_v_web_id():
        characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        t = len(characters)
        n = str(int(time.time())).encode('utf-8').hex()
        r = [''] * 36
        r[8] = r[13] = r[18] = r[23] = "_"
        r[14] = "4"
        for i in range(36):
            if not r[i]:
                o = random.randint(0, t - 1)
                r[i] = characters[3 if i == 19 else 0 + o % 8]
        return "verify_" + n + "_" + "".join(r)

    cookies = {
         'ttwid': getttwid({'User-Agent': ua}),
         'msToken': generate_random_str(107),
         's_v_web_id': get_s_v_web_id()}
    return cookies
    

class get_post():
    def __init__(self, cookies,ua) -> None:
        self.msToken = cookies['msToken']
        self.ttwid = cookies['ttwid']

        # self.s_v_web_id = cookies['s_v_web_id']
        self.url = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?'
        self.ua = ua
        self.douyin_headers = {
            'User-Agent': self.ua,
            'referer': 'https://www.douyin.com/user/MS4wLjABAAAAo1nZ1NZ1GB3c2xhhC7zThrdAUYpjnX7UbBAUb0YvOfDpkbErTzmWE23V6vfmRSyt',
            'accept-encoding': None,
            # 'Cookie': cookie,
            # 'Cookie': f"s_v_web_id={self.s_v_web_id}; msToken={self.msToken}; ttwid={self.ttwid}; odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69; passport_csrf_token=f61602fc63757ae0e4fd9d6bdcee4810;"
            'Cookie': f"msToken={self.msToken}; ttwid={self.ttwid}; odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69; passport_csrf_token=f61602fc63757ae0e4fd9d6bdcee4810;"
        }
    def getShareLink(self,string):
            return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)[0]

    def getAweme(self,url):
        key = None
        key_type = None

        try:
            r = requests.get(url=url, headers=self.douyin_headers)
        except Exception as e:
            print('[  错误  ]:输入链接有误！\r')
            return key_type, key

        urlstr = str(r.request.path_url)
        if "/video/" in urlstr:
            # 获取作品 aweme_id
            key = re.findall('video/(\d+)?', urlstr)[0]
            key_type = "aweme"
        elif "/note/" in urlstr:
            # 获取note aweme_id
            key = re.findall('note/(\d+)?', urlstr)[0]
            key_type = "aweme"
        return key_type, key
    


    def getXbogus(self,payload, form=''):
            xbogus = self.get_xbogus(payload, form)
            params = payload + "&X-Bogus=" + xbogus
            return params

    def _0x30492c(self,a, b):
            d = [i for i in range(256)]
            c = 0
            result = bytearray(len(b))

            for i in range(256):
                c = (c + d[i] + ord(a[i % len(a)])) % 256
                e = d[i]
                d[i] = d[c]
                d[c] = e

            t = 0
            c = 0

            for i in range(len(b)):
                t = (t + 1) % 256
                c = (c + d[t]) % 256
                e = d[t]
                d[t] = d[c]
                d[c] = e
                result[i] = ord(b[i]) ^ d[(d[t] + d[c]) % 256]

            return result

    def get_arr2(self,payload, form):
            ua = self.ua
            salt_payload_bytes = hashlib.md5(hashlib.md5(payload.encode()).digest()).digest()
            salt_payload = [byte for byte in salt_payload_bytes]

            salt_form_bytes = hashlib.md5(hashlib.md5(form.encode()).digest()).digest()
            salt_form = [byte for byte in salt_form_bytes]

            ua_key = ['\u0000', '\u0001', '\u000e']
            salt_ua_bytes = hashlib.md5(base64.b64encode(self._0x30492c(ua_key, ua))).digest()
            salt_ua = [byte for byte in salt_ua_bytes]

            timestamp = int(time.time())
            canvas = 1489154074

            arr1 = [
                64,  # 固定
                0,  # 固定
                1,  # 固定
                14,  # 固定 这个还要再看一下，14,12,0都出现过
                salt_payload[14],  # payload 相关
                salt_payload[15],
                salt_form[14],  # form 相关
                salt_form[15],
                salt_ua[14],  # ua 相关
                salt_ua[15],
                (timestamp >> 24) & 255,
                (timestamp >> 16) & 255,
                (timestamp >> 8) & 255,
                (timestamp >> 0) & 255,
                (canvas >> 24) & 255,
                (canvas >> 16) & 255,
                (canvas >> 8) & 255,
                (canvas >> 0) & 255,
                64,  # 校验位
            ]

            for i in range(1, len(arr1) - 1):
                arr1[18] ^= arr1[i]

            arr2 = [arr1[0], arr1[2], arr1[4], arr1[6], arr1[8], arr1[10], arr1[12], arr1[14], arr1[16], arr1[18], arr1[1],
                    arr1[3], arr1[5], arr1[7], arr1[9], arr1[11], arr1[13], arr1[15], arr1[17]]

            return arr2

    def get_garbled_string(self,arr2):
            p = [
                arr2[0], arr2[10], arr2[1], arr2[11], arr2[2], arr2[12], arr2[3], arr2[13], arr2[4], arr2[14],
                arr2[5], arr2[15], arr2[6], arr2[16], arr2[7], arr2[17], arr2[8], arr2[18], arr2[9]
            ]

            char_array = [chr(i) for i in p]
            f = []
            f.extend([2, 255])
            tmp = ['ÿ']
            bytes_ = self._0x30492c(tmp, "".join(char_array))

            for i in range(len(bytes_)):
                f.append(bytes_[i])

            return f

    def get_xbogus(self,payload, form):
            ua = self.ua
            short_str = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="
            arr2 = self.get_arr2(payload, form)

            garbled_string = self.get_garbled_string(arr2)

            xbogus = ""

            for i in range(0, 21, 3):
                char_code_num0 = garbled_string[i]
                char_code_num1 = garbled_string[i + 1]
                char_code_num2 = garbled_string[i + 2]
                base_num = char_code_num2 | char_code_num1 << 8 | char_code_num0 << 16
                str1 = short_str[(base_num & 16515072) >> 18]
                str2 = short_str[(base_num & 258048) >> 12]
                str3 = short_str[(base_num & 4032) >> 6]
                str4 = short_str[base_num & 63]
                xbogus += str1 + str2 + str3 + str4

            return xbogus

    def getUserInfoApi(self,sec_uid, mode="post", count=10, max_cursor=0):
        if sec_uid is None:
            return None

        awemeList = []
        if mode == "post":
            url = 'https://www.douyin.com/aweme/v1/web/aweme/post/?' + self.getXbogus(
                f'sec_user_id={sec_uid}&count={count}&max_cursor={max_cursor}&device_platform=webapp&aid=6383&msToken={self.msToken}')
        else:
            return None
        # self.douyin_headers['referer'] = f'https://www.douyin.com/user/{sec_uid}'
        res = requests.get(url=url, headers=self.douyin_headers)
        datadict = json.loads(res.text)
        # datadict = res.json()
        return datadict

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/cookie', methods=['GET'])
def cookie():
    ua = get_ua()
    try:
         data = {'Cookie': get_cookie(ua), 'ua':ua, 'msg':'success'}
    except: data = {'msg': '失败'}
    return jsonify(data)

# 用于获取数据的接口，需要传入 Cookie
@app.route('/user_data', methods=['POST'])
def user():
    # 从请求中获取传入的 Cookie
    try:
        cookie = request.json.get('Cookie')
        sec_id = request.json.get('sec_id')
        ua = request.json.get('ua')
        if not cookie or not sec_id or not ua: return jsonify({'msg':'请求参数错误'})
        if cookie.get('ttwid') and cookie.get('msToken'):
            data = get_post(cookie,ua).getUserInfoApi(sec_id)
            data['msg'] = 'success'
            return jsonify(data)
        else: return jsonify({'msg':'请求参数错误'})
    except: return jsonify({'msg':'未知错误'})

if __name__ == '__main__':
    # ua = get_ua()
    # cookies = get_cookie(ua)
    # print(cookies)
    # print(get_post(cookies,ua).getUserInfoApi("MS4wLjABAAAAWDrQ_XVZfIiwW0YxhTZFNTaOdZirJ8ADejcbNfFGifI"))
    app.run(debug=False, port=5253)


