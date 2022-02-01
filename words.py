"""wordle.txtからwordリストを返す"""


def generate_word():
    with open('wordle.txt') as f:
        for word in f:
            yield word.strip().upper()


def get_word_list():
    return [word for word in generate_word()]
