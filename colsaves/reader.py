import os
import sys
import json
from pathlib import Path
import tools

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import binascii
global building_bist_glob
building_bist_glob = []

ORDERS = [
	"no order",
	"sentry",
	"trade route",
	"go to",
	"0x04",
	"0x05",
	"fortify",
	"0x07",
	"plow",
	"road"
]

NATION_FLAG = [
"icons.ss_118.png",
"icons.ss_119.png",
"icons.ss_120.png",
"icons.ss_121.png",
]

CONTROL = [
	"player",
	"ai",
	"withdrawn from new world"
]

DIFFICULTY = [
	"Discoverer",
	"Explorer",
	"Conquistador",
	"Governor",
	"Viceroy"
]

OCCUPATIONS = [
	"Farmer",		   # 0x00
	"Sugar planter",	# 0x01
	"Tobacco planter",  # 0x02
	"Cotton planter",   # 0x03
	"Fur trapper",	  # 0x04
	"Lumberjack",	   # 0x05
	"Ore miner",		# 0x06
	"Silver miner",	 # 0x07
	"Fisherman",		# 0x08
	"Distiller",		# 0x09
	"Tobacconist",	  # 0x0A
	"Weaver",		   # 0x0B
	"Fur Trader",	   # 0x0C
	"Carpenter",		# 0x0D
	"Blacksmith",	   # 0x0E
	"Gunsmith",		 # 0x0F
	"Preacher",		 # 0x10
	"Statesman",		# 0x11
	"Teacher",		  # 0x12
	"unknown (0x13)",   # 0x13
	"Pioneer",		  # 0x14
	"Vet. Soldier",	 # 0x15
	"Scout",			# 0x16
	"Veteran dragoon",  # 0x17
	"Missionary",	   # 0x18
	"Ind. Servant",	 # 0x19
	"Criminal",		 # 0x1A
	"Indian convert",   # 0x1B
	"Free colonist",	# 0x1C
	"Armed brave",	  # 0x1D
	"Mounted brave",	# 0x1E
	"unknown (0x1f)"	# 0x1F
]

DIRECTIONS = [
	"N",
	"E",
	"S",
	"W",
	"NW",
	"NE",
	"SE",
	"SW"
]

BUILDINGS = [
	"Stockade", "Fort", "Fortress", "Armory", "Magazine", "Arsenal", "Docks", "Drydock",
	"Shipyard", "Town hall", "Town hall", "Town hall", "Schoolhouse", "College", "University", "Warehouse",
	"Warehouse Exp", "Stable", "Custom house", "Printing press", "Newspaper", "Weavers house", " Weavers shop", "Textile mill",
	"Tobacconists house", "Tobacconists shop", "Cigar factory", "Rum distillers house", "Rum distillers shop", "Rum factory", "Capitol", "Capitol Exp",
	"Fur traders house", "Fur traders shop", "Fur factory", "Carpenters shop", "Lumber mill", "Church", "Cathedral", "Blacksmiths house",
	"Blacksmiths shop", "Iron works", "Artillery", "Wagon Train", "Caravel", "Merchantman", "Galleon", "Privateer",
	"Frigate", "Nothing"
]

GOODS = [
	"Food",		 # 0x00
	"Sugar",		# 0x01
	"Tabacco",	  # 0x02
	"Cotton",	   # 0x03
	"Furs",		 # 0x04
	"Lumber",	   # 0x05
	"Ore",		  # 0x06
	"Silver",	   # 0x07
	"Horses",	   # 0x08
	"Rum",		  # 0x09
	"Cigars",	   # 0x0A
	"Cloth",		# 0x0B
	"Coats",		# 0x0C
	"Trade Goods",  # 0x0D
	"Tools",		# 0x0E
	"Muskets"	   # 0x0F
]

NATIONS = [
	"English",   # 0x00
	"French",	# 0x01
	"Spanish",   # 0x02
	"Dutch",	 # 0x03
	"Inca",	  # 0x04
	"Aztec",	 # 0x05
	"Arawak",	# 0x06
	"Iroquios",  # 0x07
	"Cherokee",  # 0x08
	"Apache",	# 0x09
	"Sioux",	 # 0x0A
	"Tupi",	  # 0x0B
]

UNITS = {
	0: "Colonist",
	1: "Soldier",
	2: "Pioneer",
	3: "Missionary",
	4: "Veteran dragoon",
	5: "Scout",
	6: "Regular (Tory Army)",
	7: "Cavalery (Continental Army)",
	8: "Cavalery (Tory Army)",
	9: "Regular (Continental Army)",
	10: "Treasure",
	11: "Artillery",
	12: "Wagon Train",
	13: "Caravel",
	14: "Merchantman",
	15: "Galleon",
	16: "Privateer",
	17: "Frigate",
	18: "Man-O-War (Continental Army)",
	19: "Brave",
	20: "Armed Brave",
	21: "Mounted Brave",
}

