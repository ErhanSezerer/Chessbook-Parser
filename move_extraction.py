import os
import re

def parse_text(f):

	content = f.read()

	# standard move description e.g. KtxP
	#move_1 = re.search("\s{1}(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?\s?(-|x|X)\s?(\n)?(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?(\d)?(\s)?(double)?(\n)?(ch)?(mate)?", content, re.DOTALL)
	#for move_1 in re.finditer("\s{1}(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?\s?(-|x|X)\s?(\n)?(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?(\d)?(\s)?(double)?(\n)?(ch)?(mate)?",content,re.DOTALL):
		#print(move_1)
	#if not (move_1 is None):
	#	print(move_1.group())

	# textual move description with move location e.g. Bishop capture on K5
	move_2 = re.search("(\w+)\s{1}(from|to|at|on|with)(\s|\n)?(R|Kt|B|Q|K|P)?-?(R|Kt|B|Q|K|P)\d", content, re.DOTALL)
	for move_2 in re.finditer('(\w+)\s{1}(\w+)\s{1}(from|to|at|on|with)(\s|\n)?(R|Kt|B|Q|K|P)?-?(R|Kt|B|Q|K|P)\d',content,re.DOTALL):
	#for move_2 in re.finditer('(\w+)\s{1}(\w+)\s{1}(from|to|at|on)\s{1}?(R|Kt|B|Q|K|P)\s{1}?(\d)', content):
		print(move_2)
	#if not (move_2 is None):
	#	print(move_2.group())

	# a move sequence in parenthesis that is embedded into sentences e.g. (1. Kt-B4 or K3, 2. B-Kt2, 3. R-Q1)
	#move_3 = re.search("\(1.\s{1}(R|Kt|B|Q|K|P)(.*)\)", content)
	#for move_3 in re.finditer('\(1.\s{1}(R|Kt|B|Q|K|P)(.*)\)', content):
	# for move_3 in re.finditer('(\w+)\s{1}(\w+)\s{1}(from|to|at|on)\s{1}?(R|Kt|B|Q|K|P)\s{1}?(\d)', content):
		#print(move_3)
	# if not (move_3 is None):
	#	print(move_3.group())

	# move sequence description as a paragraph
	# e.g. 1. KtxB, KtxKt; 2. RxKt, QxR; 3. Kt-B7ch, K-Kt1; 4. Kt-R6 double ch, K-R1; 5 Q-Kt8ch, RxQ; 6. Kt-B7 mate.
	# a delimiter must be placed right after this paragraph
	#move_4 = re.search("1\.\s{1}(R|Kt|B|Q|K|P)(.*)We", content, re.DOTALL)
	#for move_4 in re.finditer('1\.\s{1}(R|Kt|B|Q|K|P)(.*)We',content, re.DOTALL):
	# for move_4 in re.finditer('(\w+)\s{1}(\w+)\s{1}(from|to|at|on)\s{1}?(R|Kt|B|Q|K|P)\s{1}?(\d)', content):
		#print(move_4.group(0))
	# if not (move_4 is None):
	#	print(move_4.group())

book1 = "CH4 - The Opening.txt"
path_to_books = "./data/book"
file_handler = open(os.path.join(path_to_books, book1), "r", encoding="utf8")

#with open(diagram, 'r') as file_handler:
#file_handler = open(diagram, "r", encoding="utf8")

parse_text(file_handler)


file_handler.close()

