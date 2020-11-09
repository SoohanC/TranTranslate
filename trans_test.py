from googletrans import Translator
from time import sleep

def getTranslate(text,**kwargs):
    translator = Translator()
    result = None
    while result == None:
        try:
            result = translator.translate(text,**kwargs)
        except Exception as e:
            print(e)
            translator = Translator()
            sleep(0.5)
            pass
    return result     
    
result = getTranslate('hello',dest='ja')            
print(result)