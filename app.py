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
	return result

#-----------flask--------------

from flask import Flask, render_template, redirect, url_for, request, flash
app = Flask(__name__)

app.secret_key = 'super_secret_key'

@app.route('/',methods=['GET','POST'])
def home():
	error = None
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
					flash(row[2])
				redirect(url_for('home'))
		except ValueError:
			error = 'Clip value not set'

	return render_template("index.html", error=error)

if __name__ == '__main__':
	_pool = Pool(processes=4)
	try:
		app.run(debug=True)
	except KeyboardInterrupt:
		_pool.close()
		_pool.join()