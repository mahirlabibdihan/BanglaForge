import ast
import re

def get_arg_names_from_call(call_str: str):
    import ast
    tree = ast.parse(call_str, mode='eval')
    if not isinstance(tree.body, ast.Call):
        raise ValueError("Not a function call")
    arg_names = []
    for arg in tree.body.args:
        if isinstance(arg, ast.Name):
            arg_names.append(arg.id)
        else:
            arg_names.append(ast.unparse(arg))
    return arg_names

def parse_assert(assert_str: str):
    """
    Parse an assert statement string like:
    "assert func(arg1, arg2) == expected"
    and return (func_name, args, expected).
    """
    # Parse into AST
    tree = ast.parse(assert_str)

    # We assume the first statement is `assert`
    assert_node = tree.body[0]
    if not isinstance(assert_node, ast.Assert):
        raise ValueError("Not an assert statement")

    # Extract comparison (func(...) == expected)
    comp = assert_node.test
    if not isinstance(comp, ast.Compare):
        raise ValueError("Not a comparison in assert")

    # Left side: function call
    call = comp.left
    if not isinstance(call, ast.Call):
        raise ValueError("Left side is not a function call")

    func_name = call.func.id  # e.g. "max_chain_length"

    # Arguments of the function
    args_code = [ast.unparse(arg) for arg in call.args]

    # Expected value (right side of ==)
    expected_code = ast.unparse(comp.comparators[0])

    return func_name, args_code, expected_code

def to_docstring(s, func):
    func_name, args_code, expected_code = parse_assert(s)
    arg_names = get_arg_names_from_call(func)
    args = []
    for arg in args_code:
        arg_name = arg_names[len(args)]
        try:
            e_arg = eval(arg)
            args.append((arg_name, arg, type(e_arg)))
        except Exception as e:
            args.append((arg_name, arg, '<unknown type>'))
    
    expected = (expected_code, type(eval(expected_code)))
    
    template = """
        Args:
            {args}
            
        Returns:
            {returns}

        Example:
            >>> {example_function_call}
            {example_return}
    """
    
    arg_str = "\n\t".join(f"{name} ({type_}): Example: {example}" + (" (Try to infer the parameter type from example. If user-defined type needed, declare one.)" if type_ == '<unknown type>' else "") for name, example, type_ in args)

    return_str = f"{expected[1]}: Example: {expected[0]}"

    example_function_call = f"{func_name}({', '.join(args_code)})"

    example_return = expected_code
    
    return template.format(
        args=arg_str,
        returns=return_str,
        example_function_call=example_function_call,
        example_return=example_return
    )
# print(parse_assert("assert first_repeated_char(\"abcabc\") == \"a\""))

# s = "assert max_chain_length([Pair(5, 24), Pair(15, 25),Pair(27, 40), Pair(50, 60)], 4) == 3"
# s = "assert max_chain_length([(5, 24), (15, 25), (27, 40), (50, 60)], 4) == 3"
# s = "assert arc_length(9,45)==3.5357142857142856"


print("Function:", func_name)
print("Args:", args_code)
print("Expected:", expected_code)





print("Args (evaluated):", args)
print("Expected (evaluated):", expected)






print()