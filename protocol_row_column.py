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
dst_plate = wells_availaible[0]

lft_pipette = pipettes_availaible[3]
rgt_pipette = pipettes_availaible[1]


tiprack_used = tips_availaible[2]

aspirate_volume = 100
##SLOT STRUCTURE IN OT2
# 10  11  12
# 7   8   9
# 4   5   6
# 1   2   3
##NOTE - 12 is not availaible

## hardcoded for 72x192
## does row pipetting, run before rotation -> rotate slots 10, 7, 4 -> set s = 4 -> run again
def run(protocol: protocol_api.ProtocolContext):

    # labware
    # Load SOURCE wellplates at slots 10, 7, 4 respectively
    src_plt_1 = protocol.load_labware(src_plate, '10')
    src_plt_2 = protocol.load_labware(src_plate, '7')
    src_plt_3 = protocol.load_labware(src_plate, '4')
    src_plts  = [src_plt_1, src_plt_2, src_plt_3]
    # Load a DEST wellplate at slot 8
    dst_plt = protocol.load_labware(dst_plate, '8')
    # Load a 3 tipracks in slot 1, 2, 3
    tiprack_1 = protocol.load_labware(tiprack_used, '1')
    tiprack_2 = protocol.load_labware(tiprack_used, '2')
    tiprack_3 = protocol.load_labware(tiprack_used, '3')

    # Load a P300 Multi GEN2 on the right mount
    left_pipette = protocol.load_instrument(
         lft_pipette, 'left', tip_racks=[tiprack_1, tiprack_2, tiprack_3])

    right_pipette = protocol.load_instrument(
         rgt_pipette, 'right', tip_racks=[tiprack_1, tiprack_2, tiprack_3])

    # commands
    s = 1
    for sp in src_plts:
        for i in range(1, 9):
            left_pipette.pick_up_tip()
            left_pipette.aspirate(aspirate_volume, sp['A' + str(i)])
            left_pipette.dispense(aspirate_volume, dst_plt['A' + str(s)])
            left_pipette.drop_tip()
        s = s + 1
