

class TextSegments():

    """Divide text up into k-mers."""

    def __init__(self):
        """Process text."""
        pass

    def compare_texts(self, path_to_text_1, path_to_text_2, segment_length=12):
        """Compare two texts according to the segments they contain."""

        segments_1 = self.segment_text(path_to_text_1, segment_length=segment_length)
        segments_2 = self.segment_text(path_to_text_2, segment_length=segment_length)

        return self._compare_segments(segments_1, segments_2)

    def segment_text(self, path_to_text, segment_length=12):
        """Turn text into segments of given length."""
        text = self.process_text(path_to_text)

        # Get length of text.
        last_char = len(text)
        segments = []

        for i, x in enumerate(text):

            span = i + segment_length

            # Make sure segment terminates before end of text.
            if span < last_char:
                segment = text[i:span]
                segments.append(segment)

        return segments

    def process_text(self, path_to_text):
        """Open text and store as raw text."""
        return self._open(path_to_text)

    def _open(self, path_to_text):
        """Open text and read as utf-8 string."""
        with open(self.path_to_text, "rb") as f:
            text = f.read().decode("utf8").lower().replace("\n", " ")
        return text

    def _compare_segments(seg1, seg2):
        """Take 2 sets of segments and compare."""
        set1 = set(seg1)
        set2 = set(seg2)
        overlap = set1.intersection(set2)
        set1diff = set1.difference(set2)
        set2diff = set2.difference(set1)
        nonoverlap = set1diff.union(set2diff)
        return len(overlap), len(set1diff), len(set2diff), len(nonoverlap)





