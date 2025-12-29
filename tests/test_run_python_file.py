from functions.run_python_file import run_python_file

def tests():
    result = run_python_file("calculator", "main.py")
    print(result)
    print("")
    
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print("")
    
    result = run_python_file("calculator", "tests.py")
    print(result)
    print("")
    
    result = run_python_file("calculator", "../main.py")  # error
    print(result)
    print("")
    
    result = run_python_file("calculator", "nonexistent.py")  # error
    print(result)
    print("")
    
    result = run_python_file("calculator", "lorem.txt")  # error
    print(result)
    print("")


if __name__ == "__main__":
    tests()