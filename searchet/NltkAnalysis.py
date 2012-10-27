
import nltk
import numpy

class NltkAnalysis:
    
    def __init__(self):
        pass
    
    def Analaysis(self, keywords):
        tokens = nltk.word_tokenize(keywords)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)
        return entities
    
    
    
if __name__ == "__main__":
    
    nltk_ins = NltkAnalysis()
    keywords = "washington boston"
    result = nltk_ins.Analaysis(keywords)
    print result
