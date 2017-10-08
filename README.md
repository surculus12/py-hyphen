# py-hyphen
Implementation of knuth-liang

# Usage
Object can either be instantiated with an iso-valid language code (at which point the pattern file will be fetched) or with a relative path to a language file.

## Example
```
from hyphen import Hyphen
hyphenator = Hyphen(lang_code='en-us')
hyphenator.hyphenate_word('Floccinaucinihilipilification')
# out: 'Floc-cinau-cini-hilip-il-i-fi-ca-tion'
hyphenator.hyphenate_word('geographical')
# out: 'ge-o-graph-i-cal'
```
