SLOT STRUCTURE
10[source 1]	11		12[trash]
7[source 2]	8[destination]	9
4[source 3]	5		6
1[tiprack 1]	2[tiprack 2]   	3[tiprack 3]


1) protocol_row_column.py
	a) has code for row and column pipetting for 72x192 case
	b) does row pipetting -> run before rotation -> rotate slots 10, 7, 4 -> set s = 4 (on line 65) -> run again
2) protocol_diagonal_brute.py
	a) has code for diagonal pipetting for 72x192 case
	b) bruteforce in the sense that doing one source well at a time
	c) has to be run before rotation
3) Instructions to run and simulate:
	$ pip(or pip3) install opentrons
	$ opentrons_simulate my_protocol.py
4) please also do a manual reading of the code to see if this looks right.
5) labware used can be easily changed by changing the first few lines of the code in each file.
6) informative comments, please read for better understanding!
7) TODOS:
	a) optimize code for diagonal
	b) have consultaion call with ot2 guys


