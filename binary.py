
"""
Create a New Colab Notebook to complete the following problems.

 

1) Here is Psuedo Code for a popular algorithm called Binary Search. 

BINARY_SEARCH(list,target):
   a <- 0
   b <- index of end of list
   midpoint = midpoint index between [a,b]
   while target is not found:
         if item at midpoint is target:
               return midpoint
         if target is less than item at midpoint:
             update b to be the index before midpoint
         if target is greater than item at midpoint
              update a to be the index after midpoint
          update the midpoint
          if the a and b are 1 apart and don't contain the target
                return NIL

1) Walk through this psuedo code on paper with a partner and until you get the hang of how it is working

2) Implement the Binary Search. Run a few examples in your Colab to make sure that it is working

3) There are actually 2 ways to implement the algorithm. One uses iteration (the psuedocode that I provided). The other uses recursion.  If you get the 1st version then try the recursive version.

 

REMEMBER: The point of this exercise is not to get the right code. The point is to get the write code THAT YOU THOUGHT THROUGH AND IMPLEMENTED. If you use AI you are actually being extra silly, because python has binary search implemented as part of the language. This is an exercise to sharpen your thinking and coding. Please take it as such.

"""

def binary_search(list, target):
  a = 0
  b = len(list) - 1
  while a <= b:
    midpoint = (a + b) // 2
    if list[midpoint] == target:
      return midpoint
    if target < list[midpoint]:
      b = midpoint - 1
    else:
      a = midpoint + 1
  return None

print(binary_search([1,2,3,4,5,6,7,8,9,10], 10))

def binary_search_recursive(list, target, start=0, end=None):
  if end is None:
    end = len(list) - 1
  if start > end:
    return None
  midpoint = (start + end) // 2
  if list[midpoint] == target:
    return midpoint
  if target < list[midpoint]:
    return binary_search_recursive(list, target, start, midpoint - 1)
  return binary_search_recursive(list, target, midpoint + 1, end)

print(binary_search_recursive([1,2,3,4,5,6,7,8,9,10], 10))