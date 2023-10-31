import datetime
import re

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
				files_list.append(match.group(1))
	
	return files_list

all_data = []

pattern = r'^(\d+)\$\d+\$(.+?)\$\d+\$\d+\$\d+\$\d+\$\d+\$\$(\d+)\$\d+\$\d+\$\d+\$'

with open('pl_pages.php', 'r', encoding='utf-8') as pages_file:
	for pages_line in pages_file:
		match = re.search(pattern, pages_line)
		if match:
			page_id, page_content, page_date = match.group(1), match.group(2), match.group(3)
			page_ext = find_ext(page_id + "$")
			page_files = find_files(page_id)
			
			all_data.append((page_date, page_content, page_ext, page_files,))

all_data.sort(key = lambda x: x[0])

print(all_data)


'''
timestamp = 1007293260
data_i_czas = datetime.datetime.fromtimestamp(timestamp)



print(data_i_czas)
'''
