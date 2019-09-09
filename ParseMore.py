#Lets parse the fine from Chat directory
#Goal: first dataset of tyler1,ninja,traceytron
    # second dataset of wraxu, psychobunny, and drdisrespectlive
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import ast
import json
import os


path = "C:/Users/phunous/Documents/Chat/Try"

global poptword,poptemo
poptemo = set()
poptword = set()

def findpopular(streamer: str):
    popemo = []
    popwor = []


    #Should also write that into a file
    #Return Top 25 each
    return popwor, popemo

def writedata(path: str,info: list):



#main

#list of streamers
#streamers = []
#with open(path + "Streamers.txt", "r") as file:
    #streamers = file.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    #streamers = [x.strip() for x in streamers]
#file.close()

#let's not loop, just select which streamer
popword1,popemo1  = findpopular("v108826042.txt")
popword2,popemo2 = findpopular("v109020966.txt")
popword3,popemo3 = findpopular("v214173238.txt")

#All Popular

poptword = popword1+popword2+popword3

poptemo = popemo1+popemo2+popemo3

#Select one video from each streamer
#Read the first line and make it into a list so we can easily get the data
#Manually copy the path
#0-id, 1-streamer, 2-game, 3-length

video1=[]
video2=[]
video3=[]
#Count and write it into a CSV form
writedata(path1,video1)
writedata(path2,video2)
writedata(path3,video3)

#Manually append all three files into 1