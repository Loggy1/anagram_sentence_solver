# This script is used to first convert a list of all germans words into a list of all words sorted by their letters
# This is done to make the search for anagrams faster
# We are then able to search the list with a binary search

import os
import linecache
import requests

# Get most german words from https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
# Download this file and save it as german_words/words/wordlist-german.txt
def init():
    if os.path.isfile("german_words/words/wordlist-german.txt"):
        print("german words already downloaded")
    else:
        print("Building sorting tree for german words... This may take a while")
        os.mkdir("german_words/words") 
        print("downloading german words")
        url = "https://gist.githubusercontent.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4/raw/36b70dd6be330aa61cd4d4cdfda6234dcb0b8784/wordlist-german.txt"
        response = requests.request("GET", url, headers={}, data={})
        with open('german_words/words/wordlist-german.txt', "w") as f:
            f.write(response.text)
        print("done downloading german words")
        sort_letters()
        sort_words()
        tidy_up()

# Sort letters in each word
# We need this as we use binary search to find anagrams
# We then also sort the anagram so that we can compare the anagram to out sorted word in the binary search
def sort_letters():
    words=[]
    with open('german_words/words/wordlist-german.txt', "r") as f:
        for line in f:
            words.append((line.strip()).lower())
    print("done reading words")
    # Sorting letters in each word
    print("start sorting individual words")
    with open('german_words/words/german_words_sorted.txt', "w") as f:
        for word in words:
            # convert to sorted word
            sorted_word = [sorted(word), [word]]
            f.write(str(sorted_word) + "\n")
    print("done sorting words individual")

# Sort words by sorted letters of the original words
def sort_words():
    # Sort file by first element
    print("start sorting file")
    words = []
    with open('german_words/words/german_words_sorted.txt', "r") as f:
        for line in f:
            words.append(eval(line.strip()))
    words.sort(key=lambda x: x[0])
    with open('german_words/words/german_words_sorted_sorted.txt', "w") as f:
        for word in words:
            f.write(str(word) + "\n")
    print("done sorting file")

# Tidy up files by removing duplicate anagrams
# If files have the same line[0] then they are anagrams of each other
# We can then remove all lines that have the same line[0] as the previous line and add the word to the previous line
def tidy_up():
    print("start joining anagrams")
    words=[]
    with open('german_words/words/german_words_sorted_sorted.txt', "r") as f:
        for line in f:
            line = eval(line.strip())
            if len(words) > 0 and words[len(words)-1][0] == line[0]:
                # words are anagrams of each other
                anagrams = words[len(words)-1]
                anagrams[1].append(line[1][0])
                words[len(words)-1] = anagrams
            else:
                words.append(line)
    # write to file
    with open('german_words/words/german_words_sorted_joined.txt', "w") as f:
        for word in words:
            f.write(str(word)+ "\n")
    print("done joining anagrams")
    words[len(words)-1][0]

def fix_word(word):
    word = word.lower()
    word = word.replace(".", "")
    word = word.replace(",", "")
    word = word.replace("!", "")
    word = word.replace("?", "")
    word = word.replace(":", "")
    word = word.replace('"', "")
    word = word.replace("-", "")
    word = word.replace("(", "")
    word = word.replace(")", "")
    word = word.replace(";", "")
    word = word.replace("=", "")
    word = word.replace("[", "")
    word = word.replace("]", "")
    word = word.replace("[", "")
    # replace \u201e
    word = word.replace("\u201e", "")
    word = word.replace("\u201c", "")
    word = word.replace("\u0107", "")
    if any(char.isdigit() for char in word):
        return "zahl"
    return word

def fix_special_letters(words, original_word):
    has_upper = any(char.isupper() for char in original_word)
    has_dott = any(char in original_word for char in ["."])
    new_words = words

    # Checking for upper letters
    if has_upper:
        # Deletes all words that dont have the same upper letter as the original word
        new_words = words
        # Give all words an upper letter
        new_words = list(map(lambda x: x[0].upper() + x[1:], new_words))
        word_starts_with = original_word[next(i for i, c in enumerate(original_word) if c.isupper())]
        new_words = list(filter(lambda x: x[0] == word_starts_with, new_words))

    # Adding back the dott
    if has_dott:
        new_words = list(map(lambda x: x + ".", new_words))

    if len(new_words) == 0:
        return words
    
    return new_words

# We need hardcoded words for some smaller words
hardcoded_words = ["der", "die", "das", "in", "an", "im", "zu", "am", "er", "es", "wo", "wie", "sich", "gibt"]
# This function checks if the word is hardcoded
def is_hardcoded(word):
    for hardcoded_word in hardcoded_words:
        # Return True if the word contains same letters as one of the hardcoded
        if sorted(hardcoded_word) == sorted(word):
            return True
# Returns hardcoded anagrams
def get_hardcoded_anagrams(word):
    for hardcoded_word in hardcoded_words:
        if sorted(hardcoded_word) == sorted(word):
            return [hardcoded_word]
        
# Returns anagrams of a word
# If the word is hardcoded then we return the hardcoded anagrams
# Else we use binary search to find the word in the file we generated
# The file is sorted by all possible anagrams in the german language
# Attached to each of these anagrams are the related german words, which will be returned in this function
def search_word(word):
    if (is_hardcoded(fix_word(word))):
        return fix_special_letters(get_hardcoded_anagrams(fix_word(word)), word)
    word_found = sorted(fix_word(word))
    # binary search
    upper_bound = 1818418 #len(words)
    lower_bound = 0
    while(upper_bound - lower_bound > 1):

        # get middle word
        middle = (upper_bound + lower_bound) // 2
        line = linecache.getline('german_words/words/german_words_sorted_joined.txt', middle)
        line = eval((line).replace("\n", ""))
        # compare middle word with sorted_word and keep on searching
        if "".join(line[0]) == "".join(word_found):
            return fix_special_letters(line[1], word)
        elif "".join(line[0]) > "".join(word_found):
            upper_bound = middle
        else:
            lower_bound = middle
    print("word not found: " + word)
    return [word]
