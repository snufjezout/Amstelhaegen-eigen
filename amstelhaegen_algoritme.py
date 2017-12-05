# HEURISTIEKEN
# Project: Amstelhaegen
# Autors: Tim Jansen, Jaap Meesters, Christoffel Doorman

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import classes
import random
import pdb
import numpy as np
import locale
import timeit
import math

start = timeit.default_timer()

ITERATIONS = 10000
TOTAL_HOUSES = 20
X_DIMENSION = 360
Y_DIMENSION = 320
best_iteration = 0

def pythagoras(x1, y1, x2, y2):
	distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

	return distance

def drawBuilding(building, x, y, edgecolor):

	# add building to map
	ax1.add_patch(
	    patches.Rectangle(
	        (x, y),   			# (x,y)
	        building.width,    # length
	        building.length,     # width	# color
			linewidth = 1,
			edgecolor = edgecolor,
			facecolor = 'none'
	    )
	)

def overlap(building1, building2):
	overlap = True

	if (building1.left_bottom[0] > building2.right_bottom[0] or building2.left_bottom[0] > building1.right_bottom[0]
		or building1.left_bottom[1] > building2.left_top[1] or building2.left_bottom[1] > building1.left_top[1]):
		overlap = False

	return overlap

def h_build(buildings, h_counter):


	xrandom = random.randint(0, X_DIMENSION - classes.House.width)
	yrandom = random.randint(0, Y_DIMENSION - classes.House.length)
	house = classes.House(xrandom, yrandom)

	olap = True
	for building in buildings:
		olap = overlap(house, building)

		if olap:
			break

	if not olap:
		buildings.append(house)
		# drawBuilding(house, house.left_bottom[0], house.left_bottom[1], 'red')
		h_counter += 1

	return buildings, h_counter

def b_build(buildings, b_counter):

	xrandom = random.randint(0, X_DIMENSION - classes.Bungalow.width)
	yrandom = random.randint(0, Y_DIMENSION - classes.Bungalow.length)
	bungalow = classes.Bungalow(xrandom, yrandom)
	if random.choice((True, False)):
		if True:
			bungalow.length, bungalow.width = bungalow.width, bungalow.length
			bungalow.left_top[1] = yrandom + bungalow.length
			bungalow.right_top = [xrandom + bungalow.width, yrandom + bungalow.length]
			bungalow.right_bottom[0] = xrandom + bungalow.width

	olap = True
	for building in buildings:
		olap = overlap(bungalow, building)

		if olap:
			break

	if not olap:
		buildings.append(bungalow)
		# drawBuilding(bungalow, bungalow.left_bottom[0], bungalow.left_bottom[1], 'blue')
		b_counter += 1

	return buildings, b_counter

def m_build(buildings, m_counter):

	xrandom = random.randint(0, X_DIMENSION - classes.Maison.width)
	yrandom = random.randint(0, Y_DIMENSION - classes.Maison.length)
	maison = classes.Maison(xrandom, yrandom)
	# random: length, width = width, length
	if random.choice((True, False)):
		if True:
			maison.length, maison.width = maison.width, maison.length
			maison.left_top[1] = yrandom + maison.length
			maison.right_top = [xrandom + maison.width, yrandom + maison.length]
			maison.right_bottom[0] = xrandom + maison.width

	olap = True
	for building in buildings:
		olap = overlap(maison, building)

		if olap:
			break

	if not olap:
		buildings.append(maison)
		# drawBuilding(maison, maison.left_bottom[0], maison.left_bottom[1], 'green')
		m_counter += 1

	return buildings, m_counter

def w_build():
	choice = random.getrandbits(1)
	if choice:
		w_length = random.randint(1, 90)
		w_width = random.randint(1, 4) * w_length
		print "true"

	else:
		print "false"
		w_width = random.randint(1, 80)
		w_length = random.randint(1, 4) * w_width


	xrandom = random.randint(0, X_DIMENSION - w_width)
	yrandom = random.randint(0, Y_DIMENSION - w_length)
	print xrandom, yrandom, w_width, w_length
	water = classes.Water(xrandom, yrandom, w_length, w_width)

	return water


