#! /usr/bin/python
import sys
import Scanner as scanner
'''
Ensures correct parameter count and passes it to Scanner if it's all gucci
'''
def main():
    if(len(sys.argv) != 2):
        print("Illegal parameter count, please pass in the relative file path of your c file")
    else:
        scanner.scan(str(sys.argv[1]))

if __name__ == "__main__":
    main()
