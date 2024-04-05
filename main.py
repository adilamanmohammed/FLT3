"""
Name : Adil Aman Mohammed
Course : Formal language theory
Assignment no: 3
CWID : A20395630
Description: the below code is an implementation of taking input CFG and applying 2 algorithms (unproductive removal, unreachable removal)
"""
import sys

#This function reads the CFG from a file and returns three sets: 
#the CFG itself, the set of terminal symbols, and the set of non-terminal symbols.

def function_parse_grammar(file_path):
    CFG_Grammar = {}  # The following dictionary will store the CFG
    terminals_list = set()  # The following set will store all the terminal symbols.
    non_terminals_list = set()  # The following set will store all the non-terminal symbols.

    with open(file_path, 'r') as file:
        file_content = file.read().strip()  # Read the entire file content and strip leading/trailing whitespaces

        if not file_content:
            print("Empty file")
            exit(1)  # Exit the program indicating an error

        for line in file_content.split('\n'):
            line = line.strip()
            if line:
                LHS, RHS = line.split("::=")
                LHS = LHS.strip()

                # New rule: Check for the "><" pattern in RHS
                if "><" in RHS:
                    print("Space error: Non-terminal symbols must be separated by spaces.")
                    exit(1)

                RHS_symbols = RHS.split()

                for symbol in RHS_symbols:
                    if symbol.startswith("<") and symbol.endswith(">"):
                        non_terminals_list.add(symbol)
                    elif not symbol.startswith("<") and not symbol.endswith(">"):
                        terminals_list.add(symbol)
                    else:
                        print("Symbols must be properly classified and separated by spaces")
                        exit(1)

                RHS = tuple(symbol.strip() for symbol in RHS_symbols if symbol.strip())
                non_terminals_list.add(LHS)
                for symbol in RHS:
                    if symbol.startswith("<") and symbol.endswith(">"):
                        non_terminals_list.add(symbol)
                    else:
                        terminals_list.add(symbol)

                if LHS in CFG_Grammar:
                    CFG_Grammar[LHS].add(RHS)
                else:
                    CFG_Grammar[LHS] = {RHS}

    return CFG_Grammar, terminals_list, non_terminals_list


def function_remove_unproductive(CFG_Grammar, terminals_list, non_terminals_list):
    """
   the following functionremoving thes unproductive non-terminals and productions from the CFG.
    A non-terminal is unproductive if it does not derive any string of terminal symbols.
    """
    productive_char_set = set(terminals_list)
    productive_CFG_Grammar = {}

    change = True
    while change:
        change = False
        for non_terminal in non_terminals_list:
            if non_terminal not in productive_char_set:
                for production in CFG_Grammar.get(non_terminal, set()):
                    #if all the symbols in a production are productive,adding the non-terminal to productive_char_set.
                    if all(symbol in productive_char_set for symbol in production):
                        productive_char_set.add(non_terminal)
                        change = True
                        break

    #removing the unproductive non-terminals and productions from the CFG.
    for non_terminal in non_terminals_list:
        if non_terminal in productive_char_set:
            productive_CFG_Grammar[non_terminal] = set()
            for production in CFG_Grammar.get(non_terminal, set()):
                if all(symbol in productive_char_set for symbol in production):
                    productive_CFG_Grammar[non_terminal].add(production)

    return productive_CFG_Grammar, terminals_list, productive_char_set

