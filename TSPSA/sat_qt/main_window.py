import random
import sys
import matplotlib
import matplotlib.gridspec as gridspec

from matplotlib import pyplot as plt
# noinspection PyUnresolvedReferences
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# noinspection PyUnresolvedReferences
from PyQt5 import uic, QtWidgets

from src.anneal import SimAnneal
from src.visualize_tsp import TSPPlotter

from src.defaults import Defaults
from src.pandas_model import TableModel

uiapp = 'ui/qt_app.ui'
form, base = uic.loadUiType(uifile=uiapp)
matplotlib.use("QT5Agg")


class MainWindow(form, base):

    def __init__(self):

        super(base, self).__init__()
        self.setupUi(self)

        self.point_color = 'cyan'
        self.vector_color = 'blue'
        self.temperature_color = 'red'
        self.fitness_color = 'blue'

        self.__set_default_values()
        self.__connect_canvas()
        self.__connect_buttons()
        self.__connect_combo_boxes()

    def __set_default_values(self):

        self.iterations_spinbox.setMinimum(Defaults.MIN_ITERATIONS)
        self.iterations_spinbox.setMaximum(Defaults.MAX_ITERATIONS)
        self.iterations_spinbox.setValue(Defaults.DEFAULT_ITERATIONS_AMOUNT)

        self.amount_of_points_spinbox.setMinimum(Defaults.MIN_AMOUNT_OF_POINTS)
        self.amount_of_points_spinbox.setMaximum(Defaults.MAX_AMOUNT_OF_POINTS)
        self.amount_of_points_spinbox.setValue(Defaults.DEFAULT_AMOUNT_OF_POINTS)

        self.interval_left_value_double_spinbox.setMinimum(Defaults.MIN_INTERVAL_VALUE)
        self.interval_left_value_double_spinbox.setMaximum(Defaults.MAX_INTERVAL_VALUE)
        self.interval_left_value_double_spinbox.setValue(Defaults.DEFAULT_INTERVAL_LEFT_BOUND)

        self.interval_right_value_double_spinbox.setMinimum(Defaults.MIN_INTERVAL_VALUE)
        self.interval_right_value_double_spinbox.setMaximum(Defaults.MAX_INTERVAL_VALUE)
        self.interval_right_value_double_spinbox.setValue(Defaults.DEFAULT_INTERVAL_RIGHT_BOUND)

        self.animation_delay_double_spinbox.setMinimum(Defaults.MIN_TSP_ANIMATION_DELAY)
        self.animation_delay_double_spinbox.setMaximum(Defaults.MAX_TSP_ANIMATION_DELAY)
        self.animation_delay_double_spinbox.setValue(Defaults.TSP_ANIMATION_DELAY)

        self.point_color_combo_box.addItems(Defaults.COLORS)
        self.point_color_combo_box.setCurrentText(self.point_color)

        self.vector_color_combo_box.addItems(Defaults.COLORS)
        self.vector_color_combo_box.setCurrentText(self.vector_color)

        self.temperature_color_combo_box.addItems(Defaults.COLORS)
        self.temperature_color_combo_box.setCurrentText(self.temperature_color)

        self.fitness_color_combo_box.addItems(Defaults.COLORS)
        self.fitness_color_combo_box.setCurrentText(self.fitness_color)

    def __connect_buttons(self):

        self.start_button.clicked.connect(
            self.__process_start_button_clicked
        )

    def __connect_combo_boxes(self):

        self.point_color_combo_box.activated[str].connect(
            self.__set_point_color
        )

        self.vector_color_combo_box.activated[str].connect(
            self.__set_vector_color
        )

        self.temperature_color_combo_box.activated[str].connect(
            self.__set_temerature_color
        )

        self.fitness_color_combo_box.activated[str].connect(
            self.__set_fitness_color
        )

    def __set_point_color(self, color: str):
        self.point_color = color

    def __set_vector_color(self, color: str):
        self.vector_color = color

    def __set_temerature_color(self, color: str):
        self.temperature_color = color

    def __set_fitness_color(self, color: str):
        self.fitness_color = color

    def __connect_canvas(self):

        self.figure = plt.figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.gs = gridspec.GridSpec(3, 3)

        lay = QtWidgets.QVBoxLayout(self.plot_widget)
        lay.addWidget(self.toolbar)
        lay.addWidget(self.canvas)

        self.plotter = TSPPlotter(self.figure)

    @staticmethod
    def generate_random_coords(r, l, num_nodes):
        return [[random.uniform(r, l), random.uniform(r, l)] for _ in range(num_nodes)]

    def __prep_table(self, results):

        table_model = TableModel(results)

        self.results_table.setModel(table_model)
        self.results_table.resizeColumnsToContents()
        self.results_table.resizeRowsToContents()

        horizontal_header = self.results_table.horizontalHeader()
        horizontal_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        horizontal_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        vertical_header = self.results_table.verticalHeader()
        vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        vertical_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

    def __process_start_button_clicked(self):

        iter_num = self.iterations_spinbox.value()
        points_num = self.amount_of_points_spinbox.value()
        interval_left_border = self.interval_left_value_double_spinbox.value()
        interval_right_border = self.interval_right_value_double_spinbox.value()
        animation_delay = self.animation_delay_double_spinbox.value()

        coords = self.generate_random_coords(
            interval_right_border,
            interval_left_border,
            points_num
        )

        sa = SimAnneal(coords, stopping_iter=iter_num)
        sa.anneal()

        results = sa.get_results()
        self.__prep_table(results)

        self.figure.clf()

        self.plotter.plot_temperature(sa.temperature_list, self.temperature_color)
        self.plotter.plot_learning(sa.fitness_list, self.fitness_color)
        self.plotter.visualize_routes([sa.best_solution],
                                      sa.coords,
                                      animation_delay,
                                      self.point_color,
                                      self.vector_color)

        self.canvas.draw()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
