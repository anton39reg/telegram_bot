import telebot
import urllib.request
from bs4 import BeautifulSoup


def show_new_films(self):
    result = []
    page = urllib.request.urlopen('https://www.kinopoisk.ru/afisha/new/city/6126/')
    soup = BeautifulSoup(page, 'lxml')
    films = soup.find_all('div', attrs={"item"})
    for film in films:
        name = film.find('div', class_='name').find('a').text
        link = 'https://www.kinopoisk.ru' + film.find('div', class_='name').find('a').get('href')
        director = film.find('div', class_='gray').find('a').text
        try:
            rating = film.find('div', class_='rating').find('span').text
        except AttributeError:
            rating = '----'
        result.append((name, director, rating, link))
    return result


def find_film(self, name):
    find = name.replace(' ', '%20')
    page = 'https://www.kinopoisk.ru/index.php?kp_query='+find+'&what='
    film = urllib.request.urlopen(page)
    film_soup = BeautifulSoup(film, 'lxml')
    result = film_soup.find('div', class_='element most_wanted')
    
    if result:
        link = result.find('p', class_='name').find('a').get('data-url')
        film = result.find('p', class_='name').find('a').text
        year = result.find('p', class_='name').find('span').text
        director = result.find('i', class_='director').find('a').text
        rating = result.find('div', class_='rating ratingGreenBG').text
        info = 'https://www.kinopoisk.ru'+link
        info += ('\n' + film + ';\n' + year + ';\nРежиссёр - ' +  director + ';\nРейтинг - ' + rating + ';\n')
        return info
    else:
        info = 'Извини, я ничего не нашёл('
        return info


telebot.TeleBot.find_film = find_film
telebot.TeleBot.show_new_films = show_new_films


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
        films = bot.show_new_films()
        result = str()
        for elem in films:
            result += (elem[0] + ';\nрежиссёр - ' + elem[1] + ';\nрейтинг - ' + elem[2]
                       + ';\n' + elem[3])
            result += '\n\n'
        bot.send_message(message.from_user.id, result)
    elif message.text[:10] == '/show_film':
        try:
            result = bot.find_film(message.text[11:])
            bot.send_message(message.from_user.id, result)
        except UnicodeEncodeError:
            bot.send_message(message.from_user.id, 'Используй, пожалуйста, английское название фильма')
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши /help")


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, timeout=0)
        except Exception:
            pass
