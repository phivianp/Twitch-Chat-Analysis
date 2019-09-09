from nltk.tokenize import word_tokenize
import json
import os
path = r'C:\Users\phunous\Documents\Fall 2017\Capstone\TwitchPython\\'

with open(path+"Streamers.txt", "r") as file:
    for user in file:
        os.chdir(path+user)

        print("Current Path: "+os.getcwd())
        for filename in os.listdir(path+user):
            with open(path+user+"\\"+filename,"r") as chat:
                for record in chat:
                    newfile = "Pop_Phrase_Emoji" + filename
                    newpath = path + user + '\\' + newfile

                    if (os.path.isfile(newpath)):
                        print('chat from video ' + newfile + ' has been parsed.')
                    else:
                        with open(newfile, "w") as filewriter:
                            countemo = dict()
                            countword = dict()
                            list = record.split(",")
                            #time, body, fragments[]
                            fragments = json.dumps(list[2])
                            for x in fragments:
                                if 'emoticon' in x:
                                    emoid = x['emoticon']['emoticon_id']
                                    emotext = x['text']
                                    emo = emotext+emoid
                                    if emo in countemo.keys():
                                        countemo[emo] += 1
                                    else:
                                        countemo.append(emo,1)
                                else:
                                    words = word_tokenize(x.get('text'))
                                    for word in words:
                                        if word in countword.keys():
                                            countword[word] += 1
                                        else:
                                            countword.append(word,1)

                            for key,value in countword.items():
                                filewriter.write(key+": "+value+"\n")

                            for key,value in countemo.items():
                                filewriter.write(key + ": " + value + "\n")

                            filewriter.close()

                chat.close()
    file.close()
                    #Later, After Finding All Phrases and Words
                    #newfile = "parse"+filename
                    #newpath = path + user + '\\' + newfile

                    #if (os.path.isfile(newpath)):
                        #print('chat from video ' + newfile + ' has been parsed.')
                    #else:
                        #with open(newfile,"w") as filewriter:


