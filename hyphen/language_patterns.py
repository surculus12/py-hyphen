"""
Parses hyphenation rules for a language
"""

from string import digits
from .trie import Trie


class LanguagePatterns(Trie):
    """
    This class handles language-specific
    rules for hyphenation
    """

    def __init__(self, code):
        super(LanguagePatterns, self).__init__()
        __lang_code__ = code
        self.parse_language()

    def iterate_language_patterns(self):
        "Generate language patterns from .tex pattern file"
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

    def parse_language(self):
        "Parses the language patterns into a usable dictionary"
        for pattern in self.iterate_language_patterns():
            key = pattern.translate(None, digits)
            self.insert(key, pattern)