# The following function is used to remove un reachable
def function_remove_unreachable_character(CFG_Grammar, start_char):
    """
   the following function removing thes unreachable non-terminals and productions from the CFG.
    A non-terminal is unreachable if it cannot be derived from the start symbol.
    """
    reachable_char_set = {start_char}
    new_added_set = True
    while new_added_set:
        new_added_set = False
        for non_terminal in list(reachable_char_set):  
            if non_terminal in CFG_Grammar:
                for production in CFG_Grammar[non_terminal]:
                    for symbol in production:
                        if symbol not in reachable_char_set:
                            reachable_char_set.add(symbol)
                            new_added_set = True

    #removing the unreachable non-terminals and productions from the CFG.
    unreachable_CFG_Grammar = {k: v for k, v in CFG_Grammar.items() if k in reachable_char_set}
    for non_terminal in unreachable_CFG_Grammar:
        unreachable_CFG_Grammar[non_terminal] = {production for production in unreachable_CFG_Grammar[non_terminal] if all(symbol in reachable_char_set for symbol in production)}

    return unreachable_CFG_Grammar, reachable_char_set

if __name__ == "__main__":
    #checking if the correct number of command line arguments are provided
    if len(sys.argv) != 3:
        print("Usage error: format is: python script_name.py input_file output_file")
        sys.exit(1)


    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    
    CFG_Grammar, terminals_list, non_terminals_list = function_parse_grammar(input_file_path)
    # print("CFG :\n",CFG_Grammar,"\nterminals :\n",terminals_list, "\nnon terminals :\n",non_terminals_list,"\n",end="")
    start_char = next(iter(CFG_Grammar))

    #removing the unproductive non-terminals and productions.
    productive_CFG_Grammar, productive_terminals_list, productive_non_terminals_list = function_remove_unproductive(CFG_Grammar, terminals_list, non_terminals_list)
    # print("CFG :\n",productive_CFG_Grammar,"\nterminals :\n",productive_terminals_list, "\nnon terminals :\n",productive_non_terminals_list,"\n",end=" ")
    #removing the unreachable non-terminals and productions.
    reachable_CFG_Grammar, reachable_char_set = function_remove_unreachable_character(productive_CFG_Grammar, start_char)
    # print("CFG\n",reachable_CFG_Grammar,"\nstart symbol\n",start_char)
    # Final CFG
    final_CFG_Grammar, final_non_terminals_list, final_start_char = reachable_CFG_Grammar, reachable_char_set, start_char
    # print("Final CFG :\n",final_CFG_Grammar,"\nfinal non terminals :\n",final_non_terminals_list, "\nfinal terminals :\n",productive_terminals_list,"\n",end=" ")
    #displaying and store the final CFG.

    # with open(output_file_path, 'w') as output_file:
    #     for non_terminal in sorted(final_non_terminals_list):
    #         if non_terminal in final_CFG_Grammar:
    #             for production in sorted(final_CFG_Grammar[non_terminal], key=lambda x: ' '.join(x)):
    #                 production_str = f"{non_terminal} ::= {' '.join(production)}"
    #                 print(production_str)  #displaying to console
    #                 output_file.write(production_str + '\n')  #writting to the output file

    # with open(output_file_path, 'w') as output_file:
    #     for non_terminal in final_non_terminals_list:  # Iterating without sorting
    #         if non_terminal in final_CFG_Grammar:
    #             for production in final_CFG_Grammar[non_terminal]:  # Accessing productions directly
    #                 production_str = f"{non_terminal} ::= {' '.join(production)}"
    #                 print(production_str)  # Displaying to console
    #                 output_file.write(production_str + '\n')  # Writing to the output file

with open(output_file_path, 'w') as output_file:
    # First, write the productions for the start symbol "S"
    if final_start_char in final_CFG_Grammar:
        for production in final_CFG_Grammar[final_start_char]:
            production_str = f"{final_start_char} ::= {' '.join(production)}"
            print(production_str)  # Displaying to console
            output_file.write(production_str + '\n')  # Writing to the output file

    # Then, write the productions for the rest of the non-terminals, excluding "S"
    for non_terminal in final_non_terminals_list:
        if non_terminal != final_start_char and non_terminal in final_CFG_Grammar:
            for production in final_CFG_Grammar[non_terminal]:
                production_str = f"{non_terminal} ::= {' '.join(production)}"
                print(production_str)  # Displaying to console
                output_file.write(production_str + '\n')  # Writing to the output file
