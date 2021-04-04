import pygame
import sys


'''
INFORMATION:
	- fromLeft is the number of blocks between left border and current block
	- fromTop is the number of blocks between top border and current block
	- "block" <=> "rectangle"
'''


'''
DEFINE CONSTANTS
'''
# color tupels
BLACK = (0,0,0)
WHITE = (200,200,200)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)


class Screen:
	def __init__ (self, window_width, window_height, block_size):
		if (block_size >= window_height or block_size >= window_width):
			sys.exit("Error: Block size is bigger than window size.")
		self._window_width = window_width
		self._window_height = window_height
		self._block_size = block_size
		self._window = None
		self._clock = pygame.time.Clock()	# framerate
		self._blocks = [None] * (window_width * window_height)	# list of all blocks (indexed by blockNumber; stores color of block)
		self._startBlocks = [] 	# stores all start blocks (fromLeft, fromTop)
		self._endBlocks = []
		self._blocksPerRow = window_width // block_size
		self._blocksPerColumn = window_height // block_size
		self._startBlock = None 	# current start block number
		self._endBlock = None		# current end block number


	def setupGrid(self):
		# pygame setup
		pygame.init()
		pygame.display.init()
		self._window = pygame.display.set_mode ((self._window_width, self._window_height))
		pygame.display.set_caption ("Pathfinding visualization")
		self._window.fill(WHITE)
		# draw initial grid
		for x in range(self._blocksPerRow):
			for y in range(self._blocksPerColumn):
				rectangle = pygame.Rect(x * self._block_size, y * self._block_size,
				self._block_size, self._block_size)
				self._blocks[y*self._blocksPerRow+x] = WHITE
				pygame.draw.rect(self._window, BLACK, rectangle, 1)	# draw black frame

		# listen for mouse events (drawing)
		drawingFinished = False	# if drawing phase is finished
		while (True and (not(drawingFinished))):
			for event in pygame.event.get():
				# check if user closes window
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				# check if drawing is done (by pressing the Enter key)
				if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
					drawingFinished = True
					self._finishedDrawing = True
					break
			# drawing rectangles
			self.drawStart()
			self.drawEnd()
			self.drawBorders()
			self._clock.tick(60)			# 60 fps (if smaller no fluent drawing)
			pygame.display.update()

		# finished drawing but still show the window
		if len(self._startBlocks) == 1 and len(self._endBlocks) == 1:
			pass
		else:
			sys.exit("Error: You have to select one start and one end block!")
		while True and drawingFinished:
			for event in pygame.event.get():
				# check if user closes window
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self._clock.tick(60)
			pygame.display.update()
			return True


	'''
	DRAW RECTANGLES (BORDER/START/END RECTANGLES)
		- Border rectangles: 	BLACK	-> left click
		- START rectangle: 		GREEN	-> mouse wheel click
		- END rectangle:		RED		-> right click
		-> use pygame.mouse.get_pressed() to see which mouse button was clicked (returns triple of booleans)
	'''
	def drawRectangle(self,colorToDraw):
		# fill the current block with certain color and store change in blocks[]
		xPosMouse = pygame.mouse.get_pos()[0]
		yPosMouse = pygame.mouse.get_pos()[1]
		fromLeft = xPosMouse // self._block_size	# 0 is start index of columns
		fromTop = yPosMouse // self._block_size	# 0 is start index of rows
		blockNumber = fromTop*self._blocksPerRow + fromLeft
		self._blocks[blockNumber] = colorToDraw
		rect = pygame.Rect(fromLeft * self._block_size, fromTop * self._block_size, self._block_size, self._block_size)
		pygame.draw.rect(self._window, colorToDraw, rect)
		return (fromLeft, fromTop, blockNumber)


	def drawStart(self):
		# mouse wheel for start block
		if pygame.mouse.get_pressed() == (False, True, False):
			if len(self._startBlocks) == 1:
				# delete previous start block and make it WHITE
				fromLeftPrevious = self._startBlocks[0][0]
				fromTopPrevious = self._startBlocks[0][1]
				del self._startBlocks[0]
				blockNumberPrevious = fromTopPrevious * self._blocksPerRow + fromLeftPrevious
				self._blocks[blockNumberPrevious] = WHITE
				rect = pygame.Rect(fromLeftPrevious * self._block_size, fromTopPrevious * self._block_size, self._block_size, self._block_size)
				pygame.draw.rect(self._window, WHITE, rect)
				pygame.draw.rect(self._window, BLACK, rect, 1)	# black frame
			else:
				# draw new start block and store it in startBlocks[]
				(fromLeftNew, fromTopNew, blockNumberNew) = self.drawRectangle(GREEN)
				self._startBlock = blockNumberNew
				self._blocks[blockNumberNew] = GREEN
				self._startBlocks.append((fromLeftNew, fromTopNew))


	def drawEnd(self):
		# right mouse button for end block
		if pygame.mouse.get_pressed() == (False, False, True):
			if len(self._endBlocks) == 1:
				# delete previous end block and make it WHITE
				fromLeftPrevious = self._endBlocks[0][0]
				fromTopPrevious = self._endBlocks[0][1]
				del self._endBlocks[0]
				blockNumberPrevious = fromTopPrevious * self._blocksPerRow + fromLeftPrevious
				self._blocks[blockNumberPrevious] = WHITE
				rect = pygame.Rect(fromLeftPrevious * self._block_size, fromTopPrevious * self._block_size, self._block_size, self._block_size)
				pygame.draw.rect(self._window, WHITE, rect)		# white fill color
				pygame.draw.rect(self._window, BLACK, rect, 1)	# black frame
			else:
				# draw new start block and store it in endBlocks[]
				(fromLeftNew, fromTopNew, blockNumberNew) = self.drawRectangle(RED)
				self._endBlock = blockNumberNew
				self._blocks[blockNumberNew] = RED
				self._endBlocks.append((fromLeftNew, fromTopNew))


	def drawBorders (self):
		# left mouse button for border block
		if pygame.mouse.get_pressed() == (True, False, False):
			self.drawRectangle(BLACK)


	'''
	GETTERS AND SETTERS
	'''
	def getStartBlock(self):		
		return self._startBlock
	

	def getEndBlock(self):
		return self._endBlock
	

	def getBlocks(self):
		return self._blocks


	def colorBlock(self, blockNumber, colorToDraw):
		# sets color of a certain block
		self._blocks[blockNumber] = colorToDraw
		# draw it in grid
		fromLeft = blockNumber % self._blocksPerRow
		fromTop = blockNumber // self._blocksPerRow
		rect = pygame.Rect(fromLeft * self._block_size, fromTop * self._block_size, self._block_size, self._block_size)
		pygame.draw.rect(self._window, colorToDraw, rect)
		pygame.display.update()
