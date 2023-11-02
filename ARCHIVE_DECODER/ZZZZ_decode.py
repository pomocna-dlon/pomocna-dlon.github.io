import re
import datetime
import os

def find_ext(page_id):
	pattern = r'^\d+\$(.*)\$\$\$\$\$\$\$\d+\$'
	
	with open('pl_pages_ext.php', 'r', encoding='utf-8') as pages_ext_file:
		for pages_ext_line in pages_ext_file:
			if pages_ext_line.startswith(page_id):
				match = re.search(pattern, pages_ext_line)
				page_content = match.group(1)
				return page_content
	
	return None

def find_files(page_id):
	files_list = []
	
	pattern = r'^\d+\$' + page_id + '\$([^\$]+)'
	
	with open('pl_pages_files.php', 'r', encoding='utf-8') as pages_files_file:
		for pages_files_line in pages_files_file:
			match = re.search(pattern, pages_files_line)
			if match:
				for i in ("01", "02",):
					file_path = "../img/archive_files/%s/%s"%(i, match.group(1),)
					if os.path.isfile(file_path):
						os.rename(file_path, file_path.lower())
						file_path = file_path.lower()
						
						if not file_path[-3:] in ("swf", "doc", "docx", "pdf",):
							files_list.append("img/archive_files/%s/%s"%(i, os.path.basename(file_path),))
	
	return files_list
	
def remove_unwanted_stuff(s):
	s = re.sub(r'\s*style=(?:"[^"]*"|\'[^\']*\')', '', s)
	s = re.sub(r'<object[^>]*>.*?</object>', '', s)
	s = re.sub(r'<p>\s*</p>', '', s)
	s = re.sub(r'<p>(<br\s*/?>\s*)+</p>', '', s)
	s = re.sub(r'(<br\s*/?>\s*)+', '<br>', s, flags=re.IGNORECASE)
	s = s.replace("<span>", '')
	s = s.replace("</span>", '')
	s = re.sub(r'<script[^>]*>.*?</script>', '', s)
	
	return s

all_data = []

pattern = r'^(\d+)\$\d+\$(.+?)\$\d+\$\d+\$\d+\$\d+\$\d+\$\$(\d+)\$\d+\$\d+\$\d+\$'

with open('pl_pages.php', 'r', encoding='utf-8') as pages_file:
	for pages_line in pages_file:
		match = re.search(pattern, pages_line)
		if match:
			page_id, page_content, page_date = match.group(1), match.group(2).replace("$$", "").strip(), match.group(3)
			page_ext = find_ext(page_id + "$").strip()
			page_files = find_files(page_id)
			
			all_data.append((page_date, datetime.datetime.fromtimestamp(int(page_date)), page_content, page_ext, page_files,))

all_data.sort(key = lambda x: x[0])

all_data_by_year = dict()

for data in all_data:
	if not data[1].year in all_data_by_year:
		all_data_by_year[data[1].year] = []
	
	all_data_by_year[data[1].year].append(data)
		

for year in all_data_by_year.keys():
	with open('../Archive' + str(year) + '.md', 'w', encoding='utf-8') as f:
		f.write("""---
title: Archiwum %d
---

"""%(year,))

		for data in all_data_by_year[year]:
			f.write('<div class="archiveItem">\n<i>')
			f.write(str(data[1]))
			f.write("</i><br>\n")
			f.write(remove_unwanted_stuff(data[2]))
			f.write("<br>\n")
			f.write(remove_unwanted_stuff(data[3]))
			f.write("<br>\n")
			
			if len(data[4]) > 0:
				f.write('<a href="#" class="loadImages">ZOBACZ ZDJĘCIA</a><br>\n<div class="centerImgsEmpty">\n')
			
			for img in data[4]:
				f.write('<a href="%s" target="_blank"><img data-src="%s" /></a><br>\n'%(img, img,))
			
			if len(data[4]) > 0:
				f.write("</div>\n")
			f.write("</div>\n")

#print(all_data)
