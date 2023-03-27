from enum import Enum, auto
from timeit import default_timer as timer


class TokenType(Enum):
	NUMBER = auto()
	STRING = auto()
	IDENTIFIER = auto()
	ACCESSOR = auto()
	EQUALS = auto()
	OPEN_PAREN = auto()
	CLOSE_PAREN = auto()
	ARITHMETIC_OPERATOR = auto()
	RELATIONAL_OPERATOR = auto()
	UNARY_OPERATOR = auto()
	LET = auto()
	CONST = auto()
	LINE_BREAK = auto()


KEYWORDS = {"let": TokenType.LET, 'const': TokenType.CONST}


class Token:

	def __init__(self, value: str, type: TokenType):
		self.value = value
		self.type = type

	def __repr__(self):
		return f'{{ value: {repr(self.value)}, type: {self.type} }}'

	value: str
	type: TokenType


def tokenize(source: str) -> list[Token]:
	cursor = 0
	tokens: list[Token] = []

	print(source)

	while cursor < len(source):
		if source[cursor] == '(':
			tokens.append(Token(source[cursor], TokenType.OPEN_PAREN))
			cursor += 1
		elif source[cursor] == ')':
			tokens.append(Token(source[cursor], TokenType.CLOSE_PAREN))
			cursor += 1
		elif source[cursor] in ('+', '-', '*', '/', '%'):
			if source[cursor] == '+' and source[cursor + 1] == '+':
				tokens.append(
				    Token(source[cursor] + source[cursor + 1],
				          TokenType.UNARY_OPERATOR))
				cursor += 2
			elif source[cursor] == '-' and source[cursor + 1] == '-':
				tokens.append(
				    Token(source[cursor] + source[cursor + 1],
				          TokenType.UNARY_OPERATOR))
				cursor += 2
			else:
				tokens.append(
				    Token(source[cursor], TokenType.ARITHMETIC_OPERATOR))
				cursor += 1
		elif source[cursor] == '=':
			if source[cursor + 2] == '=':
				tokens.append(
				    Token(
				        source[cursor] + source[cursor + 1] +
				        source[cursor + 2], TokenType.RELATIONAL_OPERATOR))
				cursor += 3
			elif source[cursor + 1] == '=':
				tokens.append(
				    Token(source[cursor] + source[cursor + 1],
				          TokenType.RELATIONAL_OPERATOR))
				cursor += 2
			else:
				tokens.append(Token(source[cursor], TokenType.EQUALS))
				cursor += 1
		elif source[cursor] == '!':
			# TODO: this is tricky so we'll just leave it like this for now
			# because ! can be used to invert statements e.g. !(a > b)
			if source[cursor + 2] == '=':
				tokens.append(
				    Token(
				        source[cursor] + source[cursor + 1] +
				        source[cursor + 2], TokenType.RELATIONAL_OPERATOR))
				cursor += 3
			elif source[cursor + 1] == '=':
				tokens.append(
				    Token(source[cursor] + source[cursor + 1],
				          TokenType.RELATIONAL_OPERATOR))
				cursor += 2
			else:
				tokens.append(
				    Token(source[cursor], TokenType.RELATIONAL_OPERATOR))
				cursor += 1
		elif source[cursor] == '>':
			if source[cursor + 1] == '=':
				tokens.append(
				    Token(source[cursor] + source[cursor + 1],
				          TokenType.RELATIONAL_OPERATOR))
				cursor += 2
			else:
				tokens.append(
				    Token(source[cursor], TokenType.RELATIONAL_OPERATOR))
				cursor += 1
		elif source[cursor] == '<':
			if source[cursor + 1] == '=':
				tokens.append(
				    Token(source[cursor] + source[cursor + 1],
				          TokenType.RELATIONAL_OPERATOR))
				cursor += 2
			else:
				tokens.append(
				    Token(source[cursor], TokenType.RELATIONAL_OPERATOR))
				cursor += 1
		elif source[cursor].isnumeric():
			num = ""
			while cursor < len(source) and source[cursor].isnumeric():
				num += source[cursor]
				cursor += 1
			tokens.append(Token(num, TokenType.NUMBER))
		elif source[cursor] == '.':
			tokens.append(Token(source[cursor], TokenType.ACCESSOR))
			cursor += 1
		elif source[cursor] == '"':
			cursor += 1
			literal = ""
			while cursor < len(source) and source[cursor] != '"':
				literal += source[cursor]
				cursor += 1
			tokens.append(Token(literal, TokenType.STRING))
			cursor += 1
		elif source[cursor].isalpha():
			ident = ""
			while cursor < len(source) and source[cursor].isalpha():
				ident += source[cursor]
				cursor += 1
			reserved = KEYWORDS.get(ident)
			if reserved == None:
				tokens.append(Token(ident, TokenType.IDENTIFIER))
			else:
				tokens.append(Token(ident, reserved))
		elif source[cursor] in (";", '\n'):
			tokens.append(Token(source[cursor], TokenType.LINE_BREAK))
			cursor += 1
		elif source[cursor].isspace():  # skip over spaces
			cursor += 1
		else:
			print(f"unmatched char: {source[cursor]}")
			cursor += 1

	for token in tokens:
		print(token)

	return tokens


def main():
	# 	tokenize("""
	# 5++ ++ ++ ++ ++ +
	# if (5 < 5) return
	# if (5 === 5) return
	# console.log("Hello, World!")
	# let a = 1;
	# """)
	tokenize("""
a==b
a===b
a!=b
a!==b
""")


if __name__ == '__main__':
	start = timer()
	main()
	end = timer()
	print(f"Execution completed in {end - start}s")
