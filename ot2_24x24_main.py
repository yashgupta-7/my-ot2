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

# 0 1 
# 2 3 
# 4 5 
## hardcoded for (24*24)x72
def run(protocol: protocol_api.ProtocolContext):

    # labware
    # Load SOURCE wellplates at slots 10, 7, 4, 8, 4, 5, 6
    src_plt_1 = protocol.load_labware(src_plate, '10')
    src_plt_2 = protocol.load_labware(src_plate, '11')
    src_plt_3 = protocol.load_labware(src_plate, '7')
    src_plt_4 = protocol.load_labware(src_plate, '8')
    src_plt_5 = protocol.load_labware(src_plate, '4')
    src_plt_6 = protocol.load_labware(src_plate, '5')
    src_plts  = [src_plt_1, src_plt_2, src_plt_3, src_plt_4, src_plt_5, src_plt_6]

    dst_plt = protocol.load_labware(dst_plate, '6')

    tiprack_1 = protocol.load_labware(tiprack_used, '9')
    # tiprack_2 = protocol.load_labware(tiprack_used, '11')
    # tiprack_3 = protocol.load_labware(tiprack_used, '3')
    # tiprack_4 = protocol.load_labware(tiprack_used, '10')
    tipracks = [tiprack_1] #, tiprack_2] #, tiprack_3, tiprack_4]

    left_pipette = protocol.load_instrument(
         lft_pipette, 'left', tip_racks=tipracks)

    right_pipette = protocol.load_instrument(
         rgt_pipette, 'right', tip_racks=tipracks)

    tips_remaining = 96*len(tipracks)
    def get_tiprack(tips_remaining):
        if tips_remaining%96 == 0:
            x = tips_remaining//96 - 1
        else:
            x = tips_remaining//96
        return tipracks[len(tipracks) - 1 - x]

    def get_tipcol(tips_remaining):
        x = tips_remaining
        y = 0
        while(x > 8):
            x -= 8
            y += 1
        return str(12 - y)

    def refill(tips_remaining):
        if tips_remaining == 0:
            # while True:
            print("Refilling TipRacks Complete? (Answer 1 if yes)")
                # a = int(input())
                # if a==1:
                #     break
            return True
        return False

    #COLUMN
    for s, sp in enumerate(src_plts):
        for i in range(1, 13):
            left_pipette.pick_up_tip()
            left_pipette.aspirate(aspirate_volume, sp['A' + str(i)])
            left_pipette.dispense(aspirate_volume, dst_plt['A' + str(s//2 + 1)])
            left_pipette.drop_tip()
            tips_remaining -= 8
            # print(tips_remaining)
            if refill(tips_remaining):
                left_pipette.reset_tipracks()
                tips_remaining = 96*len(tipracks)


    def transfer(aspirate_volume, source_tip, source, destination):
        left_pipette.pick_up_tip(source_tip)
        left_pipette.aspirate(aspirate_volume, source)
        left_pipette.dispense(aspirate_volume, destination)
        left_pipette.drop_tip()
 
    dst_dict = {}
    dst_dict[src_plts[0]] = [(4, 5) if c<=8 else (5, 6) for c in range(1,13)]
    dst_dict[src_plts[1]] = [(5, 6) if c<=4 else (6, 4) for c in range(1,13)]
    dst_dict[src_plts[2]] = [(6, 4) if c<=8 else (4, 5) for c in range(1,13)]
    dst_dict[src_plts[3]] = [(4, 5) if c<=4 else (5, 6) for c in range(1,13)]
    dst_dict[src_plts[4]] = [(5, 6) if c<=8 else (6, 4) for c in range(1,13)]
    dst_dict[src_plts[5]] = [(6, 4) if c<=4 else (4, 5) for c in range(1,13)]
    half_done = False
    for hd, sp in enumerate([src_plts[0], src_plts[2], src_plts[4], src_plts[1], src_plts[3], src_plts[5]]):
        for c in range(1, 13):
            k = c - 1
            if half_done:
                if c < 5:
                    c += 4
                else:
                    c -= 4
            else:
                if c > 8:
                    c -= 8
            src_tip = chr(ord('A') + c - 1) + get_tipcol(tips_remaining) #str(c)
            src_well = chr(ord('A') + c - 1) + str(k+1)
            dst_well = chr(ord('A')) + str(dst_dict[sp][k][0])
            transfer(aspirate_volume, get_tiprack(tips_remaining)[src_tip], sp[src_well], dst_plt[dst_well])

            if c!=1:
                src_tip = chr(ord('A')) + get_tipcol(tips_remaining) #str(c)
                src_well = chr(ord('A')) + str(k+1)
                dst_well = chr(ord('A') + 9 - c) + str(dst_dict[sp][k][1])
                transfer(aspirate_volume, get_tiprack(tips_remaining)[src_tip], sp[src_well], dst_plt[dst_well])

            tips_remaining -= 8
            if refill(tips_remaining):
                left_pipette.reset_tipracks()
                tips_remaining = 96*len(tipracks)
        if hd == 2:
            half_done = True


    dst_dict = {}
    dst_dict[src_plts[0]] = [(9, 7) if c<=8 else (8, 9) for c in range(1,13)]
    dst_dict[src_plts[1]] = [(8, 9) if c<=4 else (7, 8) for c in range(1,13)]
    dst_dict[src_plts[2]] = [(8, 9) if c<=8 else (7, 8) for c in range(1,13)]
    dst_dict[src_plts[3]] = [(7, 8) if c<=4 else (9, 7) for c in range(1,13)]
    dst_dict[src_plts[4]] = [(7, 8) if c<=8 else (9, 7) for c in range(1,13)]
    dst_dict[src_plts[5]] = [(9, 7) if c<=4 else (8, 9) for c in range(1,13)]
    half_done = False
    for hd, sp in enumerate([src_plts[0], src_plts[2], src_plts[4], src_plts[1], src_plts[3], src_plts[5]]):
        for c in range(1, 13):
            k = c - 1
            if half_done:
                if c < 5:
                    c += 4
                else:
                    c -= 4
            else:
                if c > 8:
                    c -= 8

            if c!=1:
                src_tip = chr(ord('A') + 9 - c) + get_tipcol(tips_remaining) #str(c)
                src_well = chr(ord('A') + 9 - c) + str(k+1)
                dst_well = chr(ord('A')) + str(dst_dict[sp][k][0])
                transfer(aspirate_volume, get_tiprack(tips_remaining)[src_tip], sp[src_well], dst_plt[dst_well])

            src_tip = chr(ord('A')) + get_tipcol(tips_remaining) #str(c)
            src_well = chr(ord('A')) + str(k+1)
            dst_well = chr(ord('A') + c - 1) + str(dst_dict[sp][k][1])
            transfer(aspirate_volume, get_tiprack(tips_remaining)[src_tip], sp[src_well], dst_plt[dst_well])

            tips_remaining -= 8
            if refill(tips_remaining):
                left_pipette.reset_tipracks()
                tips_remaining = 96*len(tipracks)
        if hd == 2:
            half_done = True