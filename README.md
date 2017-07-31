
# Novelty Filter

The novelty filter can be used to compute the proportion of text segments (of length *k*) that are new over a series of intervals in a larger text file. The algorithm uses a Bloom Filter to optimize performance on very large text files.

The code examples below can be run interactively with [Jupyter Notebooks](http://jupyter.org/) via [Novelty.ipynb](novelty/Novelty.ipynb). A helpful introduction can be found in [NoveltyIntro.ipynb](novelty/NoveltyIntro.ipynb).

## Information Novelty

To compute novelty of k-length segments over a given chunk of text, change to the novelty filter directory and open a Python shell. By default k is 5 and the interval over which novelty is computer is 10,000, but other inputs may be supplied.

Run basic novelty analysis, to return 4 values: 
- **Slope**: The slope of the line that was fit to the novelty data (slope will always be negative).
- **r^2**: A measure of how well the best-fit line explains the data (ranges from 0 to 1).
- **# Intervals**: The number of intervals in which the percent of novel strings was calculated; value is determined by the interval variable, which can be assigned when running the novelty calculation.
- **Lexical Diversity**: A standard measure computed by dividing the number of unique tokens by the number of total tokens

The code below will produce a filter file ("./filter.txt") and a csv file containing output values for the supplied text ("./output.txt").


```python
from run_novelty import Novelty
n = Novelty()
n.get_novelty("/path/to/text")
```

    Text                                               Slope      r^2        # Intervals Lexical Diversity
    Joyce_Ulysses.txt                                  -0.0008    0.5941     151        0.115     


Running the `mark_up_text` function will additionally create an annotated text file for a given book; including mark-up novelty data about each interval.


```python
from run_novelty import Novelty
n = Novelty()
n.get_novelty("/path/to/text")
n.mark_up_text()
```

Code to create filter 'pool' with contents of given directory poured one at a time over the same filter.

## By Corpus

Store filter and results for a corpus.


```python
import os
from novelty_filter import NoveltyFilter
directory = "/path/"

for f in os.listdir(directory):

    # Select all .txt files in a given directory, excluding the marked-up files
    # created e.g. in the previous cell.
    if f.endswith(".txt") and "_intervals" not in f:

        full_path = os.path.join(directory, f)
        print(full_path)
        
        # Use delete keyword "False" so that the filter won't be reinitialized for each text.
        n = NoveltyFilter(delete=False)
        
        # The paths to store outputs *must* exist prior to running this code.
        n.save_outputs(full_path, filter_output="outputs/filters/texts/", graph_output="outputs/results/texts/")
```
