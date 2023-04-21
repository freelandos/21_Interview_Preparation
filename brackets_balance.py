import re


class Stack:

    def __init__(self):
        self.stack = []

    def is_empty(self):
        return not bool(self.stack)

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)


def check_brackets_balance(string):
    if not string:
        return 'Сбалансированно'
    brackets_string = re.sub(r'[^[\](){}]', '', string)
    if not brackets_string:
        return 'Сбалансированно'
    if len(brackets_string) % 2 == 0:
        stack = Stack()
        brackets_pairs = {
            ']': '[',
            ')': '(',
            '}': '{'
        }
        for bracket in brackets_string:
            if bracket in brackets_pairs:
                if stack.is_empty():
                    return 'Несбалансированно'
                elif stack.peek() != brackets_pairs[bracket]:
                    return 'Несбалансированно'
                stack.pop()
            else:
                stack.push(bracket)
        return 'Сбалансированно'
    return 'Несбалансированно'


if __name__ == '__main__':
    s = input('Введите строку со скобками: ')
    print(check_brackets_balance(s))