icons = {
'Stockade': 'icons.ss_0.png',
'Fort': 'icons.ss_1.png',
'Fortress': 'icons.ss_2.png',
'Colony': 'icons.ss_3.png',
'UNKNOWN': 'icons.ss_4.png',
'Caravel': 'icons.ss_5.png',
'Merchantman': 'icons.ss_6.png',
'Galleon': 'icons.ss_7.png',
'Wagon Train': 'icons.ss_8.png',
'Artillery': 'icons.ss_9.png',
'INDIAN_1': 'icons.ss_10.png',
'INDIAN_2': 'icons.ss_11.png',
'INDIAN_3': 'icons.ss_12.png',
'INDIAN_4': 'icons.ss_13.png',
'Privateer': 'icons.ss_14.png',
'Frigate': 'icons.ss_15.png',
'Treasure': 'icons.ss_16.png',
'Colonist': 'icons.ss_58.png',
'Soldier': 'icons.ss_59.png',
'Pioneer': 'icons.ss_60.png',
'Missionary': 'icons.ss_61.png',
'Artillery (damaged)': 'icons.ss_65.png',
'Indian convert': 'icons.ss_66.png',
'Colonist (Pioneer)': 'icons.ss_73.png',
'Vet. Soldier': 'icons.ss_74.png',
'Scout': 'icons.ss_75.png',
'Veteran dragoon': 'icons.ss_76.png',
'Missionary': 'icons.ss_77.png',
'Farmer': 'icons.ss_81.png',
'Sugar planter': 'icons.ss_82.png',
'Tobacco planter': 'icons.ss_83.png',
'Cotton planter': 'icons.ss_84.png',
'Fur trapper': 'icons.ss_85.png',
'Lumberjack': 'icons.ss_86.png',
'Ore miner': 'icons.ss_87.png',
'Silver miner': 'icons.ss_88.png',
'Fisherman': 'icons.ss_89.png',
'Distiller': 'icons.ss_90.png',
'Tobacconist': 'icons.ss_91.png',
'Weaver': 'icons.ss_92.png',
'Fur Trader': 'icons.ss_93.png',
'Carpenter': 'icons.ss_94.png',
'Blacksmith': 'icons.ss_95.png',
'Gunsmith': 'icons.ss_96.png',
'Preacher': 'icons.ss_97.png',
'Statesman': 'icons.ss_98.png',
'Teacher': 'icons.ss_99.png',
'Free Colonist': 'icons.ss_100.png',
'Pioneer': 'icons.ss_101.png',
'Vet. Soldier': 'icons.ss_102.png',
'Scout': 'icons.ss_103.png',
'Veteran dragoon': 'icons.ss_104.png',
'Missionary': 'icons.ss_105.png',
'Ind. Servant': 'icons.ss_106.png',
'Criminal': 'icons.ss_107.png',
'INDIAN_LAND': 'icons.ss_108.png',
'Indian convert': 'icons.ss_109.png',
'Brave': 'icons.ss_109.png',
'Armed brave': 'icons.ss_110.png',
'Mounted brave': 'icons.ss_111.png',
'Armed Mounted brave': 'icons.ss_112.png',
'English': 'icons.ss_118.png',
'French': 'icons.ss_119.png',
'Spanish': 'icons.ss_120.png',
'Dutch': 'icons.ss_121.png',
'Regular (Tory Army)': 'icons.ss_125.png',
'Cavalery (Tory Army)': 'icons.ss_126.png',
'Man-O-War (Continental Army)': 'icons.ss_127.png',
'Regular (Continental Army)': 'icons.ss_128.png',
'Cavalery (Continental Army)': 'icons.ss_129.png',
'FLAG': 'icons.ss_130.png',
}

FOUNDING_FATHERS = [
	"Adam Smith",			# 00
	"Jakob Fugger",		  # 01
	"Peter Minuit",		  # 02
	"Peter Stuyvesant",	  # 03
	"Jan de Witt",		   # 04
	"Ferdinand Magellan",	# 05
	"Francisco Coronado",	# 06
	"Hernando de Soto",	  # 07

	"Henry Hudson",		  # 08
	"Sieur De La Salle",	 # 09
	"Hernan Cortes",		 # 0A
	"George Washington",	 # 0B

	"Paul Revere",		   # 0C
	"Francis Drake",		 # 0D
	"John Paul Jones",	   # 0E
	"Thomas Jefferson",	  # 0F

	"Pocahontas",			# 10
	"Thomas Paine",		  # 11
	"Simon Bolivar",		 # 12
	"Benjamin Franklin",	 # 13

	"William Brewster",	  # 14
	"William Penn",		  # 15
	"Jean de Brebeuf",	   # 16
	"Juan de Sepulveda",	 # 17

	"Bartolme de las Casas"  # 18
]

