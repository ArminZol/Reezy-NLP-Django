from words_db import Worker, Analyzer

import os

w = Worker()
a = Analyzer(w)

count = 0

for dirpath, dirnames, files in os.walk('../../../text_content'):
	for name in files:
		location = os.path.join(dirpath, name)
		a.fitfile(open(location), True)
w.finish()