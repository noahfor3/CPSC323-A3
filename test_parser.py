from parser import Parser

# Test case function for assignment statement
def test_assignment():
    parser = Parser()
    parser.token = "id"  # Initial token
    tokens = ["id", "=", "id", "+", "id"]

    def custom_lexer():
        if tokens:
            parser.token = tokens.pop(0)
        else:
            parser.token = None

    parser.lexer = custom_lexer
    parser.A()
    parser.print_instr_table()

# Test case function for while statement
def test_while():
    parser = Parser()
    parser.token = "while"  # Initial token
    tokens = ["while", "(", "id", "<", "id", ")", "id", "=", "id", "+", "id"]

    def custom_lexer():
        if tokens:
            parser.token = tokens.pop(0)
        else:
            parser.token = None

    parser.lexer = custom_lexer
    parser.while_statement()
    parser.print_instr_table()

# Test case function for if statement
def test_if():
    parser = Parser()
    parser.token = "if"  # Initial token
    tokens = ["if", "(", "id", ">", "id", ")", "id", "=", "id", "*", "id", "fi"]

    def custom_lexer():
        if tokens:
            parser.token = tokens.pop(0)
        else:
            parser.token = None

    parser.lexer = custom_lexer
    parser.if_statement()
    parser.print_instr_table()

# Run test cases
if __name__ == "__main__":
    print("Test Case 1: Assignment")
    test_assignment()

    print("\nTest Case 2: While Loop")
    test_while()

    print("\nTest Case 3: If Statement")
    test_if()
