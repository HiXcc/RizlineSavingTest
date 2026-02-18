from Crypto.Cipher import AES
import uuid
import random
import requests
import base64

def rizline_aes_decrypt(encrypt_data: bytes, key: bytes, iv: bytes) -> str | None:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec_data = cipher.decrypt(encrypt_data)
    last_byte = dec_data[-1]
    pad_len = (~last_byte) & 0xFF
    if 0 < pad_len <= 16:
        real_data = dec_data[:-pad_len]
    else:
        real_data = dec_data
    return real_data.decode('utf-8')

phone = "这里是手机号"
headers = {"game_id":"pigeongames.rizline","phone":phone,"device_id":str(uuid.uuid4()),"channel_id":str(random.randint(1,11))}
data = {
    "phone": phone,
    "password": "密码"
}
#如果遇到KeyError: 'set_token'就先在手机过验证码就能在今天期限内无限次用密码登录
res = requests.post("https://rizserver.pigeongames.net/account/login",json=data,headers=headers)
#print(res.headers,res.text)
token = res.headers["set_token"]
headers.update({"token":token})
start = requests.post("https://rizserver.pigeongames.net/game/game_start",json={},headers=headers)
gameplayId = eval(rizline_aes_decrypt(base64.b64decode(start.text)))["data"]

data = {
  "gameplayId": gameplayId,
  "trackAssetId": f"track.Skyscape.Plum.0",
  "difficultyClassName": "EZ",
  "score": 1003300,
  "completeRate": 120.00000762939453,
  "completeRateScale": 1.0,
  "maxPerfect": 33,
  "perfect": 106,
  "miss": 0,
  "bad": 0,
  "early": 0,
  "late": 0,
  "comboScore": 532,
  "updateRks": True
}
end = requests.post("https://rizserver.pigeongames.net/game/after_play",json=data,headers=headers)
decoding_result = rizline_aes_decrypt(base64.b64decode(end.text))
while decoding_result[-1] != "}":
    decoding_result = decoding_result[:-1]
d = eval(decoding_result)
print(d)
print(f"新增{d["deltaDot"]}dot,现有{d["newDot"]}dot,单曲rks:{d["levelRks"]},玩家rks:{d["totalRks"]}")
