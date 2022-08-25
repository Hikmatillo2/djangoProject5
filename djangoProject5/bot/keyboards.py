from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, text: list, width: int = 2):
        super().__init__()
        self.text = text
        self.row_width = width
        self.make_keyboard()

    def make_keyboard(self):
        for text in self.text:
            if type(text[0]) == list:
                self.row(*[InlineKeyboardButton(text_[0], callback_data=text_[1]) for text_ in text])
            elif 'http' in text[1]:
                self.add(InlineKeyboardButton(text[0], url=text[1]))
            else:
                self.add(InlineKeyboardButton(text[0], callback_data=text[1]))
