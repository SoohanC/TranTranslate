from flask import Flask, render_template,request,jsonify
from googletrans import Translator


app = Flask(__name__)
translator=Translator()

@app.route('/')
def intro():  # 함수명 수정 - 이름만 보고 접속되는 페이지를 확인할 수 있게!
    return render_template('intro.html')

@app.route('/main')
def main():  # 함수명 수정 - 이름만 보고 접속되는 페이지를 확인할 수 있게!
    return render_template('main.html')

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

@app.route('/multi-trans',methods=['POST'])
def multi_translate():
    string=request.form['string']
    src=request.form['src']
    dest1=request.form['dest1']
    dest2=request.form['dest2']
    #1차
    first_translation_1=translator.translate(string,src=src,dest=dest1)
    first_translation_2=translator.translate(string,src=src,dest=dest2)
    first_result_1= first_translation_1.text
    first_result_2= first_translation_2.text
    #1차
    final_translation_1=translator.translate(first_result_1,src=dest1,dest='ko')
    final_translation_2=translator.translate(first_result_2,src=dest2,dest='ko')
    final_result_1= final_translation_1.text
    final_result_2= final_translation_2.text
    return jsonify({'result': 'success','firstResult1':first_result_1,'firstResult2':first_result_2,'finalResult1':final_result_1,'finalResult2':final_result_2})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)