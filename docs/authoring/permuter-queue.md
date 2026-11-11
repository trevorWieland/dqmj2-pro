# Permuter queue

Generated from `ops/harvest_filter.py`. Every family below fails at least one of the seven
harvest conditions, i.e. its bytes are not shape-determined by the current source model;
the smallest member is the suggested first permute target.

- scanned rows: 617
- failing families: 46 (140 rows, 21422 bytes)
- passing families (not queued): 2
- singleton rows (not queued as families): 473

| # | module | family | rows | bytes | first row | reasons |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ov006 | `push sub adds ldr ldr ldr ldr ldr` | 12 | 984 | `021f4c80` (68 B) | rule1 branch on call result; rule1 post-call reload; rule3 stack=3; rule4 record chain |
| 2 | ov006 | `push ldr ldr bl ldr ldr bl ldr` | 9 | 1032 | `021fb958` (104 B) | rule4 record chain |
| 3 | ov006 | `push sub str ldr movs ldr add ldr` | 8 | 1088 | `021ffbc4` (132 B) | rule1 branch on call result; rule1 post-call reload; rule2 saved=4; rule3 stack=2; rule3 stack=3; rule4 record chain |
| 4 | ov006 | `push sub adds ldr movs ldr add ldr` | 7 | 608 | `021f25c8` (60 B) | rule1 branch on call result; rule1 post-call reload; rule3 stack=1; rule3 stack=2; rule4 record chain; rule5 branch-merged address select |
| 5 | ov006 | `ldr ldrh movs lsls ands asrs beq movs` | 7 | 500 | `02203ebc` (48 B) | rule4 record chain; rule6 mask-equality idiom |
| 6 | ov006 | `push movs bl cmp bne movs bl cmp` | 5 | 1232 | `021f5a00` (76 B) | rule1 branch on call result; rule2 saved=3; rule3 stack=1; rule4 record chain |
| 7 | ov006 | `push bl cmp beq cmp beq pop movs` | 5 | 288 | `021f6fcc` (52 B) | rule1 branch on call result; rule3 stack=1 |
| 8 | ov006 | `push sub ldr add movs ldrb adds strb` | 4 | 612 | `021fb4cc` (132 B) | rule4 record chain |
| 9 | ov006 | `push sub adds ldr ldr adds adds ldr` | 4 | 376 | `021f3e3c` (80 B) | rule1 branch on call result; rule1 post-call reload; rule3 stack=3; rule4 record chain |
| 10 | ov006 | `push adds adds cmp beq ldr adds str` | 3 | 598 | `021ecc84` (162 B) | rule1 branch on call result; rule2 saved=3; rule2 saved=4; rule3 stack=1; rule4 record chain |
| 11 | ov006 | `push ldr movs adds bl cmp beq movs` | 3 | 504 | `021f6768` (156 B) | rule1 branch on call result; rule2 saved=2; rule4 record chain |
| 12 | ov006 | `push movs adds blx cmp bne movs lsls` | 3 | 352 | `02200c0c` (96 B) | rule1 branch on call result; rule2 saved=2; rule4 record chain |
| 13 | ov006 | `push ldr ldr bl ldr movs ldrh movs` | 3 | 224 | `021fd984` (72 B) | rule4 record chain |
| 14 | ov006 | `push sub ldr ldr ldr adds ldrb str` | 3 | 144 | `021ff02c` (48 B) | rule3 stack=2; rule4 record chain |
| 15 | ov006 | `push cmp bne b movs ldrsh cmp bls` | 2 | 1476 | `021ee348` (696 B) | rule1 branch on call result; rule4 record chain; rule5 branch-merged address select |
| 16 | ov006 | `push ldr ldr ldr cmp beq b adds` | 2 | 824 | `021fa7f8` (392 B) | rule1 branch on call result; rule4 record chain |
| 17 | main | `push sub adds movs str ldr adds adds` | 2 | 800 | `020aa894` (228 B) | rule1 branch on call result; rule1 post-call reload; rule2 saved=4; rule3 stack=10; rule3 stack=3; rule4 record chain |
| 18 | ov006 | `push ldr ldr ldr cmp bne adds ldrb` | 2 | 800 | `021f8244` (388 B) | rule1 branch on call result; rule2 saved=2; rule4 record chain; rule5 branch-merged address select |
| 19 | ov006 | `push sub add movs strh strh strh strh` | 2 | 764 | `021f91f4` (148 B) | rule1 branch on call result; rule1 post-call reload; rule2 saved=4; rule3 stack=18; rule3 stack=4; rule4 record chain |
| 20 | ov006 | `push movs bl cmp beq movs bl movs` | 2 | 684 | `021f4828` (284 B) | rule1 branch on call result; rule2 saved=2; rule4 record chain |
| 21 | ov006 | `push sub ldr add ldrh strh ldrh strh` | 2 | 664 | `021f9a44` (128 B) | rule1 branch on call result; rule1 post-call reload; rule2 saved=4; rule3 stack=10; rule3 stack=4; rule4 record chain; rule5 branch-merged address select |
| 22 | ov006 | `push bl cmp bls b adds add ldrh` | 2 | 660 | `0220238c` (308 B) | rule1 branch on call result; rule2 saved=2; rule4 record chain; rule5 branch-merged address select |
| 23 | ov006 | `push sub ldr bl cmp beq ldr movs` | 2 | 608 | `021f4464` (292 B) | rule1 branch on call result; rule2 saved=4; rule4 record chain; rule5 branch-merged address select |
| 24 | ov006 | `push sub add ldr adds movs ldrb adds` | 2 | 584 | `021f65d4` (260 B) | rule1 post-call reload; rule2 saved=4; rule3 stack=1; rule4 record chain |
| 25 | ov006 | `push sub adds movs add strb strh strh` | 2 | 544 | `021ed480` (220 B) | rule1 branch on call result; rule1 post-call reload; rule2 saved=3; rule2 saved=4; rule3 stack=6; rule3 stack=7; rule4 record chain |
| 26 | ov006 | `push str adds adds adds blx adds ldr` | 2 | 472 | `021eed5c` (232 B) | rule1 branch on call result; rule1 post-call reload; rule2 saved=4; rule3 stack=1; rule4 record chain; rule5 branch-merged address select |
| 27 | ov006 | `push sub ldr add ldm stm ldm stm` | 2 | 360 | `021f9b38` (112 B) | rule1 branch on call result; rule1 post-call reload; rule4 record chain |
| 28 | ov006 | `push adds cmp blt cmp bge ldr lsls` | 2 | 284 | `021f4ac4` (140 B) | rule4 record chain; rule5 branch-merged address select |
| 29 | ov006 | `push sub adds adds adds adds adds bl` | 2 | 260 | `021ed768` (124 B) | rule1 branch on call result; rule1 post-call reload; rule2 saved=4; rule3 stack=1; rule4 record chain |
| 30 | ov006 | `push ldr ldr ldr movs strb ldr ldr` | 2 | 252 | `021feb5c` (104 B) | rule1 branch on call result; rule2 saved=3; rule4 record chain |

Full queue (every family, with member addresses) is in `permuter-queue.json`.
