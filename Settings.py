
from main import *

width = 50
height = 50
num_blocks_x = 6
num_blocks_y = 2
indentation = 2
table_size_x = width * num_blocks_x
table_size_y = height * num_blocks_y
presetting = [[Cells(0) for _ in range(num_blocks_y)] for _ in range(num_blocks_x)]
presetting[2][0] = Cells(1)
# presetting = False