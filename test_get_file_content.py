from functions.get_file_content import get_file_content

def tests():
    result = get_file_content("calculator", "lorem.txt")
    print("Result for /calculator/lorem.txt file: ")
    print(result)
    print("")

    result = get_file_content("calculator", "main.py")
    print("Result for /calculator/main.py file: ")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for pkg/calculator.py file: ")
    print(result)
    print("")

    result = get_file_content("calculator", "/bin/cat")
    print("Result for /bin/cat file: ")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/foes_not_exist.py")
    print("Result for pkg/foes_not_exist.py file: ")
    print(result)
    print("")


if __name__ == "__main__":
    tests()