import subprocess
import os
import csv
from word_novelty import WordNovelty
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
from entropy import Entropy
from pandas import read_csv
import shutil

# from pandas import *


class NoveltyFilter():
    """Class for applying Arend Hintze's novelty filter."""
    def __init__(self, delete=True, filtername="filter.txt"):
        """
        Establish class variables for the character map and filter.
        Args:
          delete(bool): deletes existing filter and output files if true.
        """
        self.path = os.getcwd()
        # The charToMap file is used for mapping characters to bytes. This file must
        # be altered if the K and N variables are changed.
        self.mapName = os.path.join(self.path, "charToKMap.txt")
        # If filter doesn't exist a new one based on the supplied text is created.
        # If filter does exist, then the new text is "poured over" the existing filter.
        self.filtername = filtername
        self.filter = os.path.join(self.path, filtername)

        # Delete previous results.
        self.data = None
        # if os.path.isfile("output.txt"):
        #    os.remove("output.txt")
        if delete:
            if os.path.isfile(self.filter):
                os.remove(self.filter)

    def save_outputs(self, path_to_text, filter_output="", graph_output="", overwrite=False):
        """Save the filters and graphs generated by running the novelty filter.

        args:
            path_to_text(str): path to text to run novelty filter on.
        kwargs:
            filter_output(str): location to store filters. each filter is 250 mb!
            graph_output(str): location to store csv output for each text.
            overwrite(bool): if true, replace existing filters and graphs with newly
                computed ones.
        """
        if not filter_output and not graph_output:
            print "No outputs specified. Complete."
        else:
            self._generate_outputs(path_to_text, filter_output, graph_output, overwrite)

    def _generate_outputs(self, text, filter_path, graph_path, overwrite):
        """Run novelty filter."""
        # Name output files using text filename.
        output_filename = "output-" + os.path.basename(text)
        filter_filename = os.path.splitext(self.filtername)[0] + "-" + os.path.basename(text)
        filter_filepath = os.path.join(filter_path, filter_filename)

        # Run novelty filter.
        self.get_novelty(text, outputName=output_filename)

        # Move results files depending on original options.
        if graph_path:
            self._move_file(output_filename, graph_path, overwrite)
        if filter_path:
            self._move_file(self.filtername, filter_filepath, overwrite)

    def _move_file(self, source_filename, dest_path, overwrite):
        """Move newly created files."""

        # Create file path for source file, which should be in the current directory.
        source_filepath = os.path.join(self.path, source_filename)

        # Create full filepath for destination file to check if it already exists.
        destination_file = os.path.join(dest_path, source_filename)

        if not os.path.exists(destination_file) or overwrite is True:
            shutil.move(source_filepath, dest_path)

    def get_novelty(self, inputName, prime=2000000001, K=5, N=12, interval=10000,
                    outputName="output.txt", entropy=False, plot=False):
        """
        Uses the novelty filter to track number of "new" K-mers per the interval.
        args:
          inputName(str): path to filename of input text
          prime(int): very large prime number
          K(int): how many bits to use to store each ASCII character
          N(int): length of each segment to be analyzed
          interval(int): segment to measure novelty level within, e.g. number of N-length segments.
          outputName(str): filename to write CSV results to
        returns:
          A CSV file with outputName in which column 1 is number of novel K-mers, column 2 is re-used K-mers,
          and column 3 is the proportion of new to total.
        """
        self.outputName = outputName
        self.filename = os.path.basename(inputName)
        self.interval = interval
        cmds = [os.path.join(self.path, "a.out"), str(prime), str(K), str(N), self.mapName, inputName,
                os.path.join(self.path, outputName), self.filter, str(interval)]
        subprocess.check_output(cmds)
        self.get_data()
        self.load_data()

        if entropy:
            en = Entropy()
            self.e = en.get_entropy(inputName)

        if plot:
            self.plot_data()
        """
        if graph:
          self.GraphNovelty()
        if curve_fit:
          self.curve_fit()
        """

    def linear_regression(self, xdata=0, ydata=0):
        """Calculate linear least-squares measurement."""
        if xdata == 0:
            if hasattr(self, "xdata"):
                xdata = self.xdata
                ydata = self.ydata
            else:
                print "Please supply or compute x and y data."
        return linregress(np.array(xdata), np.array(ydata))

    def curve_fit(self, p0=[]):
        self._curve_fit_errors = 0

        def func(x, a, b):
            return a * b**x
        try:
            self.popt, self.pcov = curve_fit(func, np.array(self.xdata), np.array(self.ydata))
        except (RuntimeError, TypeError)as e:
            print "Unable to process curve."
            print e

        """
            try:
                # p0[0] += 1
                # p0[1] -= 1
                self.popt, self.pcov = curve_fit(func, np.array(self.xdata), np.array(self.ydata))

            except (RuntimeError, TypeError):
                try:
                    # p0[0] += 1
                    # p0[1] -= 1
                    self.popt, self.pcov = curve_fit(func, np.array(self.xdata), np.array(self.ydata))

                except (RuntimeError, TypeError) as err:
                    print "ERROR - Curve Fit Failed!", err
                    self._curve_fit_errors += 1
                    self.popt = None
                    self.pcov = None
        """

    def GetCoordinates(self, entropy="I", novelty=1):
        self.curve_fit()
        self.coordinates = (self.e[entropy], self.popt[novelty])
        return self.coordinates

    def get_data(self):
        """Read output file to get results of NoveltyFilter."""
        with open(os.path.join(self.path, self.outputName)) as f:
            source = csv.reader(f, delimiter=",")
            ydata = []
            for row in source:
                ydata.append(float(row[2]))
        self.xdata = range(len(ydata))
        self.ydata = ydata

    def load_data(self):
        """Load data from output.txt."""
        self.data = read_csv(self.outputName, header=None, names=["new segments", "repeated segments", "ratio"])

    def plot_data(self):
        """Show basic plot of novelty data."""
        self.data.plot(y="ratio")

    def GraphNovelty(self):
        """
        A function to graph output.
        Returns:
          A graph in a new browser tab via Plotly
        """
        WordNovelty.BuildGraph(self.xdata, self.ydata, self.filename, self.interval)

        # data = read_csv(os.path.join(self.path, filename), sep=",",na_values=[""," "],header=None,prefix="X")
        # plot(data["X2"])
