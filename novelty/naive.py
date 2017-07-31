from __future__ import print_function
from __future__ import division
import csv
import random
import math
import nltk
import copy


class NaiveBayes(object):
    """Use NLTK to run classification using Naive Bayes approach."""
    def __init__(self):
        """Initialize class objects."""
        self.feature_sets = []
        self.classified = []
        self.unclassified = []

    def load_data_from_csv(self, path_to_csv):
        """Process features and run classification algorithm, according to CSV data.

        CSV should have a column labeled "class" and a column labeled "id".
        All other columns will be treated as features.

        args:
            path_to_csv(str): path to csv file containing data to process
        """
        self.csvfile = path_to_csv
        self._load_csv()
        print("Found {0} classified object(s)".format(len(self.classified)))
        print("Found {0} unclassified object(s)".format(len(self.unclassified)))

    def evaluate_training_data(self):
        """Use classified objects as training and test data.

        Evaluate success in classifying known items by splitting
        classified data into training and test sets.
        """
        self._set_training_and_test_sets()
        self.classifier = nltk.NaiveBayesClassifier.train(self.training_set)
        self._get_accuracy()
        self._get_useful_features()

    def _get_accuracy(self):
        """Test accuracy of model on test data."""
        acc = nltk.classify.accuracy(self.classifier, self.test_set)
        print("Accuracy on test set: {0}".format(acc))

    def _get_useful_features(self):
        """Show which features were most useful in correct classifications."""
        self.classifier.show_most_informative_features(5)

    def _set_training_and_test_sets(self):
        """Randomly shuffle data and get training and test sets."""
        total = len(self.classified)
        midpoint = int(math.ceil(total / 2))
        random.shuffle(self.classified)
        self.training_set = self.classified[:midpoint]
        self.test_set = self.classified[midpoint:]

    def _load_csv(self):
        """Load csv file and iterate through rows."""
        with open(self.csvfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self._process_row(row)

    def _process_row(self, row):
        """Assess data in row and process accordingly.

        args:
            row(dict): key will be column heading.
        """

        # Extract features from row (these have already been computed) and
        # add to feature_sets object. Each row is 1 feature_set.
        feature_set = self._extract_features(row)
        self.feature_sets.append(feature_set)

        if row['class'] != "":
            self._add_classified_data(feature_set, row['class'])
        else:
            self._add_unclassified_data(row['id'])

    def _add_classified_data(self, fileid, classname):
        """Add class label and file ID to set of classified data.

        args:
            fileid(str): id for particular row as file location.
            classname(str): class to match fileid.
        """
        self.classified.append((fileid, classname))

    def _add_unclassified_data(self, fileid):
        """If row not classified, add it to data set for prediction.

        args:
            fileid(str): id for particular row as file location.
        """
        self.unclassified.append(fileid)

    def _extract_features(self, row):
        """Extract features from supplied row.

        Since features are already computed, simply remove key:value combos
        that don't reflect features, i.e. class and id.

        Create a deep copy just to be safe.

        args:
            row(dict): key will be column heading.
        """
        features = copy.deepcopy(row)
        features.pop("class")
        features.pop("id")
        return {k: float(v) for k, v in features.items()}
