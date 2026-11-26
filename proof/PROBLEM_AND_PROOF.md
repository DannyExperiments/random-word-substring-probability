# Problem and proof outline

Two independent probabilistic words specify explicit rational distributions for independent letters. What is the exact probability of a contiguous factor? [Source](https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/LIPIcs.STACS.2026.5/LIPIcs.STACS.2026.5.pdf#page=16)

## Exact reduction

Encode one payload as 110, then the payload bits separately preceded by zeros, then a final zero. Every 11 occurs at the start of a block. The pattern stores n independent fair vertex bits and three zero bits. The text has one block per edge, in which the endpoints' bits are fixed zero and the other n+1 bits are fair. Fix the pattern draw. Only blocks for uncovered edges can match, each with exactly one successful completion among D = 2^(n+1). Multiplying block-wise nonmatch counts gives (D−1)^b D^(m−b), where b is the number of uncovered edges. Sum over all pattern draws. Modulo D−1 each cover contributes one, and every other draw contributes zero. The cover count is smaller than the modulus.

## Rational probability and approximation

Choose one integer ticket per letter, using common denominators and rejecting out-of-range branches. Counting matching branches gives a #P numerator over a known denominator. For approximation, apply Karp–Luby–Madras coverage to all offsets. Choose an offset in proportion to its matching-event mass. Sample a shared symbol from paired products at each constrained position, and draw the remaining positions as usual. Accept only if this offset is the earliest match. Acceptance has probability at least the reciprocal of the number of offsets, and the accepted draw has exactly the law conditioned on at least one match. A capped binary ticket sampler gives worst-case polynomial-time estimation, with an arbitrarily small total error from truncation.

[Complete proof](../paper/manuscript.pdf)
