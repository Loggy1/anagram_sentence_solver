# General
This program decodes sentences whose words contain randomly mixed letters
For example "Es war der Wolf." would be written as "sE awr erd Wl.of".

For this purpose I use an anagram solver (tree_builder.py).
This solver works via binary search on a file made of most german words.
This file is provided by: [MarvinJWendt](https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4).

# Setup
1. pip install -r requirements.txt
2. start mixer.py

# How the code works
1. Get the text(mixed) and save it in sentences_normal.txt
2. Solve sentence by sentence
    1. Get all anagrams for each word in the sentence
    2. Use most probable sentence as solution using spaCy
