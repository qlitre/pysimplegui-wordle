"""実際にゲームするときに使うファイル"""

import PySimpleGUI as sg
import words
from wordle import Wordle
from frontend import GuiFrontEnd


class Game:
    """ゲームの進行とロジック"""

    def __init__(self, word_list: list):
        self.frontend = GuiFrontEnd()
        self.window = self.frontend.window()
        self.wordle = Wordle(word_list)
        self.turn = 1

    @staticmethod
    def get_input_widget_key():
        """入力widgetのキーをyieldして返す"""
        for r in range(1, 7):
            for c in range(1, 6):
                key = f'r{r}c{c}'
                yield key

    @staticmethod
    def get_keyboard_key():
        """キーボードwidgetのキーをyieldして返す"""
        chars = "QWERTYUIOPASDFGHJKLZXCVBNM"
        for c in chars:
            yield c

    def filter_values_by_turn(self, values: dict):
        """ターンに応じてvaluesをフィルタ"""
        return dict(filter(lambda x: f'r{self.turn}' in x[0], values.items()))

    def get_word_by_5chars(self, values: dict):
        """5文字の英単語を作成する"""
        row = self.filter_values_by_turn(values)
        word = ''
        for char in row.values():
            word += char
        return word

    def set_focus_next(self, key: str):
        """次のキーにフォーカスする"""
        row_num = int(key[1])
        col_num = int(key[-1])
        if col_num == 5:
            next_key = f'r{row_num}c1'
        else:
            next_key = f'r{row_num}c{col_num + 1}'
        self.window[next_key].SetFocus()

    def set_focus_prev(self, key: str):
        """前のフォーカスのキーを返す"""
        row_num = int(key[1])
        col_num = int(key[-1])
        if col_num == 1:
            prev_key = f'r{row_num}c5'
        else:
            prev_key = f'r{row_num}c{col_num - 1}'
        self.window[prev_key].SetFocus()

    def clear_row(self, values: dict):
        """入力されている行をクリア"""
        row = self.filter_values_by_turn(values)
        for key in row.keys():
            self.window[key].update('')

        self.window[f'r{self.turn}c1'].SetFocus()

    def update_active_row_mark_color(self):
        """入力可能行表示マークの色をアップデート"""
        for row_num in range(1, 7):
            color = 'white'
            if row_num == self.turn:
                color = 'green'
            elif row_num < self.turn:
                color = 'gray'
            key = f'row{row_num}'
            self.window[key].update(text_color=color)

    def update_widget_bg_color(self, guess: str):
        """答えが入力された後のウィジェットの色を変える処理"""
        response = self.wordle.get_hint(guess)
        for r in response:
            pos = r['pos']
            input_key = f'r{self.turn}c{pos}'
            bg_color = r['hint']

            # 入力ボックス
            self.window[input_key].Update(text_color='white',
                                          background_color=bg_color)
            # キーボードボタン
            char = r['char']
            c = self.window[char].ButtonColor

            # 既に緑は上書きされないように
            if 'green' in c:
                continue

            # 既にオレンジのボタンが灰色に上書きされないように
            if 'orange' in c and bg_color == 'gray':
                continue
            self.window[char].Update(button_color=('white', bg_color))

    def goto_next_turn(self, values: dict):
        """次のターンに移行"""
        self.turn = self.turn + 1
        row = self.filter_values_by_turn(values)
        self.update_active_row_mark_color()
        for key in row.keys():
            self.window[key].Update(disabled=False)
        self.window[f'r{self.turn}c1'].set_focus()

    def refresh_game(self):
        """ゲームを初期化する"""

        # 入力マスを初期化
        for key in self.get_input_widget_key():
            disabled = False if 'r1' in key else True
            self.window[key].update('',
                                    text_color=self.frontend.input_box_color,
                                    background_color=self.frontend.input_box_color_bg,
                                    disabled=disabled)
        # キーボードボタンを初期化
        for key in self.get_keyboard_key():
            self.window[key].update(button_color=self.frontend.keyboard_btn_color)

        self.window.refresh()
        self.wordle.set_answer()
        self.turn = 1
        self.update_active_row_mark_color()
        self.window['r1c1'].SetFocus()

    def start_game(self):
        """ゲームスタート"""
        self.wordle.set_answer()
        keyboards_events = list(self.get_keyboard_key())
        input_box_event = list(self.get_input_widget_key())

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            focus_input = self.window.find_element_with_focus()

            if event in input_box_event:
                char = values[event]
                self.window[event].update(char.upper())

            if event in keyboards_events:
                # 違うターンのマスは入力できない
                if f'r{self.turn}' not in focus_input.Key:
                    continue
                focus_input.update(event)
                self.set_focus_next(key=focus_input.Key)

            if event == 'BACK':
                focus_input.update('')

            if event == 'PREV':
                self.set_focus_prev(key=focus_input.Key)

            if event == 'NEXT':
                self.set_focus_next(key=focus_input.Key)

            if event == 'CLEAR':
                self.clear_row(values)

            if event == 'ENTER':
                guess = self.get_word_by_5chars(values=values)

                if len(guess) != 5:
                    continue

                # 入力値が単語リストに存在しなかったら次にいけない
                if not self.wordle.is_word_in_word_list(guess=guess):
                    self.frontend.popup_does_not_exist(word=guess)
                    continue

                # widgetの背景を更新
                self.update_widget_bg_color(guess=guess)

                # wordが正解していたらゲームクリア
                if self.wordle.is_word_collect(guess=guess):
                    res = self.frontend.popup_congratulation()
                    if res == 'OK':
                        self.refresh_game()
                        continue
                    else:
                        self.frontend.popup_see_you_later()
                        break

                # 正解していなくて既に6ターン目だったらゲームオーバー
                if self.turn == 6:
                    res = self.frontend.popup_game_over(answer=self.wordle.answer)
                    if res == 'OK':
                        self.refresh_game()
                        continue
                    else:
                        self.frontend.popup_see_you_later()
                        break

                self.goto_next_turn(values=values)


def job():
    word_list = words.get_word_list()
    game = Game(word_list)
    game.start_game()


if __name__ == '__main__':
    job()
