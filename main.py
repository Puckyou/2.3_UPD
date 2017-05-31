def get_encoding(file):
    import chardet
    with open(file ,"rb") as f:
        data = f.read()
        file_encoding = chardet.detect(data)["encoding"]
    return file_encoding
def collect_text (file_name):
    import json
    with open(file_name, "r", encoding = get_encoding(file_name)) as f:
        lines = json.load(f)
        tonns_of_text = []
        for key, articles in lines["rss"]["channel"].items():
            if key == "item":
                for article in articles:
                    for akey, aitem in article.items():
                        text_list = ["title", "description"]
                        if akey in text_list:
                            if type(aitem) == dict:
                                for a in aitem.values():
                                    tonns_of_text.append(a)
                            if type(aitem) == str:
                                tonns_of_text.append(aitem)
    return tonns_of_text

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(my_text):
    s = MLStripper()
    s.feed(my_text)
    return s.get_data()
def strip_punctuation(my_text):
    import string
    table = {key: None for key in string.punctuation}
    my_list = ["«","»","\r"]
    for item in my_list:
        table[item] = None
    table["\n"] = " "
    table.pop("-", None)
    table = str.maketrans(table)
    return my_text.translate(table)
def delete_source(my_text):
    import re
    return re.sub('/[^>]+/', '', my_text)
def strip_all(my_text):
    my_text = strip_tags(my_text)
    my_text = delete_source(my_text)
    my_text = strip_punctuation(my_text)
    my_text = my_text.lower()
    return my_text
def get_words_list(file_name):
    tonns_of_text = collect_text(file_name)
    words_list = []
    for line in tonns_of_text:
        cleared_line = strip_all(line)
        words = cleared_line.split(" ")
        for word in words:
            words_list.append(word)
    return words_list
def get_word_count(file_name):
    words_list = get_words_list(file_name)
    word_count = {}
    for word in words_list:
        if len(word) > 6:
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1
    return word_count
def get_sorted_word_count(file_name):
    word_count = get_word_count(file_name)
    import operator
    sorted_word_count = sorted(word_count.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_word_count
def print_ten_words(file_name):
    sorted_word_count = get_sorted_word_count(file_name)
    for item in sorted_word_count[:9]:
            print("{} - {}".format(item[0], item[1]))
def get_file_and_print(my_file):
    file_list = []
    file_list.append(my_file)
    for a_file in file_list:
        print("\n{}\n".format(a_file))
        print_ten_words(a_file)
get_file_and_print("newsafr.json")
