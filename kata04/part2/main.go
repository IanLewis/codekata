/*
Part Two: Soccer League Table

The file football.dat contains the results from the English Premier League for
2001/2. The columns labeled ‘F’ and ‘A’ contain the total number of goals
scored for and against each team in that season (so Arsenal scored 79 goals
against opponents, and had 36 goals scored against them). Write a program to
print the name of the team with the smallest difference in ‘for’ and ‘against’
goals.
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

    // NOTE: Assuming that any difference in football scores is less
    //       than or equal to the maximum value for a int64.
    var smallest int64 = math.MaxInt64;
    var smallest_name string;
    for scanner.Scan() {
        line, err := scanner.Text(), scanner.Err()
        if (err != nil) {
            // for now
            panic(err)
        }

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
