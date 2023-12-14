#!/bin/sh

__usage() {
    echo "Usage: $0 <input>"
    echo "  input:  'input' or 'sample'"
    exit 1
}

case "$1" in
    input)
        input=input.txt
        ;;
    sample)
        input=sample.txt
        ;;
    *)
        __usage
        ;;
esac

for i in $(seq 25); do
    [ -d "day-$i" ] || continue
    echo "========  day $i ========"

    .venv/bin/python "day-$i"/main.py < "day-$i"/"$input"
    echo "-------------------------"
    echo ""
done