TERRAIN = {
	0: "terrain/00 tundra.png", 
	1: "terrain/01 desert.png", 
	2: "terrain/02 plains.png", 
	3: "terrain/03 prairie.png",
	4: "terrain/04 grassland.png",
	5: "terrain/05 savannah.png", 
	6: "terrain/06 march.png", 
	7: "terrain/07 swamp.png", 
}

TERRAIN_NON_LAND = {
	0: "terrain/09 arctic.png", 
	1: "terrain/0B sea.png", 
	2: "terrain/0A sealane.png", 
}

RIVER_START = 0
MOUNTAIN_START = 32
HILL_START = 48
FOREST_START = 64
ROADS_START = 80
FOG_OF_WAR = 104
COAST_FOG_OF_WAR = 112
COAST = 150


class Context:
	def __init__(self, file):
		self.file = file
		self.objects = []


class Tell:
	def read(self, context):
		return context.file.tell()


class String:
	def __init__(self, length):
		self.length = length

	def read(self, context):
		string = context.file.read(self.length).decode("utf-8")
		first_nul = string.find("\0")
		if first_nul >= 0:
			return string[:first_nul]
		return string


class Bits:

	"""
	 Extract :num_bits each from :num_bytes bytes. The length of the result array ist num_bytes // num_bits.
	"""

	def __init__(self,  num_bytes, num_bits):
		self.num_bytes = num_bytes
		self.num_bits = num_bits

	def read(self, context):
		bytes = context.file.read(self.num_bytes)
		return list(tools.stream_bits(bytes, self.num_bits))


class Skip:
	def __init__(self, bytes):
		self.bytes = bytes

	def read(self, context):
		return context.file.seek(bytes, os.SEEK_CUR)


class Byte:
	def read(self, context):
		return tools.readu8(context.file)


class Bytes:
	def __init__(self, length):
		self.length = length

	def read(self, context):
		return context.file.read(self.length)


class Short:

	def read(self, context):
		return tools.read16(context.file)


class Word:
	def read(self, context):
		return tools.readu16(context.file)


class Int:

	def read(self, context):
		return tools.read32(context.file)


class Lookup:
	def __init__(self, array, reader, default=None):
		self.array = array
		self.reader = reader
		self.default = default

	def read(self, context):
		index = self.reader.read(context)
		return self.lookup_index(self.default, index)

	def lookup_index(self, default, index):
		if default is None:
			default = index
		try:
			return self.array[index]
		except IndexError:
			return default
		except KeyError:
			return default


class LookupList(Lookup):
	def read(self, context):
		index_list = self.reader.read(context)
		return [self.lookup_index(self.default, index) for index in index_list]


class Loop:
	def __init__(self, count_function, reader):
		self.count_function = count_function
		self.reader = reader

	def read(self, context):
		result = []

		for i in range(self.count_function(context)):
			context.loop_index = i
			result.append(self.reader.read(context))

		context.loop_index = -1
		return result


class Bean:
	def __init__(self, factory, **kwargs):
		self.factory = factory
		self.reader = kwargs

	def read(self, context):
		bean = self.factory()
		context.objects.append(bean)
		for name, reader in self.reader.items():
			result = reader.read(context)
			setattr(bean, name, result)

		context.objects.pop()
		# if the bean has an after_read() method, call it after reading all properties
		if hasattr(bean, 'after_read'):
			bean.after_read(context)

		return bean


class Position(Bean):
	def __init__(self, reader=Byte()):
		super().__init__(Position,
						 x=reader,
						 y=reader)

	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(self, ["x", "y"])


class ColonistType(Byte):
	def read(self, context):
		byte = super().read(context)
		return OCCUPATIONS[byte]


class Player(Bean):
	def __init__(self):
		super().__init__(Player,
						 name=String(24),
						 continent=String(24),
						 byte1=Byte(),
						 control=Lookup(CONTROL,  Byte()),
						 diplomacy=Word())

	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(self, ["name", "continent", "byte1", "control", "diplomacy"])


class Colonist():
	def __serialize__(self):
		tile_string = ""
		if hasattr(self, "tile"):
			tile_string = " on tile {}".format(self.tile)
		return {"text": "{0} working as {1} for {2} rounds{3}".format(self.specialization, self.occupation, self.time, tile_string)}


