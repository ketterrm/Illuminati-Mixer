## Illuminati Mixer Tool   - 3D Print in the color you want!

A Cura plugin that adds support for the [M3D Quad Crane 3D Printer](https://store.printm3d.com/products/crane-3d-printer) with  QuadFusion Extruder.

This Plugin for Cura allows users to define 8 tools set up in Cura for printing on the M3D Crane QuadFusion 3D Printhead.

First Install [Cura](https://ultimaker.com/en/products/ultimaker-cura-software). 
In Cura Machine Settings, goto Printer tab and set the Number of Extruders to 8. 

Machine Settings with 8 different materials willnow be assigned to them so colors are visable in Cura.
   
   The colors assigned in the machine settings are only for visual representation in the Cura tool and are not really used with this plugin. So pick any materials with a color close to what you want the end color to look like.   You can see what you will print prior to slicing.

Mixtures that are defined in the plugin settings are what really affect the final mixture of the 4 filaments.

Users will pull individual .stl or other files in Cura, and then assign a color from one of 8 extractors defined.
   - Use Cura's Merge parts function to get related materials to fit together nicely in Cura.
   - Tools such as Meshmixer may be used to split single .stl files into multiple .stl files.

 To install the pluin file in windows, put this python file Illuminati.py in the plugings directory found at:
    C:\Program Files\Ultimaker Cura 3.4\plugins\PostProcessingPlugin\scripts
    Restart Cura to be able to see plugin.
    Goto Extensions -> Post Processing -> Modify Gcode .  From the select a script button, select the illuminati plug-in.

 Typically 4 filaments are CMYK with Cyan in input 1, Magenta in 2, Yellow in 3 and Key in 4.  When assigning values to each tool, the sum of the for comma separated inputs representing the propotional amount of filament for the mixture should sum to 1. 
 Current Version contains Support for 4 extruders.  (not sure if it will work for 2)

The Temperature entered in the pluging will be used for all the mixtures as there is only one extruder on the Quad Crane.

## Cura
[Cura](https://ultimaker.com/en/products/ultimaker-cura-software) is a 3rd party slicing software created and maintained by the folks over at [Ultimaker](https://ultimaker.com/). This software is provided for free and can be used to generate [.gcode](https://en.wikipedia.org/wiki/G-code) files for use with your [M3D Quad Crane 3D Printer](https://store.printm3d.com/pages/promega).

## M3D
[M3D](http://printm3d.com/) is one of the leading manufacturers of consumer 3D printers and filaments in the world. M3D is the company that produces the [M3D Quad Crane 3D Printer](https://store.printm3d.com/).

## MELT
[melt](https://github.com/gargansa/MELT) is a plugin that adds support for some of the new / advanced features of the [M3D ProMega 3D Printer](https://store.printm3d.com/pages/promega).  The Illuminati Mixer was forked from MELT built by gargansa.




## Version History
none
