from __future__ import print_function, division
import os
import csv
import subprocess
from novelty_filter import NoveltyFilter
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles


class Compare(object):

    """Take two existing filters and compare."""

    def __init__(self, plot=False, merge=False, venn=False, printout=False):
        """Initialize with output options.

        kwargs:
            plot(bool): return graph of novelty for each text.
            merge(bool): create combination filter from individual filters.
            venn(bool): create venn diagram of results.
        """
        self._plot = plot
        self._merge = merge
        self._venn = venn
        self._csv = csv_out
        self.printout = printout

        self._compare_path = os.path.join(os.getcwd(), "compare.out")

    def compare_filters(self, filtera, filterb):
        """Compare already created filters.

        args:
            filtera(str): name of first filter.
            filterb(str): name of second filter.
        """
        self.filtera = filtera
        self.filterb = filterb
        self.a_label = os.path.basename(filtera)
        self.b_label = os.path.basename(filterb)
        self._run_comparison()

    def compare_texts(self, texta, textb, filtera="filtera.txt", filterb="filterb.txt"):
        """Initialize texts and compare filters.

        args:
            texta(str): path to first text
            textb(str): path to second text
        """
        self.texta = texta
        self.textb = textb
        self.filtera = "filtera.txt"
        self.filterb = "filterb.txt"
        self.a_label = os.path.basename(texta)
        self.b_label = os.path.basename(textb)
        self._generate_filters()

    def _generate_filters(self):
        """Create new filter files for the two texts being examined."""
        self._run_novelty(self.texta, self.filtera, plot=self._plot)
        self._run_novelty(self.textb, self.filterb, plot=self._plot)
        self._run_comparison()

    def _run_comparison(self):
        """Check for results of comparison of two created filters."""
        args = [self._compare_path, self.filtera, self.filterb]
        if self._merge:
            args.append("filterab.txt")
        self._run_process(args)

    def _run_process(self, args):
        """Run subprocess of filter comparison.

        args:
            args(list): list of args to be joined and run.
        """
        p = subprocess.check_output(args)
        print(p)
        self._process_result(p)

    def _process_result(self, result):
        """Process results for output to screen.

        args:
            result(str): result from compare.out, should be 4 numbers in a string
                separated by spaces.
        """
        resultlist = [int(n) for n in result.split()]
        neither = resultlist[0]
        texta_unique = resultlist[1]
        textb_unique = resultlist[2]
        shared = resultlist[3]

        self.resultlist = resultlist

        total = sum(resultlist)
        total_occurring = sum(resultlist[1:])

        self.shared_pct = shared / total_occurring

        if self.printout:
            print("{0:<40}{1:>11}".format("Non-occurring", neither))
            print("{0:<40}{1:>11} ({2:>7.2%})".format(self.a_label, texta_unique, texta_unique / total_occurring))
            print("{0:<40}{1:>11} ({2:>7.2%})".format(self.b_label, textb_unique, textb_unique / total_occurring))
            print("{0:<40}{1:>11} ({2:>7.2%})".format("Shared", shared, self.shared_pct))
            print("{0:<40}{1:>11}".format("TOTAL", total))

        if self._venn:
            sizes = (texta_unique, textb_unique, shared)
            labels = (self.a_label, self.b_label)
            self._venn_diagram(sizes, labels)

    def _venn_diagram(self, sizes, labels):
        """Build venn diagram from data.

        args:
            sizes(tuple): tuple of sizes for each part of the venn diagram, e.g.
                unique to cirlce a, unique to circle b, and shared.
            labels(tuple): label for each circle.
        """
        v = venn2(subsets=sizes, set_labels=labels)
        plt.show()

    def _run_novelty(self, text, filtername, plot=False):
        """Run novelty on individual text.

        args:
            text(str): path to text to run novelty of
            filtername(str): filename to use for filter.
        kwargs:
            plot(bool): if true create plot of results.
        """
        n = NoveltyFilter(filtername=filtername)
        n.get_novelty(text, plot=plot)


class CompareNovelty:
    """Run novelty of a given text given an existing filter."""

    def __init__(self, text1, text2):
        """Compare novelty decay of two texts.

        args:
            stext(str): filename of source text (to process first)
            otext(str): filename of text to process second.
        """
        self.text1 = text1
        self.text2 = text2
        if self._check_text(text1) and self._check_text(text2):
            self._run_comparison(text1, text2)

    def _check_text(self, textfile):
        """Attempt to load text for processing.

        args:
            text(str): path to file to open for processing.
        """
        text = True
        # Check if file exists
        if not os.path.isfile(textfile):
            print("Unable to locate file: {0}".format(textfile))
            text = False
        return text

    def _run_comparison(self, text1, text2):
        """Run comparison of two texts.

        args:
            text1(str): path to text to process first
            text2(str): path to text to process second
        """
        # Calculate the novelty decay for the first text, then thes second text
        # in relation to it.
        self.novelty_1 = self._filter_first_text(text1)
        self.novelty_2_rel = self._filter_against_text(text2)

        # Calculate the novelty decay for the second text, then the first text
        # in relation to it.
        self.novelty_2 = self._filter_first_text(text2)
        self.novelty_1_rel = self._filter_against_text(text1)

        self.novelty_1_diff = self.novelty_1["ratio"] - self.novelty_1_rel["ratio"]
        self.novelty_2_diff = self.novelty_2["ratio"] - self.novelty_2_rel["ratio"]

    def _filter_first_text(self, text):
        """Run novelty calculation against empty filter.

        args:
            text(str): path to file containing text.
        """
        self.n = NoveltyFilter(delete=True)
        self.n.get_novelty(text, outputName="output.txt", plot=False)
        return self.n.data

    def _filter_against_text(self, text):
        """Run novelty against current (undeleted) filter.

        args:
            text(str): path to file containing text.
        """
        self.n = NoveltyFilter(delete=False)
        self.n.get_novelty(text, outputName="output.txt", plot=False)
        return self.n.data
