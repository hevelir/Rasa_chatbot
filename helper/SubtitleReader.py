import glob

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter


def read_subtitle():
    count = 0
    lines = []
    list_of_files = glob.glob('./subtitles/BigBangTheory/*.srt')
    for file in list_of_files:
        with open(file) as fp:
            for line in fp:
                line = line.rstrip('\n')
                if not (line.__contains__("-->") or line.isnumeric() or line == ""):
                    lines.insert(count, line)
                    count += 1
    return lines


def line_to_words():
    stop_words = set(stopwords.words('english'))
    word_tokens = []
    for line in read_subtitle():
        for words in word_tokenize(line):
            word_tokens.append(words.lower())
    words = [word for word in word_tokens if word.isalpha()]

    filtered_words = []
    for w in words:
        if w not in stop_words:
            filtered_words.append(w)

    trigram = zip(filtered_words, filtered_words[1:], filtered_words[2:])
    counts = Counter(trigram)
    return counts.most_common()


count = 0

for tuplee in line_to_words():
    count += 1
    print(tuplee)
    if count == 50:
        break

