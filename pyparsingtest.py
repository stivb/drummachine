import pyparsing as pp

number = pp.Word( pp.nums,max=2 )
plusOrMinus  = pp.Word( "+-/", max=1 )
transposition= pp.Combine(plusOrMinus + number)
lpar  = pp.Literal( '{' ).suppress()
rpar = pp.Literal( '}' ).suppress()
startend = pp.Optional(pp.Combine(number + "-" + number))
whitespace = pp.ZeroOrMore(" ")
space = pp.Optional(pp.OneOrMore(" "))
pattern = pp.Combine(lpar + number + space + transposition + space + startend + rpar)
repeatCount = pp.Combine("*"+number)
patterns = pp.OneOrMore(pattern|repeatCount)
print patterns.parseString("{0 +0 1-32}*4 {0 +5 1-32}*2 {0 +0}*2 {0 +7 1-32} {0 +5 1-32} {0 +0 1-32} {0 +0 1-16} {0 +7 17-32}")








# from pyparsing import Literal,Word,ZeroOrMore,Forward,nums,oneOf,Group
#
# def Syntax():
#     op = oneOf('+ -')
#     lpar  = Literal( '{' ).suppress()
#     rpar  = Literal( '}' ).suppress()
#     num = Word(nums)
#     expr = Forward()
#     atom = num | Group(lpar + expr + rpar)
#     expr << atom + ZeroOrMore(op + atom)
#     return expr
#
# if __name__ == "__main__":
#     expr = Syntax()
#
#
#
#     def test(s):
#         results = expr.parseString(s)
#         print s,'->', results
#
#
#
#     test( "{9 + 3}" )
#     test( "{9 + 3} * {4 / 5}" )

#
#  nested.py
#  Copyright, 2007 - Paul McGuire
#
#  Simple example of using nestedExpr to define expressions using
#  paired delimiters for grouping lists and sublists
#
#
# from pyparsing import *
# import pprint
#
# data = """
# {
#      { item1 "item with } in it" }
#      {
#       {item2a item2b }
#       {item3}
#      }
#
# }
# """
#
# # use {}'s for nested lists
# nestedItems = nestedExpr("{", "}")
# print(( (nestedItems+stringEnd).parseString(data).asList() ))
#
# # use default delimiters of ()'s
# mathExpr = nestedExpr()
# print(( mathExpr.parseString( "((( ax + by)*C) *(Z | (E^F) & D))") ))