def closest_distance(current_building, buildings):

	closest = 50000

	for building in buildings:

        # area linksboven
		if (building.right_bottom[0] < current_building.left_top[0]
		 	and building.right_bottom[1] > current_building.left_top[1]):

            # calculate distance
			distance = pythagoras(current_building.left_top[0], current_building.left_top[1],
			building.right_bottom[0], building.right_bottom[1])

			# update closest distance if closer
			if distance < closest:
				closest = distance

        # area midden boven
		if (building.right_bottom[1] > current_building.left_top[1]
			and building.right_bottom[0] > current_building.left_top[0]
			and building.left_bottom[0] < current_building.right_top[0]):

			# calculate distance
			distance = building.right_bottom[1] - current_building.right_top[1]

            # update closest distance if closer
			if distance < closest:
				closest = distance

        # area rechtsboven
		if (building.left_bottom[0] > current_building.right_top[0]
		 	and building.right_bottom[1] > current_building.left_top[1]):

			# calculate distance
			distance = pythagoras(current_building.right_top[0], current_building.right_top[1],
			building.left_bottom[0], building.left_bottom[1])

			# update closest distance if closer
			if distance < closest:
				closest = distance

        # area midden rechts
		if (building.left_bottom[0] > current_building.right_top[0]
			and building.left_bottom[1] < current_building.right_top[1]
			and building.left_top[1] > current_building.right_bottom[1]):

			# calculate distance
			distance = building.left_bottom[0] - current_building.right_bottom[0]

			# update closest distance if closer
			if distance < closest:
				closest = distance

        # area rechtsonder
		if (building.left_top[0] > current_building.right_bottom[0]
		 	and building.right_top[1] < current_building.right_bottom[1]):

			# calculate distance
			distance = pythagoras(current_building.right_bottom[0], current_building.right_bottom[1],
			building.left_top[0], building.left_top[1])

			# update closest distance if closer
			if distance < closest:
				closest = distance

		# area midden onder
		if (building.right_top[1] < current_building.left_bottom[1]
			and building.right_top[0] > current_building.left_bottom[0]
			and building.left_top[0] < current_building.right_bottom[0]):

			# calculate distance
			distance = current_building.right_top[1] - building.right_bottom[1]

			# update closest distance if closer
			if distance < closest:
				closest = distance

        # area linksonder
		if (building.right_top[0] < current_building.left_bottom[0]
		 	and building.right_top[1] < current_building.left_bottom[1]):

			# calculate distance
			distance = pythagoras(current_building.left_bottom[0], current_building.left_bottom[1],
			building.right_top[0], building.right_top[1])

			# update closest distance if closer
			if distance < closest:
				closest = distance

        # area midden rechts
		if (building.right_bottom[0] < current_building.left_bottom[0]
			and building.right_bottom[1] < current_building.left_top[1]
			and building.right_top[1] > current_building.left_bottom[1]):

			# calculate distance
			distance = current_building.left_bottom[0] - building.right_bottom[0]

			# update closest distance if closer
			if distance < closest:
				closest = distance

	return closest

if __name__ == "__main__":

	water = w_build()
	print water

	for i in range(ITERATIONS):

		# fill building array with a house at a random point
		buildings = []

		# append first house to array 'buildings'
		buildings.append(classes.House(X_DIMENSION, Y_DIMENSION))

		# set number of each building type
		h_number = 0.6 * TOTAL_HOUSES
		b_number = 0.25 * TOTAL_HOUSES
		m_number = 0.15 * TOTAL_HOUSES

	    # create counters to count number of each building
		h_counter, b_counter, m_counter = 0, 0, 0

		# build houses until maximum is reached
		while (len(buildings) - 1) < TOTAL_HOUSES:

	        # choose random building type
			building_type = random.choice(['house', 'bungalow', 'maison'])

			if building_type == 'house' and h_counter < h_number:
				buildings, h_counter = h_build(buildings, h_counter)

			if building_type == 'bungalow' and b_counter < b_number:
				buildings, b_counter = b_build(buildings, b_counter)

			if building_type == 'maison' and m_counter < m_number:
				buildings, m_counter = m_build(buildings, m_counter)

	    # delete first house from array
		buildings.pop(0)

	    # calculate closest distance to buildings
		counter = 0
		total_value = 0
		for current_building in buildings:
			counter += 1
			closest = closest_distance(current_building, buildings)
			total_value += current_building.score(closest)



		if total_value > best_iteration:
			best_iteration = total_value

			fig1 = plt.figure()
			ax1 = fig1.add_subplot(111, aspect='equal')
			ax1.set_xlim(0, 360)
			ax1.set_ylim(0, 320)

			for building in buildings:
				if building.name == 'house':
					drawBuilding(building, building.left_bottom[0], building.left_bottom[1], 'red')
				if building.name == 'bungalow':
					drawBuilding(building, building.left_bottom[0], building.left_bottom[1], 'blue')
				if building.name == 'maison':
					drawBuilding(building, building.left_bottom[0], building.left_bottom[1], 'green')

			# safe figure
			fig1.savefig('20_best_10D.png', dpi=90, bbox_inches='tight')

		print total_value
		print best_iteration

	stop = timeit.default_timer()
	print "De tijd is: ", stop - start
	print "De hoogste score is: ", best_iteration
