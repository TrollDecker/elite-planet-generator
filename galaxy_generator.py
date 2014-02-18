from classes.star import Star

# Seed values from which the galaxy will be constructed.
seed = [0x5A4A, 0x0248, 0xB753]
galaxy_seed = seed

#List to hold all the galaxies, represented as lists holding its stars as objects.
galaxies = []

star_bins = []  # Holds the six binary strings used to calculate a star's data.
seed_bin = ""   # Used to hold the binary value of each seed value in order to perform a roll-left.

# Input variables used to look up a planet by its galaxy and star numbers.
galaxy_num = ""
star_num = ""

DIGRAM_STRING = "@@LEXEGEZACEBISOUSESARMAINDIREA'ERATENBERALAVETIEDORQUANTEISRION"

for galaxy in range(8):
	# Adds a new list to galaxies, into which new stars will be added.
	galaxies.append([])
	
	# List holding each set of values that will make up each star and its properties.
	star_twists = []
	
	for star in range(256):
		
		# If it's the first star, add the seed values, otherwise use the last three
		# values from the last twist.
		if star == 0:
			star_twists.append(galaxy_seed[:])
		else:
			# First two values are the last two from the previous twist.
			# Last one is the sum of the last twist's final three values modulo 65536.
			star_twists.append(star_twists[star - 1][4:6])
			star_twists[star].append(sum(star_twists[star - 1][3:6]) % 65536)
		
		# Add the last three values to the current twist by taking the previous three
		# values in the same twist modulo 65536.
		for extra_twists in range(3,6):
			star_twists[star].append(sum(star_twists[star][extra_twists - 3:extra_twists]) % 65536)
		
		# Convert the values in the current twist to binary.
		star_bins = []
		for ind, new_bin in enumerate(star_twists[star]):
			star_bins.append(bin(new_bin)[2:])
			# Append leading zeros to ensure each binary string is 16 characters long.
			star_bins[ind] = "0" * (16 - len(star_bins[ind])) + star_bins[ind]
		
		# Add a new star object to the current galaxy, using the newly-converted binary
		# strings to calculate its properties.
		galaxies[galaxy].append(Star(star_bins))
	
	# Perform an 8-bit roll-left operation on the seed values.
	# Basically, in every 8 bits of each value, the first binary digit becomes the last
	# binary digit.
	for ind, seed_val in enumerate(galaxy_seed):
		seed_bin = bin(seed_val)
		seed_bin = "0" * (16 - len(seed_bin[2:])) + seed_bin[2:]
		seed_bin = "0b" + seed_bin[1:8] + seed_bin[0] + seed_bin[9:16] + seed_bin[8]
		galaxy_seed[ind] = int(seed_bin, 2)
	
# Get rid of now-redundant variables.
del star_twists
del star_bins

while not galaxy_num == -1:
	try:
		galaxy_num = int(raw_input("Enter galaxy number: "))
	except ValueError:
		print "Not a number."
		continue
	else:
		if galaxy_num >= len(galaxies):
			print "There aren't that many galaxies."
			continue

	try:
		star_num = int(raw_input("Enter star number: "))
	except ValueError:
		print "Not a number."
		continue
	else:
		if star_num >= len(galaxies[galaxy_num]):
			print "There aren't that many stars."
			continue
	
	galaxies[galaxy_num][star_num].print_data(DIGRAM_STRING)
