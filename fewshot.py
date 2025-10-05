import ast
import re
import pandas as pd

def convert_csv_to_json(csv_file):
    df = pd.read_csv(csv_file, encoding='utf-8')
    df['test_list'] = df['test_list'].apply(lambda x: ast.literal_eval(ast.literal_eval(x)) if isinstance(x, str) else x)
    df['instruction_en'] = df['instruction_en'].str.replace(r'\s*Example:.*', '', regex=True)
    return df.to_dict(orient='records')

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
   
trial_set = convert_csv_to_json("trial_with_en_v1.csv")

EXAMPLE_TEMPLATE = '''
> Instruction
```python
def {function_call}:
    """{instruction}"""
    """Translated: {instruction_en}"""
    {docstring}
```
> Solution
```python
{solution}
```
'''

examples = []
for item in trial_set:
    function_call = item["instruction"].split("\n")[2].strip()
    instruction = item["instruction"].split("\n")[0].strip()
    instruction_en = item["instruction_en"].split("\n")[0].strip()
    function_name = ""
    match = re.match(r"(\w+)\s*\(", function_call)
    if match:
        function_name = match.group(1)

    docstring = to_docstring(item["test_list"][0], function_call)
    
    examples.append(EXAMPLE_TEMPLATE.format(
        function_call=function_call,
        instruction=instruction,
        instruction_en=instruction_en,
        docstring=docstring,
        solution=docstring
    ))
    

for example in examples:
    print(example)


# 'assert smallest_multiple(13)==360360' -> 'check(1, smallest_multiple(13), 360360)'

def assert_to_check(idx, assert_str: str) -> str:
    func_name, args_code, expected_code = parse_assert(assert_str)
    func_call = f"{func_name}({', '.join(args_code)})"
    return f"check({idx}, {func_call}, {expected_code})"