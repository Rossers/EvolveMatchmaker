# This file is just python notes. Not needed for the EvolveMatchmaker.
import sys

# print(sys.version)

print("Start of line...", end=" ")
print("end of the same line.")

# print text and number.
print("I am", 34, "years old.")

x = str(3)    # x will be '3'
X = str(4)    # X will be '4', capitalization matters.
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0
print(type(x))
print(type(y))
print(type(z))

x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
x = y = z = "Apple"

fruits = ["apple", "banana", "cherry"]
a, b, c = fruits
print(a)
print(b)
print(c)
print(a, b, c)
print(a + b + c)

# GLOBAL VARIABLES
g = "awesome"
l = "amazing"

def myfunc():
  g = "fantastic"
  global l
  l = "wonderful"
  print("Python is " + g + " and " + l)

myfunc()

print("Python is " + g + " and " + l)

# NOTES
# Python has negative indexes, to access things from the end of a list, array, etc.
# Python's indexes typically include the first index and exclude the last index.


# STRINGS & FORMATTING
# strings are arrays, there are no chars, just 1-length arrays.
a = " Hello, World! "
# splicing
print(a[2:])
print(b[-5:-2]) # negative index starts from back of word.
a.upper()
a.lower()
a.strip()
a.replace("H", "J")
print(a.split(",")) # returns ['Hello', ' World!']
# \ is the escape character for illegal characters.

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)
# https://www.w3schools.com/python/python_strings_methods.asp


# OPERATORS
x = 12
y = 5

print(x / y)
print(x // y)
print(x % y)

# COLLECTIONS (aka ARRAYS to store multiple values)
# List: ordered/indexed, changeable, allows duplicates, any/mixed data types.
#   myList = ["apple", "orange", "pear"]
#   .insert(), .append(), .extend(<other list>), myList[1:-2], clear()
#   .remove(<item>), .pop(<index) no index removes last, del myList[0]
#   .sort(), .reverse(), .copy() or list() or myList[:]
# Tuple: ordered/indexed, UNchangeable, allow duplicates, any data type & different types.
#   myTuple = ("apple", "orange", "pear")
#   cannot add/remove items froma  tuple
#   len()
# Set: unordered(no index), unchangeable (can add/remove), no duplicatesm any/mixed data types.
#   mySet = {"apple", "banana", "cherry"}
#   .add() add one item, .update() add another set/array
#   remove(), discard() no error if not exist, .pop() remove random, .clear()
#   frozenset cannot have items added/removed
# Dictionary: ordered, changeable, no duplicates.
#   myDict = {
#       "brand": "Ford",
#       "model": "Mustang",
#       "year": 1964
#   }