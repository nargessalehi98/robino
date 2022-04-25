import collections
from parsivar import Normalizer, Tokenizer
from robinodemo.utils import get_db_handle, get_collection_handle

db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')
inverted_index_handler = get_collection_handle(db_handler, 'inverted_index')


def normalize_data(data):
    return Normalizer().normalize(data)


def pruning(data):
    pruned_letter = ['.', ':', ';', '!', '@', '#', '$', '%', '^', '&', '*',
                     '(', ')', '_', '-', '+', '=', ',', '1', '2', '3', '4',
                     '5', '6', '7', '8', '9', '0', '۱', '۲', '۳', '۴', '۵',
                     '۶', '۷', '۸', '۹', '۰', 'http', '\"', '/', '|', '÷',
                     '`', '~', '\u200c', '\u202b', '\u200f', 'https', '...',
                     '\xa0', '،', ')', '(', '٪', '()', '()'
                     ]
    for word in data:
        if word in pruned_letter :
            data.remove(word)
    return data


def list_stop_words():
    word_list = []
    with open('search_engine/stop_words.txt', 'r') as file:
        for line in file:
            word = line.strip()
            word_list.append(word)
    return word_list


def del_stop_words(data):
    stop_words = list_stop_words()
    for stop_word in stop_words:
        for word in data:
            if stop_word == word:
                data.remove(word)
    return data


def tokenize_data(data):
    tokenizer = Tokenizer()
    return tokenizer.tokenize_words(data)


def create_inverted_index(query, _id):
    for item in query:
        inverted_index_handler.find_one_and_update({"token": item, "doc_id": {"$size": 100}}, {"$pop": {"doc_id": -1}})
        output = inverted_index_handler.find_one_and_update({"token": item}, {"$addToSet": {"doc_id": _id}})
        if output is None:
            inverted_index_handler.insert_one({"token": item, "doc_id": [_id]})


def search_query(query):
    query = normalize_data(query)
    query = tokenize_data(query)
    query = pruning(query)
    query = del_stop_words(query)
    doc_list = []
    for item in query:
        token_list = list(inverted_index_handler.find({"token": item}, {"doc_id": 1, "_id": 0}))
        if token_list:
            token_list = token_list[0]["doc_id"]
        doc_list += token_list
    occurrences = collections.Counter(doc_list).most_common()
    occurrences = [item[0] for item in occurrences]
    return occurrences


def pre_processing(query, _id):
    query = normalize_data(query)
    query = tokenize_data(query)
    query = pruning(query)
    query = del_stop_words(query)
    create_inverted_index(query, _id)
    return query


