"""実際にゲームするときに使うファイル"""

import PySimpleGUI as sg
import words
from wordle import Wordle
from frontend import GuiFrontEnd


class Game:
    """ゲームの進行とロジック"""

    def __init__(self, word_list):
        self.frontend = GuiFrontEnd()
        self.window = self.frontend.window()
        self.wordle = Wordle(word_list)
        self.turn = 1

    def get_row_by_turn(self, values: dict):
        """ターンに応じて行のvaluesを取得"""
        return dict(filter(lambda x: f'r{self.turn}' in x[0], values.items()))

    def count_up_turn(self):
        """ターンを一つ繰り上げる"""
        self.turn += 1

    @staticmethod
    def build_word_by_5chars(row: dict):
        """5文字の英単語を作成する"""
        word = ''
        for char in row.values():
            word += char
        return word

    @staticmethod
    def get_next_focus_input_key(key: str):
        """次のフォーカスのキーを返す"""
        row_num = int(key[1])
        col_num = int(key[-1])
        # 最後の場合は最初に戻る
        if col_num == 5:
            return f'r{row_num}c1'
        else:
            return f'r{row_num}c{col_num + 1}'

    @staticmethod
    def get_prev_focus_input_key(key: str):
        """前のフォーカスのキーを返す"""
        row_num = int(key[1])
        col_num = int(key[-1])
        # 最初の場合は最後に送る
        if col_num == 1:
            return f'r{row_num}c5'
        else:
            return f'r{row_num}c{col_num - 1}'

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

    def update_active_row_mark_by_turn(self):
        """現在入力中の行の表示を切りかえる"""
        for row_num in range(1, 7):
            color = 'white'
            # これから入力できる行
            if row_num == self.turn:
                color = 'green'
            # 入力済みの行
            elif row_num < self.turn:
                color = 'gray'
            key = f'row{row_num}'
            self.window[key].update(text_color=color)

    def update_widget(self, row: dict):
        for i, char in enumerate(row.values()):
            row_num = self.turn
            col_num = i + 1
            input_key = f'r{row_num}c{col_num}'
            pos = i

            if self.wordle.is_char_right_position(char, pos):
                bg_color = 'green'
            elif self.wordle.is_char_in_answer(char):
                bg_color = 'orange'
            else:
                bg_color = 'gray'

            # 既にgreenのものが上書きされないようにする
            self.window[input_key].Update(text_color='white', background_color=bg_color)
            c = self.window[char].ButtonColor
            if c[1] != 'green':
                self.window[char].Update(button_color=('white', bg_color))

    def refresh_game(self):
        """ゲームを初期化する"""

        # 入力マスを初期化
        for key in self.get_input_widget_key():
            disabled = False if 'r1' in key else True
            self.window[key].update('',
                                    text_color=self.frontend.color_input,
                                    background_color=self.frontend.color_input_background,
                                    disabled=disabled)
        # キーボードボタンを初期化
        for key in self.get_keyboard_key():
            self.window[key].update(button_color=self.frontend.color_keyboard)

        # リフレッシュ
        self.window.refresh()
        # 答えを新しくセット
        self.wordle.set_answer()
        # ターンを戻す
        self.turn = 1
        # 入力可能行マークを最初に
        self.update_active_row_mark_by_turn()
        # フォーカスを一番最初に
        self.window['r1c1'].SetFocus()

    def start_game(self):
        """ゲームスタート"""
        # wordleに答えをセット
        self.wordle.set_answer()
        keyboards_events = list(self.get_keyboard_key())

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            if event in keyboards_events:
                focus_input = self.window.find_element_with_focus()
                # 違うターンの場合は入力できない
                if f'r{self.turn}' not in focus_input.Key:
                    continue

                if focus_input:
                    focus_input.update(event)
                    next_key = self.get_next_focus_input_key(focus_input.Key)
                    self.window[next_key].SetFocus()

            # フォーカスされているマスを消去
            if event == 'BACK':
                focus_input = self.window.find_element_with_focus()
                focus_input.update('')

            # 前のマスに移動
            if event == 'PREV':
                focus_input = self.window.find_element_with_focus()
                prev_key = self.get_prev_focus_input_key(focus_input.Key)
                self.window[prev_key].SetFocus()

            # 次のマスに移動
            if event == 'NEXT':
                focus_input = self.window.find_element_with_focus()
                next_key = self.get_next_focus_input_key(focus_input.Key)
                self.window[next_key].SetFocus()

            if event == 'ENTER':
                row = self.get_row_by_turn(values)
                word = self.build_word_by_5chars(row)
                # 5文字入力されているかの確認
                if len(word) != 5:
                    continue

                # 入力値が単語リストに存在しなかったら次にいけない
                if not self.wordle.is_word_in_word_list(word):
                    self.frontend.popup_does_not_exist(word)
                    continue
                # widgetの更新
                self.update_widget(row)

                # wordが正解していたらゲーム終了
                if word == self.wordle.answer:
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

                # ターンを繰り上げる
                self.count_up_turn()
                # 入力可能行の色を切り替える
                self.update_active_row_mark_by_turn()
                # 次の行を入力可能にする
                row = self.get_row_by_turn(values)
                for key in row.keys():
                    self.window[key].Update(disabled=False)
                self.window[f'r{self.turn}c1'].set_focus()


def job():
    # 単語リストを取得
    word_list = words.get_word_list()
    game = Game(word_list)
    # ゲーム開始
    game.start_game()


if __name__ == '__main__':
    job()
