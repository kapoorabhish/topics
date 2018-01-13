import logging
from gensim import corpora
from pymongo import MongoClient
from settings import Settings


class Dictionary(object):
    def __init__(self, cursor, dictionary_path, business_ids=[]):
        self.cursor = cursor
        self.dictionary_path = dictionary_path
        self.business_ids = business_ids

    def build(self):
        self.cursor.rewind()
        if self.business_ids:
            dictionary = corpora.Dictionary(review["words"] for review in self.cursor if review['business'] in
                                            self.business_ids)
        else:
            dictionary = corpora.Dictionary(review["words"] for review in self.cursor)
        dictionary.filter_extremes(keep_n=10000)
        dictionary.compactify()
        corpora.Dictionary.save(dictionary, self.dictionary_path)

        return dictionary


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    only_restaurant = True
    dictionary_path = "models/dictionary.dict"

    business_ids = []

    if only_restaurant:
        business_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
            Settings.BUSINESS_COLLECTION]
        business_cursor = business_collection.find({'categories': 'Restaurants'}, {'business_id': 1})
        for doc in business_cursor:
            business_ids.append(doc['business_id'])

    corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][
        Settings.CORPUS_COLLECTION]
    reviews_cursor = corpus_collection.find({})

    Dictionary(reviews_cursor, dictionary_path, business_ids=business_ids).build()

if __name__ == '__main__':
    main()
