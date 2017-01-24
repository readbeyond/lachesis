# lachesis

**lachesis** automates the segmentation of a transcript into closed captions

* Version: 0.0.2
* Date: 2017-01-24
* Developed by: [Alberto Pettarin](http://www.albertopettarin.it/)
* License: the GNU Affero General Public License Version 3 (AGPL v3)
* Contact: [info@readbeyond.it](mailto:info@readbeyond.it)

**DO NOT USE THIS PACKAGE IN PRODUCTION UNTIL IT REACHES v1.0.0 !!!**


## Goal

**lachesis** automates the segmentation of a transcript into closed captions,
by using POS tagging, sentence segmentation, and syntax parsing
provided by one of the base NLP libraries below.

It contains the following major functions:

* download closed captions from YouTube (using ``youtube-dl``)
* parse closed caption TTML files (using ``lxml``)
* POS tagging a given text or closed caption file
* segment a given text into sentences
* segment a given text into closed captions, using different split algorithms
* prepare input files for training machine learning models


## Installation

**DO NOT USE THIS PACKAGE IN PRODUCTION UNTIL IT REACHES v1.0.0 !!!**

```bash
pip install lachesis
```


### Installing NLP Libraries

To perform POS tagging and sentence segmentation, ``lachesis`` can use
one of the following libraries:

* ``pattern`` (install with ``pip install pattern``)
* ``NLTK`` (install with ``pip install nltk`` and symlink the language model directory as ``~/nltk_data``)
* ``spaCy`` (install with ``pip install spacy`` and symlink the language model directory as ``~/spacy_data``)
* ``UDPipe`` (install with ``pip install ufal.udpipe`` and symlink the language model directory as ``~/udpipe_data``)


## Usage

### Download closed captions from YouTube or parse an existing TTML file:

```python
from lachesis.downloaders import Downloader
from lachesis.language import Language

# URL of the video
url = u"http://www.youtube.com/watch?v=NSL_xx2Qnyc"

# language
language = Language.ENGLISH

# download English automatic CC, storing the raw TTML file in /tmp/
options = { "auto": True, "output_file_path": "/tmp/auto.ttml" }
doc = Downloader.download_closed_captions(url, language, options)
print(doc)

# download English manual CC
options = { "auto": False }
doc = Downloader.download_closed_captions(url, language, options)
print(doc)

# parse a given TTML file (downloaded from YouTube)
ifp = "/tmp/auto.ttml"
doc = Downloader.read_closed_captions(ifp, options={u"downloader": u"youtube"})

# retrieve document language
print(doc.language)

# get several representations of the CCs
doc.raw_flat_clean_string               # as a single string, no CC line marks, no newlines
doc.raw.string(flat=True, eol=u"|")     # as a single string, CC lines separated by "|" characters
doc.raw.string(raw=True, eol=u"")       # CC lines separated by a blank line
```

### Tokenize, split sentences, and POS tagging:

```python
from lachesis.elements import Document
from lachesis.language import Language
from lachesis.nlpwrappers import NLPEngine

# work on this Unicode string
s = u"Hello, World. This is a second sentence, with a comma too! And a third sentence."

# but you can also pass a list with pre-split text
# s = [u"Hello World.", u"This is a second sentence.", u"Third one, bla bla"]

# create a Text object from the Unicode string
doc = Document(raw=s, language=Language.ENGLISH)

# tokenize, split sentences, and POS tagging
# the best NLP library will be chosen,
# depending on the language of the text
nlp1 = NLPEngine()
nlp1.analyze(doc)

# the text has been divided into tokens,
# grouped in sentences:
for s in doc.sentences:
    print(s)                                        # raw
    print(s.string(tagged=True))                    # tagged
    print(s.string(raw=True, eol=u"|", eos=u""))    # raw, no CC line and sentence marks

# explicitly specify an NLP library
# in this case, use "nltk"
# (other options include: "pattern", "spacy", "udpipe")
nlp2 = NLPEngine()
nlp2.analyze(doc, wrapper=u"nltk")
...

# if you need to analyze many documents,
# you can preload (and keep cached) an NLP library,
# even different ones for different languages
nlp3 = NLPEngine(preload=[
    (u"eng", u"spacy"),
    (u"deu", u"nltk"),
    (u"ita", u"pattern"),
    (u"fra", u"udpipe")
])
nlp3.analyze(doc)
...
```

### Split into closed captions

```python
from lachesis.elements import Document
from lachesis.language import Language
from lachesis.nlpwrappers import NLPEngine
from lachesis.splitters import GreedySplitter

# create a document from a raw string
s = u"Hello, World. This is a second sentence, with a comma too! And a third sentence."
doc = Document(raw=s, language=Language.ENGLISH)

# analyze it using pattern as NLP library
nlpe = NLPEngine()
nlpe.analyze(doc, wrapper=u"pattern")

# feed the document into the greedy splitter
# with max 42 chars/line and max 2 lines/cc
gs = GreedySplitter(doc.language, 42, 2)
gs.split(doc)

# print the segmented CCs
# which can be accessed with the ccs property
for cc in doc.ccs:
    for line in cc.elements:
        print(line)
    print(u"")
```


## License

**lachesis** is released under the terms of the
GNU Affero General Public License Version 3.
See the [LICENSE](LICENSE) file for details.
