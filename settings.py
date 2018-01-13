import os


class Settings:
    def __init__(self):
        pass

    DATASET_FILE = 'dataset/review.json'
    MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
    REVIEWS_DATABASE = "Dataset_Challenge_Reviews"
    TAGS_DATABASE = "Tags"
    REVIEWS_COLLECTION = "Reviews"
    CORPUS_COLLECTION = "Corpus"
    BUSINESS_COLLECTION = "Business"

    @staticmethod
    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
