# draw_rna

This script generates secondary structure diagrams for nucleic acids.

## Usage

### Input file

An input file is used to specify the sequence, secondary structure, and coloring of the desired drawing. The format is as follows

```
filename      # image will be written to filename.svg
GTGANNNNNTCAC # nucleic acid sequence
((((.....)))) # nucleic acid secondary structure in dot-bracket notation
rrrrbbbbbgggg # optional: coloring of each base (e.g. r for red, g for green, b for blue)
```

Multiple sequences can be specified in one file as in `example_input.txt`.

### Execution

The draw script can be run with

```
python draw_all.py example_input.txt
```
