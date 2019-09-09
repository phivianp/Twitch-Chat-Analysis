from nltk.tokenize import word_tokenize
import json
import os
import ast

def find_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)
path = r'C:\Users\phunous\Documents\Fall 2017\Capstone\TwitchPython\loltyler1\\'
os.chdir(path)
vid = "v179154546.txt"
with open(vid,"r") as file:
    line = file.readline()
    print(line)
    index = find_2nd(line, ",") + 2
    third_item = line[index:]
    # time, body, fragments[]

    print(third_item)
file.close()

example = ['Mary had a little lamb' ,
           'Jack went up the hill' ,
           'Jill followed suit' ,
           'i woke up suddenly' ,
           'it was a really bad dream...']
tokenized_sents = [word_tokenize(i) for i in example]
for i in tokenized_sents:
    print(i)

data = "[{'emoticon': {'emoticon_set_id': ' ', 'emoticon_id': '120232'}, 'text': 'TriHard'}, {'text': ' 7'}]"
jsdata = ast.literal_eval(third_item)

for x in jsdata:
    if 'emoticon' in x:
        print(x['emoticon']['emoticon_id']+x['text'])


list = set()
list = [3,5,6,3,6,7,4,2]

for num in list:
    print(num)
print("-")
for num1 in list:
    print(num1)