from multiprocessing import Pool
from acronym import genAcronym

_pool = None

#for the worker:
dictionary_file = 'dictionary.txt'
#load dictionary data
with open(dictionary_file,'r') as f:
	dictionary = f.readlines()
dictionary = [i.strip('\n') for i in dictionary]
#define worker
def worker(words,clip):
	words = words.split(' ')
	clip = int(clip)
	result = genAcronym(words,clip,dictionary)
	for_web_result = []
	for r, row in enumerate(result):
		components = []
		for cell in row[1]:
			components.append([cell[0][:cell[1]],cell[0][cell[1]:]])
		processed_acronym = ''
		for l, letter in enumerate(row[2]):
			if letter == '?':
				processed_acronym += row[0][l]
			else:
				processed_acronym += letter

		for_web_result.append([row[0],components,processed_acronym,row[3]])
	return for_web_result

#-----------flask--------------

from flask import Flask, render_template, redirect, url_for, request, flash
import time
app = Flask(__name__)

app.secret_key = 'super_secret_key'

@app.route('/',methods=['GET','POST'])
def home():
	error = None
	start_time = time.time()
	if request.method == 'POST':
		try:
			if len(request.form['words']) == 0:
				error = 'Input word(s)'
			elif int(request.form['clip']) < 1:
				error = 'Clip too short!'
			else:
				f = _pool.apply_async(worker,[request.form['words'],request.form['clip']])
				r = f.get(timeout=10)
				for row in r:
					flash(row,'result')
				redirect(url_for('home'))
		except ValueError:
			error = 'Clip value not set'
	return render_template("index.html", error=error, processtime=round(time.time()-start_time,3))

if __name__ == '__main__':
	_pool = Pool(processes=4)
	try:
		app.run(debug=True)
	except KeyboardInterrupt:
		_pool.close()
		_pool.join()