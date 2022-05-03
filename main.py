import json
import random
import numpy as np
import os
import pygame as pg

pageSize = (1024, 576)
imageScale = 50 #How much to scale distances buy so that they coincide with the size of tile sprites.

class Deck:
	#TODO:Need to add ability to set the first card in the deck to the starting tile.
	def __init__(self, deckFile = "decks/vanillaDeck.json"):
		#TODO: we might be abel to get something similar to "Deck.__init__" in a more generic way using __name__ to get the function name.
		print("Deck.__init__: Creating deck")
		with open(deckFile, "r") as f:
			self.tileList = json.loads(f.read())

		self.deck = []
		self.nTiles = 0 #total number of tiles in deck.
		self.drawPos = 0
		for tileName in self.tileList:
			amount = self.tileList[tileName]['amount']
			tileDict = self.tileList[tileName]['tileDict']

			#TODO: Can this be done in one line?
			tileCount = 0
			for i in range(amount):
				self.deck.append(Tile(tileDict,tileName))
				self.nTiles += 1
				tileCount += 1
				print(f"{self.nTiles:3d} {tileCount:3d} {tileName} loaded")
		print("")

	def shuffle(self, resetDrawPos = True, firstTile = "startingTile"):
		if firstTile is None:
			print("Deck.shuffle: Shuffling deck")
			random.shuffle(self.deck)
		else:
			if firstTile in self.tileList:
				print(f"Deck.shuffle: Shuffling deck with {firstTile} as first tile.")
				self.deck = []
				for tileName in self.tileList:
					if firstTile == tileName:
						amount = self.tileList[tileName]['amount']-1
					else:
						amount = self.tileList[tileName]['amount']
					tileDict = self.tileList[tileName]['tileDict']

					self.deck = self.deck + [Tile(tileDict,tileName) for i in range(amount)]

				random.shuffle(self.deck)
				self.deck.insert(0,Tile(self.tileList[firstTile]['tileDict'],firstTile))
			else:
				print(f"Deck.shuffle: Unable to find {firstTile}. Shuffling normally.")
				random.shuffle(self.deck)

		if resetDrawPos:
			print("Deck.shuffle: resetting draw position.")
			self.drawPos = 0

	def draw(self):
		if self.drawPos < self.nTiles:
			newTile = self.deck[self.drawPos]
			self.drawPos += 1
			print(f"Deck.draw: Drew a {newTile.tileName} tile.")
			return newTile
		else:
			print("Deck.draw: Reached end of deck.")
			return None

	def printTileList(self):
		print("Deck.printTileList: Deck tile list:")
		for tileName in self.tileList:
			print(f"{tileName} x{self.tileList[tileName]['amount']}")
			# print(self.tileList[tile]['tileDict'],"\n")
			for feature in self.tileList[tileName]['tileDict']:
				print(f"  {feature}")
				for i in self.tileList[tileName]['tileDict'][feature]:
					print(f"    {i}")
		print("")

	def printDeck(self, style = "pretty"):
		print("Deck.printDeck: Deck contents in order:")
		#print(self.deck) #prints dict obj locations
		for tile in self.deck:
			tile.tileInfo(style = "pretty")
			



