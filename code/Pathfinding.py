import Window
import Queue
import pygame
import sys


class Pathfinder:
	def __init__(self,window_width,window_height,blockSize,enableDiagonalPaths):
		# setup window and draw start/end/borders
		self.enableDiagonalPaths = enableDiagonalPaths
		self.window_width = window_width
		self.window_height = window_height
		self.block_size = blockSize
		self.blocksPerRow = self.window_width // self.block_size
		self.blocksPerColumn = self.window_height // self.block_size
		self.game = Window.Screen(self.window_width,self.window_height,self.block_size)
		while self.game.setupGrid() == False:
			pass	# still drawing
		self.blocks = self.game.getBlocks()	# all blocks in grid with corresponding color
	
	
	def startPathfinding(self):
		self.breadthFirstSearch()


	def breadthFirstSearch(self):
		q = Queue.Queue()
		predecessor = [None] * self.window_width * self.window_height
		visited = [False] *  self.window_width * self.window_height
		start = self.game.getStartBlock()
		end = self.game.getEndBlock()
		q.enqueue(start)
		while not(q.isEmpty()):
			current = q.dequeue()	# current block
			if current == end:
				print("Success: Path was found!")
				# get path
				temp = predecessor[end]
				path = []
				while predecessor[temp] != start:
					path.append(temp)
					temp = predecessor[temp]
				path.append(temp)
				# print path
				for block in path:
					fromLeft = block % self.blocksPerRow
					fromTop = block // self.blocksPerRow
					rect = pygame.Rect(fromLeft * self.block_size, fromTop * self.block_size,
					 self.block_size, self.block_size)
					pygame.draw.rect(self.game._window, Window.BLUE, rect)
				# show result (blue path)
				while True:
					for event in pygame.event.get():
						# check if user closes window
						if event.type == pygame.QUIT:
							pygame.quit()
							sys.exit()
					pygame.display.update()
			else:
				if current != start:
					self.game.colorBlock(current, Window.YELLOW)	# color block as visited
				for neighbour in (self.getValidNeighbours(current)):
					if visited[neighbour] == False:
						predecessor[neighbour] = current
						q.enqueue(neighbour)
						visited[neighbour] = True
		print("There is no path from start block to end block!")


	# all neighbours which are not a border block and unvisited (WHITE) and exist (not outside of grid)
	# are valid neighbours
	def getValidNeighbours(self, currentBlock):
		fromLeft = currentBlock % self.blocksPerRow
		fromTop = currentBlock // self.blocksPerRow
		"""
		Neighbours of current:
			n1  |  n2   |  n3
		________|_______|_______
			n4  |current|  n5 
		________|_______|_______
			n6  |  n7   |  n8
				|       |
		"""			
		n1 = currentBlock - self.blocksPerRow - 1	
		n2 = n1 + 1									
		n3 = n2 + 1									
		n4 = currentBlock - 1						
		n5 = currentBlock + 1						
		n6 = currentBlock + self.blocksPerRow - 1	
		n7 = n6 + 1									
		n8 = n7 + 1
		possibleNeighbours = [n1,n2,n3,n4,n5,n6,n7,n8]
		# check which neighbours are valid
		validNeighbours = []
		validNeighbours = [False for i in range(8)]	# initialize with False values
		
		# TODO: how to check valid neighbours cleaner than with bunch of if-else-statements
		if fromLeft == 0 or fromTop == 0 or fromLeft == self.blocksPerRow-1 or fromTop == self.blocksPerColumn-1:
			# block is in first/last row/column of grid -> does not have all 8 neighbours	
			alreadyMatched = False # to not override result of previous if statement
			if fromLeft == 0:
				if fromTop == 0:
					# n1,n2,n3,n4,n6 do not exist --> remember that array is 0 indexed! -> only [4],[6],[7] exist
					validNeighbours[4] = True	# n5
					validNeighbours[6] = True	# n7
					validNeighbours[7] = True	# n8
					alreadyMatched = True
				elif fromTop == self.blocksPerColumn - 1:
					# n1,n4,n6,n7,n8 do not exist
					validNeighbours[1] = True
					validNeighbours[2] = True
					validNeighbours[4] = True
					alreadyMatched = True
				else:
					# n1,n4,n6 do not exist
					validNeighbours[1] = True
					validNeighbours[2] = True
					validNeighbours[4] = True
					validNeighbours[6] = True
					validNeighbours[7] = True
					alreadyMatched = True
			if fromTop == 0 and alreadyMatched == False:
				if fromLeft == self.blocksPerRow - 1:
					# n1,n2,n3,n5,n8 do not exist
					validNeighbours[3] = True
					validNeighbours[5] = True
					validNeighbours[6] = True
					alreadyMatched = True
				else:
					# n1,n2,n3 do not exist
					validNeighbours[3] = True
					validNeighbours[4] = True
					validNeighbours[5] = True
					validNeighbours[6] = True
					validNeighbours[7] = True
					alreadyMatched = True
			if fromTop == self.blocksPerColumn - 1 and alreadyMatched == False:
				if fromLeft == self.blocksPerRow - 1:
					# n3,n5,n7,n8 do not exist
					validNeighbours[0] = True
					validNeighbours[1] = True
					validNeighbours[3] = True
					validNeighbours[5] = True
					alreadyMatched = True
				else:
					# n6,n7,n8 do not exist
					validNeighbours[0] = True
					validNeighbours[1] = True
					validNeighbours[2] = True
					validNeighbours[3] = True
					validNeighbours[4] = True
					alreadyMatched = True
			if fromLeft == self.blocksPerRow - 1 and alreadyMatched == False:
				# n3,n5,n8 do not exist
				validNeighbours[0] = True
				validNeighbours[1] = True
				validNeighbours[3] = True
				validNeighbours[5] = True
				validNeighbours[6] = True
				alreadyMatched = True
		else:
			# block is "inner block" -> does have all 8 neighbours
			validNeighbours = [True for i in range(8)]

		# return all neighbours that are valid
		output = []
		for i in range(len(validNeighbours)):
			neighbour = possibleNeighbours[i]
			if self.enableDiagonalPaths == True:	# all 8 neighbours can be valid neighbours (diagonal routes allowed)
				if (((self.blocks[neighbour]) == Window.WHITE or (self.blocks[neighbour]) == Window.RED) 
					and validNeighbours[i] == True):
					output.append(neighbour)
			else:	# only neighbours n2, n4, n5, n7 can be valid (no diagonal routes)
				if i == 1 or i == 3 or i == 4 or i == 6:
					if (((self.blocks[neighbour]) == Window.WHITE or (self.blocks[neighbour]) == Window.RED) 
						and validNeighbours[i] == True):
						output.append(neighbour)
		return output


def main():
	p = Pathfinder(900, 900, 30, False)
	p.startPathfinding()


main()
