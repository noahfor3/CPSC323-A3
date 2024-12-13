from lexer import Lexer
from parser import Parser


def process_file(file_path):
    print(f"Processing file: {file_path}\n")
    
    # Read the source code
    with open(file_path, 'r') as file:
        source_code = file.read()
        print(f"Test Case Content:\n{source_code}\n")
    
    # Tokenize the source code
    lexer = Lexer(source_code)
    lexer.tokenize()
        
    # Initialize the parser with the lexer
    parser = Parser(lexer)
    parser.lexer_next()  # Initialize the first token

    # Parse the source code
    while parser.token:
        if parser.token == "keyword" and parser.lexeme == "integer":
            # Handle declarations
            parser.lexer_next()  # Consume 'integer'
            while parser.token != "separator" or parser.lexeme != ";":
                if parser.token == "identifier":
                    parser.insert_symbol(parser.lexeme, "integer")
                parser.lexer_next()
            parser.lexer_next()  # Consume ';'
        elif parser.token in {"identifier", "keyword"}:
            if parser.lexeme == "while":
                parser.while_statement()
            elif parser.lexeme == "if":
                parser.if_statement()
            elif parser.lexeme in {"get", "put"}:
                parser.S()
            else:
                parser.A()  # Assume an assignment
        else:
            parser.error_message("Unexpected token")

    # Output the results
    print("\nGenerated Assembly Code (Instruction Table):")
    parser.print_instr_table()
    print("\nGenerated Symbol Table:")
    parser.print_symbol_table()


if __name__ == "__main__":
    # Test files to process
    files = ["test1.txt", "test2.txt", "test3.txt"]

    for file in files:
        process_file(file)
        print("\n" + "=" * 50 + "\n")
