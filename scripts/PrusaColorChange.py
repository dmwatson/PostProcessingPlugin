# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class ColorChange(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Color Change",
            "key": "ColorChange",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "layer_number":
                {
                    "label": "Layer",
                    "description": "At what layer should color change occur. This will be before the layer starts printing. Specify multiple color changes with a comma.",
                    "unit": "",
                    "type": "str",
                    "default_value": 1
                },

                "initial_retract":
                {
                    "label": "Initial Retraction",
                    "description": "Initial filament retraction distance",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 300.0
                },
                "later_retract":
                {
                    "label": "Later Retraction Distance",
                    "description": "Later filament retraction distance for removal",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 30.0
                }
            }
        }"""

    def execute(self, data: list):

        """data is a list. Each index contains a layer"""
        layer_nums = self.getSettingValueByKey("layer_number")
        initial_retract = self.getSettingValueByKey("initial_retract")
        later_retract = self.getSettingValueByKey("later_retract")
        
        color_change = "M600"
        
        if initial_retract is not None and initial_retract > 0.:
            color_change = color_change + (" E%.2f" % initial_retract)
        
        if later_retract is not None and later_retract > 0.:
            color_change = color_change + (" L%.2f" % later_retract)
        
        color_change = color_change + " ; Generated by ColorChange plugin"
        
        layer_targets = layer_nums.split(',')
        if len(layer_targets) > 0:
            for layer_num in layer_targets:
                layer_num = int( layer_num.strip() )
                if layer_num < len(data):
                    layer = data[ layer_num - 1 ]
                    lines = layer.split("\n")
                    lines.insert(2, color_change )
                    final_line = "\n".join( lines )
                    data[ layer_num - 1 ] = final_line

        return data
