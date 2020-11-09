import requests
import os
import json
from dotenv import load_dotenv


def getKakaoTrans(text, src, dest):
    def joinContents(text):
        separator = " "
        result = separator.join(text)
        return result

    API_KEY = os.getenv("KAKAO_API_KEY")
    kakao_url = "https://dapi.kakao.com"
    headers = {
        "Authorization": f"KakaoAK {API_KEY}",
        "Content-type": "application/x-www-form-urlencoded",
    }
    data = {"query": text, "src_lang": src, "target_lang": dest}
    r = requests.post(
        kakao_url + "/v2/translation/translate", headers=headers, data=data
    )
    response = json.loads(r.text)
    if response.get("code"):
        result = {"status": False, "output": None}
    else:
        output = joinContents(response["translated_text"][0])
        result = {"status": True, "output": output}
    return result

print(getKakaoTrans("안녕하세요","kr","jp"))
