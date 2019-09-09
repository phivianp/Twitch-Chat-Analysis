from collections import Counter
from nltk.tokenize import RegexpTokenizer
import pprint
import codecs
import collections

pp = pprint.PrettyPrinter(indent=4)
tokens = RegexpTokenizer(r'\w+')
global data, markov_model, newmarkov_model, node_model, newnode_model
data = {}
markov_model = {}
newmarkov_model = {}
node_model = {}
newnode_model = {}

def read_file():
    """ Read in the contents of a file. """
    global data

    with open ('77416610&114323060.txt', 'r', encoding="utf8") as f:
        d = f.readlines()
    f.close()
    for line in d:
        list = line.split("^*") # Split ^* from each line.
        #cant have list as a key, only a string
        data.update({list[0]: list[1]}) #message: sexual rating, string: string

def markov():
    """ Build the Markov Model. Not using Dictogram Class."""
    global data, markov_model
    #Basically Auto-Complete
    for key in data.keys():
        message = tokens.tokenize(key)
        for index in range(0, len(message) - 1):
            # print(x[word]) # inital word.
            # print(x[word+1]) # next word.

            if message[index] in markov_model:#Check if word is in Markov
                if message[index + 1] in markov_model[message[index]].keys(): #Check if the second word is in inner dict
                    markov_model[message[index]][message[index + 1]] =+ 1
                else:
                    newdict = {message[index + 1]: 1}
                    markov_model[message[index]].update(newdict)

            else:
                newdict = {message[index + 1]: 1}
                markov_model.update({message[index]:newdict})

       #word : {word2 : #}
        # dont need to reverse

def get_edge_values ():
    global markov_model, newmarkov_model
    for word ,inner in markov_model.items():
        number_of_edges = sum(inner.values()) # this is the sum of all the OUTWARD edges of one word
        for word2,num in inner.items():
            newnode = float (num / number_of_edges)
            if word in newmarkov_model:#Check if word is in New Markov
                if word2 not in newmarkov_model[word].keys(): #Check if the second word is not in inner dict
                    newdict = {word2: newnode}
                    newmarkov_model[word].update(newdict)

            else:
                newdict = {word2: newnode}
                newmarkov_model.update({word:newdict})


def count_total_messages():
    """ Collect all of the Messages in a Response."""
    global data
    count = len(data) # get length of file list, messages are already is a sequence.
    count_2 = 0
    for message, sexrate in data.items():
        if sexrate == '2': #match string or numeric
            count_2 += 1
    count += count_2

    return count

def count_words():
    """ Collect of all of the Words in a File and Count their Occurrence. """
    total = {}
    global data
    for key,rate in data.items():
        comment = set(tokens.tokenize(key))
        #just look for unique because it will count more than once per comment

        if rate == '1':
            for word in comment:
                if word in total.keys():
                    total[word] += 1
                else:
                    total.update({word: 1})
        if rate == '2':
            for word in comment:
                if word in total.keys():
                    total[word] += 2
                else:
                    total.update({word: 2})

    return total

def get_node_values(count_of_word: dict, total_messages: float):
    """ Get the Node Values of each Word. """
    global node_model
    for word, count in count_of_word.items():
        nodevalue = float(count/total_messages)
        node_model.update({word:nodevalue})

def get_new_node():
    #Look at every single keys of the value to find the edge towards the node
    global node_model, newmarkov_model , newnode_model
    for searchword, nodevalue in node_model.items():
        newnode = nodevalue
        for word, innerdict in newmarkov_model.items():#search through every edge
            for innerkey , edgevalue in innerdict.items():
                if searchword == innerkey:
                    newnode += float(node_model.get(word, 0) * edgevalue)
        newnode_model.update({searchword:newnode})


#(1)
read_file()
#in data, always tokenize the key to get each word


#(2)
markov()

#(3)
# Now update the edge value by counting mentions OUTWARD
get_edge_values()

#(4)Find the node value
#Denominator
total_messages = count_total_messages() #very sexual count as 2
#print(total_messages)

#Numerator
count_of_words = count_words() #should be a dictionary {word:mentions}
#print(count_of_words)

#Numerator/Denonminator = Node Model Value
get_node_values(count_of_words, total_messages)
#print(node_model)


#(5)Update new node value
get_new_node()

#Sort them, because we need to know if consistent
#Write them into file, data and node values
ordered_datakeys = sorted(data)
r = codecs.open('Data.txt', 'w', 'utf-8')
for key in ordered_datakeys:
    r.write(key +": "+data[key]+"\n")
r.close()
ordered_modelkeys = sorted(newnode_model)
with open('NewNodeModel.txt', 'w') as f:
    for key in ordered_modelkeys:
        f.write(key +": "+str(newnode_model[key])+"\n")
f.close()

#Test for probability
example0 = "go for the kill cuz she cant kill"
example1 = "Kaceytron makes a hospital porno"
example2 = "Bitch are u live if ye then take out your clothes"
#probability = average of node values

list0 = example0.split()
list1 = example1.split()
list2 = example2.split()

sum0 = 0
sum1 = 0
sum2 = 0

#Calculate the averages
for word in list0:
    sum0 += newnode_model.get(word, 0)
    print(newnode_model.get(word, 0))
print(example0 +"= " +str((sum0/len(list0))*1000))

for word in list1:
    sum1 += newnode_model.get(word, 0)
    print(newnode_model.get(word, 0))
print(example1 +"= " +str((sum1/len(list1))*1000))

for word in list2:
    sum2 += newnode_model.get(word, 0)
    print(newnode_model.get(word, 0))
print(example2 +"= " +str((sum2/len(list2))*1000))