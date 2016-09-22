import nltk
import re
import string 

class Preprocessing(object):
	""" Handles feature engineering and automating label assignment(wherever possible) """ 

	def __init__(self):
		"""
		Initializing regex patterns and parameters for easy extraction 
		"""
		super(Preprocessing, self).__init__()

		url_regex = r'^(//)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$'
		self.pattern = re.compile(url_regex)
		self.indicators = set({'by','at','in','"s','over','about','of'})

		#just to automate tagging, not features  
		self.days = set({'monday','tuesday','wednesday','thursday','friday','saturday','sunday'})
		self.disasters = set({'earthquake','quake','storm','flood','flash','flooding','floods','storms','landslide','typhoon','super-typhoon','tsunami','landslides','blaze','volcano','eruption','volcanoes','fire','wildfire','rain','rains'})
		self.months = set({'january','february','march','april','may','june','july','august','september','october','november','december'})
		self.cities_for_label = set({'Italy','Bam', 'Minamisanriku','Alaska'})
		self.ignore = set({'.',':','km','th'})
		self.punctuation = string.punctuation

	def tokenize_feature(self, filename, labelfile, flag, outputfile):
		"""
		Use nltk to tokenize and featurize tokens 

		Input : Filename containing raw text 
		Output : outputfile containing List[List[Word, f1, f2, f3, ...fn, label]] 

		Optional : Missing/Additional labels are added manually - To retain those changes, set flag=True. 
		Function will read labels directly from labelfile if true. 
		"""

		f = open(filename, "r")
		lines = f.readlines()
		data = [line for line in lines if line!='\n']
		f.close()

		listt = []

		for index in range(len(data)):
			line = nltk.word_tokenize(data[index].decode("utf8").strip('\n'))
			line = nltk.pos_tag(line)

			for pred in line:
				isNumber = 1 if pred[0].isnumeric() else 0

				text = pred[0].encode('ascii', 'ignore')
				if pred[1] == 'CD':
					isNumber = 1 

				isCapital = 1 if text and text[0].isupper() else 0	
				first = text[0] if text else ""
				last = text[-1] if text else ""
				punc = 1 if text in self.punctuation else 0 

				checkLink = self.pattern.search(text)
				isLink = 1 if checkLink else 0 

				label = "Irrelevant"

				if text in self.cities_for_label:
					label = "Location" 

				if text: 
					pref3 = text[:3] 
					pref4 = text[:4]
					suff3 = text[-3:]
					suff4 = text[-4:]
					length_ = len(text)
					len1 = 1 if length_==1 else 0 
					len2 = 1 if length_==2 else 0
					len35 = 1 if length_>=3 and length_<=5 else 0
					len6 = 1 if length_>=6 else 0 
				else:
					pref3, pref4, suff3, suff4, len1, len2, len35, len6 = 0, 0, 0, 0, 0, 0, 0, 0

				lower = text.lower()

				isIndicator = 1 if lower in self.indicators else 0
				isMonth = 1 if text in self.months else 0
				
				if lower in self.days or lower in self.months:
					label = "Time"
				if isNumber and len(lower)==4 and (lower not in self.ignore) and not lower.isalpha():
					label = "Time"
				if lower in self.disasters:
					label = "Disaster"


			 	listt.append([text, pred[1], isNumber, isCapital, isIndicator, isMonth, isLink, punc, first, last, pref3, pref4, suff3, suff4, len1, len2, len35, len6, label])
			listt.append("\n")

		if flag:
			l = open(labelfile, "r")
			lines = l.readlines()
			l.close()
			labels = [line.strip('\n').split(" ")[-1] if line!='\n' else '\n' for line in lines]

			for i in range(len(labels)):
				if listt[i]!='\n':
					listt[i][-1] = labels[i]

		f = open(outputfile,"w+")
		for index in listt:
			f.write(" ".join(map(str,index)))
			if index!='\n':
				f.write("\n")
		f.close()

if __name__ == '__main__':
	train = Preprocessing()
	train.tokenize_feature("../training/raw.txt", "../training/labels.txt", True, "../training/training.txt")

	high = Preprocessing()
	high.tokenize_feature("../testing/raw_high.txt", "../testing/high_labels.txt", True, "../testing/testing_high.txt")

	low = Preprocessing()
	low.tokenize_feature("../testing/raw_low.txt", "../testing/low_labels.txt", True, "../testing/testing_low.txt")

