import os
from diagram_extractor import *
#from move_operations import *
import re
import string
import numpy as np






###
###
###
###
###
def detect_paragraph_transitions(book_paragraphs):
	addition_terms = {"furthermore","moreover","in addition","also","besides","further","and","not only…but also","both X and Y","as well as"}
	addition_terms_refined = {"Diagram","furthermore","moreover","in addition","also","besides","further","as well as"}
	example_terms = {"for example","for instance","to illustrate","specifically","such as","in particular","namely","one example is","for one","not the least"}
	example_terms_refined = {"case","example","for example","for instance","to illustrate","specifically","such as","in particular","namely","one example is","for one","not the least"}
	contrast_terms = {"in contrast","however","yet","at the same time","nevertheless","though","although","conversely","while","on the one hand","on the other hand","on the contrary"}
	comparison_terms = {"similarly","likewise","similar to","by comparison","in a similar manner","in the same way","by the same token","in similar fashion"}
	emphasis_terms = {"indeed","of course","in fact","most importantly","above all","certainly","besides","further","undoubtedly","especially","truly"}
	addition_terms_refined.update(example_terms_refined)
	addition_terms_refined.update(contrast_terms)
	addition_terms_refined.update(comparison_terms)
	addition_terms_refined.update(emphasis_terms)
	bag_of_transition_paragraphs = dict()
	for paragraph in book_paragraphs:
		for term in addition_terms_refined:
			result = paragraph.find(term)
			if result != -1 and result < 120:
				paragraph_index = book_paragraphs.index(paragraph)
				if paragraph[0].isupper():
					try:
						bag_of_transition_paragraphs[paragraph_index].append(term)
					except KeyError:
						bag_of_transition_paragraphs[paragraph_index] = [term]

	return bag_of_transition_paragraphs



###
###
###
###
###
def print_bag_of_transition_paragraphs(book_paragraphs,bag_of_transition_paragraphs):
	for item in bag_of_transition_paragraphs:
		print(book_paragraphs[item] + "\n")
		print(bag_of_transition_paragraphs.get(item))
		print("\n")





###
###
###
###
###
def parse_text(path, write_diagrams=False):
	diagram_parse = False
	diagram_count = 0
	board = []
	diagram_string = ""
	book = ""

	with open(path, "r", encoding="utf8") as file_handler:
		for line in file_handler:
			#diagram start
			if line.strip()=="---------------------------------------" and not diagram_parse:
				board.append(line)
				diagram_string += line
				diagram_parse = True
				diagram_count += 1
			#diagram cont.
			elif diagram_parse and not any(x in line for x in ["Diag.","diag.","DIAG.","Diagram 19."]):
				#empty line
				if line==None or line=="" or line=="\n":
					continue
				board.append(line)
				diagram_string += line
			#diagram end
			elif diagram_parse and any(x in line for x in ["Diag.","diag.","DIAG.","Diagram 19."]):
				diagram_parse = False
				if write_diagrams:
					FEN_notation = get_FEN_notation(board)
					diagram_string += ("\nFEN:" + FEN_notation)

					filename = "Diagram" + str(diagram_count) + ".txt"
					output_file = os.path.join(PARAM.diagram_path,filename)
					with open(output_file, "w") as file2write:
						file2write.write(diagram_string)
				diagram_string = ""
			#not a diagram
			else:		
				book += line
	return book





