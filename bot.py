import telebot
import urllib.request
from bs4 import BeautifulSoup


def show_new_films():
    res = []
    page = urllib.request.urlopen('https://www.kinopoisk.ru/afisha/new/city/6126/')
    soup = BeautifulSoup(page, 'lxml')
    films = soup.find_all('div', attrs={"item"})
    for ref in films:
        name = ref.find('div', class_='name').find('a').text
        link = 'https://www.kinopoisk.ru' + ref.find('div', class_='name').find('a').get('href')
        director = ref.find('div', class_='gray').find('a').text
        try:
            rating = ref.find('div', class_='rating').find('span').text
        except AttributeError:
            rating = '----'
        res.append((name, director, rating, link))
    return res


def find_film(name):
    find = name.replace(' ', '%20')
    t = 'https://www.kinopoisk.ru/index.php?kp_query='+find+'&what='
    film = urllib.request.urlopen(t)

    film_soup = BeautifulSoup(film, 'lxml')
    res = film_soup.find('div', class_='element most_wanted')
    if res:
        link = res.find('p', class_='name').find('a').get('data-url')
        film = res.find('p', class_='name').find('a').text
        year = res.find('p', class_='name').find('span').text
        director = res.find('i', class_='director').find('a').text
        rating = res.find('div', class_='rating ratingGreenBG').text
        info = 'https://www.kinopoisk.ru'+link
        info += (film + ';\n' + year + ';\nРежиссёр - ' +  director + ';\nРейтинг - ' + rating + ';\n')
        return info
    else:
        info = 'Извини, я ничего не нашёл('
        return info



bot = telebot.TeleBot('889866095:AAEK8yduZz8nWky-bJW_FkVVuXeAkBL5oNk')





@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id,
                         """Привет! Напиши /help, чтобы узнать, что я умею""")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Рад видеть, что ты заинтересовался.\n"
                         "Напиши /new_films и я покажу фильмы, которые сейчас показывают в кинотеатрах.\n"
                         "Напиши /show_film 'yourfilm' и я постараюсь найти информацию о нём."
                         " Только использую анлийское название фильма")
    elif message.text == "/new_films":
        films = show_new_films()
        res = str()
        for elem in films:
            res += (elem[0] + ';\nрежиссёр - ' + elem[1] + ';\nрейтинг - ' + elem[2]
                    + ';\n' + elem[3])
            res += '\n\n'
        bot.send_message(message.from_user.id, res)
    elif message.text[:10] == '/show_film':
        try:
            res = find_film(message.text[11:])
            bot.send_message(message.from_user.id, res)
        except UnicodeEncodeError:
            bot.send_message(message.from_user.id, 'Используй, пожалуйста, английское название фильма')
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши /help")


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=0)
    except Exception:
        pass
