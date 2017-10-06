"""
Our language pattern
"""

from string import digits
from .trie import Trie


class LanguagePatterns(Trie):
    """
    This class creates a trie of a language pattern
    """

    def __init__(self, lang_code):
        super(LanguagePatterns, self).__init__()
        self.parse_language(lang_code)

    def iterate_language_patterns(self, lang_code):
        "Generate language patterns from .tex pattern file"
        # TODO: Fetch via lang_code
        with open('hyphen/lang/english.tex') as lang:
            amreadingpatterns = False
            # read file line-by-line
            for line in lang:
                # skip comments and empty lines
                if line[:1] == "%" or line[:1] == "\n":
                    continue
                # stop yielding at the end of the patterns block
                elif line[:1] == "}":
                    break
                # only yield if inside the patterns block
                elif amreadingpatterns is True:
                    yield line[:-1]  # cut out the newline
                # say that we've reached the patterns block
                elif line[:10] == r"\patterns{":
                    amreadingpatterns = True

    def parse_language(self, lang_code):
        "Parses the language patterns into a usable dictionary"
        for pattern in self.iterate_language_patterns(lang_code):
            key = pattern.translate(None, digits)
            self.insert(key, pattern)
