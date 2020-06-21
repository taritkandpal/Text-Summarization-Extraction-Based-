import bs4 as bsoup
import urllib.request
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize






#Getting the text to be converted from a url

def get_content_of_article():

	#fetching the content from the URL
	fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/20th_century')
	#fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/French_Revolution')
	#fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Dinosaur')

	#read the scraped data object
	article_read = fetched_data.read()

	#parsing the URL content and storing in a variable
	article_parsed = bsoup.BeautifulSoup(article_read,'html.parser')

	#returning <p> tags
	#thus we only get that content from the html that is in paragraph tags
	paragraphs = article_parsed.find_all('p')

	#looping through the paragraphs and adding them to the variable
	article_content = ''
	for p in paragraphs:  
		article_content += p.text

	return article_content






#we will clean the text by removing the noise through stopwords in the nltk corpus
#we will also reduce words to their root form using Porter Stemmer
#we will also create a dictionary of the frequency of occurence of each word

def data_cleansing_and_frequency_table(text):
	
	#removing stop words
	stop_words = set(stopwords.words("english"))
	words = word_tokenize(text)
	
	#reducing words to their root form using stemming 
	#also creating the dictionary of word frequency
	freq = dict()
	stem = PorterStemmer()
	for var in words:
		#attaining the root word
		var = stem.stem(var)
		#if the word is in stopwords then dont include it in the table
		if var in stop_words:
			continue
		#if word already found then increment its frequency
		if var in freq:
			freq[var] += 1
		#if word found first time then insert it in table with frequency=1
		else:
			freq[var] = 1
	
	return freq






#we will  now calculate the score of each sentence
#based on the frequencies of the words in it
#frequency of each important word will be added to get the score
#score will be normalized by dividing score of each sentence by the number of words in the sentence

def sentence_score(sentences, freq):
	
	#score is a dictionary that will contain the score of each sentence
	#sentences will be indexed based on their first 15 characters
	score = dict()
	for sentence in sentences:
		totalwordcount = len(word_tokenize(sentence))
		wordcount_without_stopwords = 0
		#iterate freq table
		for checkword in freq:
			#if the word is also present in the sentence
			if checkword in sentence.lower():
				#increase no of words found
				wordcount_without_stopwords += 1
				#add the frequency of the word to the sentence score
				#also indexing of sentence is based on first 15 characters
				if sentence[:15] in score:
					score[sentence[:15]] += freq[checkword]
				else:
					score[sentence[:15]] = freq[checkword]

		#normalize the score using number of important words
		score[sentence[:15]] = score[sentence[:15]] / wordcount_without_stopwords

	return score






#calculating the threshhold score of the sentences

def threshhold_score(score):

	#get total score for sentences
	sum_sentence = 0
	for var in score:
		sum_sentence += score[var]

	#average score
	avg = sum_sentence / len(score)

	return avg






#Getting the article summary
#those sentences that have a score greater than threshhold will be added to the summary

def article_summary(sentences, score, threshhold):

	summary = ''
	for sentence in sentences:
		if sentence[:15] in score and score[sentence[:15]] > threshhold:
			summary += sentence + " "

	return summary






#main function

def Main():
	#Getting the text to be converted from a url
	article = get_content_of_article()
	
	#getting frequency table and cleaning the data
	freq_table = data_cleansing_and_frequency_table(article)

	#tokenizing the sentences
	sentences = sent_tokenize(article)

	#getting the sentence scores
	score = sentence_score(sentences, freq_table)

	#getting the threshhold score
	threshhold = threshhold_score(score)
	#this multiplication factor to the threshhold will control the size of the summary
	#greater the factor, smaller the summary
	threshhold = 1.5*threshhold

	#getting the final summary
	summary = article_summary(sentences, score, threshhold)

	print(summary)






if __name__ == '__main__':

	Main()

	