from bs4 import BeautifulSoup
import random
import spacy
nlp = spacy.load("de_core_news_lg")
from german_words.tree_builder import search_word, init


sentences = ["Das ist ein Satz.", "Das ist ein anderer Satz.", "Das ist ein dritter Satz."]
with open("sentences_normal.txt", "w") as f:
    f.writelines("")

# shuffle each line
for sentence in sentences:
    sentence = sentence.split()
    newsentence = []
    # shuffle letters in each word
    for word in sentence:
        word = list(word)
        random.shuffle(word)
        word = "".join(word)
        newsentence.append(word)
    sentence = " ".join(newsentence)
    with open("sentences_normal.txt", "a") as f:
        f.writelines(sentence + "\n")
        
# This function returns a list of anagrams for a given word
# We use binary search on all german words to find the anagrams
def get_anagrams(word):
    return search_word(word)

# Returns the word out of list that is most related to a given word
def get_next_word(word, list):
    similarity_scores = [nlp(word).similarity(nlp(w)) for w in list]
    best_word = list[similarity_scores.index(max(similarity_scores))]
    return best_word

# This function returns the most probable sentence from a list of sentences
def get_most_probable_sentence(anagrams):
    sentence = ""
    last_word = ""
    for anagram in anagrams:
        word=""
        if last_word != "":
            word = get_next_word(last_word, anagram)
        else:
            word = anagram[0]
        sentence += word + " "
        last_word = word
    return sentence


# Gets html from the given website
def getArticleWebpage(url):
    import requests
    response = requests.request("GET", url, headers={}, data={})
    return(response.text)

# This function writes the encoded article to a file
# TODO: This needs redooing if u want to use this for any page that doesnt match the format of the given page
def writeArticle(title, description, sections):
    # Join sections together. 
    joined_sections = ""
    for section in sections:
        splitted_text = section.text.split(" ")
        for word in splitted_text:
            # Filter out empty words
            if word == " " or word == "" or len(word) == 1:
                continue
            word = word.replace("\n", "")
            # After every dot a new line is added
            if "." in word and len(word)>2:
                joined_sections += word + "\n"
            else:
                joined_sections += word + " "
    with open("sentences_solved.txt", "w") as f:
        f.writelines(title + "\n" + description + "\n")
    with open("sentences_normal.txt", "w") as f:
        f.writelines(joined_sections)

# This function gets the article from the webpage and writes it to a file
# TODO: This needs redooing if u want to use this for any page that doesnt match the format of the given page
def getArticle():
    soup = BeautifulSoup(getArticleWebpage("link to a page"), "html.parser") # TODO: Add link to a page
    title = soup.find("meta", property="og:title").get("content")
    description = soup.find("meta", property="og:description").get("content")
    sections = soup.find_all("p", class_="text text-blurred")
    writeArticle(title, description, sections)


# Solve sentence by sentence
# Get all anagrams for each word in the sentence
# Get all possible sentences from the anagrams
# Use most probable sentence as solution using spacy
init()
#TODO set up getArticle() if u want to pull webcontent and unscrammble it
sentences = []
with open("sentences_normal.txt", "r") as f:
    for line in f:
        sentences.append(line)
# remove old file
with open("sentences_solved.txt", "w") as f:
        f.writelines("")
for sentence in sentences:
    print(sentence)
    anagrams = []
    sentence = sentence.split()
    for word in sentence:
        try:
            anagrams.append(get_anagrams(word))
        except:
            anagrams.append([word])
    anagrams = get_most_probable_sentence(anagrams)

    with open("sentences_solved.txt", "a") as f:
        f.writelines(anagrams + "\n")
print("Solved text can be found in sentences_solved.txt")