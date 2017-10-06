"""
Our implementation of knuth-liang
"""

from string import digits
from .language_patterns import LanguagePatterns


class KnuthLiang(object):
    """
    This class implements knuth-liang
    """

    __slots__ = ['language_patterns', 'limit_left', 'limit_right',
                 'usecache', 'cache']

    def __init__(self, lang_code, limit_left=2, limit_right=3, usecache=False):
        self.language_patterns = LanguagePatterns(lang_code)
        self.limit_left = limit_left
        self.limit_right = limit_right
        self.usecache = usecache
        self.cache = {}

    def hyphenate_word(self, word_input):
        "Hyphenates a word"
        if self.usecache and word_input in self.cache:
            return self.cache[word_input]

        word = '.' + word_input + '.'
        word_len = len(word)
        found_patterns = dict()

        for left_pos in range(word_len):
            word_concat = word[left_pos:]
            for pattern in self.language_patterns.iterate(word_concat):
                # double enumeration to save i (index in pattern)
                #   and j (index in digit tuple)
                patts = [(i, p) for i, p in enumerate(pattern) if p in digits]
                for j, (i, char) in enumerate(patts):
                    digit_pos = left_pos + i - j - 1
                    if (digit_pos not in found_patterns or
                            found_patterns[digit_pos] < int(char)):
                        found_patterns[digit_pos] = int(char)

        # we don't hyphen at the left-right limits
        for i in (range(0, self.limit_left) +
                  range(word_len - self.limit_right, word_len)):
            found_patterns[i] = 0

        # we find all the odd-numbered digits in the pattern and hyphenate
        hyphens = (h for h in found_patterns.keys() if found_patterns[h] & 1)
        for i, hyphen in enumerate(hyphens):
            index = i + hyphen + 1
            word = word[:index] + '-' + word[index:]

        word = word[1:-1]
        if self.usecache:
            self.cache[word_input] = word

        return word

    def clear_cache(self):
        "Clears local cache"
        self.cache = {}
