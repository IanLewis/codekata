
package main

import "fmt"
import "os"
import "strconv"

var letters = []int64{2, 3, 5, 5, 15, 16, 22, 23, 26, 27, 27, 30, 32, 33, 38, 38, 39, 40, 40, 45, 46, 50, 50, 51, 55, 56, 56, 58, 60, 66, 69, 71, 72, 73, 73, 74, 74, 74, 75, 75, 80, 81, 81, 83, 87, 89, 89, 92, 99, 100}

var NOT_FOUND = -1

func bsearch_functional(s []int64, key int64) int {
    min := 0
    max := len(s) - 1

    // Check base condition
    if (max < min) {
        return NOT_FOUND
    }

    for min <= max {
        // Find the midpoint without adding min and max
        // and possibly causing an overflow error.
        midpoint := min + ((max - min) / 2)

        if (s[midpoint] == key) {
            return midpoint
        } else if (key < s[midpoint]) {
            // The value will be found in the lower half of the slice.
            max = midpoint - 1
        } else {
            // The value will be found in the upper half of the slice.
            min = midpoint + 1
        }
    }

    return NOT_FOUND
}

func bsearch_recursive(s []int64, key int64) int {
    return _bsearch_recursive(s, key, 0, len(s) - 1)
}

func _bsearch_recursive(s []int64, key int64, min int, max int) int {
    if (max < min) {
        return NOT_FOUND
    }

    // Find the midpoint without adding min and max
    // and possibly causing an overflow error.
    midpoint := min + ((max -min) / 2)
    if (s[midpoint] == key) {
        return midpoint
    } else if (key < s[midpoint]) {
        return _bsearch_recursive(s, key, min, midpoint - 1)
    } else {
        return _bsearch_recursive(s, key, midpoint + 1, max)
    }
}

func main() {
    search_key, _ := strconv.ParseInt(os.Args[1], 10, 32)

    // index := bsearch_functional(letters, search_key)
    index := bsearch_recursive(letters, search_key)
    if (index == -1) {
        fmt.Printf("%d not found.\n", search_key)
    } else {
        fmt.Printf("%d found at index %d.\n", search_key, index)
    }
}
