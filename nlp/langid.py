__author__ = 'rahmaniac'
#logic by Misja Hoebe

from nltk.util import trigrams as nltk_trigrams
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.probability import FreqDist
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader.util import StreamBackedCorpusView, concat


class LangIdCorpusReader(CorpusReader):
    CorpusView = StreamBackedCorpusView


    #get the weight of each trigram stored in the nltk corpus
    def _get_trigram_weight(self, line):
        data = line.strip().split(' ')
        if len(data) == 2:
            return data[1], int(data[0])

    #fetches the nltk corpus and reads blocks of trigrams and gets the weight of each trigram
    def _read_trigram_block(self, stream):
        freqs = []
        for i in range(20): # Read 20 lines at a time.
            freqs.append(self._get_trigram_weight(stream.readline()))
        return filter(lambda x: x is not None, freqs)

    def freqs(self, fileids=None):
        return concat([self.CorpusView(path, self._read_trigram_block)
                       for path in self.abspaths(fileids=fileids)])

class LangDetect(object):
    language_trigrams = {}
    #laod the corpus text
    langid = LazyCorpusLoader('langid', LangIdCorpusReader, r'(?!\.).*\.txt')

    #languages en, frenchm german and spanish are lodaed
    def __init__(self, languages=['en', 'fr', 'de', 'es']):
        for lang in languages:
            self.language_trigrams[lang] = FreqDist()
            for f in self.langid.freqs(fileids=lang+"-3grams.txt"):
                self.language_trigrams[lang].inc(f[0], f[1])

    def detect(self, text):

        #tokenize the words
        words    = nltk_word_tokenize(text.lower())
        trigrams = {}
        scores   = dict([(lang, 0) for lang in self.language_trigrams.keys()])

        #get the trigrams and insert count of trigrams in a list
        for match in words:
            for trigram in self.get_word_trigrams(match):
                if not trigram in trigrams.keys():
                    trigrams[trigram] = 0
                trigrams[trigram] += 1

        total = sum(trigrams.values())

        #normalie the frequency and sort according to the keys.
        for trigram, count in trigrams.items():
            for lang, frequencies in self.language_trigrams.items():
                # normalize and add to the total score
                scores[lang] += (float(frequencies[trigram]) / float(frequencies.N())) * (float(count) / float(total))

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[0][0]

    def get_word_trigrams(self, match):
        return [''.join(trigram) for trigram in nltk_trigrams(match) if trigram != None]