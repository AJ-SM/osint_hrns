from rank_bm25 import BM25Okapi


class Collected:
    def __init__(self,doc:list,query:str):
        self.doc = doc 
        self.tockenize_doc = []
        self.query= query
    
    def tockenize(self):
        self.tockenize_doc = [
            dok.lower().split()
            for dok in self.doc 
        ]
        self.bm25  = BM25Okapi(self.tockenize_doc)

    def find(self):
        self.tockenize()
        tockenized_q = self.query.lower().split()
        score = self.bm25.get_scores(tockenized_q)
        print(score)
        return score
    



if __name__ == "__main__":
    documents = [
    "python is a programming language",
    "machine learning uses python",
    "bm25 is used for information retrieval",
    "python is useful for artificial intelligence"
        ]

    query = "python machine learning"
    clt = Collected(doc=documents,query=query)
    print(clt.find().argsort())

