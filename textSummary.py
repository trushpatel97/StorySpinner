import bs4 as bs
import urllib.request
import re
import nltk
import heapq

source = urllib.request.urlopen('https://en.wikipedia.org/wiki/Coronavirus')
soup = bs.BeautifulSoup(source,'lxml')
maxWordsAllowed=15#no sentence should have more words than this many
maxSentencesAllowed=2#no more than this many sentences allowed
#getting all paragraphs in the html
text = ""
for paragraph in soup.find_all('p'):
    text += paragraph.text

#formatting the sentences
text = re.sub(r'\[[0-9]*\]',' ',text)
text = re.sub(r'\s+',' ',text)
#we want a clean text that has no periods commas etc as it would mess up our sentences
clean_text = text.lower()
clean_text = re.sub(r'\W',' ', clean_text)
clean_text = re.sub(r'\d',' ', clean_text)
clean_text = re.sub(r'\s+',' ', clean_text)

#tokenizing the text
sentences = nltk.sent_tokenize(text)
stop_words = nltk.corpus.stopwords.words('english')


word2count = {}#used for tracking score of the words
for word in nltk.word_tokenize(clean_text):#tokenize the words
    if word not in stop_words:#if it is not a stop word
        if word not in word2count.keys():#check to see if word is in the keys yet or not
            word2count[word] = 1#new word
        else:
            word2count[word] += 1#inc this frequency by one
            
for key in word2count.keys():#going through the keys 
    word2count[key] = word2count[key]/max(word2count.values())#dividing this specific word's frequency by the max numbers frequency
    
sent2score = {}#used for sentence score
for sentence in sentences:#go through the sentences 
    for word in nltk.word_tokenize(sentence.lower()):#lowercase the words
        if word in word2count.keys():#if the word is in 
            if len(sentence.split(' '))<maxWordsAllowed:#checks to see if the sentence is less than the specified
                if sentence not in sent2score.keys():#if sentence is not in the list
                    sent2score[sentence] = word2count[word]#add the words frequency score to sent2score
                else:
                    sent2score[sentence] += word2count[word]#sentence already in the list so we want to add the words score and update it
                    
best_sentences = heapq.nlargest(maxSentencesAllowed,sent2score,key=sent2score.get)#this will specify how many sentences allowed, get the sentences with the best scores and use those
newString = ""
for sentence in best_sentences:#printing the best sentences
    print(sentence)