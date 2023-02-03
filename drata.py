import sys, os
from dataclasses import dataclass
import binascii
from copy import copy

if len(sys.argv) < 3:
    print("Please provide more than 1 file ...")
    sys.exit(-1)


@dataclass
class candidateDC:
    fname: str
    content: bytes
    size: int
    hex_content: list[str]
    format_hex_content: list[str]
    format_content: bytes


candidates: list[candidateDC] = []

for file in range(1, len(sys.argv)):
    with open(sys.argv[file], "rb") as f:
        candidates.append(
            candidateDC(
                fname=f.name,
                content=f.read(),
                size=os.stat(f.name).st_size,
                hex_content=[],
                format_content=b"",
                format_hex_content=[],
            )
        )

for candidate in candidates:
    candidate_copy = copy(candidate.content)
    candidate.content = candidate.content.ljust(
        max([c.size for c in candidates]), b"\x00"
    )

    # candidate.format_content = candidate_copy
    # for x in range(max([c.size for c in candidates]) - candidate.size):
    #     candidate.format_content += b"\033[4m\x00\033[0m"

for candidate in candidates:
    _hex = str(binascii.hexlify(candidate.content), "ascii")
    candidate.hex_content = [_hex[i : i + 2] for i in range(0, len(_hex), 2)]

    for candidate in candidates:
        if candidate.size < len(candidate.hex_content):
            for x in range(len(candidate.hex_content) - candidate.size):
                candidate.hex_content[-x - 1] = (
                    "\033[4m" + candidate.hex_content[-x - 1] + "\033[0m"
                )


def print_candidates():
    for no, candidate in enumerate(candidates):
        print(
            f"C{no+1}\n{candidate.fname} - {candidate.size} B | {candidate.size/1024:.2f} KB \n\t {candidate.content[:10] if candidate.size <= 10 else candidate.content} ... \n\t {candidate.hex_content[:10] if candidate.size <= 10 else candidate.hex_content} ...\n"
        )


bada_naam = 0


def kon_bada_naam():
    for candidate in candidates:
        if len(candidate.fname) > bada_naam:
            bada_naam = len(candidate.fname)


def print_drata():
    for candidate in candidates:
        print(candidate.fname.ljust(bada_naam + 3, " ") + ": ", end="")
        print(" ".join(candidate.hex_content))


print("Processing ...")
print_candidates()
print()

temp_list: list[str] = []
for candidate in candidates:
    temp_list.append(candidate.hex_content)


def loop_candidates_change(candidates: list[candidateDC], index: int | None = None):
    if index is None:
        return

    for candidate in candidates:
        candidate.hex_content[index] = (
            "\033[44m" + candidate.hex_content[index] + "\033[0m"
        )


for no, zipped_hex_content in enumerate(zip(*temp_list)):
    # for com in zipped_hex_content:
    if all(c == zipped_hex_content[0] for c in zipped_hex_content):
        loop_candidates_change(candidates=candidates, index=no)

# print_candidates()
print("Drata - ")
print_drata()
