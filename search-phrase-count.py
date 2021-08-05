import requests, webbrowser, numpy as np, pyinputplus as pyip
from bs4 import BeautifulSoup
from googlesearch import search


#Fetch URLs for query
query = pyip.inputStr('Search: ')
numOpen = pyip.inputInt('Number of links: ')

url_list = []
for i in search(query, tld= "co.in", num = numOpen, stop = numOpen, pause = .200):
    url_list.append(i)
    print(i)
numLinks = len(url_list)

#Filter out sub-links
print()
sub_links = []
for x in range(1, numLinks):
    if url_list[x-1] in url_list[x]:
       sub_links.append(x)

numSubLinks = len(sub_links)
if numSubLinks > 0:
    for y in sorted(sub_links, reverse = True):
        del url_list[y]
    print("{} Sub-links were removed from list".format(numSubLinks))

numLinks = len(url_list)

#Filter out Youtube / Common forums
youtube_links = []
forum_links = []
filter_indexes = []
filter_indexes_2 = []
for i in range(numLinks):
    if "www.youtube" in url_list[i]:
        LinkToAdd = url_list[i]
        youtube_links += [LinkToAdd]
        filter_indexes += [i]

    elif "reddit" in url_list[i] or "quora" in url_list[i]:
        LinkToAdd = url_list[i]
        forum_links += [LinkToAdd]
        filter_indexes_2 += [i]

numYoutube = len(youtube_links)
numForum = len(forum_links)

if numYoutube > 0:
    for j in sorted(filter_indexes, reverse = True):
        del url_list[j]
        
if numForum > 0:
    for j2 in sorted(filter_indexes_2, reverse = True):
        del url_list[j2]
        
print("{} youtube links were removed from list".format(numYoutube))
print("{} forum links were removed from list".format(numForum))
print()
numLinks = len(url_list)
print("-------{} links have been loaded-------".format(numLinks))

#Search phrase count in each URL
print()

search_phrase = pyip.inputStr("Search phrase in text: ")
numLinks = len(url_list)
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
        print("[%d]: %d instances found (%s)" % (k+1, phrase_count, url))


#Open links/ see phrase context
print('\n' * 10)
phrase_count_ordered = np.flip(np.argsort(phrase_count_list))
num_phrase_list = len(phrase_count_ordered)

for m in range(num_phrase_list):
    phrase_idx = phrase_count_ordered[m]
    print("[%d]: %d locations: %s" % (m+1, phrase_count_list[phrase_idx], url_list[phrase_idx]))

print("-------{} links contain the phrase-------".format(num_phrase_list))
print()
option = pyip.inputStr("[O] to open links: " )

while(1):
    if option == 'O':
        open_link = pyip.inputInt("Open link #: ")
        phrase_idx = phrase_count_ordered[open_link]
        urlToOpen = url_list[phrase_idx]
        webbrowser.open(urlToOpen)
        option2 = pyip.inputStr("[T] to terminate, [O] to open another link: ")
    if option2 == "T":
        break

exit()   
