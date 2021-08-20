
import random

def minesweeper(width: int, height: int, totalMines: int) -> list:
    
    if totalMines > (width * height - 16):
        raise Exception("FATAL - Too many mines for board size")
    if (width < 4) or (height < 4) or (width == 4 and height == 4):
        raise Exception("FATAL - Board too small")
    
    output = [0 for i in range(width * height)]
    
    for i in range(totalMines):
        loop = 0
        while True:
            if loop > 100:
                raise Exception("FATAL - Failed to generate valid mine location")
            loop += 1
            
            #sudoLocation = 0
            sudoLocation = random.randrange(0, width * height - 16 - i)
            
            location = sudoLocation + 2
            
            while output[location] == -1:
                location += 1
            if location >= width - 4 + 2:
                location += 4
                
            while output[location] == -1:
                location += 1
            if location >= 2 * width - 2:
                location += 2
                
            while output[location] == -1:
                location += 1
            if location >= width * height - 2 * width - 6 + 6:
                location += 2
                
            while output[location] == -1:
                location += 1
            if location >= width * height - width - 8 + 6:
                location += 4
            
            while output[location] == -1:
                location += 1
            if output[location] != -1 and location < width * height - 2:
                break
        
        output[location] = -1
    
    for index, value in enumerate(output):
        if value == 0:
            checks = ["" for i in range(8)]
            if index - width >= 0 and index % width != 0:
                checks[0] = index - width - 1
            if index - width >= 0:
                checks[1] = index - width
            if index - width >= 0 and (index + 1) % width != 0:
                checks[2] = index - width + 1
            if index % width != 0:
                checks[3] = index - 1
            if (index + 1) % width != 0:
                checks[4] = index + 1
            if index + width < width * height and index % width != 0:
                checks[5] = index + width - 1
            if index + width < width * height:
                checks[6] = index + width
            if index + width < width * height and (index + 1) % width != 0:
                checks[7] = index + width + 1

            mines = 0
            for i in checks:
                if i != "":
                    if output[i] == -1:
                        mines += 1
            
            output[index] = mines
    
    return output
