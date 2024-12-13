class Parser:
    def __init__(self):
        self.token = None  # Current token
        self.instr_address = 1  # Instruction address counter
        self.instr_table = []  # Instruction table
        self.symbol_table = {
            "a": 9001, "b": 9002, "c": 9003, "x": 9004, "i": 9000, "max": 9001
        }  # Example symbol table
        self.jump_stack = []  # Stack for jump addresses

    def lexer(self):
        """Simulate a lexer by fetching the next token."""
        pass  # Replace with your lexer implementation

    def gen_instr(self, op, oprnd):
        """Generate an instruction and add it to the instruction table."""
        self.instr_table.append({"address": self.instr_address, "op": op, "oprnd": oprnd})
        self.instr_address += 1

    def get_address(self, id):
        """Retrieve the memory address for an identifier."""
        return self.symbol_table.get(id, None)

    def A(self):
        """Assignment Statement: A -> id = E { gen_instr (POPM, get_address(id)) }"""
        if self.token == "id":
            save = self.token
            self.lexer()
            if self.token == "=":
                self.lexer()
                self.E()
                self.gen_instr("POPM", self.get_address(save))
            else:
                self.error_message("= expected")
        else:
            self.error_message("id expected")

    def E(self):
        """Expression: E -> T E'"""
        self.T()
        self.E_prime()

    def E_prime(self):
        """Expression Prime: E' -> + T { gen_instr (ADD, nil) } E' | epsilon"""
        if self.token == "+":
            self.lexer()
            self.T()
            self.gen_instr("ADD", None)
            self.E_prime()

    def T(self):
        """Term: T -> F T'"""
        self.F()
        self.T_prime()

    def T_prime(self):
        """Term Prime: T' -> * F { gen_instr (MUL, nil) } T' | epsilon"""
        if self.token == "*":
            self.lexer()
            self.F()
            self.gen_instr("MUL", None)
            self.T_prime()

    def F(self):
        """Factor: F -> id { gen_instr (PUSHM, get_address(id)) }"""
        if self.token == "id":
            self.gen_instr("PUSHM", self.get_address(self.token))
            self.lexer()
        else:
            self.error_message("id expected")

    def while_statement(self):
        """While Statement: W -> while ( C ) S"""
        if self.token == "while":
            addr = self.instr_address
            self.gen_instr("LABEL", None)
            self.lexer()
            if self.token == "(":
                self.lexer()
                self.C()
                if self.token == ")":
                    self.lexer()
                    self.S()
                    self.gen_instr("JUMP", addr)
                    self.back_patch(self.instr_address)
                else:
                    self.error_message(") expected")
            else:
                self.error_message("( expected")
        else:
            self.error_message("while expected")

    def C(self):
        """Condition: C -> E R E"""
        self.E()
        if self.token in ["<", ">", "==", "!=", "<=", ">="]:
            op = self.token
            self.lexer()
            self.E()
            if op == "<":
                self.gen_instr("LES", None)
            elif op == ">":
                self.gen_instr("GRT", None)
            elif op == "==":
                self.gen_instr("EQU", None)
            elif op == "!=":
                self.gen_instr("NEQ", None)
            elif op == "<=":
                self.gen_instr("LEQ", None)
            elif op == ">=":
                self.gen_instr("GEQ", None)
            self.jump_stack.append(self.instr_address)
            self.gen_instr("JUMPZ", None)
        else:
            self.error_message("Relational operator expected")

    def back_patch(self, jump_addr):
        """Back-patch the JUMPZ instruction."""
        addr = self.jump_stack.pop()
        self.instr_table[addr - 1]["oprnd"] = jump_addr

    def if_statement(self):
        """If Statement: I -> if ( C ) S fi"""
        if self.token == "if":
            self.lexer()
            if self.token == "(":
                self.lexer()
                self.C()
                if self.token == ")":
                    self.lexer()
                    self.S()
                    self.back_patch(self.instr_address)
                    if self.token == "fi":
                        self.lexer()
                    else:
                        self.error_message("fi expected")
                else:
                    self.error_message(") expected")
            else:
                self.error_message("( expected")
        else:
            self.error_message("if expected")

    def S(self):
        """Placeholder for statement parsing."""
        pass  # Implement based on grammar rules

    def error_message(self, message):
        """Display an error message."""
        print(f"Error: {message}")

    def print_instr_table(self):
        """Print the instruction table."""
        print("Address\tOp\tOprnd")
        for instr in self.instr_table:
            print(f"{instr['address']}\t{instr['op']}\t{instr['oprnd']}")

# Example usage
parser = Parser()
parser.token = "id"  # Set initial token for testing
parser.A()  # Test assignment statement
parser.print_instr_table()
