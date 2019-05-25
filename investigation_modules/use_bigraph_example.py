from bigraph import Bigraph

b = Bigraph()
b['a'] = {('e', 2), ('c', 2), ('d', 4)}
b['b'] = {('c', 1)}
b['c'] = {('d', 1), ('c', 1)}
print(b)           # class Bigraph doesn't really need a string representation,
# function __srt__() and this print statement were implemented
# just to show how it works
print("Reactions to 'a':", b['a'])
print("Incentives for 'd':", b.get_incentives('d'))
