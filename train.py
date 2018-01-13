import logging
import gensim
from gensim.corpora import BleiCorpus
from gensim import corpora
from pymongo import MongoClient
from settings import Settings


class Corpus(object):
    def __init__(self, cursor, reviews_dictionary, corpus_path, business_ids=[]):
        self.cursor = cursor
        self.reviews_dictionary = reviews_dictionary
        self.corpus_path = corpus_path
        self.business_ids = business_ids

    def __iter__(self):
        self.cursor.rewind()
        for review in self.cursor:
            if self.business_ids:
                if review["business"] in self.business_ids:
                    yield self.reviews_dictionary.doc2bow(review["words"])
            else:
                yield self.reviews_dictionary.doc2bow(review["words"])

    def serialize(self):
        BleiCorpus.serialize(self.corpus_path, self, id2word=self.reviews_dictionary)

        return self


class Train:
    def __init__(self):
        pass

    @staticmethod
    def run(lda_model_path, corpus_path, num_topics, id2word):
        corpus = corpora.BleiCorpus(corpus_path)
        lda = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=id2word)
        lda.save(lda_model_path)

        return lda


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    lda_num_topics = 20
    only_restaurant = True
    business_ids = []

    dictionary_path = "models/dictionary_restaurant.dict"
    corpus_path = "models/corpus_restaurant.lda-c"
    lda_model_path = "models/lda_model_20_topics.lda"

    if only_restaurant:
        business_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
            Settings.BUSINESS_COLLECTION]
        business_cursor = business_collection.find({'categories': 'Restaurants'}, {'business_id': 1})
        for doc in business_cursor:
            business_ids.append(doc['business_id'])

    corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][
        Settings.CORPUS_COLLECTION]
    reviews_cursor = corpus_collection.find({})

    dictionary = corpora.Dictionary.load(dictionary_path)
    Corpus(reviews_cursor, dictionary, corpus_path, business_ids=business_ids).serialize()
    Train.run(lda_model_path, corpus_path, lda_num_topics, dictionary)


if __name__ == '__main__':
    main()
