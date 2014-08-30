/*
Part One: Weather Data

In weather.dat you’ll find daily weather data for Morristown, NJ for June 2002.
Download this text file, then write a program to output the day number (column
one) with the smallest temperature spread (the maximum temperature is the
second column, the minimum the third column).
 */

package main

import (
    "os"
    "bufio"
    "fmt"
    "strings"
    "strconv"
    "math"
)


func getLines(file_name string, skip_lines int) []string {
    file, err := os.Open(file_name)
    if (err != nil) {
        panic(err)
    }

    defer file.Close()

    scanner := bufio.NewScanner(file)
    for i := 1; i <= skip_lines; i++ {
        scanner.Scan()
    }

    var lines []string
    for scanner.Scan() {
        line, err := scanner.Text(), scanner.Err()
        if (err != nil) {
            // for now
            panic(err)
        }
        lines = append(lines, line)
    }

    return lines
}

func main2() {
    lines := getLines(os.Args[1], 2)

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


func main() {
    lines := getLines(os.Args[1], 1)


    // NOTE: Assuming that any difference in football scores is less
    //       than or equal to the maximum value for a int64.
    var smallest int64 = math.MaxInt64;
    var smallest_name string;
    for i := range lines {
        line := lines[i]

        // Each valid line of data has 10 fields separated by
        // whitespace.
        fields := strings.Fields(line)
        if (len(fields) == 10) {

            for_goals, for_err := strconv.ParseInt(fields[6], 10, 64)
            against_goals, against_err := strconv.ParseInt(fields[8], 10, 64)

            // The fields should be integers but if they aren't integers than
            // just ignore them.
            if (for_err == nil && against_err == nil) {
                // We need to do some casting back and forth from float64 because
                // Abs only accepts floats. Should this just be done manually?
                diff := int64(math.Abs(float64(for_goals - against_goals)))
                if (smallest > diff) {
                    smallest = diff
                    smallest_name = fields[1]
                }
            }

        }
    }

    fmt.Println(smallest_name)
}
