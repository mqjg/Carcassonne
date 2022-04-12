import json

class deck:
	def __init__(self, deckFile = "vanillaDeck.json"):
		print("Creating deck")
		with open(deckFile, "r") as f:
			self.tileList = json.loads(f.read())

		self.deck = []
		for tile in tileList:
			amount = tileList[tile]['amount']
			tileDict = tileList[tile]['tileDict']

			#TODO: Can this be done in one line?
			for i in range(amount):
				self.deck.append(tile(tileDict))


	def shuffle(self):
		print("Shuffling deck")

	def draw(self):
		print("Drawing card")

	def printTileList(self):
		for tile in self.tileList:
			print(f"{tile} x{self.tileList[tile]['amount']}")
			print(self.tileList[tile]['tileDict'])
			



class tile:
	"""
	carcosonne tiles are defined by thier edges and center. The edges can be roads, cities, or fields. The centers can be monasteries, crossroads, or city entrances. Expansions can introduce other edges or centers. We call these parts of the tile "features"

	You can divide the tiles edges into 12 portions (the center being a 13 portion). We represent this using a 13-element array of strings. For example the starting tile would be:

		self.sides = [city,city,city,field,road,field,field,field,road,field,None]

	the last element of the list represents the center portion of the tile. None indicates that there is no special center to the tile.

	This representation allows for easy accesing for tile compatibility checks, but does not encode how tile elements (roads,cities, etc) are connected. To store this information we keep a dictionary of the contents of the tile. Each dictionary entry will be a 2-d nested list. Each each element will be a list of integers indicating which of the edge are connected. For example the starting tile would be:

		self.tileDict = {cities: [[0,1,2]], roads: [[10,4]], fields: [[11,3],[9,8,7,6,5]], monastery: [], cityEntrance: [], crossroad: []}

		TODO: Would a list of sets be better? Should we combine the center entrys (monastery,cityEntrance,etc.) into just one entry called "center" or something?


	"""

	def __init__(self, tileDictInput):


		#TODO: This allows for portions of the tiles to overwritten and for some portions of the tile to remain undefined. Undefined edges will likely also be unrepresented in 
		self.sides = ["None" for i in range(13)] 
		for feature in tileDictInput:
			for i in tileDictInput[feature]:
				for j in i:
					self.sides[j] = feature 

		self.tileDict = tileDictInput
		self.neighbors = [None,None,None,None] #tile objects to the top, bottom, left, and right sides of this tile

	def tileInfo(self):
		print("tile dictionary: ",self.tileDict, "\n")
		print("sides list: ",self.sides, "\n")
		print("neighbors list: ",self.neighbors, "\n")





# class road:
# 	def __init__(self, owner = None):
# 		print("Creating road")
# 		self.owner = owner

# class city:
# 	def __init__(self, owner = None):
# 		print("Creating city")
# 		self.owner = owner

# class field:
# 	def __init__(self, owner = None):
# 		print("Creating field")
# 		self.owner = owner


# class map:

# 	"""
# 	The map is a collection of tiles
# 	"""

# 	self.roads = []
# 	self.cities = []
# 	self.fields = []
# 	self.monasteries = []

# 	def __init__(self):
# 		print("this is the map")

# 	def score():
# 		print("This is the score.")



if __name__ == '__main__':

	# startingTile = {"cities": [[0,1,2]], "roads": [[10,4]], "fields": [[11,3],[9,8,7,6,5]], "monastery": [], "cityEntrance": [], "crossroad": []}

	# testTile = tile(startingTile)
	# testTile.tileInfo()
	#deckFile="testTile.json"
	testDeck = deck()
	testDeck.printTileList()