from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import textdistance
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app)

##Text-distance Algorithm
jac_algo = textdistance.Jaccard()
lev_algo = textdistance.Levenshtein()

## translate_kakao function
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


@app.route("/api/kakao/translate", methods=["POST"])
def translate():
    data = request.get_json()
    source = data["source"]
    to = data["to"]
    translation = getKakaoTrans(source, "kr", to)
    translated = translation["output"]
    if translation["status"] == True:
        tran_translation = getKakaoTrans(translated, to, "kr")
        result = tran_translation["output"]
        if tran_translation["status"] == True:
            jaccard = jac_algo.normalized_similarity(source, result)
            levenshtein = lev_algo.normalized_similarity(source, result)
            return jsonify(
                {
                    "status": True,
                    "translation": translated,
                    "result": result,
                    "jaccard": jaccard,
                    "leven": levenshtein,
                }
            )
    return jsonify({"status": False, "result": "No1!!"})


@app.route("/api/kakao/multi-trans", methods=["POST"])
def multiTrans():
    data = request.get_json()
    original = data["original"]
    source = data["source"]
    src = data["from"]
    # 제1번역
    to_1 = data["to1"]
    to_2 = data["to2"]
    trans_1 = getKakaoTrans(source, src, to_1)
    trans_2 = getKakaoTrans(source, src, to_2)
    result_1 = None
    result_2 = None
    if trans_1["status"] == True:
        trans_1 = trans_1["output"]
        result_1 = getKakaoTrans(trans_1, to_1, "kr")
        if result_1["status"] == True:
            result_1 = result_1["output"]
    if trans_2["status"] == True:
        trans_2 = trans_2["output"]
        result_2 = getKakaoTrans(trans_2, to_2, "kr")
        if result_2["status"] == True:
            result_2 = result_2["output"]

    if result_1 == None or result_2 == None:
        return jsonify({"status": False})
    jac_1 = jac_algo.normalized_similarity(original, result_1)
    lev_1 = lev_algo.normalized_similarity(original, result_1)
    jac_2 = jac_algo.normalized_similarity(original, result_2)
    lev_2 = lev_algo.normalized_similarity(original, result_2)

    return jsonify(
       {
           "status": True,
           "trans1": trans_1,
           "result1": result_1,
           "jac1": jac_1,
           "lev1": lev_1,
           "trans2": trans_2,
           "result2": result_2,
           "jac2": jac_2,
           "lev2": lev_2,
       }
   )



@app.route("/api/kakao/trans-to-kor", methods=["POST"])
def transToKor():
    data = request.get_json()
    original = data["original"]
    lang_type = data["langType"]
    dest_1 = data["destination1"]
    dest_2 = data["destination2"]
    dest_3 = data["destination3"]
    trans_1=None
    trans_2=None
    trans_3=None
    result_1=None
    result_2=None
    result_3=None
    #1차
    if(dest_1 !=""):
        temp=getKakaoTrans(original,lang_type,dest_1)
        if(temp["status"] == True):
            trans_1=temp["output"]
            temp=getKakaoTrans(trans_1,dest_1,"kr")
            if(temp["status"] == True):
                result_1=temp["output"]
    else:
        trans_1 =original
        temp=getKakaoTrans(trans_1,lang_type,"kr")
        if(temp["status"] == True):
            result_1=temp["output"]
    temp=getKakaoTrans(original,lang_type,dest_2)
    if(temp["status"] == True):
        trans_2 =temp["output"]
    temp=getKakaoTrans(original,lang_type,dest_3)
    if(temp["status"] == True):
        trans_3 =temp["output"]
    if trans_1 ==None or trans_2 ==None or trans_3==None:
        return jsonify({"status": False})
    #2차
    temp=getKakaoTrans(trans_2,dest_2,"kr")
    if(temp["status"] == True):
        result_2 =temp["output"]
    temp=getKakaoTrans(trans_3,dest_3,"kr")
    if(temp["status"] == True):
        result_3 =temp["output"]
    return jsonify(
       {
           "status": "success",
           "trans1": trans_1,
           "trans2": trans_2,
           "trans3": trans_3,
           "result1": result_1,
           "result2": result_2,
           "result3": result_3,
       }
   )




@app.route("/api/status", methods=["GET"])
def status():
    print(request)
    return jsonify({"status": True})


if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)
