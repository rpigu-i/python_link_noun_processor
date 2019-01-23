import requests
import json
from nltk import word_tokenize

urls =[]
keywords = {}
terms = ["ddos", "data", "intrusion", "theft", "fake news", "psychometrics", "propaganda", "voting machines", "targeted ads", "social media", "crash", "virus", "malware", "email", "psychological", "phishing", "leak", "accident"]


def download_document(url):
    """
    Grab document for keyword
    comparison
    """
    
    headers = {'user-agent': 'Chrome/35.0.1916.47'}
    response = requests.get(url.rstrip('\n'), headers=headers)
    raw = response.text
    return raw.lower()

def compare_keywords(raw):
    for term in terms:
        if int(raw.find(term)) > 0:
            if term in keywords:
                ac = keywords[term]['article_count']
                ac = ac + 1
            else:
                ac = 1

            update_counts = {
             'article_count': ac,
            }
            keywords[term] = update_counts

if __name__ == '__main__':
    with open('research_data.txt', 'r') as f:
        urls = f.readlines()

    print (urls)
    for url in urls:
        print (url)
        try:
            tokens = download_document(url)
            compare_keywords(tokens)
        except:
            pass


    with open('preselected_keywords.txt', 'w') as file:
        file.write(json.dumps(keywords))
