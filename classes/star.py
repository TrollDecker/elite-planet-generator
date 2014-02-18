from math import floor
from os import system, name

class Star(object):
	def __init__(self, star_bins):
	
		self.x = self.set_basic(star_bins[1][:8])                           # X coordinate on the map.
		self.y = self.set_basic(star_bins[0][:8])                           # Y coordinate on the map.
		self.radius_x = self.set_radius(star_bins[2][4:8])                  # Radius of the planet in km (not really used beyond flavour text?).
		
		self.gov = self.set_basic(star_bins[1][10:13])                      # Government type.
		self.eco = int(self.set_eco(star_bins[0][5:8]))                     # Economy type.
		
		# The positions on the digram string, from which 3 or 4 digrams will be extracted.
		self.digrams = self.set_digrams(star_bins[0][9:10], [star_bins[2][3:8], star_bins[3][3:8], star_bins[4][3:8], star_bins[5][3:8]])
		
		# The dominant inhabitants on this planet.
		self.inhabitants = self.set_inhabitants([star_bins[2][3:6], star_bins[2][0:3], [star_bins[0], star_bins[1]], star_bins[2][6:8]])
		
		# Has this world been colonised by humans?
		self.humans = self.set_humans(star_bins[2][8:])
		
		self.tech_level = self.set_tech_level([star_bins[0], star_bins[1]]) # Level of technological advancement on the planet.
		self.population = self.set_population()                             # Population of inhabitants, in billions.
		self.production = self.set_production([star_bins[0], star_bins[1]]) # Production rate of the planet, in Mcr (whatever that is).
	
	# -----------------------------------------------------------------------------------
	# Methods to retrieve data from star_bins and use them in the various calculations
	# made to determine each star's data.
	# -----------------------------------------------------------------------------------

	# Method for setting the value of a property if all that is needed is to convert
	# the extracted binary to an integer.
	# Used by x, y and gov.
	def set_basic(self, binary_extract):
		return int("0b" + binary_extract, 2)
	
	# Converts a binary value to integer and uses it to calculate the radius of a planet
	# in km.
	def set_radius(self, binary_extract):
		modifier = int("0b" + binary_extract, 2)
		return 256 * (11 + modifier) + self.x
	
	# Converts a binary value to integer. If gov is less than 2, does maths on it.
	# Otherwise, just returns the vanilla converted value.
	def set_eco(self, binary_extract):
		eco = int("0b" + binary_extract, 2)
		if self.gov < 2:
			return floor(eco / 4) * 4 + 2 + (eco % 2)
		else:
			return eco
	
	# Determines the number of digrams with which to construct a planet name (3 or 4).
	# Then returns a list of values.
	def set_digrams(self, digram_count_binary, digram_binaries):
		digram_count = int("0b" + digram_count_binary, 2) + 3
		digrams = []                                                        # List to which digrams will be appended to and returned.
		
		for digram in range(0, digram_count):
			digrams.append(int("0b" + digram_binaries[digram], 2) * 2)
		
		return digrams
	
	# Assembles a list of values with which to construct a description of a planet's
	# inhabitants, and returns it.
	def set_inhabitants(self, binary_extracts):
		inhabitants = [None] * 4                                            # List to which inhabitant description values will be appended to and returned.
		extract_values = [None] * 2                                         # Stores the integer versions of the values stored in binary_extracts.
		
		# Ensures the first and second description values cannot exceed 3 and 6,
		# respectively, since these values are used in list lookups.
		inhabitants[0] = min([int("0b" + binary_extracts[0], 2), 3])
		inhabitants[1] = min([int("0b" + binary_extracts[1], 2), 6])
		
		third_attribute = 0                                                 # Calculated value used as the third description value and to calculate the fourth.
		
		
		for step in range(3):
			
			# Start and end positions for list slicing. In each iteraction of step,
			# the for loop ahead takes one of the last three bits of the highest
			# significant byte, last bit first, and converts it to int.
			binary_start = 8 - (step + 1)
			binary_end = binary_start + 1
			
			for val in range(2):
				extract_values[val] = int("0b" + binary_extracts[2][val][binary_start:binary_end], 2)
			
			combined_values = (extract_values[0] + extract_values[1]) % 2
			
			# If this isn't the first step, multiply the combined values by 2 or 4,
			# respectively, before adding to third_attribute.
			if step > 0:
				combined_values *= (2*step)
			
			third_attribute = third_attribute + combined_values
		
		inhabitants[2] = min([third_attribute, 6])                          # The third description value cannot exceed 6.
		
		inhabitants[3] = (int("0b" + binary_extracts[3], 2) + third_attribute) % 8
		
		return inhabitants
	
	# Returns a true/false value with which to determine whether a planet has human
	# colonists rather than a unique indigenous species.
	def set_humans(self, binary_extract):
		if int("0b" + binary_extract, 2) < 127:
			return 1                                                        # Human Colonists
		else:
			return 0                                                        # Indigenous Species
	
	# Calculates the technology level of the planet.
	def set_tech_level(self, binary_extracts):
		tl = self.get_tl_data(binary_extracts)
		
		return float((1 - tl[0]) * 4 + (1 - tl[1]) * 2 + 1 - tl[2] + tl[3] + tl[4] + tl[5] + 1)
	
	# Calculates the production rate of a planet. This depends on some of the data used
	# to calculate tech_level.
	def set_production(self, binary_extracts):
		tl = self.get_tl_data(binary_extracts)
		
		return ((1 - tl[0]) * 4 + (1 - tl[1]) * 2 + 1 - tl[2] + 3) * (self.gov + 4) * self.population * 80
	
	# Converts the bits of data used in the calculation of both tech_level and production.
	def get_tl_data(self, binary_extracts):
		tl = [None] * 6
		tl[0] = int("0b" + binary_extracts[0][5:6], 2)
		tl[1] = int("0b" + binary_extracts[0][6:7], 2)
		tl[2] = int("0b" + binary_extracts[0][7:8], 2)
		tl[3] = int("0b" + binary_extracts[1][6:8], 2)
		tl[4] = int("0b" + binary_extracts[1][10:12], 2)
		tl[5] = int("0b" + binary_extracts[1][12:13], 2)
		
		return tl
	
	# Calculates the population of the planet, in billions. Relies on tech_level, gov
	# and eco for this calculation.
	def set_population(self):
		return ((self.tech_level - 1) * 4 + self.gov + self.eco + 1) / 10
	
	# -----------------------------------------------------------------------------------
	# Methods to output a star's data onto the screen.
	# -----------------------------------------------------------------------------------
	# Outputs a star's data to screen.
	def print_data(self, digram_string):
		system("cls" if name == "nt" else "clear")
		print "Name:        " + self.get_star_name(digram_string)
		print "Loc:         " + str(self.x) + ":" + str(self.y)
		print "Radius:      " + str(self.radius_x) + " km"
		
		print "Government:  " + self.get_gov()
		print "Economy:     " + self.get_eco()
		
		print "Inhabitants: " + self.get_inhabitants()
		
		print "Tech Level:  " + str(int(self.tech_level))
		print "Population:  " + str(self.population) + " Billion"
		print "Production:  " + str(int(self.production)) + " Mcr"
	
	# Constructs the name of the planet, based on the values provided in the digrams
	# list, and returns it.
	def get_star_name(self, digram_string):
		
		# The star's name, into which each digram extracted from digram_string will be
		# concatenated before it is returned.
		star_name = ""
		
		for ind, digram in enumerate(self.digrams):
			
			# Get the start and end positions within which to extract the two-letter
			# digrams.
			digram_start = digram
			digram_end = digram_start + 2
			
			# Find
			star_name = star_name + digram_string[digram_start:digram_end]
		
		# Remove instances of special characters from the star's name, further
		# shortening the name and even producting odd-numbered name lengths.
		star_name = star_name.replace("@","")
		star_name = star_name.replace("'","")
		
		return star_name
	
	# Constructs and returns the inhabitant description for a planet as long as humans
	# is set to 0. Otherwise just returns the phrase "Human Colonists".
	def get_inhabitants(self):
		if self.humans == 0:
			inhabitants = ""
			in_data = [["Large", "Fierce", "Small", ""],
					   ["Green", "Red", "Yellow", "Blue", "Black", "Harmless", ""],
					   ["Slimy", "Bug-Eyed", "Horned", "Bony", "Fat", "Furry", ""],
					   ["Rodents", "Frogs", "Lizards", "Lobsters", "Birds", "Humanoids", "Felines", "Insects"]]
			
			for ind, val in enumerate(self.inhabitants):
				if not in_data[ind][val] == "":
					inhabitants = inhabitants + in_data[ind][val]
					if ind < 3:
						inhabitants = inhabitants + " "
			
			return inhabitants.strip()
		else:
			return "Human Colonists"
	
	# Finds the government type that corresponds to the value of gov and returns it.
	def get_gov(self):
		governments = ["Anarchy", "Feudal", "Multi-Government", "Dictatorship", "Communist", "Confederacy", "Democracy", "Corporate State"]
		
		return governments[self.gov]
	
	# Finds the economy type that corresponds to the value of gov and returns it.
	def get_eco(self):
		economies = ["Rich Industrial", "Average Industrial", "Poor Industrial", "Mainly Industrial", "Mainly Agricultural", "Rich Agricultural", "Average Agricultural", "Poor Agricultural"]
		
		return economies[self.eco]
