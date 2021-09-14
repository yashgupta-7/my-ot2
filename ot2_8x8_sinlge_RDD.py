import numpy as np 
import pandas as pd 
from opentrons import protocol_api


# metadata
metadata = {
    'protocolName': 'COVID-19',
    'author': 'Yash',
    'description': 'XPRIZE Tapestry',
    'apiLevel': '2.6'
}

#PIPETTES AVAILAIBLE = 
pipettes_availaible = ['p20_single_gen2', 'p300_single_gen2', 'p1000_single_gen2', 'p300_multi_gen2', 'p20_multi_gen2']

#WELLPLATES AVAILAIBLE of size 96
wells_availaible = ['corning_96_wellplate_360ul_flat', 'biorad_96_wellplate_200ul_pcr', 'nest_96_wellplate_100ul_pcr_full_skirt', 'nest_96_wellplate_200ul_flat', 'nest_96_wellplate_2ml_deep', 'usascientific_96_wellplate_2.4ml_deep']

#TIPRACKS AVALAIBLE
tips_availaible = ['opentrons_96_tiprack_10ul', 'opentrons_96_tiprack_20ul', 'opentrons_96_tiprack_300ul', 'opentrons_96_tiprack_1000ul', 'opentrons_96_filtertiprack_10ul', 'opentrons_96_filtertiprack_20ul', 'opentrons_96_filtertiprack_200ul', 'opentrons_96_filtertiprack_1000ul']

src_plate = wells_availaible[0]
dst_plate = wells_availaible[4]

lft_pipette = pipettes_availaible[3]
rgt_pipette = pipettes_availaible[0]


tiprack_used = tips_availaible[2]

aspirate_volume = 80
##SLOT STRUCTURE IN OT2
# 10  11  12
# 7   8   9
# 4   5   6
# 1   2   3
##NOTE - 12 is not availaible

def run(protocol: protocol_api.ProtocolContext):
	src_plt = protocol.load_labware(src_plate, '10')
	dst_plt = protocol.load_labware(dst_plate, '6')
	tiprack_1 = protocol.load_labware(tiprack_used, '9')
	tiprack_2 = protocol.load_labware(tiprack_used, '8')
	tiprack_3 = protocol.load_labware(tiprack_used, '7')
	tipracks = [tiprack_1]

	left_pipette = protocol.load_instrument(lft_pipette, 'left', tip_racks=tipracks)

	right_pipette = protocol.load_instrument(rgt_pipette, 'right', tip_racks=tipracks)

	dst_well = chr(ord('A')) + str(1)
	for i in range(1, 9):
		left_pipette.pick_up_tip()
		left_pipette.aspirate(aspirate_volume, src_plt['A' + str(i)])
		left_pipette.dispense(aspirate_volume, dst_plt[dst_well])
		left_pipette.drop_tip()

	####################################################################################

	for c in range(1, 9):
		src_tip = chr(ord('A') + c - 1) + str(c)
		src_well = chr(ord('A') + c - 1) + str(c)
		dst_well = chr(ord('A')) + str(2)
		left_pipette.pick_up_tip(tiprack_2[src_tip])
		left_pipette.aspirate(aspirate_volume, src_plt[src_well])
		left_pipette.dispense(aspirate_volume, dst_plt[dst_well])
		left_pipette.drop_tip()

		if c==1:
		    continue

		src_tip = chr(ord('A')) + str(c)
		src_well = chr(ord('A')) + str(c)
		dst_well = chr(ord('A') + 9 - c) + str(2)
		left_pipette.pick_up_tip(tiprack_2[src_tip])
		left_pipette.aspirate(aspirate_volume, src_plt[src_well])
		left_pipette.dispense(aspirate_volume, dst_plt[dst_well])
		left_pipette.drop_tip()

	####################################################################################

	for c in range(1, 9):
		
		src_tip = chr(ord('A') + 8 - c) + str(c)
		src_well = chr(ord('A') + 8 - c) + str(c)
		dst_well = chr(ord('A')) + str(3)
		left_pipette.pick_up_tip(tiprack_3[src_tip])
		left_pipette.aspirate(aspirate_volume, src_plt[src_well])
		left_pipette.dispense(aspirate_volume, dst_plt[dst_well])
		left_pipette.drop_tip()

		if c==8:
			continue

		src_tip = chr(ord('A')) + str(c)
		src_well = chr(ord('A')) + str(c)
		dst_well = chr(ord('A') + c) + str(3)
		left_pipette.pick_up_tip(tiprack_3[src_tip])
		left_pipette.aspirate(aspirate_volume, src_plt[src_well])
		left_pipette.dispense(aspirate_volume, dst_plt[dst_well])
		left_pipette.drop_tip()