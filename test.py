@app.route('/translate',methods=["POST"])
def translate_input():
    string=request.form['string']
    target_Lang=request.form['dest']
    #make data
    first_translation=translator.translate(string, dest=target_Lang)
    result_string1=first_translation.text
    second_translation=translator.translate(result_string1,src=target_Lang,dest='ko')
    result_string2=second_translation.text
    similarity= textAlgorithm.normalized_similarity(string,result_string2)
    test1= al_1.normalized_similarity(string,result_string2)
    #make data
    return jsonify({'result': 'success', 'trans1':result_string1,"trans2":result_string2,"similarity":similarity,"lev":test1})

@app.route('/api/multi-trans',methods=['POST'])
def multi_translate():
    original=request.form['original']
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
    similarity_1= textAlgorithm.normalized_similarity(original,final_result_1)
    test_1= al_1.normalized_similarity(original,final_result_1)
    similarity_2= textAlgorithm.normalized_similarity(original,final_result_2)
    test_2= al_1.normalized_similarity(original,final_result_2)

    return jsonify({'result': 'success','firstResult1':first_result_1,'firstResult2':first_result_2,'finalResult1':final_result_1,'finalResult2':final_result_2,"similarity1":similarity_1,"similarity2":similarity_2,"test1":test_1,"test2":test_2})
