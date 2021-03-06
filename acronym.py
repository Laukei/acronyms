#words = ['Quantum','Advanced','Nanowire','Detector','Photon','Superconductivity','Non-equilibrium','Nanoscale']
#clip = 5 #match at most first n letters of word in words

def genAcronym(words,clip,dictionary):
	#create list of possible fragments
	wildcards = list(str(words)).count('?')
	word_fragments = {i:[word.lower()[:clip][:i] for word in words] for i in range(1,clip+1)}

	successes = []
	for word in dictionary:
		mask = [None]*len(word)
		for i in sorted(word_fragments.keys())[::-1]:
			for f, fragment in enumerate(word_fragments[i]):
				if f not in mask and fragment in word:
					occupied = False
					for i in range(len(fragment)):
						if mask[i+word.index(fragment)] != None:
							occupied = True
					if occupied == False:
						for i in range(len(fragment)):
							mask[i+word.index(fragment)] = f
						if None not in mask:
							break
			if mask.count(None) <= wildcards:
				i = -1
				result = ''
				result_words = []
				for index in mask:
					if index != i:
						if index == None:
							result += '?'
							result_words.append(['?',1])
						else:
							result += words[index][:mask.count(index)]
							result_words.append([words[index],mask.count(index)])
							i = index
				successes.append([word,result_words,result,len(word)])
				break
	return sorted(successes, key=lambda s: len(s[0]))[::-1]
		
#for row in genAcronym(words,clip):
#	print row
