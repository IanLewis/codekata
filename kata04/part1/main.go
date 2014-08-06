package main

import (
    "os"
    "bufio"
    "fmt"
)

func main() {
    file_name := os.Args[1]
    file, err := os.Open(file_name)
    if (err != nil) {
        panic(err)
    }

    defer file.Close()

    scanner := bufio.NewScanner(file)

    // Read off two lines (header and blank line)
    scanner.Scan()
    scanner.Scan()

    var lines []string
    for scanner.Scan() {
        line, err := scanner.Text(), scanner.Err()
        if (err != nil) {
            // for now
            panic(err)
        }
        lines = append(lines, line)
    }

    // Read all lines omitting the last line
    // (of monthly averages?)
    for _, line := range lines[:len(lines)-1] {
        // All we have to do is read the first, second, and third column
        // and print them out.
        dy := line[0:4]
        mxt := line[5:10]
        mnt := line[11:16]

        fmt.Printf("%6s%6s%6s\n", dy, mxt, mnt)
    }
}
