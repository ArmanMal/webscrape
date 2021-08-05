import webbrowser, bs4, pyinputplus as pyip
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
    filter_query = pyip.inputStr("{} link(s) are Youtube, filter them out? (Y/N): ".format(numYoutube))
    if filter_query == "Y":
        for j in sorted(filter_indexes, reverse = True):
            del url_list[j]

if numForum > 0:
    filter_query_2 = pyip.inputStr("{} link(s) are Reddit/Quora, filter them out? (Y/N): ".format(numForum))
    if filter_query == "Y":
        for j2 in sorted(filter_indexes_2, reverse = True):
            del url_list[j2]

print("{} youtube links were removed from list".format(numYoutube))
print("{} forum links were removed from list".format(numForum))
print()
numLinks = len(url_list)
print("-------{} links have been loaded-------".format(numLinks))


#Update URL list and open pages
print()
numLinks = len(url_list)
numToOpen = pyip.inputInt("{} links are loaded, Enter # of links to open: ".format(numLinks), max=numLinks)
for k in range(numToOpen):
    urlToOpen = url_list[k]
    webbrowser.open(urlToOpen)
