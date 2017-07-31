from __future__ import division
import nltk
import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
import string
import codecs

py.sign_in("msunovelty", "ftnj6jov5q")


def lexical_diversity(path):
    """Get lexical diversity for text located at path.

    args:
        path(str): absolute address of text.
    """
    text = get_text(path)
    tokens = [word.lower() for word in nltk.word_tokenize(text)]
    ld = len(set(tokens)) / len(tokens)
    return round(ld, 3)


def get_text(path):
    """Extract text from file.

    args:
        path(str): full path to text.
    """
    with codecs.open(path, "rb") as f:
        text = f.read()
    return text.translate(None, string.punctuation)


class WordNovelty():
    """Class for assessing word-level novelty over a given text"""
    def __init__(self, file_path):
        """Takes text file as argument and does basic processing."""
        self.file_path = file_path
        self.TextString = open(file_path, "r").read()
        self.Tokens = nltk.word_tokenize(self.TextString)
        self.Text = nltk.Text(self.Tokens)

    def GetWordNovelty(self, interval, lemmatize=False):
        """
        Finds novelty rates for words per interval.
        Args:
          interval(int): Segment over which to measure novelty.
          lemmatize(boolean): if True, words are stemmed before assessing novelty.
        Returns:
          self.Novelty(list): list of integers expressing number of novel words for each interval.
          self.Table(dict): Builds a dictionary with entries for each word and their location in the text.
        """
        new_words = 0
        self.Novelty = []
        self.Table = {}
        if lemmatize is False:
            token_set = self.Tokens
        else:
            token_set = self.Lemmatize()

        for i, word in enumerate(token_set):
            if word.lower() in self.Table:
                self.Table[word.lower()].append(i)
            else:
                self.Table[word.lower()] = [i]
                new_words += 1
            if (i + 1) % interval == 0:
                self.Novelty.append(new_words)
                new_words = 0
        return self.Novelty

    def Lemmatize(self):
        """Function to provide stemming of the text."""
        porter = nltk.PorterStemmer()
        token_set = (porter.stem(t) for t in self.Tokens)
        return token_set

    def GraphData(self, interval):
        """Calls GetWordNovelty and turns resulting data into x and y data for graphing."""
        ydata = [x/interval for x in self.GetWordNovelty(interval)]
        xdata = range(len(ydata))
        return xdata, ydata

    def BestFit(self, interval, poly_value):
        """
        Calls graph data, then uses x and y data to make a best fit line.
        Args:
          poly_value(int): the level of complexity of the polynomial expression used to fit the graph.
        Returns:
          par(list): contains coefficients for each value of polynomial -- therefore describes slope and y-intercept.
        """
        xdata, ydata = self.GraphData(interval)
        par = np.polyfit(xdata, ydata, poly_value, full=True)
        return par

    def GetSlope(self, interval, poly_value):
        """Retrieves slope of function."""
        par = self.BestFit(interval, poly_value)
        slope = par[0]
        return slope

    def GraphNovelty(self, interval):
        """Calls graph data and uses result to call build_graph function."""
        xdata, ydata = self.GraphData(interval)
        self.build_graph(xdata, ydata, os.path.basename(self.file_path), interval)

    @staticmethod
    def build_graph(xdata, ydata, filename, interval):
        """Builds graph using Plotly."""
        layout = Layout(
            title='Novelty for {0}'.format(filename),
            xaxis=XAxis(title="Intervals ({0})".format(interval)),
            yaxis=YAxis(title="Ratio of Novelty"),
        )
        rawdata = Scatter(
            x=xdata,
            y=ydata
        )
        fitline = Scatter(
            x=self.xdata_entropy_bestfit,
            y=self.ydata_entropy_bestfit,
            name='Best Fit Line',
            mode='lines',
            line=Line(
                color='rgb(164, 194, 244)'
            )
        )
        data = Data([rawdata, fitline])
        # novelty_data_lemma = self.WordNovelty(interval, lemmatize=True)
        figure = Figure(data=data, layout=layout)
        plot_url = py.iplot(figure, filename=filename)
