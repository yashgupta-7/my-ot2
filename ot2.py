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


print("Enter mat file name")
# fname = str(input())
fname = "Tapestry_Pooling_72x192.xlsx"
xls = pd.ExcelFile(fname)
df1 = pd.read_excel(xls, 'Matrix')
print(df1.columns)
print(df1.info)


## hardcoded for 72x192
def run1(protocol: protocol_api.ProtocolContext):

    # labware
    # Load SOURCE wellplates at slots 10, 7, 4 respectively
    src_plt_1 = protocol.load_labware('corning_96_wellplate_360ul_flat', '10')
    src_plt_2 = protocol.load_labware('corning_96_wellplate_360ul_flat', '7')
    src_plt_3 = protocol.load_labware('corning_96_wellplate_360ul_flat', '4')
    src_plts  = [src_plt_1, src_plt_2, src_plt_3]
    # Load a DEST wellplate at slot 8
    dst_plt = protocol.load_labware('corning_96_wellplate_360ul_flat', '8')
    # Load a tiprack for 300uL tips
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')

    # Load a P300 Multi GEN2 on the right mount
    left_pipette = protocol.load_instrument(
         'p300_multi_gen2', 'left', tip_racks=[tiprack])

    # commands
    s = 1
    for j, sp in enumerate(src_plts):
	    for i in range(1, 9):
		    left_pipette.pick_up_tip()
		    left_pipette.aspirate(100, sp['A' + str(i)])
		    left_pipette.dispense(100, dst_plt['A' + str(s)])
		    left_pipette.drop_tip()
		s = s + 1

def run2(protocol: protocol_api.ProtocolContext):

    # labware
    # Load SOURCE wellplates at slots 10, 7, 4 respectively
    src_plt_1 = protocol.load_labware('corning_96_wellplate_360ul_flat', '10')
    src_plt_2 = protocol.load_labware('corning_96_wellplate_360ul_flat', '7')
    src_plt_3 = protocol.load_labware('corning_96_wellplate_360ul_flat', '4')
    src_plts  = [src_plt_1, src_plt_2, src_plt_3]
    # Load a DEST wellplate at slot 8
    dst_plt = protocol.load_labware('corning_96_wellplate_360ul_flat', '8')
    # Load a tiprack for 300uL tips
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')

    # Load a P300 Multi GEN2 on the right mount
    left_pipette = protocol.load_instrument(
         'p300_multi_gen2', 'left', tip_racks=[tiprack])

    # commands
    s = 4
    for j, sp in enumerate(src_plts):
	    for i in range(1, 9):
		    left_pipette.pick_up_tip()
		    left_pipette.aspirate(100, sp['A' + str(i)])
		    left_pipette.dispense(100, dst_plt['A' + str(s)])
		    left_pipette.drop_tip()
		s = s + 1






def aspiration_test(protocol: protocol_api.ProtocolContext):
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    pipette = protocol.load_instrument(
        'p300_single', 'right', tip_racks=[tiprack])
    plate = protocol.load_labware('opentrons_96_tiprack_300ul', 3)
    pipette.pick_up_tip()

    # Aspirate at the default flowrate of 150 ul/s
    pipette.aspirate(50, plate['A1'])
    # Dispense at the default flowrate of 300 ul/s
    pipette.dispense(50, plate['A1'])

    # Change default aspirate speed to 50ul/s, 1/3 of the default
    pipette.flow_rate.aspirate = 50
    # this aspirate will be at 50ul/s
    pipette.aspirate(50, plate['A1'])
    # this dispense will be the default 300 ul/s
    pipette.dispense(50, plate['A1'])

    # Slow down dispense too
    pipette.flow_rate.dispense = 50
    # This is still at 50 ul/s
    pipette.aspirate(50, plate['A1'])
    # This is now at 50 ul/s as well
    pipette.dispense(50, plate['A1'])

    # Also slow down the blow out flowrate from its default
    pipette.flow_rate.blow_out = 100
    pipette.aspirate(50, plate['A1'])
    # This will be much slower
    pipette.blow_out()

    pipette.drop_tip()

def basic(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_1])

    p300.transfer(100, plate['A1'], plate['B1'])

def plate_mapping(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 3)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 4)
    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_1, tiprack_2])

    # these uL values were created randomly for this example
    water_volumes = [
        1,  2,  3,  4,  5,  6,  7,  8,
        9,  10, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 20, 21, 22, 23, 24,
        25, 26, 27, 28, 29, 30, 31, 32,
        33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48,
        49, 50, 51, 52, 53, 54, 55, 56,
        57, 58, 59, 60, 61, 62, 63, 64,
        65, 66, 67, 68, 69, 70, 71, 72,
        73, 74, 75, 76, 77, 78, 79, 80,
        81, 82, 83, 84, 85, 86, 87, 88,
        89, 90, 91, 92, 93, 94, 95, 96
      ]

    p300.distribute(water_volumes, reservoir['A12'], plate.wells())