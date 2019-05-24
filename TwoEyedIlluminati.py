#      Created by ketterrm and the 2 Eyed Illuminati - FTC 10098
#
# This Plugin for Cura allows users to define 8 tools set up in Cura for printing on the
#  M3D Crane QUAD
# Machine Settings with 8 different materials are assigned to them so colors are visable in Cura.
#   In Cura Machine Settings, goto Printer tab and set Number of Extruders to 8.
#   The colors assigned in the machine settings are only for visual representation in the Cura tool and
#   are not really used with this plugin.  But you can see what you will print prior to slicing.
#
# Mixtures that are defined in the plugin are what really affect the final mixture of filament.
# Users will pull individual .stl or other files in Cura, and then assign a color from one of 8 extractors defined.
# Use Cura's Merge parts function to get related materials to fit together nicely in Cura.
# Tools such as Meshmixer may be used to split single .stl files into multiple .stl files.
#
# Typically 4 filaments are CMYK with Cyan in input 1, Magenta in 2, Yellow in 3 and Key in 4.
#
# To install in windows, put this python file in the plugings directory found at:
#    C:\Program Files\Ultimaker Cura 3.4\plugins\PostProcessingPlugin\scripts
#    Restart Cura to be able to see plugin.
#    Goto Extensions -> Post Processing -> Modify Gcode
#
# Current Version contains Support for 4 extruders.  (not sure if it will work for 2)
#

# Future Updates
# 19MAY2019 - CURA 4.0 updates
#     - Added Bed Temp Control, updated default color mixes,
#

# Credits for contributions
# gargansa - based off MELT plugin
#

from ..Script import Script
import random


# Just used to output info to text file to help debug
def print_debug(*report_data):
    setup_line = ";Debug "
    for item in report_data:
        setup_line += str(item)
    setup_line += "\n"
    return setup_line

# Function to compile extruder info into a string
def adjust_tool_mix(tool, *ext):
    i = 0
    for item in ext:
        if i == 0:
            setup_line =  "M567 P" + tool + " E" + str(item)
        else:
            setup_line += ":" + str(item)
        i += 1
    setup_line += "\n"
    return setup_line

