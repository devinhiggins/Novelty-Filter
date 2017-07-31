from novelty_filter import NoveltyFilter
import os
import csv
import json
import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
from graph import PlotlyGraph, marker, line
from scipy.optimize import curve_fit
# from entropy import Entropy
from word_novelty import lexical_diversity
from operator import sub
import codecs
from datetime import date


class Novelty():
    def __init__(self):
        self.results = []
        self.xdata_all = []
        self.ydata_all = []
        self.corpus = None
        self.corpus_name = None

    def _get_files(self, path):
        """Gather all text files from specified path.

        Marked up files will contain "_intervals" in the file name. The second
        half of the if statement will make sure these are skipped.
        """
        return (f for f in os.listdir(path) if f.endswith(".txt") and "_intervals" not in f)

    def get_novelty(self, path, **kwargs):
        """Use NoveltyFilter class to produce novelty for individual texts.

        args:
            path(str): path to individual text file.
            entropy(bool): if true produce entropy calculation.
        kwargs:
            (**kwargs): set of keword args to pass along to the novelty filter.
        """
        self.filepath = path

        # Print headings for single result.
        if not self.corpus:
            self._print_headings()

        # Initialize novelty filter and get novelty using kw arguments.
        self.nf = NoveltyFilter()
        self.nf.get_novelty(path, **kwargs)

        self.filename = os.path.basename(path)

        # Collect statistical results.
        self.slope, self.intercept, self.rvalue, pvalue, self.stderr = self.nf.linear_regression()
        self.ld = lexical_diversity(path)

        # Print results for each text.
        print self.filename.ljust(50),\
            str(round(self.slope, 4)).ljust(10),\
            str(round(self.rvalue**2, 4)).ljust(10),\
            str(len(self.nf.xdata)).ljust(10),\
            str(self.ld).ljust(10)

    def mark_up_corpus(self):
        """Add mark-up to texts based on novelty results."""
        for text in self.results:
            self.mark_up_text(text)

    def mark_up_text(self, data={}):
        """Add mark up to individual text."""
        if not data:
            self.ydata_pred = self.get_line_data()
            data = {
                "filename": self.filename,
                "filepath": self.filepath,
                "xdata": self.nf.xdata,
                "ydata": self.nf.ydata,
                "residuals": map(sub, self.nf.ydata, self.ydata_pred),
                "error": self.get_error(),
                "rsquared": round(self.rvalue**2, 4),
                "slope": round(self.slope, 4),
                "ld": self.ld
            }
        self._process_text(data)

    def _process_text(self, data):
        """Write to new text file with novelty as mark-up."""
        filepath = data["filepath"]
        xdata = data["xdata"]
        ydata = data["ydata"]
        error = data["error"]
        residuals = data["residuals"]

        # Create output path for new marked-up file.
        splitpath = os.path.splitext(filepath)
        markuppath = splitpath[0] + "_intervals" + splitpath[1]

        # Load full text.
        with codecs.open(filepath, "rb", "utf-8") as textin:
            text = textin.read()

        # Open new file to write 'text' root, then alternating 'interval' elements
        # and text for that interval.
        with codecs.open(markuppath, "w", "utf-8") as textout:

            # Write 'text' element.
            textout.write("<text id={0} error={1} rsquared={2} slope={3} ld={4}>\n"
                          .format(data["filename"], round(error, 4), round(data["rsquared"], 4),
                                  round(data["slope"], 3), data["ld"]))

            # Iteratate over all intervals.
            for index, value in enumerate(xdata):
                residual = round(residuals[index], 4)
                yvalue = ydata[index]
                level = self._assign_level(residual, error)

                # Establish text for the current interval.
                interval = "<interval value={0} novelty={1} residual={2} level={3}>".format(index, yvalue, residual, level)
                textout.write(interval)
                start = 10000 * index
                end = 10000 * (index + 1)
                textout.write(text[start:end])
                textout.write("</interval>")
            textout.write("</text>")

    def _assign_level(self, residual, error):
        """Assign value based on difference between residual and acceptable error."""
        if abs(residual) > error and residual > 0:
            level = 'high'
        elif abs(residual) > error and residual < 0:
            level = 'low'
        else:
            level = 'normal'
        return level

    def get_error(self):
        """Get RMSE based on linear regression."""
        p = PlotlyGraph()
        return p.get_rmse(self.nf.ydata, self.ydata_pred)

    def graph_novelty(self, fit_line=True):
        """Create novelty graph for selected text.

        kwargs:
            fit_line(bool): create fit line on graph.
        """
        p = PlotlyGraph()

        xaxis = {"title": "Intervals ({0})".format(self.nf.interval)}
        yaxis = {"title": "Ratio of Novelty"}
        title = "Novelty for {0}".format(self.filename)
        p.set_layout(xaxis=xaxis, yaxis=yaxis, title=title)

        scatterdata = {
            "x": self.nf.xdata,
            "y": self.nf.ydata,
            "mode": "markers",
            "name": "novelty data",
            "marker": marker(**{'color': 'rgb(234, 153, 153)'})
        }
        p.set_scatter(**scatterdata)

        self.ydata_pred = self.get_line_data()
        linedata = {
            "x": self.nf.xdata,
            "y": self.ydata_pred,
            "mode": "lines",
            "name": "best fit line",
            "line": line(**{'color': 'rgb(164, 194, 244)'}),
            "error_y": dict(type='constant',
                            value=p.get_rmse(self.nf.ydata, self.ydata_pred),
                            color='#85144B',
                            thickness=1,
                            width=3,
                            opacity=.5)
        }
        p.set_line(**linedata)

        p.plot()

    def get_line_data(self):
        """Get y-values from x-values slope and intercept."""
        ydata = []
        for x in self.nf.xdata:
            y = self.slope * x + self.intercept
            ydata.append(y)
        return ydata

    def corpus_novelty(self, path, p0=[0.0, 0.0], entropy=False, output=None, corpus_name=None):
        """Produce novelty calculations for each file in a corpus.

        args:
            path(str): directory containing text files.
        kwargs:
            p0(list)
            entropy(bool): if true produce entropy calculation.
            output(str): output results in particular format, only 'csv' currently supported.
        """
        self.results = []
        self.path = path
        self.corpus_name = corpus_name
        self.corpus = True
        files = self._get_files(path)
        self._print_headings()
        for f in set(files):
            filepath = os.path.join(path, f)
            self.get_novelty(filepath, entropy=entropy)
            self.ydata_pred = self.get_line_data()
            error = self.get_error()
            self.results.append({
                "corpus": self.corpus_name,
                "filename": os.path.basename(f),
                "filepath": filepath,
                "xdata": self.nf.xdata,
                "intervals": len(self.nf.xdata),
                "ydata": self.nf.ydata,
                "residuals": map(sub, self.nf.ydata, self.ydata_pred),
                "error": error,
                "rsquared": round(self.rvalue**2, 4),
                "slope": round(self.slope, 4),
                "ld": self.ld
            })

        if output == "csv":
            self.write_csv()
        elif output == "json":
            self.write_json()
        # self.interval = nf.interval
        # self.errors = nf._curve_fit_errors

    def write_csv(self):
        """Write results object to csv file."""
        outfile = self._set_filename()
        self.csv_fields = ["filename", "rsquared", "slope", "ld", "intervals"]
        with open(outfile, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_fields, extrasaction="ignore")
            writer.writeheader()
            for text in self.results:
                writer.writerow(text)
        print "Wrote output at {0}.".format(outfile)

    def write_json(self):
        """Write results to json file."""
        outfile = self._set_filename(ending=".json")
        with open(outfile, "w") as jsonfile:
            json.dump(self.results, jsonfile)

        print "Wrote output at {0}.".format(outfile)

    def _set_filename(self, ending=".csv"):
        """Create name for csv output."""
        if self.corpus_name:
            basename = self.corpus_name
        else:
            basename = os.path.dirname(self.path)
        today = date.today().isoformat()
        filename = basename + "-" + today + ending
        return os.path.join(self.path, filename)

    def _print_headings(self):
        """Print headings for novelty output."""
        print "Text".ljust(50), "Slope".ljust(10), "r^2".ljust(10),\
              "# Intervals".ljust(10), "Lexical Diversity".ljust(10)

    def PrintFields(self, *args):
        for doc in self.results:
            for i, field in enumerate(args):
                print field, doc[field]

    def CorpusCurveFit(self, p0=[]):
        self._curve_fit_errors = 0

        def func(x, a, b):
            return a * b**x
        try:
            self.popt, self.pcov = curve_fit(func, np.array(self.xdata_all), np.array(self.ydata_all), p0=p0)
        except (RuntimeError, TypeError):
            try:
                # p0[0] += 0.10
                # p0[1] -= 0.10
                self.popt, self.pcov = curve_fit(func, np.array(self.xdata_all), np.array(self.ydata_all), p0=p0)

            except (RuntimeError, TypeError):
                try:
                    # p0[0] += 0.10
                    # p0[1] -= 0.10
                    self.popt, self.pcov = curve_fit(func, np.array(self.xdata_all), np.array(self.ydata_all), p0=p0)

                except (RuntimeError, TypeError):
                    print "ERROR - Curve Fit Failed!"
                    self._curve_fit_errors += 1
                    self.popt = None
                    self.pcov = None
        if self.popt.all():
            self.xdata_bestfit = list(set(self.xdata_all))
            self.ydata_bestfit = func(np.array(self.xdata_bestfit), self.popt[0], self.popt[1])

    def CorpusGraph(self):
        """Builds graph using Plotly."""
        self.CorpusCurveFit(p0=[1.0, 1.0])

        layout = Layout(
            title='Novelty for set of {0} texts'.format(len(self.results)),
            xaxis=XAxis(title="Intervals ({0})".format(self.interval)),
            yaxis=YAxis(title="Ratio of Novelty"),
        )
        trace0 = Scatter(
            x=self.xdata_all,
            y=self.ydata_all,
            mode='markers',
            name='Novelty Data',
            marker=Marker(
                color='rgb(234, 153, 153)'
            )
        )
        trace1 = Scatter(
            x=self.xdata_bestfit,
            y=self.ydata_bestfit,
            name='Best Fit Line',
            mode='lines',
            line=Line(
                color='rgb(164, 194, 244)'
            )
        )
        data = Data([trace0, trace1])

        figure = Figure(data=data, layout=layout)
        plot_url = py.plot(figure, filename="Plot for Corpus")

    def EntropyGraph(self, entropy="I", novelty=1):
        self.xdata_entropy = []
        self.ydata_entropy = []
        self.entropy_text = []
        for x, item in enumerate(self.results):
            if item["popt"] is not None:
                self.entropy_text.append(item["filename"])
                self.xdata_entropy.append(float(item["entropy"][entropy]))
                self.ydata_entropy.append(float(item["popt"][novelty]))

        if self.EntropyCurveFit():

            layout = Layout(
                title='Novelty over Information for set of {0} texts'.format(len(self.results)),
                xaxis=XAxis(title="Information".format(self.interval)),
                yaxis=YAxis(title="Novelty"),
            )
            trace0 = Scatter(
                x=self.xdata_entropy,
                y=self.ydata_entropy,
                mode='markers',
                name='Novelty/Entropy',
                text=self.entropy_text,
                marker=Marker(
                    color='rgb(234, 153, 153)'
                )
            )
            trace1 = Scatter(
                x=self.xdata_entropy_bestfit,
                y=self.ydata_entropy_bestfit,
                name='Best Fit Line',
                mode='lines',
                line=Line(
                    color='rgb(164, 194, 244)'
                )
            )
            data = Data([trace0, trace1])
            figure = Figure(data=data, layout=layout)
            plot_url = py.plot(figure, filename="Entropy/Novelty/Information")

    def EntropyCurveFit(self, p0=[]):
        def func(x, a, b):
            return a * x + b
        try:
            self.popt, self.pcov = curve_fit(func, np.array(self.xdata_entropy), np.array(self.ydata_entropy))

        except (RuntimeError, TypeError) as err:
            print "No line created: {0}".format(err)
            return False

        if self.popt.all():
            self.xdata_entropy_bestfit = self.xdata_entropy
            self.ydata_entropy_bestfit = func(np.array(self.xdata_entropy), self.popt[0], self.popt[1])
            return True
        else:
            return False