class Tile:
	"""
	carcosonne tiles are defined by their edges and center. The edges can be roads, cities, or fields. The centers can be monasteries, crossroads, or city entrances. Expansions can introduce other edges or centers. We call these parts of the tile "features"

	You can divide the tiles edges into 12 portions (the center being a 13 portion). We represent this using a 13-element array of strings. For example the starting tile would be:

		self.sides = [city,city,city,field,road,field,field,field,road,field,None]

	the last element of the list represents the center portion of the tile. None indicates that there is no special center to the tile.

	This representation allows for easy accessing for tile compatibility checks, but does not encode how tile elements (roads,cities, etc) are connected. To store this information we keep a dictionary of the contents of the tile. Each dictionary entry will be a 2-d nested list. Each each element will be a list of integers indicating which of the edge are connected. For example the starting tile would be:

		self.tileDict = {cities: [[0,1,2]], roads: [[10,4]], fields: [[11,3],[9,8,7,6,5]], monastery: [], cityEntrance: [], crossroad: []}

		TODO: Would a list of sets be better? Should we combine the center entrys (monastery,cityEntrance,etc.) into just one entry called "center" or something?
	"""

	def __init__(self, tileDictInput,tileNameInput, imageDir="sprites/tileImages"):

		#TODO: This allows for portions of the tiles to overwritten and for some portions of the tile to remain undefined. Undefined edges will likely also be unrepresented in 
		
		self.sides = ["None" for i in range(13)] 
		for feature in tileDictInput:
			for i in tileDictInput[feature]:
				for j in i:
					self.sides[j] = feature 

		self.tileDict = tileDictInput
		self.tileName = tileNameInput
		self.neighbors = [None,None,None,None] #tile objects to the top, right, bottom, left sides of this tile in clockwise order
		self.printStyles = ["pretty","verbose"]
		self.pos = None #this will become a 3d numpy integer array. The first two number will indicate the x,y position. The last digit will indicate the orientation of the tile (either 0,1,2,3 corresponding to rotating the tile 90 degrees clockwise)
		self.orient = 0 #Will be an integer to indicate the orientation of the tile (either 0,1,2,3 corresponding to rotating the tile 90 degrees clockwise)

		self.tileImage = pg.image.load(os.path.join(imageDir, self.tileName)+".png").convert()
		self.tileImage = pg.transform.scale(self.tileImage, (imageScale, imageScale))
		self.tileImageRect = self.tileImage.get_rect()

	def tileInfo(self, style = "pretty"):

		if style == "pretty":
			print(self.tileName)
			for feature in self.tileDict:
				print(f"  {feature}")
				for i in self.tileDict[feature]:
					print(f"    {i}")
			print("")
		elif style == "verbose":
			print("self.tileDict = ",self.tileDict)
			print("self.sides = ",self.sides)
			print("self.neighbors = ",self.neighbors, "\n")
		else:
			print(f"invalid style: {style}")
			print(f"valid print styles {self.printStyles}")

	def visualizeTile(self,style = "image" , vpos = (0,0)):

		if style == "text":
			s = [side[0] for side in self.sides] #first letter of each side feature.
			print("  ____________","\n",
			      "| \ 0| 1 |2 /|","\n",
			      "|11\ |   | /3|","\n",
			      "|___\|___|/__|","\n",
			      "|    |   |   |","\n",
			      "|10  |   |  4|","\n",
			      "|____|___|___|","\n",
			      "|   /|   |\  |","\n"
			      " | 9/ |   | \\5|","\n",
			      "|_/_8|_7_|6_\|")

			print("  ____________________","\n",
			      "|  \ ",s[0],"| ",s[1]," |"     ,s[2],"/  |","\n",
			      "|" ,s[11],"\   |     |  /"      ,s[3],"|","\n",
			      "|____\__|_____|_/____|","\n",
			      "|    |          |    |","\n",
			      "|" ,s[10]," |   ",s[12],"    | ",s[4],"|","\n",
			      "|____|__________|____|","\n",
			      "|    /  |     | \    |","\n"
			      " |",s[9],"/   |     |  \\"     ,s[5],"|","\n",
			      "|__/_",s[8],"|_",s[7],"_|"    ,s[6],"\__|")
		elif style == "image":
			if self.pos is None:
				window.blit(self.tileImage, self.tileImageRect)
				pg.display.update()
			else:
				window.blit(self.tileImage, tuple(self.pos))
				pg.display.update()
		else:
			print(f"invalid style: {style}")

	def rotateTile(self):
		if self.orient < 3:
			self.orient += 1
		else:
			self.orient = 0

		self.tileImage = pg.transform.rotate(self.tileImage, -90)
		self.visualizeTile(style="image")
		print(f"Tile.rotateTile: rotating tile to  {self.orient}.")

