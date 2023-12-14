#!/bin/sh

__fail() {
    echo "$1"
    exit 1
}

__usage() {
    echo "Usage: $0 <day> <input>"
    echo "  day:    Day to run"
    echo "  input:  stdin or sample"
    exit 1
}

day="$1"

[ -n "$day" ] || __usage

case "$2" in
    stdin)
        input=/dev/stdin
        ;;
    input)
        input=day-"$day"/input.txt
        ;;
    sample)
        input=day-"$day"/sample.txt
        ;;
    *)
        __usage
        ;;
esac

[ -f "$input" ] || __fail "Input file not found: $input"

echo "Running day $day with input $input"

.venv/bin/python "day-$day"/main.py < "$input"