class Colony(Bean):
	def __init__(self):
		super().__init__(
			Colony,
			x=Byte(),
			y=Byte(),
			name=String(24),
			nation=Lookup(NATIONS, Byte()),
			dummy1=Bytes(4),
			colonists_num=Byte(),
			colonists_occupation=Loop(lambda _: 32, ColonistType()),
			colonists_specialization=Loop(lambda _: 32, ColonistType()),
			colonists_time=Bytes(16),
			tile_usage=Bytes(8),
			dummy2=Bytes(12),
			buildings_bitset=Bytes(6),
			customs_house=Bytes(2),
			dummy3=Bytes(6),
			hammers=Word(),
			current_production=Lookup(BUILDINGS, Byte(), BUILDINGS[-1]),
			dummy4=Bytes(5),
			storage=Loop(lambda _: len(GOODS), Word()),
			dummy5=Bytes(8),
			bells=Int(),
			data=Int(),
			)

	def merge_colonist_data(self):
		self.colonists = []
		for i in range(self.colonists_num):
			colonist = Colonist()
			colonist.occupation = self.colonists_occupation[i]
			colonist.specialization = self.colonists_specialization[i]
			time = self.colonists_time[i//2]
			nibbles = [time >> 4, time & 0x0F]
			colonist.time = nibbles[1 - (i % 2)]
			self.colonists.append(colonist)

		for direction_index, colonist in enumerate(self.tile_usage):
			if colonist < len(self.colonists):
				self.colonists[colonist].tile = DIRECTIONS[direction_index]

		del self.colonists_occupation
		del self.colonists_specialization
		del self.colonists_time
		del self.tile_usage

	def merge_buildings_data(self):
		global building_bist_globs
		buildings_bits = list(tools.stream_bits(self.buildings_bitset))
		building_bist_glob.append(buildings_bits)
		self.buildings = [BUILDINGS[building_index] for building_index, build_flag in enumerate(buildings_bits) if build_flag == 1]
		del self.buildings_bitset

	def merge_goods_data(self):
		self.goods = {GOODS[goods_index]: goods_count for goods_index, goods_count in enumerate(self.storage)}
		del self.storage
		customs_house_bits = list(tools.stream_bits(self.customs_house))
		self.customs_house = [GOODS[goods_index] for goods_index, flag in enumerate(customs_house_bits) if flag == 1]

	def after_read(self, _):
		self.merge_colonist_data()
		self.merge_buildings_data()
		self.merge_goods_data()

	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(
			self, [
				"x", "y", "name", "nation", "dummy1",
				"colonists_num",
				"colonists",
				"dummy2",
				"buildings",
				"customs_house",
				"dummy3",
				"hammers",
				"current_production",
				"dummy4",
				"goods",
				"dummy5",
				"bells",
				"data"
				]
			)


class Unit(Bean):
	def __init__(self):
		super().__init__(
			Unit,
			pos=Position(),
			type=Lookup(UNITS, Byte()),
			nation_index=Byte(),
			dummy1=Byte(),
			used_moves=Byte(),
			dummy2=Bytes(2),  # order { PLOW = 8, ROAD = 9 }
			order=Lookup(ORDERS, Byte()),
			goto_pos=Position(),
			dummy3=Bytes(1),
			num_cargo=Byte(),
			cargo_types=LookupList(GOODS, Bits(3, 4)),
			cargo_amount=Bytes(6),  # last cargo pos used for num of tools for pioneer
			dummy4=Bytes(1),
			profession=Lookup(OCCUPATIONS, Byte()),
			data=Bytes(4)
			)

	def after_read(self, context):
		self.id = context.loop_index
		# swap cargo types (ony when we have cargo)
		if self.num_cargo > 0:
			self.cargo_types[0], self.cargo_types[1] = self.cargo_types[1], self.cargo_types[0]
			self.cargo_types[2], self.cargo_types[3] = self.cargo_types[3], self.cargo_types[2]
			self.cargo_types[4], self.cargo_types[5] = self.cargo_types[5], self.cargo_types[4]

		self.cargo = [(cargo_type, self.cargo_amount[index]) for index, cargo_type in enumerate(self.cargo_types[:self.num_cargo])]

		self.nation = NATIONS[self.nation_index & 15]
		self.dummy0 = self.nation_index >> 4

		#del self.num_cargo
		#del self.cargo_types
		#del self.cargo_amount

	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(
			self, [
				"id", "pos", "type", "nation", "dummy0", "dummy1", "used_moves", "dummy2", "order", "goto_pos", "dummy3", "cargo",
				"num_cargo",
				"cargo_types",
				"cargo_amount",
				"dummy4",
				"profession",
				"data"
				]
			)


class Europe(Bean):
	def __init__(self):
		super().__init__(
			Europe,
			padding1=Bytes(1),
			tax_rate=Byte(),
			next_recruits=Loop(lambda _: 3, Lookup(OCCUPATIONS, Byte()),),
			padding2=Bytes(2),
			founding_fathers_bitset=Bytes(4),
			padding3=Bytes(1),
			current_bells=Word(),
			padding4=Bytes(4),
			current_founding_father=Lookup(FOUNDING_FATHERS, Word(), "none"),
			padding5=Bytes(10),
			bought_artillery=Byte(),
			padding6=Bytes(11),
			gold=Word(),
			padding7=Bytes(2),
			current_crosses=Word(),
			needed_crosses=Word(),
			padding8=Bytes(26),
			goods_price=Loop(lambda _: len(GOODS), Byte()),
			goods_unknown=Loop(lambda _: len(GOODS), Short()),
			goods_balance=Loop(lambda _: len(GOODS), Int()),
			goods_demand=Loop(lambda _: len(GOODS), Int()),
			goods_demand2=Loop(lambda _: len(GOODS), Int()),
			)

	def reverse_sublist(self, lst, start, end):
		sublist = lst[start:end]
		sublist.reverse()
		lst[start:end] = sublist

	def after_read(self, _):
		founding_fathers_bits = list(tools.stream_bits(self.founding_fathers_bitset))
		# reverse bits
		self.reverse_sublist(founding_fathers_bits, 0, 8)
		self.reverse_sublist(founding_fathers_bits, 8, 16)
		self.reverse_sublist(founding_fathers_bits, 16, 24)
		self.reverse_sublist(founding_fathers_bits, 24, 32)

		self.founding_fathers = [FOUNDING_FATHERS[father_index] for father_index, flag in enumerate(founding_fathers_bits) if flag == 1]

	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(self, [
			"padding1",
			"tax_rate",
			"next_recruits",
			"padding2",
			"founding_fathers",
			"padding3",
			"current_bells",
			"padding4",
			"current_founding_father",
			"padding5",
			"bought_artillery",
			"padding6",
			"gold",
			"padding7",
			"current_crosses",
			"needed_crosses",
			"padding8",
			"goods_price",
			"goods_unknown",
			"goods_balance",
			"goods_demand",
			"goods_demand2",
			])


class Tribe(Bean):
	def __init__(self):
		super().__init__(
			Tribe,
			pos=Position(),
			nation=Lookup(NATIONS,  Byte()),
			state=Byte(),
			population=Byte(),
			mission=Lookup(NATIONS,  Byte(), "none"),
			padding1=Bytes(4),
			panic=Byte(),
			padding2=Bytes(5),
			debug_number=Byte(),
			population_loss_in_current_turn=Byte()
			)

	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(
			self, [
				"pos",
				"nation",
				"state",
				"population",
				"mission",
				"padding1",
				"panic",
				"padding2",
				"debug_number",
				"population_loss_in_current_turn",
				]
			)


class Indian(Bean):
	def __init__(self):
		super().__init__(
			Indian,
			padding1=Bytes(58),
			meet=Loop(lambda _: 4, Byte()),
			padding2=Bytes(8),
			aggression=Loop(lambda _: 4, Word())
			)

	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(
			self, [
				"padding1",
				"meet",
				"padding2",
				"aggression",
				]
			)

class Tile:
	pass

class Map:
	def __init__(self, map_size_function):
		self.map_size_function = map_size_function;
			
	def read(self, context):
		self.map_data = []
		map_size = self.map_size_function(context)
		for y in range(map_size.y):
			self.map_data.append(context.file.read(map_size.x))
			
		tiles = []
		total_map_size = map_size.x * map_size.y
		for index in range(total_map_size):
			x = index % map_size.x
			y = index // map_size.x
			tile = Tile()
			data = self.map_data[y][x]
			tile.image_id = data & 7
			tile.non_land = (data & int('0x10', 16)) >> 4 
			if tile.non_land == 0:
				tile.forest = (data & int('0x08', 16)) >> 3
				tile.mountain = (data & int('0x20', 16)) >> 5
			else:
				tile.forest = 0
				tile.mountain = 0

			tiles.append(tile)
			
		# find neighbours
		for index in range(total_map_size):
			tile = tiles[index]
			top = tiles[index - map_size.x]
			down = tiles[min(index + map_size.x, total_map_size - 1)]
			left = tiles[index - 1]
			right = tiles[min(index + 1, total_map_size - 1)]
			
			tile.forest_neighbours = (top.forest << 3) + (down.forest << 2) + (left.forest << 1) + right.forest
			tile.mountain_neighbours = (top.mountain << 3) + (down.mountain << 2) + (left.mountain << 1) + right.mountain

		self.tiles = tiles
		return self

	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(self, ["map_data"])


class Savegame:
	def __serialize__(self):
		return tools.object_attributes_to_ordered_dict(self, [
			"magic", "padding1",
			"map_size",
			"padding2",
			"year",
			"autumn",
			"turn",
			"padding3",
			"active_unit",
			"padding4",
			"num_tribes",
			"num_units",
			"num_colonies",
			"padding5",
			"difficulty",
			"padding6",
			"royal_force",
			"padding7",
			 "players",
			"padding8",
			 "colonies",
			 "units",
			 "europe",
			 "tribes",
			 "indians",
			"padding9",
			"cursor_pos",
			"padding10",
			"viewport",
			"map", 
			"pos",
			"map", 
			"padding_final",
			])

	def __str__(self):
		return json.dumps(self, indent=3, cls=tools.Encoder)


format = Bean(
	Savegame,
	magic=String(8),
	padding1=Bytes(4),
	map_size=Position(Word()), 
	padding2=Bytes(10),
	year=Word(),
	autumn=Word(),
	turn=Word(),
	padding3=Bytes(2),
	active_unit=Word(),
	padding4=Bytes(6),
	num_tribes=Word(),
	num_units=Word(),
	num_colonies=Word(),
	padding5=Bytes(6),
	difficulty=Lookup(DIFFICULTY, Byte()),
	padding6=Bytes(51),
	royal_force=Loop(lambda _: 4, Word()),
	padding7=Bytes(44),
	players=Loop(lambda _: 4, Player()),
	padding8=Bytes(24),
	colonies=Loop(lambda context: context.objects[-1].num_colonies, Colony()),
	units=Loop(lambda context: context.objects[-1].num_units, Unit()),
	europe=Loop(lambda _: 4, Europe()),
	tribes=Loop(lambda context: context.objects[-1].num_tribes, Tribe()),
	indians=Loop(lambda _: 8, Indian()),
	padding9=Bytes(717),
	cursor_pos=Position(Word()),
	padding10=Bytes(2),
	viewport=Position(Word()),
	map=Map(lambda context: context.objects[-1].map_size), 
	pos=Tell(),
	padding_final=Bytes(320)
	)
	
	
def read_image(image_name):
	image_name = Path(str(Path(__file__).parent.resolve())+"/images/"+image_name)
	image = Image.open(image_name)
	rgba_image = image.convert("RGBA")
	#print("{} {} {}".format(image_name, image.mode, image.info))
	return rgba_image

	
#from pudb import set_trace

def write_map(map, map_size):
#	set_trace()
	images = {k: read_image(image_name) for k, image_name in TERRAIN.items()}
	non_land_images = {k: read_image(image_name) for k, image_name in TERRAIN_NON_LAND.items()}
	forest_images = [read_image("surface/phys0.ss_{:01d}.png".format(i+FOREST_START)) for i in range(16)]
	mountain_images = [read_image("surface/phys0.ss_{:01d}.png".format(i+MOUNTAIN_START)) for i in range(16)]
	#RIVER_images = [read_image("surface/phys0.ss_{:01d}.png".format(i+RIVER_START)) for i in range(32)]
	#HILL_images = [read_image("surface/phys0.ss_{:01d}.png".format(i+HILL_START)) for i in range(16)]
	#ROADS_images = [read_image("surface/phys0.ss_{:01d}.png".format(i+ROADS_START)) for i in range(24)]
	#COAST_images = [read_image("surface/phys0.ss_{:01d}.png".format(i+COAST)) for i in range(4)]

	map_image = Image.new("RGBA", (map_size.x*16, map_size.y*16))
	for index in range(map_size.x * map_size.y):
		x = index % map_size.x
		y = index // map_size.x
		tile = map.tiles[index]

		if tile.non_land == 1:
			map_image.paste(non_land_images[tile.image_id], (x*16, y*16))
		else:
			if tile.image_id in images:
				map_image.paste(images[tile.image_id], (x*16, y*16))
			if tile.forest > 0:
				map_image.paste(forest_images[tile.forest_neighbours], (x*16, y*16), forest_images[tile.forest_neighbours])
				
			if tile.mountain > 0:
				map_image.paste(mountain_images[tile.mountain_neighbours], (x*16, y*16), forest_images[tile.mountain_neighbours])
		
		
	return map_image


def read_savegame(filename):
	import inspect
	with open(filename, "rb") as file:
		context = Context(file)
		savegame = format.read(context)

		f = open("savegame.txt", "w")
		f.write(str(savegame))
		f.close()
		map_image = write_map(savegame.map, savegame.map_size)
		colonies_dict = {}
		col_num = 0

		play_no = 0
		for i in savegame.players:
			play_no = play_no + 1
			if i.byte1 == 192:
				break
		if play_no ==1:
			player = str('English')
		if play_no ==2:
			player = str('French')
		if play_no ==3:
			player = str('Dutch')
		if play_no ==4:
			player = str('Spanish')

		for i in savegame.colonies:
			col_name = i.name
			#if i.nation != player:
				#continue
			col_num = col_num + 1
			#colonies_dict[col_num] = {}
			colonies_dict[col_name] = {}
			colonist_number = 0
			colonies_dict[col_name]['colonists'] = {}
			inspect_obj = inspect.getmembers(i, lambda a:not(inspect.isroutine(a)))
			for z in inspect_obj:
				if ' object at' not in str(z) and 'dummy' not in str(z) and not '__' in str(z):
					colonies_dict[col_name][z[0]] = z[1]
			for y in i.colonists:
				inspect_obj = inspect.getmembers(y, lambda a:not(inspect.isroutine(a)))
				colonist_number = colonist_number + 1
				colonies_dict[col_name]['colonists'][colonist_number] = {}
				for zy in inspect_obj:
					if ' object at' not in str(zy) and 'dummy' not in str(zy) and not '__' in str(zy):
						colonies_dict[col_name]['colonists'][colonist_number][zy[0]] = zy[1]

		mapped_colonies = []
		for i in colonies_dict:
			text_col = [255,255,255]
			colonies_dict[i]['nation'][0]
			if colonies_dict[i]['nation'] != player:
				#continue
				text_col = [255,0,0]
			if colonies_dict[i]['nation']  == player:
				text_col = [255,255,255]
			if colonies_dict[i]['nation'] == 'English':
				col_icon = NATION_FLAG[0]
			elif colonies_dict[i]['nation'] == 'French':
				col_icon = NATION_FLAG[1]
			elif colonies_dict[i]['nation'] == 'Spanish':
				col_icon = NATION_FLAG[2]
			elif colonies_dict[i]['nation'] == 'Dutch':
				col_icon = NATION_FLAG[3]
			colony_image2 = read_image('icons/' + col_icon)
			building_bits = building_bist_glob[list(colonies_dict.keys()).index(i)]
			n = 8
			bits_split = [building_bits[i:i+n] for i in range(0, len(building_bits), n)]
			curr_binary = ''
			for x in bits_split:
				curr_binary = x
				break
			if curr_binary[5] == 1:
				colony_image = "icons/icons.ss_2.png" #FORTRESS
			elif curr_binary[6] == 1:
				colony_image = "icons/icons.ss_1.png" #fort
			elif curr_binary[7] == 1:
				colony_image = "icons/icons.ss_0.png" #stockade
			else:
				colony_image = "icons/icons.ss_3.png"
			mapped_colonies.append(str(colonies_dict[i]['x']) + '_' + str(colonies_dict[i]['y']))
			colony_image = read_image(colony_image)
			map_image.paste(colony_image, (colonies_dict[i]['x']*16, colonies_dict[i]['y']*16),colony_image)
			map_image.paste(colony_image2, (5+colonies_dict[i]['x']*16, colonies_dict[i]['y']*16),colony_image2)
			ImageDraw.Draw(map_image).text((-len(i) + colonies_dict[i]['x']*16, colonies_dict[i]['y']*16), i + '['+colonies_dict[i]['nation'][0]+'](' + str(len(colonies_dict[i]['colonists'])) + ')',(text_col[0],text_col[1],text_col[2]))
			
		f = open("savegame.txt", "a")
		village_learned = []
		village_unlearned = []
		village_scouted = []
		village_unscouted = []
		for i in savegame.tribes:
			tribe_bin_state = str("{0:04b}".format(i.state))[-4:]
			tribe_state = ''
			tribe_name = i.nation + '('+ str(i.population) + ')'
			
			village = '(' + str(i.pos.x) + ', ' + str(i.pos.y) + ')   ' + i.nation + '('+ str(i.population) + ')' + ', ' + str('scouted(' + str(tribe_bin_state[0]) + ')' + ', ' + 'capital(' + str(tribe_bin_state[1]) + ')' + ', ' + 'learned(' + str(tribe_bin_state[2]) + ')' +', ' + 'artillery(' + str(tribe_bin_state[3]) + ')') + '\n'
			
			if tribe_bin_state[0] == '1':
				tribe_state = tribe_state + 'S'
			if tribe_bin_state[1] == '1':
				#tribe_state = tribe_state + 'C'
				tribe_name = i.nation + '*('+ str(i.population) + ')'
			if tribe_bin_state[2] == '1':
				tribe_state = tribe_state + 'L'
			if tribe_bin_state[3] == '1':
				tribe_state = tribe_state + 'A'
			tribe_name = tribe_name + '(' + tribe_state + ')'
			if i.nation == "Inca":
				colony_image = "icons/icons.ss_13.png"
			elif i.nation == "Aztec":
				colony_image = "icons/icons.ss_12.png"
			elif i.nation == "Arawak":
				colony_image = "icons/icons.ss_11.png"
			elif i.nation == "Iroquios":
				colony_image = "icons/icons.ss_11.png"
			elif i.nation == "Cherokee":
				colony_image = "icons/icons.ss_11.png"
			elif i.nation == "Apache":
				colony_image = "icons/icons.ss_11.png"
			elif i.nation == "Sioux":
				colony_image = "icons/icons.ss_10.png"
			elif i.nation == "Tupi":
				colony_image = "icons/icons.ss_10.png"
			colony_image = read_image(colony_image)
			mapped_colonies.append(str(i.pos.x) + '_' + str(i.pos.y))
			map_image.paste(colony_image, (i.pos.x*16, i.pos.y*16),colony_image)
			ImageDraw.Draw(map_image).text((-len(tribe_name) + i.pos.x*16, i.pos.y*16), tribe_name,(0,255,0))
			if tribe_bin_state[2] == '1':
				village_learned.append(village)
			else:
				village_unlearned.append(village)
			if tribe_bin_state[0] == '1':
				village_scouted.append(village)
			else:
				village_unscouted.append(village)
				
		f.write(str('\n\nLEARNED_VILLAGES:\n'))
		for i in village_learned:
			f.write(str(i))
		f.write(str('\n\nUNLEARNED_VILLAGES:\n'))
		for i in village_unlearned:
			f.write(str(i))

		f.write(str('\n\nSCOUTED_VILLAGES:\n'))
		for i in village_scouted:
			f.write(str(i))
		f.write(str('\n\nUNSCOUTED_VILLAGES:\n'))
		for i in village_unscouted:
			f.write(str(i))

		f.close()
		for i in savegame.units:
			if (str(i.pos.x)+'_'+str(i.pos.y) in mapped_colonies) == False:
				#print(i.pos.x, i.pos.y, i.type, i.order, i.nation, i.profession)
				col_type = i.type
				if str(i.type).lower() == str('Colonist').lower(): # and str(i.profession).lower() != str('Free colonist').lower():
					col_type = i.profession
				for x in icons:
					if x.lower() == str(col_type).lower():
						unit_icon = "icons/" + icons[x]
						unit_icon = read_image(unit_icon)
						map_image.paste(unit_icon, (i.pos.x*16, i.pos.y*16),unit_icon)
						flag = False
						if i.nation == 'English':
							col_icon = NATION_FLAG[0]
							flag = True
						elif i.nation == 'French':
							col_icon = NATION_FLAG[1]
							flag = True
						elif i.nation == 'Spanish':
							col_icon = NATION_FLAG[2]
							flag = True
						elif i.nation == 'Dutch':
							col_icon = NATION_FLAG[3]
							flag = True
						if flag == True:
							colony_image2 = read_image('icons/' + col_icon)
							map_image.paste(colony_image2, (5+i.pos.x*16, i.pos.y*16),colony_image2)
							if i.order == 'sentry':
								ImageDraw.Draw(map_image).text((6+i.pos.x*16, -1+i.pos.y*16), 'S',"black", stroke_width=1,stroke_fill="black")
							elif i.order == 'trade route':
								ImageDraw.Draw(map_image).text((6+i.pos.x*16, -1+i.pos.y*16), 'T',"black", stroke_width=1,stroke_fill="black")
							elif i.order == 'go to':
								ImageDraw.Draw(map_image).text((6+i.pos.x*16, -1+i.pos.y*16), 'G',"black",  stroke_width=1,stroke_fill="black")
							elif i.order == 'fortify':
								ImageDraw.Draw(map_image).text((6+i.pos.x*16, -1+i.pos.y*16), 'F',"black", stroke_width=1,stroke_fill="black")
							elif i.order == 'plow':
								ImageDraw.Draw(map_image).text((6+i.pos.x*16, -1+i.pos.y*16), 'P',"black", stroke_width=1,stroke_fill="black")
							elif i.order == 'road':
								ImageDraw.Draw(map_image).text((6+i.pos.x*16, -1+i.pos.y*16), 'R',"black", stroke_width=1,stroke_fill="black")
		map_image.save("map.png", "PNG")
		import subprocess
		subprocess.Popen("notepad savegame.txt")
		Image.open("map.png").show()

def main():
	read_savegame(sys.argv[1])

if __name__ == "__main__":
	main()


"""
"0x1a,0x1a,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0xa3,0x0,0x19,0x19,0x19,0x19,0x19,0x19,0x1a,0x1a",
"0x1a,0x1a,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0xc,0xb,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0x19,0xb,0xa,0x19,0xa,0xa,0x2,0x23,0x19,0x19,0x19,0x19,0x19,0x1a,0x1a"




0000 0011 -> Prairie
0010 0011 -> Prairie + Hills
1010 0011 -> Prairie + Mountain
0000 1010 -> Plains + Forest
0000 1011 -> Prairie + Forest

"""
