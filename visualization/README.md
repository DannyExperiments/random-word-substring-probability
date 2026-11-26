# Binary blocks and vertex covers

Extract the explorer ZIP and open index.html. Toggle pattern bits or choose the edges of a three-vertex graph. Drag the diagram or focus it and use the arrow keys. The explorer adds the exact number of nonmatching joint outcomes across all eight patterns and displays the residue modulo 15.

The GIF uses the three-vertex path. The 000 pattern leaves two edges uncovered, giving 15 × 15 nonmatches. Pattern 001 leaves one uncovered, and pattern 010 covers both. Summing over all eight patterns gives 1,985 nonmatches in 2,048 joint draws. The 63 matching outcomes give probability 63/2048, and 1985 mod 15 recovers five covers. Each blocked matching opportunity is determined by the pattern bits at the edge's endpoints.

Use Python 3.11 or newer and Pillow 10.1 or newer. Run python3 visualization/render.py from the repository root to rebuild the looping 704 × 835 GIF and the two-file offline ZIP.
