##SLOT STRUCTURE IN OT2
# 10(source)  11(destination)  12(trash)
# 7   	      8                9
# 4   	      5                6
# 1           2                3

left-pippette -> p300_multi_gen2
right-pipeete -> p20_single_gen2 (optional)

source      -> corning_96_wellplate_360ul_flat (or equivalent) -> rows A...H, cols 1..12 -> fill A1...H1 with empty wells and coffee! 
destination -> corning_96_wellplate_360ul_flat (or equivalent) -> rows A...H, cols 1..12 -> fill A1...H1 with empty wells! 

tip -> opentrons_96_tiprack_300ul

code is expected to:
1) transfer source[column 1] to destination[column 1]. This takes the first column of tips from the tiprack.
2) Report that tips are over! Replace the empty column 1 with new tips.
3) press 1 and enter.
4) transfer source[column 1] to destination[column 1] using the same first column of tips from the tiprack.


