#:coding=utf-8:

"""
Kata05: Bloom Filters

There are many circumstances where we need to find out if something is a member
of a set, and many algorithms for doing it. If the set is small, you can use
bitmaps. When they get larger, hashes are a useful technique. But when the sets
get big, we start bumping in to limitations. Holding 250,000 words in memory
for a spell checker might be too big an overhead if your target environment is
a PDA or cell phone. Keeping a list of web-pages visited might be extravagant
when you get up to tens of millions of pages. Fortunately, there’s a technique
that can help.

Bloom filters are a 30-year-old statistical way of testing for membership in a
set. They greatly reduce the amount of storage you need to represent the set,
but at a price: they’ll sometimes report that something is in the set when it
isn’t (but it’ll never do the opposite; if the filter says that the set doesn’t
contain your object, you know that it doesn’t). And the nice thing is you can
control the accuracy; the more memory you’re prepared to give the algorithm,
the fewer false positives you get. I once wrote a spell checker for a PDP-11
which stored a dictionary of 80,000 words in 16kbytes, and I very rarely saw it
let though an incorrect word. (Update: I must have mis-remembered these
figures, because they are not in line with the theory. Unfortunately, I can no
longer read the 8” floppies holding the source, so I can’t get the correct
numbers. Let’s just say that I got a decent sized dictionary, along with the
spell checker, all in under 64k.)

Bloom filters are very simple. Take a big array of bits, initially all zero.
Then take the things you want to look up (in our case we’ll use a dictionary of
words). Produce ‘n’ independent hash values for each word. Each hash is a
number which is used to set the corresponding bit in the array of bits.
Sometimes there’ll be clashes, where the bit will already be set from some
other word. This doesn’t matter.

To check to see of a new word is already in the dictionary, perform the same
hashes on it that you used to load the bitmap. Then check to see if each of the
bits corresponding to these hash values is set. If any bit is not set, then you
never loaded that word in, and you can reject it.

The Bloom filter reports a false positive when a set of hashes for a word all
end up corresponding to bits that were set previously by other words. In
practice this doesn’t happen too often as long as the bitmap isn’t too heavily
loaded with one-bits (clearly if every bit is one, then it’ll give a false
positive on every lookup). There’s a discussion of the math in Bloom filters at
www.cs.wisc.edu/~cao/papers/summary-cache/node8.html.

So, this kata is fairly straightforward. Implement a Bloom filter based spell
checker. You’ll need some kind of bitmap, some hash functions, and a simple way
of reading in the dictionary and then the words to check. For the hash
function, remember that you can always use something that generates a fairly
long hash (such as MD5) and then take your smaller hash values by extracting
sequences of bits from the result. On a Unix box you can find a list of words
in /usr/dict/words (or possibly in /usr/share/dict/words). For others, I’ve put
a word list up here: http://codekata.com/data/wordlist.txt (1)

Play with using different numbers of hashes, and with different bitmap sizes.

Part two of the exercise is optional. Try generating random 5-character words
and feeding them in to your spell checker. For each word that it says it OK,
look it up in the original dictionary. See how many false positives you get.

----

1. This word list comes from SCOWL, which is Copyright 2000-2011 by Kevin Atkinson

-----

NOTE: Because the original word list text file is large I
      compressed it into a zip file.

NOTE: Arrays of bits is not even something you can create in native Python.
      C extensions are really the only way to achive it without doing some
      crazy stuff with the array and/or struct modules.
      Here I'll use the bitarray module which implements a compact bit
      array as a C extension.

$ mktmpenv
(tmp-...)
$ pip install -r requirements.txt
"""

import sys
import re
import urllib2
import string
import gzip
import bitarray
import hashlib


class BloomFilter(object):
    """
    Implements a simple bloom filter with the given size
    (m in the literature) and list of hash functions
    (h_k in the literature).

    See: http://codekata.com/kata/kata05-bloom-filters/www.cs.wisc.edu/~cao/papers/summary-cache/node8.html

    Since the PythonSDK doesn't have a compact data structure for
    lots of binary values, we use the bitarray library to store
    the bloomfilter.
    """
    def __init__(self, size, hashers):
        self.size = size
        self.data = bitarray.bitarray(self.size)
        self.hashers = hashers

    def add(self, word):
        for hasher in self.hashers:
            self.data[self._hash_to_index(hasher, word)] = True

    def __contains__(self, item):
        return all(self.data[self._hash_to_index(hasher, item)] for hasher in self.hashers)

    def _hash_to_index(self, hasher, word):
        """
        Here we take a hexidecimal hash value and return an index into the
        binary array.

        There is a discussion on how to do this uniformly here using the hex
        representation of a hash.  This works well with the hashlib module in
        Python because it gives hex values.

        http://stats.stackexchange.com/questions/26344/how-to-uniformly-project-a-hash-to-a-fixed-number-of-buckets
        """

        # First we convert the first n hex characters into an integer.
        # We then mod that integer by the size of the array to get an index into the array.
        return int(hasher(word).hexdigest(), 16) % self.size

if __name__ == '__main__':
    dictionary = BloomFilter(500000, [hashlib.md5, hashlib.sha1, hashlib.sha224, hashlib.sha256])

    print("Loading dictionary...")
    i = 0
    with gzip.open(sys.argv[1]) as wordlist:
        for word in wordlist:
            dictionary.add(word.strip().lower())
    print("Done.")

    url = sys.argv[2]
    print("Reading Webpage: %s" % url)
    webpage_text = urllib2.urlopen(url).read()

    # Remove script and style tags.
    # This is a bit hackish and I'm not actually sure how these work.
    webpage_text = re.sub(r'<(script|style).*?</\1>(?s)', '', webpage_text,
                          flags=re.IGNORECASE | re.MULTILINE)

    # Remove html tags
    webpage_text = re.sub(r'<[^>]*?>', '', webpage_text)

    # Remove entities
    webpage_text = re.sub(r'&(([A-Za-z]+)|(#[0-9]+));', '', webpage_text)

    # Strip off punctuation and remove empty strings.
    def _wordfilter(w):
        # Ignore empty strings
        if not w:
            return False

        # Ignore numbers
        try:
            float(w)
            return False
        except ValueError:
            return True

    wordlist = filter(_wordfilter, (w.strip(string.punctuation) for w in webpage_text.split()))

    print("Done.")

    print

    print("Possibly misspelled words:")
    print("-" * 25)
    for word in wordlist:
        if word.lower() not in dictionary:
            print(word)
