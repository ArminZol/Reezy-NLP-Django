def save(text, file_name = 'data.txt'):
	print 'Appending to file:', file_name

	file = open(file_name, 'a')

	for line in text:
		try:
			file.write(line.encode('utf8', 'replace').strip() + ' ')
		except:
			print 'Line:', '"' + line + '"', 'couldn\' be converted to unicode'

	file.close()