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

    #part of speech of the word is determined.
    pos_tag = nltk.pos_tag(nltk.word_tokenize(unigram))

    #if the unigram is a NNP or NNPS (proper noun) then it is retuned without any spell check
    if pos_tag and len(pos_tag) == 1:
        unigram,pos = pos_tag[0]
        if pos in ['NNP','NNPS']:
            return unigram
    else:
        return unigram

    #for all other words do this
    #determine if any word has occurances of the same letter more than 3 times consecutively.
    #all these wrods are condensed to a shorter version.
    #for example: haaaapppyyyy is converted to hapy.
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)

    #since ing words are not part of the nltk word list, a small hack to retain those words.
    pattern1 =  re.compile("(ing)$")  #hack for all words ending in ing

    #logic to reduce the words (haappyyyy -> hapy)
    if len(pattern.findall(unigram)) > 0:
        approxWord = ''.join(letter for letter, _ in itertools.groupby(unigram))
    else:
        approxWord = unigram

    #if the word has ing, stem it here
    if len(pattern1.findall(approxWord)) > 0:
        approxWord = approxWord[0:len(approxWord)-3]

    #if the word is not in dictionary, run spell check.
    if approxWord not in wordList  and '\'' not in unigram and '-' not in unigram:
        suggestions =findSuggestions(approxWord)
        if len(suggestions) > 0:
            return suggestions[0]
        else:
            return approxWord
    else:
        return approxWord


def findSuggestions(word):

    #this uses Norvig's spell check algorithm
    #this does 4 things
    #1. Delete individual letters,
    #2. Swap characters
    #3. Edit each character
    #4. Insert characters.

    subStrings = split(word)
    deletedList = deleteLetters(subStrings)
    swappedList = swapLetters(subStrings)
    editedList = editandInsertLetters(subStrings)

    #after the processing, distinct list of suggestions is returned
    suggestions = set(deletedList + swappedList + editedList)

    #form the list, all invalid words ae weeded out
    suggestions_filtered = [s for s in suggestions if s in wordList]

    #and the final list is returned
    return suggestions_filtered #[0] returns an error. hack for now and chec later!

def editandInsertLetters(subStrings):
    returnList = []
    for part1, part2 in subStrings:
        if part2 and len(part2) > 0:
            #insert a new letter from a to  in each possible position
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
        #swap every pair of letters in the word
        if len(part2) > 1:
            returnList.append(part1 + part2[1] + part2[0] + part2[2:])
    return returnList


def deleteLetters(subStrings):
    returnList = []
    for part1,part2 in subStrings:
        #delete individual letters and for ma a new list
        if part2 and len(part2) > 0:
            returnList.append(part1 + part2[1:])
    return returnList

def split(word):
    #returns a list of words split in different combinations
    #hell is returned as (h,ell),(he,ll), (hel,l), (hell,) etc.
    return [(word[:i],word[i:]) for i in range(0,len(word)+1)]


if __name__ == "__main__":
    main()
