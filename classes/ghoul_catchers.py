import requests
import time
import base64
import datetime
import random
import json
import threading
from hashlib import md5
from pyDes import triple_des, PAD_PKCS5

class GhoulCatchers:
    def __init__(self, username, password, proxy, functions):
        self.session = requests.Session()
        self.functions = functions()
        self.crypto = Encryption()
        self.base = "https://api.jumpstart.com/"
        self.user_id = None
        self.api_token = None
        self.api_key = "4a8b1082-5a88-40fc-a9f0-44ced5699267"
        self.secret = "AFDF51E3-063E-496B-8762-260063880244"
        self.app_name = "Neopets Ghoul Catchers Google Play"
        self.language = "en-US"
        self.username = username
        self.password = password
        if self.functions.contains(proxy, ":"):
            self.set_proxy(proxy)

    def set_proxy(self, proxy):
        self.session.proxies.update({"http": f"http://{proxy}", "https": f"https://{proxy}"})

    def get_ticks(self):
        return str(int((datetime.datetime.utcnow() - datetime.datetime(1, 1, 1)).total_seconds() * 10000000))

    def url(self, path):
        return f"{self.base}{path}"

    def login_parent(self):
        encrypted_data = self.crypto.encrypt_data(f"<?xml version=\"1.0\" encoding=\"utf-16\"?><ParentLoginData xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><UserName>{self.username}</UserName><Password>{self.password}</Password><Locale>en-US</Locale><FacebookAccessToken /><ExternalUserID xsi:nil=\"true\" /><ExternalAuthData xsi:nil=\"true\" /><email xsi:nil=\"true\" /><SubscriptionID>0</SubscriptionID><ReceivesEmail>false</ReceivesEmail><AutoActivate xsi:nil=\"true\" /><SendActivationEmail xsi:nil=\"true\" /><SendWelcomeEmail xsi:nil=\"true\" /><LinkUserToFaceBook xsi:nil=\"true\" /><FavouriteTeamID xsi:nil=\"true\" /><GroupID xsi:nil=\"true\" /><UserPolicy><TermsAndConditions>true</TermsAndConditions><PrivacyPolicy>true</PrivacyPolicy></UserPolicy></ParentLoginData>")
        data = {"apiKey": self.api_key, "parentLoginData": base64.b64encode(encrypted_data)}
        response = self.session.post(self.url("Common/v3/AuthenticationWebService.asmx/LoginParent"), data=data)
        if "<string>" in response.text:
            decrypted_data = self.crypto.decrypt_data(self.functions.get_between(response.text, "<string>", "</string>"))
            if "<LoginStatus>Success" in decrypted_data:
                self.api_token = self.functions.get_between(decrypted_data, "<ApiToken>", "</ApiToken>")
                self.user_id = self.functions.get_between(decrypted_data, "<UserID>", "</UserID>")
                print(f"[{self.username}] Ghoul Catchers: Successfully logged in as {self.username}")

    def login_child(self):
        ticks, child_id = self.get_ticks(), self.crypto.encrypt_data(self.user_id)
        concate = ticks + self.secret + self.api_token + base64.b64encode(child_id).decode() + self.language
        data = {"apiKey": self.api_key, "parentApiToken": self.api_token, "ticks": ticks, "signature": md5(concate.encode()).hexdigest(), "childUserID": base64.b64encode(child_id).decode(), "locale": self.language}
        response = self.session.post(self.url("Common/AuthenticationWebService.asmx/LoginChild"), data=data)
        if "<string>" in response.text:
            self.api_token = self.crypto.decrypt_data(self.functions.get_between(response.text, "<string>", "</string>"))[:-4]

    def apply_payout(self):
        for _ in enumerate(range(50), 1):
            ticks = self.get_ticks()
            concate = ticks + self.secret + self.api_token + "GCElementMatch" + "300"
            data = {"apiToken": self.api_token, "apiKey": self.api_key, "ModuleName": "GCElementMatch", "points": "300", "ticks": ticks, "signature": md5(concate.encode()).hexdigest()}
            response = self.session.post(self.url("Achievement/AchievementWebService.asmx/ApplyPayout"), data=data)
            if "AchievementReward" in response.text:
                delay = random.uniform(100, 250)
                print(f"[{self.username}] Ghoul Catchers: Score sent successfully {_[0]}/50 - sleeping for {int(delay)} seconds..")
                time.sleep(delay)

class Encryption:
    def __init__(self):
        self.key = b'\xba\xb0,x\x8f\xee\xc0_vU*\xe0\x8d\xfe\x82\x00'

    def encrypt_data(self, data):
        return triple_des(self.key).encrypt(data.encode("utf-16-le"), padmode=PAD_PKCS5)

    def decrypt_data(self, data):
        return triple_des(self.key).decrypt(base64.b64decode(data)).decode("utf-16-le")
