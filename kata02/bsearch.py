"""
Kata02: Karate Chop

A binary chop (sometimes called the more prosaic binary search) finds the
position of value in a sorted array of values. It achieves some efficiency by
halving the number of items under consideration each time it probes the values:
in the first pass it determines whether the required value is in the top or the
bottom half of the list of values. In the second pass in considers only this
half, again dividing it in to two. It stops when it finds the value it is
looking for, or when it runs out of array to search. Binary searches are a
favorite of CS lecturers.

This Kata is straightforward. Implement a binary search routine (using the
specification below) in the language and technique of your choice. Tomorrow,
implement it again, using a totally different technique. Do the same the next
day, until you have five totally unique implementations of a binary chop. (For
example, one solution might be the traditional iterative approach, one might be
recursive, one might use a functional style passing array slices around, and so
on).

Goals

This Kata has three separate goals:

As you’re coding each algorithm, keep a note of the kinds of error you
encounter. A binary search is a ripe breeding ground for "off by one" and
fencepost errors. As you progress through the week, see if the frequency of
these errors decreases (that is, do you learn from experience in one technique
when it comes to coding with a different technique?).

What can you say about the relative merits of the various techniques you’ve
chosen? Which is the most likely to make it in to production code? Which was
the most fun to write? Which was the hardest to get working? And for all these
questions, ask yourself “why?”.

It’s fairly hard to come up with five unique approaches to a binary chop. How
did you go about coming up with approaches four and five? What techniques did
you use to fire those “off the wall” neurons?

Specification

Write a binary chop method that takes an integer search target and a sorted
array of integers. It should return the integer index of the target in the
array, or -1 if the target is not in the array. The signature will logically
be:

    chop(int, array_of_int)  -> int

You can assume that the array has less than 100,000 elements. For the purposes
of this Kata, time and memory performance are not issues (assuming the chop
terminates before you get bored and kill it, and that you have enough RAM to
run it).
"""

import sys

NOT_FOUND = -1


def bsearch(s, key):
    imin = 0
    imax = len(s) - 1

    if imax < imin:
        return NOT_FOUND

    while imin < imax:
        # Find the midpoint without adding min and max
        # and degrading performance
        midpoint = imin + ((imax - imin) / 2)

        if s[midpoint] == key:
            return midpoint
        elif key < s[midpoint]:
            imax = midpoint
        else:
            imin = midpoint

    return NOT_FOUND

if __name__ == '__main__':
    print(bsearch([2, 3, 5, 5, 15, 16, 22, 23, 26, 27, 27, 30, 32, 33, 38, 38, 39,
                   40, 40, 45, 46, 50, 50, 51, 55, 56, 56, 58, 60, 66, 69, 71, 72,
                   73, 73, 74, 74, 74, 75, 75, 80, 81, 81, 83, 87, 89, 89, 92, 99, 100],
                  int(sys.argv[1])))
