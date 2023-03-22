class EndOfFileError(Exception):

	def __init__(self, *args: str):
		super().__init__(*args)
		if args:
			self.message = args[0]
		else:
			self.message = None


class Cursor:

	def __init__(self, file: list[str], line: int = 0, char_pos: int = 0):
		self.line = line
		self.char_pos = char_pos
		self.file = file
		self.char = None

	def next(self):
		self.char_pos += 1
		if self.char_pos >= len(self.file[self.line]):
			self.char_pos = 0
			self.line += 1
		if self.line >= len(self.file):
			raise EndOfFileError
		self.char = self.file[self.line][self.char_pos]
