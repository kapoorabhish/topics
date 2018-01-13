import logging

from gensim.models import LdaModel
from gensim import corpora


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary_path = "models/dictionary_restaurant.dict"
corpus_path = "models/corpus_restaurant.lda-c"
lda_num_topics = 50
num_words = 20
lda_model_path = "models/lda_model_50_topics_restaurant.lda"

dictionary = corpora.Dictionary.load(dictionary_path)
corpus = corpora.BleiCorpus(corpus_path)
lda = LdaModel.load(lda_model_path)

for i, topic in enumerate(lda.show_topics(num_topics=lda_num_topics, num_words=num_words)):
    print '#%i: %s' %(i, str(topic))

