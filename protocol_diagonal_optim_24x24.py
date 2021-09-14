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
    src_plt_3 = protocol.load_labware(src_plate, '8')
    src_plt_4 = protocol.load_labware(src_plate, '4')
    src_plt_5 = protocol.load_labware(src_plate, '5')
    src_plt_6 = protocol.load_labware(src_plate, '6')
    src_plt_7 = protocol.load_labware(src_plate, '1')
    src_plt_8 = protocol.load_labware(src_plate, '2')
    src_plt_9 = protocol.load_labware(src_plate, '3')
    src_plts  = [src_plt_1, src_plt_2, src_plt_3, src_plt_4, src_plt_5, src_plt_6, src_plt_7, src_plt_8, src_plt_9]
    # Load a DEST wellplate at slot 8
    dst_plt = protocol.load_labware(dst_plate, '11')
    # Load a 3 tipracks in slot 1, 2, 3
    # tiprack_1 = protocol.load_labware(tiprack_used, '1')
    # tiprack_2 = protocol.load_labware(tiprack_used, '2')
    tiprack_3 = protocol.load_labware(tiprack_used, '9')

    # Load a P300 Multi GEN2 on the right mount
    left_pipette = protocol.load_instrument(
         lft_pipette, 'left', tip_racks=[tiprack_3]) ##[tiprack_1, tiprack_2, tiprack_3])

    right_pipette = protocol.load_instrument(
         rgt_pipette, 'right', tip_racks=[tiprack_3]) ##[tiprack_1, tiprack_2, tiprack_3])

    
    def transfer(aspirate_volume, source_tip, source, destination):
    # if tips_remaining == 0:
    #     while True:
    #         print("Refilling TipRack Complete? (Answer 1 if yes)")
    #         a = int(input())
    #         if a==1:
    #             break
    #     left_pipette.reset_tipracks()
    #     tips_remaining = 96
        left_pipette.pick_up_tip(source_tip)
        left_pipette.aspirate(aspirate_volume, source)
        left_pipette.dispense(aspirate_volume, destination)
        left_pipette.drop_tip()


    tips_remaining = 96
    # commands
    ## DESTINATION PLATES
    ## BLUE -> A7
    ## YELLOW -> A8
    ## RED -> A9
    for t in range(0, 3):
        dst_dict = {}
        dst_dict[src_plts[t]] = (7, 8)
        dst_dict[src_plts[t+3]] = (9, 7)
        dst_dict[src_plts[t+6]] = (8, 9)
        for sp in [src_plts[t], src_plts[t+3], src_plts[t+6]]:
            for c in range(1, 9):
                src_tip = chr(ord('A') + c - 1) + str(c)
                src_well = chr(ord('A') + c - 1) + str(c)
                dst_well = chr(ord('A')) + str(dst_dict[sp][0])
                transfer(aspirate_volume, tiprack_3[src_tip], sp[src_well], dst_plt[dst_well])

                if c==1:
                    continue

                src_tip = chr(ord('A')) + str(c)
                src_well = chr(ord('A')) + str(c)
                dst_well = chr(ord('A') + 9 - c) + str(dst_dict[sp][1])
                transfer(aspirate_volume, tiprack_3[src_tip], sp[src_well], dst_plt[dst_well])
        left_pipette.reset_tipracks()

        # for r in range(1, 9):
        #     for c in range(1, 9):
        #         src_well = chr(ord('A') + r - 1) + str(c)
        #         dst_well = None
        #         if c - r >= 0:
        #             dst_well = chr(ord('A') + c - r) + str(dst_dict[sp][0])
        #         else:
        #             dst_well =  chr(ord('A') + 8 + c - r) + str(dst_dict[sp][1])
        #         right_pipette.pick_up_tip()
        #         right_pipette.aspirate(aspirate_volume, sp[src_well])
        #         right_pipette.dispense(aspirate_volume, dst_plt[dst_well])
        #         right_pipette.drop_tip()
