from parameters import PARAM
import os
from diagram_extractor import *
import re



def main():
	#for parsing diagrams
	diagram_parse = False
	diagram_count = 0
	board = []
	diagram_string = ""
	book = ""


	#START PARSING
	with open(PARAM.book_path, "r", encoding="utf8") as file_handler:

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
				if PARAM.write_diagrams:
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


	

	#split the book into paragraphs
	book_paragraphs = book.split("\n\n")[3:]#first three are chapter headlines

	#regex for finding diagram referrals
	r_single_refer = r'(Diagram|diagram|diag.|Diag.)(\n)?\s{1}?(\n)?[0-9]+'
	r_multi_refer = r'(Diagrams|diagrams)(\n)?\s{1}?(\n)?[0-9]+(\n)?\s{1}?(\n)?and(\n)?\s{1}?(\n)?[0-9]+'
	re_diagram  = re.compile("(%s|%s)"%(r_single_refer,r_multi_refer))

	#regex for finding moves
	r_formal = r'\s{1}(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?\s?(-|x|X)\s?(\n)?(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?(\d)?(\s)?(double)?(\n)?(ch)?(mate)?'
	re_move = re.compile("(%s)"%(r_formal))

	for paragraph in book_paragraphs:
		parag_print = False
		found_diag = re_diagram.findall(paragraph)
		if len(found_diag)!=0:
			parag_print = True
			print("diagrams:")
			for i in range(len(found_diag)):
				print(found_diag[i][0])
		found_move = re_move.findall(paragraph)
		if len(found_move)!=0:
			parag_print = True
			print("moves:")
			for i in range(len(found_move)):
				print(found_move[i][0])
		if parag_print:
			parag_print = False
			print(paragraph)
			print("----------------------------")







if __name__ == "__main__":
	main()




