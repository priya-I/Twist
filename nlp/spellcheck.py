from IPython.utils.syspathcontext import appended_to_syspath

__author__ = 'rahmaniac'

import re
import nltk
import string
import stemming.porter2 as porter
import itertools
import sys
import datetime


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
wordList = nltk.corpus.words.words()
def main():
    input = 'hello, how are you ? I\'m jumping with joy because she is soooooooooo cuuuttee and !!!!.'
    word = 'seperate'
    print spellcheck(word)


def spellcheck(unigram):

    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
    pattern1 =  re.compile("(ing)$")  #hack for all words ending in ing
    if len(pattern.findall(unigram)) > 0:
        approxWord = ''.join(letter for letter, _ in itertools.groupby(unigram))
    else:
        approxWord = unigram

    if len(pattern1.findall(approxWord)) > 0:
        approxWord = approxWord[0:len(approxWord)-3]

    if approxWord not in wordList  and '\'' not in unigram and '-' not in unigram:
        suggestions =findSuggestions(approxWord)
        if len(suggestions) > 0:
            return suggestions[0]
        else:
            return approxWord
    else:
        return approxWord


def findSuggestions(word):
    subStrings = split(word)
    deletedList = deleteLetters(subStrings)
    swappedList = swapLetters(subStrings)
    editedList = editandInsertLetters(subStrings)

    suggestions = set(deletedList + swappedList + editedList)
    suggestions_filtered = [s for s in suggestions if s in wordList]
    return suggestions_filtered #[0] returns an error. hack for now and chec later!

def editandInsertLetters(subStrings):
    returnList = []
    for part1, part2 in subStrings:
        if part2 and len(part2) > 0:
            for l in letters:
                returnList.append(part1 + l + part2[1:])
                returnList.append(part1 + l + part2)
        else:
            for l in letters:
                returnList.append(part1 + l + part2)
    return returnList

def swapLetters(subStrings):
    returnList = []
    for part1, part2 in subStrings:
        if len(part2) > 1:
            returnList.append(part1 + part2[1] + part2[0] + part2[2:])
    return returnList


def deleteLetters(subStrings):
    returnList = []
    for part1,part2 in subStrings:
        if part2 and len(part2) > 0:
            returnList.append(part1 + part2[1:])
    return returnList

def split(word):
    return [(word[:i],word[i:]) for i in range(0,len(word)+1)]


if __name__ == "__main__":
    main()
