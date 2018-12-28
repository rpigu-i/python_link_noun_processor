import requests
import json

search_terms = [
        "election hacking",
        "hacking elections",
        "vote hacking",
        "hacking votes",
        "referendum hacking",
        "hacking referendums",
        "vote machine hacking",
        "hacking voting machines",
        "hacking political parties",
        "hacking election candidates"
        ]



def get_data(s):
    file_suffix = s.replace(" ","")
    f = open('processed_links_'+file_suffix+'.txt', 'w')
    for i in range(0,10):
        headers = {'user-agent': 'Chrome/35.0.1916.47'}
        page = requests.get('https://www.googleapis.com/customsearch/v1?start='+str((i*10)+1)+'&key={YOUR KEY}&cx={YOUR SEARCH ENGINE}&filter=0&q='+s, headers=headers)
        result = json.loads(page.text)
        if 'items' in result:
            for r in result['items']:
                g_link = str(r['link'])
                print(g_link)
                f.write(g_link + "\n")
    f.close()


if __name__ == "__main__":
    for s in search_terms:
        get_data(s)
