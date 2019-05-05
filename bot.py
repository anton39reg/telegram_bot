import telebot


class Bot:
    bot = telebot.TeleBot('889866095:AAEK8yduZz8nWky-bJW_FkVVuXeAkBL5oNk')

    @bot.message_handler(content_types=["text"])
    def handle_text(self, message):
        if message.text == "Привет":
            bot.send_message(message.from_user.id, "Привет! Напиши /help, чтобы узнать, что я умею")

        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Извини, но я ещё ничего не умею))")

        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши /help")

    def run(self):
        try:
            self.bot.polling(none_stop=True, timeout=1)
        except Exception:
            pass


if __name__ == '__main__':
    bot = Bot()
    bot.run()
