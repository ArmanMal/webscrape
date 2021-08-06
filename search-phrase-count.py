import requests, webbrowser, numpy as np, pyinputplus as pyip
from bs4 import BeautifulSoup
from googlesearch import search

#Search results
query = pyip.inputStr('Search: ')
numOpen = pyip.inputInt('Number of links: ')

url_list = []
sub_links = 0
ytube_links = 0
for i in search(query, tld= "co.in", num = numOpen, stop = numOpen, pause = .200):
    if len(url_list) > 0:
        if url_list[-1] in i:
            sub_links += 1
            continue
    elif "www.youtube" in i:
        ytube_links += 1
        continue
    url_list.append(i)
    print(i)
if sub_links > 0:
    print("{} Sub-links were excluded from list".format(sub_links))
if ytube_links > 0:
    print("{} youtube links were excluded from list".format(ytube_links))

print("-------{} links have been loaded-------".format(len(url_list)))


#Phrase count
print()
search_phrase = pyip.inputStr("Search phrase in text: ")
phrase_count_list = []
blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head',
    'input',
    'script'
    ]
numLinks = len(url_list)
for k in range(numLinks):
    url = url_list[k]
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, "html.parser")
    text = soup.find_all(text=True)
    text_filtered = ''

    for t in text:
        if t.parent.name not in blacklist:
            text_filtered += '{}'.format(t)
    phrase_count = text_filtered.count(search_phrase)
    if phrase_count >0:
        phrase_count_list.append(phrase_count)    
    
#Open links
print('\n' * 10)
phrase_count_ordered = np.flip(np.argsort(phrase_count_list))
num_phrase_list = len(phrase_count_ordered)

for m in range(num_phrase_list):
    phrase_idx = phrase_count_ordered[m]
    print("[%d]: %d locations: %s" % (m+1, phrase_count_list[phrase_idx], url_list[phrase_idx]))

print("-------{} links contain the phrase-------".format(num_phrase_list))
print()

while(1):
    option = pyip.inputStr("[O] to open links, [T] to terminate: " )
    if option == 'O':
        open_link = pyip.inputInt("Open link #: ")
        phrase_idx = phrase_count_ordered[open_link-1]
        urlToOpen = url_list[phrase_idx]
        webbrowser.open(urlToOpen)
    elif option == "T":
        break
exit()   


