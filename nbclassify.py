import sys,math,re

modelFile = "nbmodel.txt"
testFile = sys.argv[1]
outputFile = "nboutput.txt"
priors =[]
count = 0
vocabulary = {}
dictText = {}
stopwords = {}
stopwords = set()
classdict = {}
postDec = 0.0
postTru =0.0
postNeg = 0.0
postPos = 0.0


def readtext():
    with open(testFile) as textFile:
        for line in textFile:
            linelower = line.lower()
            words = line.strip().split()
            linelower = re.sub("\d+", "",linelower)
            linelower = re.sub(',|\.', ' ', linelower)
            linelower = re.sub(r'[^\w\s]', '', linelower)
            wordslower = linelower.strip().split()
            dictText[words[0]] = wordslower[1:]
        # print words[0]
        textFile.close()


def tokenize(wordlist):
    newlist = []
    for word in wordlist:
        if word not in stopwords:
            newlist.append(word)
    return newlist
# print dictText
# print dictLabels


def readstopwords():
    with open("stopwords.txt") as textFile:
        for line in textFile:
            words = line.lower().strip()
            stopwords.add(words)
        textFile.close()


with open(modelFile) as fileHandler:
    for line in fileHandler:
        words = line.strip().split()
        if count == 0:
            priors = [float(a) for a in words[1:]]
        elif count > 1:
            vocabulary[words[0]] = [float(a) for a in words[1:]]
        count += 1
    fileHandler.close()


readtext()
readstopwords()

# print priors
# print vocabulary
# print stopwords
# print tokenize(dictText['rml0T9JjRb5CeaejcoAv'])
# print dictText

for key in dictText:
    tokenlist = tokenize(dictText[key])
    postDec = priors[0]
    postTru = priors[1]
    postNeg = priors[2]
    postPos = priors[3]
    classes = []
    for token in tokenlist:
        if token in vocabulary:
            postDec += vocabulary[token][0]
            postTru += vocabulary[token][1]
            postNeg += vocabulary[token][2]
            postPos += vocabulary[token][3]
    if postDec > postTru:
        classes.append("deceptive")
    elif postDec <= postTru:
        classes.append("truthful")
    if postNeg > postPos:
        classes.append("negative")
    elif postNeg <= postPos:
        classes.append("positive")
    classdict[key] = classes

# print classdict

with open(outputFile,"w") as outputFileHandler:
    for key in classdict:
        outputFileHandler.write(key + " " + " ".join(classdict[key]) + "\n")