from trigram_tagger import SubjectTrigramTagger
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import re
import json
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
urls =[]
keywords = {}

# Noun Part of Speech Tags used by NLTK
# More can be found here
# http://www.winwaed.com/blog/2011/11/08/part-of-speech-tags/
NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']

def download_document(url):
    """Downloads document using BeautifulSoup, extracts the subject and all
    text stored in paragraph tags
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('title').get_text()
    document = ' '.join([p.get_text() for p in soup.find_all('p')])
    return document

def clean_document(document):
    """Remove enronious characters. Extra whitespace and stop words"""
    document = re.sub('[^A-Za-z .-]+', ' ', document)
    document = ' '.join(document.split())
    document = ' '.join([i for i in document.split() if i not in stop])
    return document

def tokenize_sentences(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    return sentences

def get_entities(document):
    """Returns Named Entities using NLTK Chunking"""
    entities = []
    sentences = tokenize_sentences(document)

    # Part of Speech Tagging
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                entities.append(' '.join([c[0] for c in chunk]).lower())
    return entities

def word_freq_dist(document):
    """Returns a word count frequency distribution"""
    words = nltk.tokenize.word_tokenize(document)
    words = [word.lower() for word in words if word not in stop]
    fdist = nltk.FreqDist(words)
    return fdist

def extract_nouns(document):
    # Get most frequent Nouns
    fdist = word_freq_dist(document)
    for w, c in fdist.most_common(50):
        if nltk.pos_tag([w])[0][1] in NOUNS:

            if w in keywords:
                ac = keywords[w]['article_count']
                ac = ac + 1
                kc = keywords[w]['keyword_count']
                kc = kc + c
            else:
                ac = 1
                kc = c

            update_counts = {
             'article_count': ac,
             'keyword_count': kc
            }
            keywords[w] = update_counts


def merge_multi_word_subject(sentences, subject):
    """Merges multi word subjects into one single token
    ex. [('steve', 'NN', ('jobs', 'NN')] -> [('steve jobs', 'NN')]
    """
    if len(subject.split()) == 1:
        return sentences
    subject_lst = subject.split()
    sentences_lower = [[word.lower() for word in sentence]
                        for sentence in sentences]
    for i, sent in enumerate(sentences_lower):
        if subject_lst[0] in sent:
            for j, token in enumerate(sent):
                start = subject_lst[0] == token
                exists = subject_lst == sent[j:j+len(subject_lst)]
                if start and exists:
                    del sentences[i][j+1:j+len(subject_lst)]
                    sentences[i][j] = subject
    return sentences


if __name__ == '__main__':
    with open('research_data.txt', 'r') as f:
        urls = f.readlines()
    for i in urls:
        try:
            print(i)
            document = download_document(i)
            document = clean_document(document)
            extract_nouns(document)
        except:
            pass


    with open('keywords.txt', 'w') as file:
        file.write(json.dumps(keywords))
