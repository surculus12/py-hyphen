"""
Our language pattern
"""

import urllib2
from contextlib import closing
from string import digits
from .trie import Trie

_PATTERN_REPO = \
'http://ctan.uib.no/language/hyph-utf8/tex/generic/hyph-utf8/patterns/tex/hyph-{0}.tex'


class LanguagePatterns(Trie):
    """
    This class creates a trie of a language pattern
    """

    __slots__ = ["lang_code", "file_path"]

    def __init__(self, lang_code, file_path):
        if not lang_code and not file_path:
            raise Exception("lang_code or file_path need to be supplied")
        super(LanguagePatterns, self).__init__()
        self.lang_code = lang_code
        self.file_path = file_path
        self.parse_language()


    def iterate_language_patterns(self):
        "Generate language patterns from .tex pattern file"
        with open(self.file_path) if self.file_path else \
             closing(urllib2.urlopen(_PATTERN_REPO.format(self.lang_code))) as lang:
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
            value = {}
            # stores trie value as a dictionary with key='position in word'
            #   and value='pattern weight'
            for i, p in ((i, p) for i, p in enumerate(pattern) if p in digits):
                value[i + len(value.keys())] = int(p)
            self.insert(key, value)
