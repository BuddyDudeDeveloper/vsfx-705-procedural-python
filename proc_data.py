# ORIGINAL CODE BY MALCOM KESSON FOR VSFX 705 AT SCAD
# In the "RenderManProgramShape->Scripts->Pre Shape Python Script" copy this text,
 
# Imports all necessary modules.
import maya.cmds as cmds
	
# COPY AND PASTE THE FOLLOWING: import rfm2.api.strings as apistr; from proc_data import add_values_to_data_attribute; add_values_to_data_attribute(apistr.expand_string("<shape>"))
#
# Writes the UI values to the Data input on the RendermanProgramNode
# 
# shape_name: The name of the RendermanProgramNode;
def add_values_to_data_attribute(shape_name):
	
	# Converts all the UI values to strings.
	marble_radius = str(cmds.getAttr(shape_name + '.marble_radius'));
	outer_radius = str(cmds.getAttr(shape_name + '.outer_radius'));
	padding = str(cmds.getAttr(shape_name + '.padding'));
	number_of_attempts = str(cmds.getAttr(shape_name + '.number_of_attempts'));
	
	# Concatenates all the string values together.
	text = marble_radius + " " + outer_radius + " " + padding + " " + number_of_attempts;

	# Writes the concatenated string to the Data input.
	cmds.setAttr(shape_name + '.data', text, type='string');
