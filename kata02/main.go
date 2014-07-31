
package main

import "fmt"
import "os"
import "strconv"

var letters = []int64{2, 3, 5, 5, 15, 16, 22, 23, 26, 27, 27, 30, 32, 33, 38, 38, 39, 40, 40, 45, 46, 50, 50, 51, 55, 56, 56, 58, 60, 66, 69, 71, 72, 73, 73, 74, 74, 74, 75, 75, 80, 81, 81, 83, 87, 89, 89, 92, 99, 100}

var NOT_FOUND = -1

func bsearch(s []int64, key int64) int {
    min := 0
    max := len(s) - 1

    // Check base condition
    if (max < min) {
        return NOT_FOUND;
    }

    for min <= max {
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

    return NOT_FOUND;
}


func main() {
    search_key, _ := strconv.ParseInt(os.Args[1], 10, 32)

    index := bsearch(letters, search_key)
    if (index == -1) {
        fmt.Printf("%d not found.\n", search_key)
    } else {
        fmt.Printf("%d found at index %d.\n", search_key, index)
    }
}
