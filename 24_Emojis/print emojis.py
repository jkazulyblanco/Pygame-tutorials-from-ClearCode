from emoji import emojize
import requests # get data from web site
from bs4 import BeautifulSoup as bs # read file form web

def get_emoji_data():
    session = requests.Session()
    session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    html = session.get('https://carpedm20.github.io/emoji/')

    # create a soup
    soup = bs(html.text, 'html.parser')
    emoji_list = []
    for row in soup.findAll('table')[0].findAll('tr')[2:-1]:
        entry = ':' + row.text.split(':')[1] + ':'
        emoji_list.append(entry)
    return sorted(emoji_list)

all_emojis = get_emoji_data()

# selected by number
num = 378
print(emojize(all_emojis[num]))
print(all_emojis[num])


# Print all emojis
for emoji in all_emojis:
    print(emojize(emoji), end= ' ')
    print(emoji, end= ' ')
