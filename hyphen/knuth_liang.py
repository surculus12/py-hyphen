"""
Handles hyphenation of words or sentences
"""

from .language_patterns import LanguagePatterns


class KnuthLiang(object):
    """
    This class handles hyphenation
    """

    def __init__(self, code, limit_left=2, limit_right=3):
        self.language_patterns = LanguagePatterns(code)
        self.limit_left = limit_left
        self.limit_right = limit_right

    def hyphenate_word(self, word):
        "Hyphenates a word"
        word = '.' + word + '.'
        word_length = len(word)
        found_patterns = dict()
        for left_pos in range(word_length + 1):
            for right_pos in range(self.limit_left, word_length-left_pos+1):
                word_concat = word[left_pos:right_pos]
                if word_concat not in self.language_patterns:
                    continue

                pattern = self.language_patterns[word_concat]
                # TODO: Find simplification to this step
                digit_cnt = 1
                for i, char in enumerate(pattern):
                    if not char.isdigit():
                        continue

                    digit_pos = left_pos + i - digit_cnt
                    if (digit_pos not in found_patterns or
                            found_patterns[digit_pos] < int(char)):
                        found_patterns[digit_pos] = int(char)

                    digit_cnt += 1

        hyphens = (h for h in found_patterns.keys() if found_patterns[h] & 1)
        for i, hyphen in enumerate(hyphens):
            index = i + hyphen + 1
            word = word[:index] + '-' + word[index:]

        return word[1:-1]
