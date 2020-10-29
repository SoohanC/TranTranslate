from flask import Flask, render_template,request,jsonify
from googletrans import Translator


app = Flask(__name__)
translator=Translator()

@app.route('/')
def home():  # 함수명 수정 - 이름만 보고 접속되는 페이지를 확인할 수 있게!
    return render_template('index.html')

@app.route('/translate',methods=["POST"])
def translate_input():
    string=request.form['string']
    target_Lang=request.form['dest']
    #make data
    first_translation=translator.translate(string, dest=target_Lang)
    result_string1=first_translation.text
    second_translation=translator.translate(result_string1,src=target_Lang,dest='ko')
    result_string2=second_translation.text
    print(result_string1,result_string2)
    #make data
    return jsonify({'result': 'success', 'trans1':
    result_string1,"trans2":result_string2})
    

if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)