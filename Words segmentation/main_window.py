import sys
import pandas as pd
import random

# noinspection PyUnresolvedReferences
from PyQt5 import uic, QtWidgets
from typing import List

from data.authors_and_books import TextData
from src.pandas_model import TableModel
from src.rws_model import RWSModel
from src.pws_model import PWSModel

main_window_ui = 'ui/main_window.ui'
form, base = uic.loadUiType(uifile=main_window_ui)


class MainWindow(form, base):

    def __init__(self):

        self.current_author = ''
        self.current_book = ''
        self.sep = '-'*164
        self.text_data = TextData()

        self.sentences_df = pd.DataFrame()

        super(base, self).__init__()
        self.setupUi(self)

        self.__connect_widgets()
        self.__set_default_values()

    def __connect_widgets(self):

        self.start_button.clicked.connect(
            self.process_start_button_click
        )

        self.authors_combo_box.activated[str].connect(
            self.get_current_author
        )
        self.books_combo_box.activated[str].connect(
            self.get_current_book
        )

    def __set_default_values(self):

        default_author: str = 'Franz Kafka'

        self.current_author = default_author
        self.current_book = self.text_data.get_books(default_author)[0]

        self.authors_combo_box.addItems(
            self.text_data.get_authors()
        )

        self.authors_combo_box.setCurrentText(
            default_author
        )
        self.books_combo_box.addItems(
            self.text_data.get_books(default_author)
        )

        self.rws_iteration_amount.setMinimum(100)
        self.rws_iteration_amount.setMaximum(15000)
        self.rws_iteration_amount.setValue(5000)

        self.rws_cooling_rate.setMinimum(0.01)
        self.rws_cooling_rate.setMaximum(100.0)
        self.rws_cooling_rate.setValue(1.2)

        self.rws_border_value.setMinimum(0.01)
        self.rws_border_value.setMaximum(10.0)
        self.rws_border_value.setValue(0.5)

        self.seg_one_freq_spinbox.setMinimum(1)
        self.seg_one_freq_spinbox.setMaximum(100)
        self.seg_one_freq_spinbox.setValue(3)

    def __update_books(self, new_author: str):

        self.books_combo_box.clear()
        self.books_combo_box.addItems(
            self.text_data.get_books(new_author)
        )

    def __prep_sentences_table(self, sentences: List[str]) -> TableModel:

        sl = len(sentences)
        self.melted = [s.replace(' ', '') for s in sentences]

        self.sentences_df = pd.DataFrame(
            zip(sentences, [self.current_author] * sl, [self.current_book] * sl),
            columns=['Sentence', 'Author', 'Book'],
            index=range(1, sl+1)
        )

        self.sentences_df.index.names = ['Sentence №']
        self.sentences_df.reset_index(level=0, inplace=True)

        return TableModel(self.sentences_df)

    def __update_sentences_table(self):

        sentences = self.text_data.get_sentences(
            self.current_author,
            self.current_book
        )

        table_model: TableModel = self.__prep_sentences_table(sentences)

        self.sentences_table.setModel(table_model)
        self.sentences_table.resizeColumnsToContents()
        self.sentences_table.resizeRowsToContents()

        horizontal_header = self.sentences_table.horizontalHeader()
        horizontal_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        horizontal_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        vertical_header = self.sentences_table.verticalHeader()
        vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        vertical_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def __update_rws_text_edit(self):
        rws_data = RWSModel(
            self.rws_border_value.value(),
            self.rws_cooling_rate.value(),
            self.rws_iteration_amount.value()
        )

        attempts = []

        for s in self.sentences_df['Sentence']:

            starting_seg = '0' * len(s)
            # starting_seg = ''.join(random.choice('10') for _ in range(len(s)))

            randomness = self.seg_one_freq_spinbox.value()
            for i in range(randomness):
                random_integer = random.randint(1, len(s) - 1)
                starting_seg = starting_seg[:random_integer] + '1' + starting_seg[random_integer+1:]

            print(f'segmentation \n{starting_seg}\nfor sentence \n{s}\n')

            s = s.replace(' ', '')
            attempts.append(
                rws_data.anneal(starting_seg, s)
            )

        s = ''
        for record in attempts:
            for k, v in record.items():
                s += f'{self.sep}\nSCORE: {k}' \
                     f'\nVALUE: {str(v)}' \
                     f'\n{self.sep}\n\n'

        self.rws_text_edit.setPlainText(s)

    def __update_pws_text_edit(self):
        pws_model = PWSModel()
        answers = []

        for s in self.sentences_df['Sentence']:
            s = s.replace(' ', '')
            print(s)
            answers.append(
                pws_model.segment(s)
            )

        s = ''
        for number, ans in enumerate(answers):
            s += f'{self.sep}SENTENCE № {number + 1}\n{str(ans)}\n{self.sep}\n\n'

        self.pws_text_edit.setPlainText(s)

    def get_current_author(self, author_: str) -> None:
        self.current_author = author_
        self.__update_books(author_)

    def get_current_book(self, book_: str) -> None:
        self.current_book = book_

    def process_start_button_click(self):
        self.__update_sentences_table()
        self.__update_rws_text_edit()
        self.__update_pws_text_edit()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