class Map:
	"""
	The map is a collection of tiles
	"""
	def __init__(self, startingTile, mapCenter = np.array([0,0])):
		print(f"Map.__init__: building Map with {startingTile.tileName} as first tile.")
		self.mapElements = [startingTile]
		startingTile.pos = mapCenter
		startingTile.orient = 0
		self.ordDirs = imageScale * np.array([[0, -1], [1, 0], [0, 1], [-1, 0]])
		self.validPositions = self.ordDirs + mapCenter #ordDirs, short for ordinal directions specifcy relative positions up, right, down, left (going clockwise) or a given location
		print("")

	def getValidPositions(self):
		print("Map.getValidPositions: Creating new valid positions array")
		self.validPositions = []
		for tile in self.mapElements:
			if tile.neighbors[0] is None: #top
				#print(f"Map.getValidPositions: top added")
				self.validPositions.append(tile.pos + self.ordDirs[0])
			if tile.neighbors[1] is None: #right
				#print(f"Map.getValidPositions: right added")
				self.validPositions.append(tile.pos + self.ordDirs[1])
			if tile.neighbors[2] is None: #bottom
				#print(f"Map.getValidPositions: bottom added")
				self.validPositions.append(tile.pos + self.ordDirs[2])
			if tile.neighbors[3] is None: #left
				#print(f"Map.getValidPositions: left added")
				self.validPositions.append(tile.pos + self.ordDirs[3])

	def validPosition(self,pos):
		for validPos in self.validPositions:
			if np.array_equal(pos,validPos):
				print(f"Map.validPosition: {pos} is a valid position.")
				return True
		return False

	def getNeighbors(self,pos):
		print(f"Map.getNeighbors: Getting neighbors of pos {pos}")
		neighborsPos = pos + self.ordDirs
		#print(f"Map.getNeighbors: {neighborsPos[0]} {neighborsPos[1]} {neighborsPos[2]} {neighborsPos[3]}")
		neighbors = [None for i in range(4)]
		for tile in self.mapElements:
			for i in range(len(neighborsPos)):
				if np.array_equal(tile.pos,neighborsPos[i]):
					neighbors[i] = tile
		return neighbors

	def validOrientationSingle(self, newTile, oldTile, ordDir):
		#Get orientation
		newTileOrient = newTile.orient
		oldTileOrient = oldTile.orient

		newTileSides = [i for i in range(12)]
		for i in range(newTileOrient):
			newTileSides = newTileSides[-3:] + newTileSides[:-3]

		oldTileSides = [i for i in range(12)]
		for i in range(oldTileOrient):
			oldTileSides = oldTileSides[-3:] + oldTileSides[:-3]

		if np.array_equal(ordDir,self.ordDirs[0]):
			newTileIndicies = newTileSides[:3]
			oldTileIndicies = oldTileSides[6:9]
		elif np.array_equal(ordDir,self.ordDirs[1]):
			newTileIndicies = newTileSides[3:6]
			oldTileIndicies = oldTileSides[9:]
		elif np.array_equal(ordDir,self.ordDirs[2]):
			newTileIndicies = newTileSides[6:9]
			oldTileIndicies = oldTileSides[:3]
		else:
			newTileIndicies = newTileSides[9:]
			oldTileIndicies = oldTileSides[3:6]

		newTileFeatures = [newTile.sides[i] for i in newTileIndicies]
		oldTileFeatures = [oldTile.sides[i] for i in oldTileIndicies]
		oldTileFeatures.reverse()

		#print("Map.validOrientationSingle: newTileFeatures ", newTileFeatures)
		#print("Map.validOrientationSingle: newTileIndicies ", newTileIndicies)
		#print("Map.validOrientationSingle: oldTileFeatures ", oldTileFeatures)
		#print("Map.validOrientationSingle: oldTileIndicies ", oldTileIndicies)
		#print("")

		if newTileFeatures == oldTileFeatures:
			print(f"Map.validOrientationSingle: {ordDir} is valid direction given orientation.")
			return True
		else:
			print(f"Map.validOrientationSingle: {ordDir} is not a valid direction given orientation.")
			return False

	def validOrientation(self, newTile, neighbors):
		#TODO: range(len(neighbors)) will probably always be 4. Should I hard code it?
		for i in range(len(neighbors)):
			if neighbors[i] is not None:
				if not self.validOrientationSingle(newTile, neighbors[i], self.ordDirs[i]):
					print(f"Map.validOrientation: {newTile.orient} is not a valid orientation.")
					return False
		print(f"Map.validOrientation: {newTile.orient} is a valid orientation.")
		return True

	def updateNeighbors(self, newTile, neighborsInput):
		print(f"Updating neighbor information for {newTile.tileName} and its neighbors.")
		newTile.neighbors = neighborsInput
		for i in range(len(neighborsInput)):
			j = i + 2
			if j >= 4:
				j -= 4
			if neighborsInput[i] is not None:
				neighborsInput[i].neighbors[j] = newTile

	def addTile(self, newTile, pos, orient):
		print(f"Map.addTile: Trying to add {newTile.tileName} at {pos} with orient {orient}.")
		newTile.pos = pos
		newTile.orient = orient
		if self.validPosition(pos):
			neighbors = self.getNeighbors(pos)
			if self.validOrientation(newTile,neighbors):
				print(f"Map.addTile: Adding {newTile.tileName} to the map.")
				self.mapElements.append(newTile)
				self.updateNeighbors(newTile, neighbors)
				self.getValidPositions() #This recreates the list of valid positions.
				return True
			else:
				print(f"Map.addTile: Could not add {newTile.tileName} to the map.")
				newTile.pos = (0,0)
				return False
		else:
			print(f"Map.addTile: Could not add {newTile.tileName} to the map.")
			newTile.pos = (0,0)
			return False

	def visualizeMap(self):
		print("Map.visualizeMap: Creating map visualization.")
		for tile in self.mapElements:
			tile.visualizeTile()

	def score(self):
		print("Map.score: This is the score.")

