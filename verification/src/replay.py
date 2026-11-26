"""Exact finite diagnostics for the binary marker and the weighted offset method."""

from fractions import Fraction as F
from itertools import combinations, product
from math import prod


def block(payload):
    return "110" + "".join("0" + str(bit) for bit in payload) + "0"


def text_blocks(n, edge):
    free = [i for i in range(n + 3) if i not in edge]
    for bits in product((0, 1), repeat=len(free)):
        payload = [0] * (n + 3)
        for i, bit in zip(free, bits):
            payload[i] = bit
        yield block(payload)


def check_graphs():
    graph_count = 0
    block_checks = 0
    direct_cases = 0
    for n in range(2, 5):
        edges = list(combinations(range(n), 2))
        patterns = list(product((0, 1), repeat=n))
        blocks = {edge: tuple(text_blocks(n, edge)) for edge in edges}
        d = 2 ** (n + 1)
        for edge in edges:
            assert len(set(blocks[edge])) == len(blocks[edge]) == d
            for x in patterns:
                pattern = block((*x, 0, 0, 0))
                matches = [pattern in text for text in blocks[edge]]
                assert sum(matches) == int(not any(x[i] for i in edge))
                for text in blocks[edge]:
                    assert text.find("11") == 0 and text.find("11", 1) == -1
                    assert (text + pattern).find("11", 1) == len(text)
                    block_checks += 1
        for edge_count in range(1, len(edges) + 1):
            for graph in combinations(edges, edge_count):
                avoid = 0
                cover_count = 0
                for x in patterns:
                    pattern = block((*x, 0, 0, 0))
                    avoid += prod(sum(pattern not in text for text in blocks[edge]) for edge in graph)
                    cover_count += all(any(x[i] for i in edge) for edge in graph)
                assert avoid % (d - 1) == cover_count
                graph_count += 1
                if n <= 3:
                    direct = sum(
                        block((*x, 0, 0, 0)) not in "".join(text_pair)
                        for x in patterns for text_pair in product(*(blocks[e] for e in graph))
                    )
                    assert direct == avoid
                    direct_cases += 1
                    if n == 3 and graph == ((0, 1), (1, 2)):
                        assert avoid == 1985 and cover_count == 5 and 2**n * d**edge_count - avoid == 63
    print(f"Marker and binary blocks: {block_checks} exact comparisons.")
    print(f"Residue recovery: {graph_count} nonempty labeled graphs; {direct_cases} direct full outcome counts.")
    print("Path fixture: 63/2048 matching; 1985 mod 15 = 5 vertex covers.")


def coverage(pattern, text):
    all_pairs = [tuple(zip(pattern, x)) + tuple(zip(text, y))
                 for x in product((0, 1), repeat=len(pattern))
                 for y in product((0, 1), repeat=len(text))]
    k = len(text) - len(pattern) + 1
    direct = F(0)
    labels = [F(0)] * k
    canonical = F(0)
    reciprocal = F(0)
    for pair in all_pairs:
        mass = prod(p if bit else 1 - p for p, bit in pair)
        if not mass:
            continue
        px = tuple(bit for _, bit in pair[:len(pattern)])
        tx = tuple(bit for _, bit in pair[len(pattern):])
        matching = [i for i in range(k) if px == tx[i:i+len(pattern)]]
        if matching:
            direct += mass
            for i in matching:
                labels[i] += mass
                if i == min(matching):
                    canonical += mass
                reciprocal += mass / len(matching)
    formula = [
        prod(a * b + (1-a) * (1-b) for a, b in zip(pattern, text[i:i+len(pattern)]))
        for i in range(k)
    ]
    assert labels == formula
    assert direct <= sum(labels) <= k * direct
    assert canonical == reciprocal == direct
    if direct:
        for i, weight in enumerate(labels):
            if not weight:
                continue
            for pair in all_pairs:
                mass = prod(p if bit else 1 - p for p, bit in pair)
                if not mass:
                    continue
                px = tuple(bit for _, bit in pair[:len(pattern)])
                tx = tuple(bit for _, bit in pair[len(pattern):])
                if px != tx[i:i+len(pattern)]:
                    continue
                # Multiply the exact conditional paired-symbol law and unpaired draws.
                joint = weight / sum(labels)
                for a, b, bit in zip(pattern, text[i:i+len(pattern)], px):
                    joint *= (a*b if bit else (1-a)*(1-b)) / (a*b + (1-a)*(1-b))
                for pos in range(len(text)):
                    if not i <= pos < i + len(pattern):
                        joint *= text[pos] if tx[pos] else 1 - text[pos]
                assert joint == mass / sum(labels)
    return bool(direct)


def check_coverage():
    laws = [F(0), F(1), F(1, 2)]
    positive = sum(coverage(layout[:2], layout[2:]) for layout in product(laws, repeat=6))
    assert positive == 657
    general = [F(1, 5), F(2, 3), F(3, 7)]
    count = 0
    for layout in product(general[:2], repeat=6):
        assert coverage(layout[:2], layout[2:]) or not any(layout)
        count += 1
    assert coverage(general[:2], general * 2)
    print("Coverage: 729 fixed/fair layouts (657 positive, 72 zero); 65 nonuniform layouts.")


if __name__ == "__main__":
    check_graphs()
    check_coverage()
