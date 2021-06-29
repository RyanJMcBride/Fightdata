import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

result = requests.get("http://ufcstats.com/statistics/events/completed?page=all") #USE PAGE WITH ALL EVENTS NOT PAGINATION
print(result.status_code)
src = result.content
soup = BeautifulSoup(src,'lxml')
eventname = []
links = soup.find_all("a")
hyperlinks = []
del links[0:7]
del links[(len(links)-16): (len(links))]
for link in links:
    linka = link.text.replace('\n                          ','')
    linkb = linka.replace('\n                        ','')
    eventname.append(linkb)
    hyperlinks.append(link.attrs['href'])
findspan = soup.find_all('span')
findspantext= []
finspantext1 = []
date = []
for i in range(len(findspan)):
    findspantext = findspan[i].text.replace('\n                          ', '')
    findspantext1 = findspantext.replace('\n                        ', '')
    date.append(findspantext1)
dateformatted= []
date.remove(date[-1])      #removing first and last dates as they are not part of the data
date.remove(date[0])
for i in range(len(date)):
    fdate = date[i]
    d = datetime.strptime(fdate, '%B %d, %Y')
    dateformatted.append(d.strftime('%Y-%m-%d'))
f1 = []
f2 = []
win = []
draw = []
nc = []
datefinal = []
eventfinal = []
count = 0

for link in hyperlinks:

    eventtemp = eventname[count]
    datetemp = dateformatted[count]
    count = count + 1

    eventreq = requests.get(link)
    eventsrc = eventreq.content
    eventsoup = BeautifulSoup(eventsrc, 'lxml')

    fightbranch = eventsoup.body.table.tbody.find_all('tr')

    if (eventreq.status_code != '200'):

        for i in range(len(fightbranch)):

            databranch = fightbranch[i].find_all('td')
            databranch1 = databranch[1]
            pbranch = databranch1.find_all('p')
            f1branch = pbranch[0].text
            f2branch = pbranch[1].text
            f1.append(f1branch)
            f2.append(f2branch)
            datefinal.append(datetemp)
            eventfinal.append(eventtemp)

            if (fightbranch[i].td.p.a.text == 'win'):

                win.append('1')
                draw.append('0')
                nc.append('0')

            elif (fightbranch[i].td.p.a.text == 'draw'):

                win.append('0')
                draw.append('1')
                nc.append('0')

            elif (fightbranch[i].td.p.a.text == 'nc'):

                win.append('0')
                draw.append('0')
                nc.append('1')

            else:

                print('not win, draw or nc')

    else:

        print('link didnt work')
for i in range(len(f1)):
    f1[i] = f1[i].replace('\n\n              ','')
    f1[i] = f1[i].replace('\n            \n','')
    f2[i] = f2[i].replace('\n\n              ','')
    f2[i] = f2[i].replace('\n            \n','')
UFC_Data = pd.DataFrame({'Date': datefinal, 'Event': eventfinal, 'F1': f1, 'F2': f2 ,'win': win, 'draw': draw, 'nc': nc})
UFC_Data.to_csv('UFC_Fight_Data_new.csv', index = False)
