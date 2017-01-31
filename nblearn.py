import sys, re, math

trainText = sys.argv[1]
trainLabel = sys.argv[2]
dictLabels = {}
dictText = {}
vocabPositive = {}
vocabNegative = {}
stopwords = {}
stopwords = set()
vocabTru = {}
vocabDec = {}
poscount = 0.00
negcount = 0.00
trucount = 0.00
deccount = 0.00
vocabulary = {}
prob = [0.0,0.0,0.0,0.0]
# vocabulary = set()

def tokenize(wordlist):
    newlist = []
    for word in wordlist:
        if word not in stopwords:
            newlist.append(word)
    return newlist

def readlabel():
    with open(trainLabel) as labelsFile:
        for line in labelsFile:
            words = line.strip().split()
            dictLabels[words[0]] = words[1:]
        labelsFile.close()

def readtext():
    with open(trainText) as textFile:
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

# print dictText
# print dictLabels
def readstopwords():
    with open("stopwords.txt") as textFile:
        for line in textFile:
            words = line.lower().strip()
            stopwords.add(words)
        textFile.close()

# print stopwords
# ne = tokenize(dictText["1Fkd0gQRjV7aA9zeddBs"])
# print ne
readlabel()
readstopwords()
readtext()


for key in dictLabels:
    if dictLabels[key][0] == "deceptive":
        tokenlist = tokenize(dictText[key])
            # print tokenlist
        deccount += len(tokenlist)
        for token in tokenlist:
            if token in vocabDec:
                vocabDec[token] += 1.0
            else:
                vocabDec[token] = 1.0
            if token not in vocabulary:
                vocabulary[token] = 1.0
    elif dictLabels[key][0] == "truthful":
        tokenlist = tokenize(dictText[key])
        trucount += len(tokenlist)
        # print tokenlist
        for token in tokenlist:
            if token in vocabTru:
                vocabTru[token] += 1.0
            else:
                vocabTru[token] = 1.0
            if token not in vocabulary:
                vocabulary[token] = 1.0
    if dictLabels[key][1] == "positive":
        tokenlist = tokenize(dictText[key])
            # print tokenlist
        poscount += len(tokenlist)
        for token in tokenlist:
            if token in vocabPositive:
                vocabPositive[token] += 1.0
            else:
                vocabPositive[token] = 1.0
            if token not in vocabulary:
                vocabulary[token] = 1.0
    elif dictLabels[key][1] == "negative":
        tokenlist = tokenize(dictText[key])
            # print tokenlist
        negcount += len(tokenlist)
        for token in tokenlist:
            if token in vocabNegative:
                vocabNegative[token] += 1.0
            else:
                vocabNegative[token] = 1.0
            if token not in vocabulary:
                vocabulary[token] = 1.0
# separateclasses()
print "DEC"
print vocabDec
print deccount
print len(vocabDec)
print "TRU"
print vocabTru
print trucount
print len(vocabTru)
print "NEG"
print vocabNegative
print negcount
print len(vocabNegative)
print "POS"
print vocabPositive
print poscount
print len(vocabPositive)
print "VOC"
print vocabulary
vocablength = len(vocabulary)
print vocablength

with open("nbmodel.txt","w") as modelfile:
    try:
        modelfile.write("token\tDEC\tTRU\tNEG\tPOS\n")
        for key in vocabulary:
            prob = [0.0,0.0,0.0,0.0]
            if key in vocabDec:
                prob[0] = ((vocabDec[key] + 1.0)/(deccount + vocablength))
            else:
                prob[0] = (1.0 / (deccount + vocablength))
            if key in vocabTru:
                prob[1] = ((vocabTru[key] + 1.0)/(trucount + vocablength))
            else:
                prob[1] = (1.0 / (trucount + vocablength))
            if key in vocabNegative:
                prob[2] = ((vocabNegative[key] + 1.0)/(negcount + vocablength))
            else:
                prob[2] = (1.0 / (negcount + vocablength))
            if key in vocabPositive:
                prob[3] = ((vocabPositive[key] + 1.0)/(poscount + vocablength))
            else:
                prob[3] = (1.0 / (poscount + vocablength))
            modelfile.write(key + " : " + " ".join([repr(math.log10(i)) for i in prob]) + "\n")
    except:
        print "Exception in writing model"
    modelfile.close()
