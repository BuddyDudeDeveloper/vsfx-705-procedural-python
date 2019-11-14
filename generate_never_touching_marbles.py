#!/usr/bin/env python

# Many thanks to Julian Fong,
#    http://graphics.pixar.com/library/indexAuthorFong.html 
# for supplying the code for this example helper app. Information about "PRMan
# for Python" can be found here,
#    https://renderman.pixar.com/resources/RenderMan_20/prmanForPython.html
# Specific information about the names of constants can be found here,
#    PATH/TO/RenderManProServer-22.X/include/ri.h
# Malcolm Kesson: March 4th 2017

# Imports all necessary modules.
import prman
import sys
import string
from random import uniform, seed;
from math import sqrt;
from os.path import join;
ri = prman.Ri()

# Calculates the distance between two points of the same y value.
#
# first_point: The first point in space for comparison.
# second_point: The second point in space for comparison.
#
# Returns the distance between the two points.
def distance_between(first_point, second_point):
	
	# Unpacks each point into variables.
	firstX, firstY, firstZ = first_point;
	secondX, secondY, secondZ = second_point;
	
	# Since the y value is always the same, only the x and z values are squared.
	xSquared = (secondX - firstX) * (secondX - firstX);
	zSquared = (secondZ - firstZ) * (secondZ - firstZ);
	
	# Returns the distance.
	return sqrt(xSquared + zSquared);

# Creates a sphere and passes along the color information.
#
# x: The location of the marble on the x-axis.
# y: The location of the marble on the y-axis.
# z: The location of the marble on the z-axis.
# user_attributes: The color information Renderman needs to accurately color the marble.
def create_marble(x, y, z, user_attributes):

	# BEGIN TRANFORM
	ri.TransformBegin();
	
	# Moves and rotates the sphere.
	ri.Translate(x, y, z);
	ri.Rotate(uniform(0, 360), uniform(0,1), uniform(0,1), uniform(0,1));
	
	# Passes the color information along to Renderman and draws a sphere.
	ri.Sphere(y, -y, y, 360);
	ri.Attribute("user", user_attributes);
	
	# END TRANSFORM
	ri.TransformEnd();

while True:
	try:
		line = raw_input().strip()
	except EOFError:
		break
	else:
	
		# To prevent the frame from generating a new sequence each frame, the seed is locked.
		seed(1);
	
		# Fetches the incoming data from the RendermanProgramNode
		detail, data = line.split(' ', 1);
		inputs = data.split()
		
		# This is all the data from the RendermanProgramNode.
		marble_radius = float(inputs[0]);
		marble_diameter = marble_radius * 2;
		outer_radius = float(inputs[1]);
		padding = float(inputs[2]);
		number_of_attempts = int(inputs[3]);
		
		# To create visual variety, color pairs are chosen based on whether the marble created is even or odd.
		green = [.347, .856, .347];
		blue = [.347, .521, .738];
		red = [.856, .445, .347];
		yellow = [.856, .840, .374];
		
		# For visual interest, the middle of the scene is left empty.
		inner_radius = outer_radius / 2;
		
		# Marbles are limited to being within the edges of the boundry factoring in their diameter.
		marble_generation_radius = outer_radius - marble_diameter;
		opposite_marble_generation_radius = -marble_generation_radius;
		
		# Open a rib stream
		ri.Begin("-")
		
		# To check if the marble can be placed, each space is stored and referenced later.
		available_space = True;
		spaces_taken = [];
		
		# The number of successful and attempts is tracked to determine whether or not a marble can be placed.
		failed_attempts = 0;
		
		# Updates as more spaces are taken.
		number_of_spaces = 0;
		
		# For color variable, this flag flips every time a marble is created.
		is_even = True;
		
		# While there is available space, create marbles.
		while available_space:
		
			# Randomly places the marble on the x and z axes within the boundry.
			x = uniform(opposite_marble_generation_radius, marble_generation_radius);
			z = uniform(opposite_marble_generation_radius, marble_generation_radius);
			
			# Calculates how far the marble is from the center of the scene.
			distance_from_center = distance_between([0, marble_radius, 0], [x, marble_radius, z]);

			# If the marble is inside the outer radius and outside the inner radius, it can be placed.
			within_radius = (distance_from_center <= marble_generation_radius) and (distance_from_center >= inner_radius);
			
			# If the marble is within the available boundries, check if it can be placed.
			if(within_radius):
	
				# Keeps track of the unoccupied spaces in the scene.
				successful_attempts = 0;
				
				# For each space taken, check if a marble can be placed there.
				for space in spaces_taken:
				
					# If the marble is far enough from another marble as well as the padding, it can be placed.
					if(distance_between([x, marble_radius, z], space) > (marble_diameter + padding)):
						successful_attempts += 1;
					else:
						failed_attempts += 1;
				
				# If the marble could be placed, decide the colors, render the sphere and add the space to the list of spaces taken.	
				if(successful_attempts == number_of_spaces):
				
					# If the marble is even, it will be blue and green. Otherwise, it will be yellow and red.
					user_attributes = {'color main_color': (blue if is_even else yellow), 'color accent_color': (green if is_even else red)};
					
					# Creates and renders the sphere.
					create_marble(x, marble_radius, z, user_attributes);
					
					# Adds the space to the list of taken spaces. 
					spaces_taken.append((x, marble_radius, z));
					
					# Updates the total number of spaces.
					number_of_spaces = len(spaces_taken);
					
					# Resets the attempts.
					successful_attempts = 0;
					failed_attempts = 0;
					
					# Flips the even check.
					is_even = not is_even;
			
			# Otherwise, mark the attempt as failed.
			else: 
				failed_attempts += 1;
			
			# There is still space remaining if the algorithm did not fail all its attempts.
			available_space = failed_attempts <= number_of_attempts;
		
		# The "/377" escape sequence tells prman we have finished.
		ri.ArchiveRecord(ri.COMMENT, "\n\377")
		sys.stdout.flush

		# Close the rib stream
		ri.End()