class TwoEyedIlluminati(Script):
    version = "4.0.0"

    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Illuminati Mixer """ +  self.version + """ - 8 mixtures ",
            "key": "TwoEyedIlluminati",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "firmware_type":     
                {
                    "label": "Firmware Type",
                    "description": "Type of Firmware Supported.",
                    "type": "enum",
                    "options": {"duet":"Duet"},
                    "default_value": "duet"
                },
                "qty_extruders":
                {
                    "label": "Number of filament inputs",
                    "description": "How many filament inputs in mixing nozzle.",
                    "type": "enum",
                    "options": {"2":"Two","3":"Three","4":"Four"},
                    "default_value": "4"
                },
                
                "t0_flow":
                {
                    "label": "Tool 0 Flow",
                    "description": "Flow to initially set extruders must total up to 1.000  ::This allows the extruder to be set for any mixture of the input filaments.",
                    "unit": "0-1",
                    "type": "str",
                    "default_value": "0.4,0.4,0.1,0.1"
                },
                "t1_flow":
                {
                    "label": "Tool 1 Flow",
                    "description": "Flow to initially set extruders must total up to 1.000 ",
                    "unit": "0-1",
                    "type": "str",
                    "default_value": "0.8,0,0,0.2"
                },
                 "t2_flow":
                {
                    "label": "Tool 2 Flow",
                    "description": "Flow to initially set extruders must total up to 1.000  ",
                    "unit": "0-1",
                    "type": "str",
                    "default_value": "0.3,0.4,0,0.3"
                },   
                 "t3_flow":
                {
                    "label": "Tool 3 Flow",
                    "description": "Flow to initially set extruders must total up to 1.000 ",
                    "unit": "0-1",
                    "type": "str",
                    "default_value": "0.3,0,0.4,0.3"
                },    
                 "t4_flow":
                {
                    "label": "Tool 4 Flow",
                    "description": "Flow to initially set extruders must total up to 1.000  ",
                    "unit": "0-1",
                    "type": "str",
                    "default_value": "0,0.8,0,0.2"

                },   
                 "t5_flow":
                {
                    "label": "Tool 5 Flow",
                    "description": "Flow to initially set extruders must total up to 1.000 ",
                    "unit": "0-1",
                    "type": "str",
                    "default_value": "0,0.3,0.4,0.3"
                },   
                 "t6_flow":
                {
                    "label": "Tool 6 Flow",
                    "description": "Flow to initially set extruders must total up to 1.000 ",
                    "unit": "0-1",
                    "type": "str",
                    "default_value": "0,0,0.7,0.3"
                },   
                 "t7_flow":
                {
                    "label": "Tool 7 Flow",
                    "description": "Flow to initially set extruders must total up to 1.000  ",
                    "unit": "0-1",
                    "type": "str",
                    "default_value": "0,0,0,1"                                                                                            
                },
                 "temp":
                {
                    "label": "Nozzel Temperature",
                    "description": "Enter the temperature for all tools to operate at",
                    "unit": "°C",
                    "type": "str",
                    "default_value": "240"                                                                                            
                },
                 "bed_temp":
                {
                    "label": "Bed Temperature",
                    "description": "Enter the temperature for the print bed to operate at",
                    "unit": "°C",
                    "type": "str",
                    "default_value": "80"                                                                                            
                }
            }
        }"""





    def execute(self, data: list):
        t0_flows = [float(t0_flow) for t0_flow in self.getSettingValueByKey("t0_flow").strip().split(',')]
        t1_flows = [float(t1_flow) for t1_flow in self.getSettingValueByKey("t1_flow").strip().split(',')]
        t2_flows = [float(t2_flow) for t2_flow in self.getSettingValueByKey("t2_flow").strip().split(',')]
        t3_flows = [float(t3_flow) for t3_flow in self.getSettingValueByKey("t3_flow").strip().split(',')]
        t4_flows = [float(t4_flow) for t4_flow in self.getSettingValueByKey("t4_flow").strip().split(',')]
        t5_flows = [float(t5_flow) for t5_flow in self.getSettingValueByKey("t5_flow").strip().split(',')]
        t6_flows = [float(t6_flow) for t6_flow in self.getSettingValueByKey("t6_flow").strip().split(',')]
        t7_flows = [float(t7_flow) for t7_flow in self.getSettingValueByKey("t7_flow").strip().split(',')]
        temperature = float(self.getSettingValueByKey("temp").strip())
        bed_temperature = float(self.getSettingValueByKey("bed_temp").strip())
        current_position = 0
        end_position = 0
        index = 0
        has_been_run = 0

        # Iterate through the layers
        for active_layer in data:

            # Remove the whitespace and split the gcode into lines
            lines = active_layer.strip().split("\n")

            modified_gcode = ""


            for line in lines:
                if ";Modified:" in line:
                   has_been_run = 1

                elif ";LAYER_COUNT:" in line:
                    modified_gcode = line + "\n"  # list the initial line info
                    modified_gcode += print_debug("Tool P0:", t0_flows)
                    modified_gcode += print_debug("Tool P1:", t1_flows)
                    modified_gcode += print_debug("Tool P2:", t2_flows)
                    modified_gcode += print_debug("Tool P3:", t3_flows)
                    modified_gcode += print_debug("Tool P4:", t4_flows)
                    modified_gcode += print_debug("Tool P5:", t5_flows)
                    modified_gcode += print_debug("Tool P6:", t6_flows)
                    modified_gcode += print_debug("Tool P7:", t7_flows)
                    modified_gcode += print_debug("Temperature:", temperature)
                    modified_gcode += print_debug("Bed Temperature:", bed_temperature)
                    # Define tools
                    modified_gcode += "M563 P0 D0:1:2:3 H1" + "\n"
                    modified_gcode += "M563 P1 D0:1:2:3 H1" + "\n"
                    modified_gcode += "M563 P2 D0:1:2:3 H1" + "\n"
                    modified_gcode += "M563 P3 D0:1:2:3 H1" + "\n"
                    modified_gcode += "M563 P4 D0:1:2:3 H1" + "\n"
                    modified_gcode += "M563 P5 D0:1:2:3 H1" + "\n"
                    modified_gcode += "M563 P6 D0:1:2:3 H1" + "\n"
                    modified_gcode += "M563 P7 D0:1:2:3 H1" + "\n"
                    # start commands
                    modified_gcode += "T0" + "\n"
                    modified_gcode += "M104 S" + str(temperature) + "\n"
                    modified_gcode += "M190 S" + str(bed_temperature) + "\n"
                    modified_gcode += "M109 S" + str(temperature) + "\n"
                    modified_gcode += "M82 ;absolute extrusion mode" + "\n"
                    modified_gcode += "M98 Pprint_start.g ;this file is part of SD card" + "\n"
                    modified_gcode += "M83 ;relative extrusion mode" + "\n"
                    #modified_gcode += "M107" + "\n"

                    # Set each tool mix ratio M567
                    modified_gcode += adjust_tool_mix("0",*t0_flows)
                    modified_gcode += adjust_tool_mix("1",*t1_flows)
                    modified_gcode += adjust_tool_mix("2",*t2_flows)
                    modified_gcode += adjust_tool_mix("3",*t3_flows)
                    modified_gcode += adjust_tool_mix("4",*t4_flows)
                    modified_gcode += adjust_tool_mix("5",*t5_flows)
                    modified_gcode += adjust_tool_mix("6",*t6_flows)
                    modified_gcode += adjust_tool_mix("7",*t7_flows)
                    # Set temperature of each tool
                    modified_gcode += "G10 P0 R" + str(temperature) + " S" + str(temperature) + "\n"
                    modified_gcode += "G10 P1 R" + str(temperature) + " S" + str(temperature) + "\n"
                    modified_gcode += "G10 P2 R" + str(temperature) + " S" + str(temperature) + "\n"
                    modified_gcode += "G10 P3 R" + str(temperature) + " S" + str(temperature) + "\n"
                    modified_gcode += "G10 P4 R" + str(temperature) + " S" + str(temperature) + "\n"
                    modified_gcode += "G10 P5 R" + str(temperature) + " S" + str(temperature) + "\n"
                    modified_gcode += "G10 P6 R" + str(temperature) + " S" + str(temperature) + "\n"
                    modified_gcode += "G10 P7 R" + str(temperature) + " S" + str(temperature) + "\n"

                # Get rid of any changes for temperatures
                elif 'M104 T' in line:
                    modified_gcode += print_debug("M104 T found and removed " )

                elif 'M109 T' in line:
                    modified_gcode += print_debug("M109 T found and removed")

                elif 'M104 S0 ' in line:                  # Keep for turning off at end
                    modified_gcode += line + "\n"
                elif 'M109 S0 ' in line:
                    modified_gcode += line + "\n"

                elif 'M109 S' in line:
                    modified_gcode += print_debug("M109 S found and removed")

                elif 'M104 S' in line:
                    modified_gcode += print_debug("M104 S found and removed")

                    # LEAVE ALL OTHER LINES ALONE SINCE THEY ARE NOT NEW LAYERS
                else:
                    modified_gcode += line + "\n"
            data[index] = modified_gcode
            index += 1
        return data
    #
