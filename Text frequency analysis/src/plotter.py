import matplotlib.pyplot as plt
import pandas as pd


class Plotter:

    @staticmethod
    def plot_freq(wfs: pd.DataFrame, figure, canvas, color_, style):

        figure.clf()

        plt.style.use(style)
        plt.barh(wfs['Words'], wfs['Count'], color=color_)
        plt.tight_layout()

        canvas.draw()