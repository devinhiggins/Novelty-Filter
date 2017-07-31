import plotly.plotly as py
from sklearn.metrics import mean_squared_error
from math import sqrt
from plotly.graph_objs import *


def marker(**kwargs):
    """Pass marker arguments."""
    return Marker(kwargs)


def line(**kwargs):
    """Pass line arguments."""
    return Line(kwargs)


class PlotlyGraph(object):
    """Create plotly graphs."""

    def __init__(self):
        """Establish graph object."""
        self.traces = []

    def plot(self):
        """Plot all traces that have been set, using layout."""
        data = Data([t for t in self.traces])
        figure = Figure(data=data, layout=self.layout)
        py.iplot(figure)

    def set_layout(self, xaxis={}, yaxis={}, title=""):
        """Establish basic graph layout.

        kwargs:
            xaxis(dict): set of arguments to pass to the xaxis parameter of layout
            yaxis(dict): set of arguments to pass to the yaxis parameter of layout
            title(str): title to display on graph
        """
        self.layout = Layout(title=title,
                             xaxis=XAxis(**xaxis),
                             yaxis=YAxis(**yaxis)
                             )

    def set_scatter(self, **kwargs):
        """Set graph data to appear on graph -- can be called multiple times.

        Some valid kwargs below.

        kwargs:
            xdata(str): array of x values
            ydata(str): array of y values
            mode(str): mode of display, e.g. "lines" or "markers"
            dtype(str): object with parameters corresponding to the mode.
            marker(plotly object): containing data about the display of the trace.
            name(str): name to display for this trace.
        """
        scatter = Scatter(kwargs)
        self.traces.append(scatter)

    def set_line(self, **kwargs):
        """Set graph data to appear on graph -- can be called multiple times.

        Some valid kwargs below.

        kwargs:
            xdata(str): array of x values
            ydata(str): array of y values
            mode(str): mode of display, e.g. "lines" or "markers"
            dtype(str): object with parameters corresponding to the mode.
            line(plotly object): containing data about the display of the trace.
            name(str): name to display for this trace.
        """
        scatter = Scatter(kwargs)
        self.traces.append(scatter)

    def get_rmse(self, y_obs, y_pred):
        """Calculate root mean square error.

        args:
            xdata(array): array of independent variable values
            y_obs(array): array of observed values
            y_pred(array): array of predicted values based on fitted curve.
        """
        return sqrt(mean_squared_error(y_obs, y_pred))
