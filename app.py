from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from googletrans import Translator
from time import sleep
import textdistance

app = Flask(__name__)
cors = CORS(app)

jac_algo = textdistance.Jaccard()
lev_algo = textdistance.Levenshtein()


def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    while result == None:
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            sleep(1)
            pass
    return result


@app.route("/api/translate", methods=["POST"])
def translate():
    data = request.get_json()
    # 한-외
    source = data["source"]
    to = data["to"]
    translation = getTranslate(source, src="ko", dest=to)
    # 외-한
    translated = translation.text
    tran_translation = getTranslate(translated, src=to, dest="ko")
    result = tran_translation.text
    jaccard = jac_algo.normalized_similarity(source, result)
    levenshtein = lev_algo.normalized_similarity(source, result)
    # 유사도 판별
    return jsonify(
        {
            "status": "success",
            "translation": translated,
            "result": result,
            "jaccard": jaccard,
            "leven": levenshtein,
        }
    )


@app.route("/api/multiTrans", methods=["POST"])
def multiTrans():
    data = request.get_json()
    original = data["original"]
    source = data["source"]
    src = data["from"]
    # 제 1번역
    to_1 = data["to1"]
    trans_1 = getTranslate(source, src=src, dest=to_1).text
    result_1 = getTranslate(trans_1, src=to_1, dest="ko").text
    jac_1 = jac_algo.normalized_similarity(original, result_1)
    lev_1 = lev_algo.normalized_similarity(original, result_1)
    # 제 2 번역
    to_2 = data["to2"]
    trans_2 = getTranslate(source, src=src, dest=to_2).text
    result_2 = getTranslate(trans_2, src=to_2, dest="ko").text
    jac_2 = jac_algo.normalized_similarity(original, result_2)
    lev_2 = lev_algo.normalized_similarity(original, result_2)
    return jsonify(
        {
            "status": "success",
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


@app.route("/api/trans-to-kor", methods=["POST"])
def trans_to_kor():
    data = request.get_json()
    original = data["original"]
    lang_type = data["langType"]
    dest_1 = data["destination1"]
    dest_2 = data["destination2"]
    dest_3 = data["destination3"]
    print(lang_type)
    print(dest_1,dest_2,dest_3)
    trans_1=None
    result_1=None
    if(dest_1 != ""):
        trans_1 = getTranslate(original,src=lang_type,dest=dest_1).text
        result_1= getTranslate(trans_1,src=dest_1,dest="ko").text
    else:
        trans_1 = original
        result_1 = getTranslate(trans_1,src=lang_type,dest="ko").text
    #번역2
    trans_2 = getTranslate(original,src=lang_type,dest=dest_2).text
    result_2= getTranslate(trans_2,src=dest_2,dest="ko").text
    #번역3
    trans_3 = getTranslate(original,src=lang_type,dest=dest_3).text
    result_3= getTranslate(trans_3,src=dest_3,dest="ko").text

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
    return jsonify({"status":True})


if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)
