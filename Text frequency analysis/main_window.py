import sys
import matplotlib
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from typing import List

from PyQt5 import uic, QtWidgets

from data.books import Books
from data.colors_and_styles import PlotColorsAndTypes

from src.pandas_model import TableModel
from src.scraper import GutenbergScraper
from src.process_text import TextAnalyser
from src.plotter import Plotter

uimain = 'ui/qt_app.ui'
form, base = uic.loadUiType(uifile=uimain)
matplotlib.use("QT5Agg")


class MainWindow(form, base):

    def __init__(self):

        super(base, self).__init__()
        self.setupUi(self)

        self.__set_default_values()

        self.__connect_canvas()
        self.__connect_comboboxes()
        self.__connect_buttons()

        self.chosen_book_link = Books.books_dict['Thus Spake Zarathustra: A Book for All and None']
        self.plot_color = "blue"
        self.plot_style = "seaborn"
        self.counted_data = None

    def __set_default_values(self):

        self.first_n_frequent_words_spinbox.setValue(75)
        self.first_n_frequent_words_spinbox.setMinimum(1)
        self.first_n_frequent_words_spinbox.setMaximum(500)

        self.available_texts_combobox.addItems(
            Books.books_dict
        )
        self.available_texts_combobox.setCurrentText(
            'Thus Spake Zarathustra: A Book for All and None'
        )

        self.plot_color_combobox.addItems(
            PlotColorsAndTypes.colors
        )
        self.plot_color_combobox.setCurrentText(
            'blue'
        )

        self.plot_styles_combobox.addItems(
            PlotColorsAndTypes.matplotlib_plot_styles
        )
        self.plot_styles_combobox.setCurrentText(
            'seaborn'
        )

    def __connect_buttons(self):

        self.start_button.clicked.connect(
            self.process_start_button_click
        )
        self.sort_table_by_words_button.clicked.connect(
            self.process_sort_request_by_words
        )
        self.sort_by_frequency_asc_button.clicked.connect(
            self.process_sort_by_freq_asc_button_click
        )
        self.sort_by_frequency_desc_button.clicked.connect(
            self.process_sort_by_freq_desc_button_click
        )

    def __connect_comboboxes(self):

        self.available_texts_combobox.activated[str].connect(
            self.set_book
        )
        self.plot_color_combobox.activated[str].connect(
            self.set_plot_color
        )
        self.plot_styles_combobox.activated[str].connect(
            self.set_plot_style
        )

    def __connect_canvas(self):

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        lay = QtWidgets.QVBoxLayout(self.plot_widget)
        lay.addWidget(self.toolbar)
        lay.addWidget(self.canvas)

    def update_table(self, datatable: pd.DataFrame) -> None:
        model = TableModel(datatable)
        self.table_view.setModel(model)

    def set_plot_color(self, color_):
        self.plot_color = color_

    def set_plot_style(self, style_):
        self.plot_style = style_

    def set_book(self, book_name):
        self.chosen_book_link = Books.books_dict[book_name]
        # print(f'{book_name}\n{self.chosen_book_link}')

    def process_start_button_click(self):

        requested_text: str | None = GutenbergScraper.pull_text(self.chosen_book_link)

        if requested_text is None:
            return

        filtered: List[str] = TextAnalyser.filter(requested_text)

        self.counted_data: pd.DataFrame = TextAnalyser.count_freq(
            filtered,
            self.first_n_frequent_words_spinbox.value()
        )

        self.update_table(self.counted_data)

        Plotter.plot_freq(
            self.counted_data,
            self.figure,
            self.canvas,
            self.plot_color,
            self.plot_style
        )

    def process_sort_request_by_words(self):

        s_bw: pd.DataFrame = self.counted_data.sort_values(by='Words')

        self.update_table(
            s_bw
        )
        Plotter.plot_freq(
            s_bw,
            self.figure,
            self.canvas,
            self.plot_color,
            self.plot_style
        )

    def process_sort_by_freq_asc_button_click(self):

        s_asc: pd.DataFrame = self.counted_data.sort_values(by='Count')

        self.update_table(
            s_asc
        )
        Plotter.plot_freq(
            s_asc,
            self.figure,
            self.canvas,
            self.plot_color,
            self.plot_style
        )

    def process_sort_by_freq_desc_button_click(self):

        s_desc: pd.DataFrame = self.counted_data.sort_values(by='Count', ascending=False)

        self.update_table(
             s_desc
        )
        Plotter.plot_freq(
            s_desc,
            self.figure,
            self.canvas,
            self.plot_color,
            self.plot_style
        )


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
