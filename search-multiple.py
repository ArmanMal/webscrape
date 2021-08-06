import webbrowser, bs4, pyinputplus as pyip
from googlesearch import search


#Fetch URLs for query
query = pyip.inputStr('Search: ')
numOpen = pyip.inputInt('Number of links: ')

url_list = []
sub_links = 0
ytube_links = 0
for i in search(query, tld= "co.in", num = numOpen, stop = numOpen, pause = .200):
    if len(url_list) > 0:
        if url_list[-1] in i:
            sub_links += 1
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

#Open pages
print()
numToOpen = pyip.inputInt("Enter # of links to open: ", max=len(url_list))
for k in range(numToOpen):
    webbrowser.open(url_list[k])
exit()
