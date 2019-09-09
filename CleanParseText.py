#This Program finds the popular words of the existing files
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
#tokenizer = RegexpTokenizer('\w+')
import ast
import json
import os

def find_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)

path = r'C:\Users\phunous\Documents\Chat\loltyler1\\'

os.chdir(path)
print("Current Path is "+os.getcwd())
vid = "v214173238.txt"

with open(vid, "r") as chat:
    newfile = "Pop_Phrase_Emoji" + vid
    countemo = dict()
    countword = dict()
    popword = set()
    popemo = set()
    print("Length Emo: " + str(len(countemo)))
    print("Length Word: " + str(len(countword)))
    if (os.path.isfile(newfile)):
        print('chat from video ' + newfile + ' has been parsed.')
    else:
        with open(newfile, "w") as filewriter:
            for record in chat:
                index = find_2nd(record, ",") + 2
                third_item = record[index:]
                # time, body, fragments[]
                try:
                    fragments = ast.literal_eval(third_item)
                except SyntaxError:
                    pass
                except ValueError:
                    pass
                for x in fragments:
                    if (type(x) is not dict):
                        pass

                    elif 'emoticon' in x:
                        emotext = x['text'].lower
                        emo = emotext

                        if emo in countemo:
                            countemo[emo] += 1
                        else:
                            countemo.update({emo: 1})
                    else:
                        if "text" in x:
                            text = x['text'].lower()
                            tokenizer = RegexpTokenizer(r'\w+')
                            words = tokenizer.tokenize(text)
                            filtered_words = [word for word in words if word not in stopwords.words('english')]
                            for word in filtered_words:
                                if word in countword:
                                    countword[word] += 1
                                else:
                                    countword.update({word: 1})

            wor = [(k, countword[k]) for k in sorted(countword, key=countword.get, reverse=True)]
            em = [(k, countemo[k]) for k in sorted(countemo, key=countemo.get, reverse=True)]

            #create popular dictionaries
            for key, value in wor:
                if value > 100:
                    filewriter.write(key + ": " + str(value) + "\n")
                    popword.add(key)
            print("words added")
            for key, value in em:
                if value>70:
                    filewriter.write(key + ": " + str(value) + "\n")
                    popemo.add(key)
            print("emotes added")

            print(newfile + " is Done")
        filewriter.close()
    chat.seek(0)
    with open("CSV"+vid, "w") as f:
        #collect bodies of the first 60 seconds
        #add it into dictionary and parse that dictionary
        chunk = dict()
        for record in chat:
            list = record.split(", ")
            #time
            time = float(list[0])
            minute = int(time/60)
            text = list[1]
            if minute in chunk.keys():
                chunk[minute] += " "
                chunk[minute] += text

            else:
                chunk.update({minute: text})

        #write the attributes
        f.write("Minute, ")
        for wor in popword:
            f.write(wor+", ")
        for em in popemo:
            f.write(emo+", ")
        f.write("\n")
        for key, value in chunk.items():
            cword = dict()
            cemote = dict()
            value = value.lower()
            tokenizer = RegexpTokenizer(r'\w+')
            words = tokenizer.tokenize(value)
            filtered_words = [word for word in words if word not in stopwords.words('english')]
            for word in filtered_words:
                if word in popword:
                    if word in cword.keys():
                        cword[word] +=1
                    else:
                        cword.update({word: 1})
                if word in popemo:
                    if word in cword.keys():
                        cword[word] +=1
                    else:
                        cword.update({word: 1})
            f.write(str(key)+", ")
            for word in popword:
                if word in cword:
                    f.write(str(cword[word])+", ")
                else:
                    f.write("0, ")
            for emo in popemo:
                if emo in cemote:
                    f.write(str(cemote[emo])+", ")
                else:
                    f.write("0, ")
            f.write("\n")
    f.close()
print("Done")
chat.close()