class Button:

	def __init__(self, imageDir = os.path.join(os.getcwd(),"sprites/marker.png"), pos = None):
		print(f"Button.__init__: creating button at {pos}")
		self.pos = pos
		self.buttonImage = pg.image.load(imageDir).convert()
		self.buttonImage = pg.transform.scale(self.buttonImage, (imageScale, imageScale))
		self.buttonRect = self.buttonImage.get_rect()
		self.buttonRect.left = pos[0] #+ self.buttonRect.width/2
		self.buttonRect.top = pos[1] #+ self.buttonRect.height/2

	def mouseOverButton(self, mouse):
		(mouseX, mouseY) = mouse
		[left, top, width, height] = [i for i in self.buttonRect]
		xMin = left
		xMax = left + width
		yMin = top
		yMax = top + height
		if xMin <= mouseX <= xMax and yMin <= mouseY <= yMax:
			print(f"Button.{self.mouseOverButton.__name__}: Button at {np.array(mouse)} selected.")
			return True
		else:
			#print(f"Button.{self.mouseOverButton.__name__}: False")
			return False

	def visualizeButton(self):
		if self.pos is None:
			window.blit(self.buttonImage, self.buttonRect)
			pg.display.update()
		else:
			window.blit(self.buttonImage, tuple(self.pos))
			pg.display.update()

if __name__ == '__main__':

	pg.init() #What does this do? :^)
	window = pg.display.set_mode(pageSize) #Make a window object?What toher args are there?
	clock = pg.time.Clock()

	deck = Deck() #load deck from file and intilize draw deck of tiles
	deck.shuffle() #shuffle the draw deck
	#print("page center: ", np.array(window.get_rect().center))
	tileMap = Map(deck.draw(),np.array(window.get_rect().center)) #create the map or gameboard where tiles are played

	#This is the draw cycle where tiles are repeatedly drawn and placed
	for i in range(deck.nTiles -1):
		print(f"\nTurn {i}")

		buttons = [Button(imageDir=os.path.join(os.getcwd(), "sprites/squareMarker.png"), pos=validPosition) for validPosition in tileMap.validPositions]  # Create a button for each valid position
		for button in buttons: button.visualizeButton()
		tileMap.visualizeMap()

		newTile = deck.draw()
		#newTile.tileInfo()
		newTile.visualizeTile(style="image")
		tileAdded = False

		#print(f"Valid positions are: \n{tileMap.validPositions}")
		while not tileAdded:
			clock.tick(7.5)  # frames to render /second TODO: Does this need to go here?
			selectedButtonPos = None
			for ev in pg.event.get():
				if ev.type == pg.QUIT:
					pg.quit()
				elif ev.type == pg.KEYDOWN:
					if ev.key == pg.K_r:
						newTile.rotateTile()
				elif ev.type == pg.MOUSEBUTTONDOWN:
					mouse = pg.mouse.get_pos()
					for button in buttons:
						if button.mouseOverButton(mouse):
							newPos = button.pos
							tileAdded = tileMap.addTile(newTile, newPos, newTile.orient)
							break





			# userInput = input("Provide location and orientation as [x,y,o]: ")
			# print("")
			# try:
			# 	userInputParsed = eval(userInput)
			# 	newPos = np.array(userInputParsed[:2])
			# 	newOrient = userInputParsed[2]
			# 	tileAdded = tileMap.addTile(newTile, newPos, newOrient)
			# 	print("")
			# 	break
			# except:
			# 	print(f"__main__: could not parse user input.")
			# 	print("")

pg.quit()

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