###
###
###
###
###
def extract_special_tokens(paragraph, diagram=True, move=True, text_move=True, num_item=True, print_all=False):

	#tokens to search for
	diagrams = None
	moves = None
	text_moves = None
	num_items = None


	#regex for finding diagram referrals
	r_single_refer = r'(Diagram|diagram|diag.|Diag.)(\n)?\s{1}?(\n)?[0-9]+'
	r_multi_refer = r'(Diagrams|diagrams)(\n)?\s{1}?(\n)?[0-9]+(\n)?\s{1}?(\n)?and(\n)?\s{1}?(\n)?[0-9]+'
	re_diagram  = re.compile("(%s|%s)"%(r_single_refer,r_multi_refer))

	#regex for finding formal moves
	r_formal = r'\s{1}(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?\s?(-|x|X)\s?(\n)?(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?(\d)?(\s)?(double)?(\n)?(\s)?(ch)?(mate)?'
	re_move = re.compile("(%s)"%(r_formal))

	#regex for finding textual move descriptions
	r_move_desc = r'(\w+)\s{1}(from|to|at|on|with)(\s|\n)?(R|Kt|B|Q|K|P)?-?(R|Kt|B|Q|K|P)\d'
	re_movetextual = re.compile("(%s)"%(r_move_desc))

	#regex for finding numbered items to catch move pairs
	r_seq_start = r'(\s?[\d]+\.)(\s*)?'
	r_seq_mid = r',?(\s+)'
	r_formal_seq_special = r'((Castles|castles)( )?(QR|KR)?|\.\.\.)'
	r_formal_seq = r'(R|Kt|B|Q|K|P)(\n)?(R|Kt|B|Q|K|P)?(\n)?(-|x|X)(\n)?(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?(\d)?(\s)?(double)?(\s)?(ch)?(\s)?(mate)?'
	r_formal_seq_end = r'(\!+|\?+)'
	re_numbered_item = re.compile("(%s(%s|%s)%s?(%s(%s|%s)%s?)?)"%(r_seq_start, r_formal_seq, r_formal_seq_special, r_formal_seq_end, r_seq_mid, r_formal_seq, r_formal_seq_special, r_formal_seq_end))
	

	if diagram:
		found_diag = re_diagram.findall(paragraph)
		if len(found_diag)!=0:
			diagrams = found_diag
			if print_all:
				print("diagrams:")
				for i in range(len(found_diag)):
					print(found_diag[i][0])

	if move:
		found_move = re_move.findall(paragraph)
		if len(found_move)!=0:
			moves = found_move
			if print_all:
				print("moves:")
				for i in range(len(found_move)):
					print(found_move[i][0])

	if num_item:
		found_numbered_item = re_numbered_item.findall(paragraph)
		if len(found_numbered_item)!=0:
			num_items = found_numbered_item
			if print_all:
				print("numbered items:")
				#initial_board_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
				#play_move_sequence(found_numbered_item,initial_board_fen)
				for item in found_numbered_item:
					print(item[0].strip())
				
	if text_move:
		found_textual_move = re_movetextual.findall(paragraph)
		if len(found_textual_move)!=0:
			text_moves = found_textual_move
			if print_all:
				print("textual move descriptions:")
				for i in range(len(found_textual_move)):
					print(found_textual_move[i][0])

	if print_all:
		print("Paragraph:\n" + paragraph)
		print("----------------------------")

	return 	diagrams, moves, text_moves, num_items





###
###
###
###
###
def parse_book(book_path):

	book = parse_text(book_path)

	#split the book into paragraphs
	book_paragraphs = book.split("\n\n")[3:]#first three are chapter headlines


	contexts = []
	context =[]
	count = 0
	sequence_start = 0
	previous_sequence = 0
	for paragraph in book_paragraphs:
		count+=1
		diagrams, moves, text_moves, num_items = extract_special_tokens(paragraph)

		if num_items != None:
			sequence_start = int(re.search(r'^\d+', num_items[0][0].strip()).group())
			sequence_end = int(re.search(r'^\d+', num_items[-1][0].strip()).group())

			if sequence_start < previous_sequence:
				contexts.append(context)
				context = []
				context.append(paragraph)
			else:
				context.append(paragraph)
				
			previous_sequence = sequence_end
			#print(str(sequence_start) + " " + str(sequence_end))
		else:
			context.append(paragraph)
			#print("0")

		
	if len(context)>0:
		contexts.append(context)
	print(len(contexts))
	print(count)

	
	#bag_of_transition_paragraphs = detect_paragraph_transitions(book_paragraphs)

	#print_bag_of_transition_paragraphs(book_paragraphs, bag_of_transition_paragraphs)







