class parameters(object):

	def __init__(self):

		#PATHS
		self.root_filepath = "/media/darg1/Data/Projects/chess/Chessbook-Parser/data"
		self.book_path = "/media/darg1/Data/Projects/chess/Chessbook-Parser/data/book/CH4 - The Opening.txt"
		self.diagram_path = "/media/darg1/Data/Projects/chess/Chessbook-Parser/data/diagrams"
		self.move_path = "/media/darg1/Data/Projects/chess/Chessbook-Parser/data/moves"

		

		# dict for FEN notation equivalent char of pieces
		self.piecesFEN = {"#R": "r", "#Kt": "n", "#B": "b", "#Q": "q", "#K": "k", "#P": "p",
	      		      	  "^R": "R", "^Kt": "N", "^B": "B", "^Q": "Q", "^K": "K", "^P": "P"}

		#flags
		self.write_diagrams = False



PARAM = parameters()
