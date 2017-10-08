"""
Our implementation of knuth-liang
"""

from string import digits
from collections import OrderedDict
from .language_patterns import LanguagePatterns


class KnuthLiang(object):
    """
    This class implements knuth-liang
    """

    __slots__ = ['language_patterns', 'limit_left', 'limit_right']

    def __init__(self, lang_code=None, file_path=None, limit_left=2, limit_right=3):
        self.language_patterns = LanguagePatterns(lang_code, file_path)
        self.limit_left = limit_left
        self.limit_right = limit_right

    def hyphenate_word(self, word_input):
        "Hyphenates a word"
        word = '.' + word_input + '.'
        word_len = len(word)
        found_patterns = OrderedDict()  # key order matters later

        for left_pos in range(word_len):
            for pattern in self.language_patterns.iterate(word[left_pos:].lower()):
                for patt_pos in pattern:
                    index = patt_pos + left_pos - 1
                    if (index not in found_patterns or
                            found_patterns[index] < pattern[patt_pos]):
                        found_patterns[index] = pattern[patt_pos]

        # we don't hyphen at the left-right limits
        for i in (range(0, self.limit_left) +
                  range(word_len - self.limit_right, word_len)):
            if i in found_patterns:
                del found_patterns[i]

        # we find all the odd-numbered digits in the pattern and hyphenate
        hyphens = (h for h in found_patterns.keys() if found_patterns[h] & 1)
        for i, hyphen in enumerate(hyphens):
            index = i + hyphen + 1
            word = word[:index] + '-' + word[index:]

        return word[1:-1]
