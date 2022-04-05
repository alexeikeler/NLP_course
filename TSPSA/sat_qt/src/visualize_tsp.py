import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class TSPPlotter:

    def __init__(self, qtfigure):
        self.fig = qtfigure
        self.gs = gridspec.GridSpec(3, 3)

    def visualize_routes(self, paths, points, delay, points_color, vector_color, num_iters=1):

        """
        path: List of lists with the different orders in which the nodes are visited
        points: coordinates for the different nodes
        num_iters: number of paths that are in the path list
        """

        # Unpack the primary TSP path and transform it into a list of ordered
        # coordinates
        ax = self.fig.add_subplot(self.gs[:, :2])

        x = []
        y = []
        for i in paths[0]:
            x.append(points[i][0])
            y.append(points[i][1])

        ax.plot(x, y, 'o', color=points_color)

        # Set a scale for the arrow heads
        a_scale = float(max(x))/float(50)

        # Draw the older paths, if provided
        if num_iters > 1:

            for i in range(1, num_iters):

                # Transform the old paths into a list of coordinates
                xi = []; yi = [];
                for j in paths[i]:
                    xi.append(points[j][0])
                    yi.append(points[j][1])

                ax.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]),
                        head_width = a_scale, color = vector_color,
                        length_includes_head = True, ls = 'dashed',
                        width = 0.001/float(num_iters))
                for i in range(0, len(x) - 1):
                    ax.arrow(xi[i], yi[i], (xi[i+1] - xi[i]), (yi[i+1] - yi[i]),
                            head_width = a_scale, color = vector_color, length_includes_head = True,
                            ls = 'dashed', width = 0.001/float(num_iters))

        # Draw the primary path for the TSP problem
        ax.arrow(x[-1], y[-1],
                 (x[0] - x[-1]),
                 (y[0] - y[-1]),
                 head_width = a_scale,
                 color=vector_color,
                 length_includes_head=True)

        for i in range(0,len(x)-1):
            ax.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]),
                     head_width=a_scale, color=vector_color, length_includes_head=True)

            plt.gcf().canvas.draw_idle()
            plt.gcf().canvas.start_event_loop(delay)

        # Set axis too slitghtly larger than the set of x and y
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.relim()

    def plot_temperature(self, temperature_list, color: str):

        ax = self.fig.add_subplot(self.gs[2, 2])
        ax.plot(temperature_list, color=color)
        ax.set_ylabel('Temperature')
        ax.set_xlabel('Iteration')
        ax.grid()

    def plot_learning(self, fitness_list, color):

        ax = self.fig.add_subplot(self.gs[:2, 2:3])
        ax.plot([i for i in range(len(fitness_list))], fitness_list, color=color)
        ax.set_ylabel('Score')
        ax.set_xlabel('Iteration')
        ax.grid()
