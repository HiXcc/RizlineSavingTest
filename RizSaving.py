from Crypto.Cipher import AES
import uuid
import random
import requests

def rizline_aes_decrypt(encrypt_data: bytes, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec_data = cipher.decrypt(encrypt_data)
    last_byte = dec_data[-1]
    pad_len = (~last_byte) & 0xFF
    if 0 < pad_len <= 16:
        real_data = dec_data[:-pad_len]
    else:
        real_data = dec_data
    return real_data.decode('utf-8')

def get_save(phone,password,headers):
    data = {"phone": phone,"password": password}
    res = requests.post("https://rizserver.pigeongames.net/account/login",json=data,headers=headers)
    if "set_token" in res.headers:
        token = res.headers["set_token"]
        headers.update({"token":token})
        res = requests.post("https://rizserver.pigeongames.net/game/rn_login",headers=headers,json={})
        shop = requests.post("https://rizserver.pigeongames.net/game/get_user_shop",headers=headers,json={}).text
        return (res,shop)
    return (res.status_code,res.text)

def get_token(phone,password):
  headers = {"game_id":"pigeongames.rizline","phone":phone,"device_id":str(uuid.uuid4()),"channel_id":str(random.randint(1,11))}
  phone_exist = requests.post("https://rizserver.pigeongames.net/account/check_phone",json={"phone": phone},headers=headers).json()
  if phone_exist["code"] == 0:
      data = {"phone": phone,"password": password}
      res = requests.post("https://rizserver.pigeongames.net/account/login",json=data,headers=headers)
      res_json = res.json()
      if res_json["code"] == 0:
          token = res.headers["set_token"]
          print("token:",res.headers["set_token"])
      else:
          print("r",res_json["msg"])
  else:
      verify_code_data = {"phone": phone,"transaction": "login"}
      requests.post("https://rizserver.pigeongames.net/account/send_verify_code",json=verify_code_data,headers=headers)
      code = int(input("riz 验证码"))
      data = {"phone": phone,"code": code}
      res = requests.post("https://rizserver.pigeongames.net/account/login",json=data,headers=headers)
      token = res.headers["set_token"]
      print("token:",res.headers["set_token"])
  result = get_save(phone,password,token)
  print(result)
