import tkinter as tk
import tkinter.font as font
from functools import partial
import random
import graphs
import timeit

colorBG = "#0A186C"
size = 30

# function for all the button for the player inventory
def play(selection):
    global playerSelection, playerButtons
    # makes sure the player has not selected a token before
    if playerSelection == -1:
        playerSelection = selection
        playerButtons[selection].config(bg="white")
    # changes change the selection of the token he previously took
    else:
        playerButtons[playerSelection].config(bg="black")
        playerSelection = selection
        playerButtons[selection].config(bg="white")

# function for all the button in the board
def modifyMatrixHuman(indexX, indexY):
    global matrixButtons, playerSelection, matrix, playerInv, playerButtons, icons, blankIMG, lastMove
    # checks the player has already a token to place
    if playerSelection != -1 and playerInv[playerSelection]!=-1:
        # change the number in the integer matrix and the picture of the tile in board
        matrix[indexX][indexY] = playerInv[playerSelection]
        matrixButtons[indexX][indexY].config(image=icons[playerInv[playerSelection]])
        # removes the token the player placed and blocks the button
        playerInv[playerSelection] = -1
        playerButtons[playerSelection].config(command=None, bg ="purple")
        playerSelection = -1
        # the coordinates of the tile are added for the calculation of points at the end of the turn
        lastMove.append([indexX, indexY])
        newPossibleMoves(indexX, indexY)

# creates the new possible tiles where the ai's can play
def newPossibleMoves(indexX, indexY):
    global matrix, possibleMoves
    # if the tile that where recently placed was is the list, it remove it
    if [indexX, indexY] in possibleMoves:
        possibleMoves.remove([indexX, indexY])
    # checks if the tile bellow is empty and it was not already in the list
    if indexX - 1 != -1:
        if matrix[indexX - 1][indexY] == -1 and [indexX - 1, indexY] not in possibleMoves:
            possibleMoves.append([indexX - 1, indexY])
    # checks if the tile above is empty and it was not already in the list
    if indexX + 1 != size:
        if matrix[indexX + 1][indexY] == -1 and [indexX + 1, indexY] not in possibleMoves:
            possibleMoves.append([indexX + 1, indexY])
    # checks if the tile on the left is empty and it was not already in the list
    if indexY - 1 != -1:
        if matrix[indexX][indexY - 1] == -1 and [indexX, indexY - 1] not in possibleMoves:
            possibleMoves.append([indexX, indexY - 1])
    # checks if the tile on the right is empty and it was not already in the list
    if indexY + 1 != size:
        if matrix[indexX][indexY + 1] == -1 and [indexX, indexY + 1] not in possibleMoves:
            possibleMoves.append([indexX, indexY + 1])
    # checks if tiles are still valid after the addition of this tile
    verifySquare()
    verifyLine()

# based on the tiles the player or ai's decide to take, calculate the points the play deserve
def calculatePointsPlay(tiles):
    # checks if the player or ai's decided to pass the turn because they could not play anything
    if len(tiles) != 0:
        points = 0
        used = []
        i=0
        fullPlay=False
        # checks the tiles in the same line or column the moves were placed
        if len(tiles)!=1 and len(tiles)!=6:
            # checks if there were tile used at the left of the play
            if tiles[0][0] + 1 == tiles[1][0] and tiles[0][1] == tiles[1][1]:
                for i in range(4):
                    if tiles[0][0]+2+i != size and [tiles[0][0]+2+i,tiles[0][1]] not in tiles:
                        if matrix[tiles[0][0]+2+i][tiles[0][1]] == -1:
                            i-=1
                            break
                        used.append([tiles[0][0]+2+i, tiles[0][1]])
                # if the for was not interrupted, it means there are 6 token adjacent and the play is for 12 points
                if i+3==6:
                    points +=12
                    fullPlay = True

            # checks if there were tile used at the right of the play
            if tiles[-1][0] + 1 == tiles[-2][0] and tiles[-1][1] == tiles[-2][1]:
                for i in range(4):
                    if tiles[-1][0]+2+i != -1 and [tiles[-1][0]+2+i, tiles[-1][1]] not in tiles:
                        if matrix[tiles[-1][0]+2+i][tiles[-1][1]] == -1:
                            i-=1
                            break
                        used.append([tiles[-1][0]+2+i, tiles[-1][1]])
                # if the for was not interrupted, it means there are 6 token adjacent and the play is for 12 points
                if i+3==6:
                    points +=12
                    fullPlay = True

            # checks if there were tile used above the play
            if tiles[0][1] + 1 == tiles[1][1] and tiles[0][0] == tiles[1][0]:
                for i in range(4):
                    if tiles[0][1]+2+i != size and [tiles[0][0], tiles[0][1]+2+i] not in tiles:
                        if matrix[tiles[0][0]][tiles[0][1]+2+i] == -1:
                            i-=1
                            break
                        used.append([tiles[0][0], tiles[0][1]+2+i])
                # if the for was not interrupted, it means there are 6 token adjacent and the play is for 12 points
                if i+3==6:
                    points +=12
                    fullPlay = True

            # checks if there were tile used bellow the play
            if tiles[-1][1] + 1 == tiles[-2][1] and tiles[-1][0] == tiles[-2][0]:
                for i in range(4):
                    if tiles[-1][1]+2+i != -1 and [tiles[-1][0], tiles[-1][1]+2+i] not in tiles:
                        if matrix[tiles[-1][0]][tiles[-1][1]+2+i] == -1:
                            i-=1
                            break
                        used.append([tiles[-1][0], tiles[-1][1]+2+i])
                # if the for was not interrupted, it means there are 6 token adjacent and the play is for 12 points
                if i+3==6:
                    points +=12
                    fullPlay = True

            # checks backwards if there were tile used at the left of the play
            if tiles[-1][0] - 1 == tiles[-2][0] and tiles[-1][1] == tiles[-2][1]:
                for i in range(4):
                    if tiles[-1][0]-2-i != size and [tiles[-1][0]-2-i,tiles[-1][1]] not in tiles:
                        if matrix[tiles[-1][0]-2-i][tiles[-1][1]] == -1:
                            i-=1
                            break
                        used.append([tiles[-1][0]-2-i, tiles[-1][1]])
                # if the for was not interrupted, it means there are 6 token adjacent and the play is for 12 points
                if i+3==6:
                    points +=12
                    fullPlay = True

            # checks backwards if there were tile used at the right of the play
            if tiles[0][0] - 1 == tiles[1][0] and tiles[0][1] == tiles[1][1]:
                for i in range(4):
                    if tiles[0][0]-2-i != -1 and [tiles[0][0]-2-i, tiles[0][1]] not in tiles:
                        if matrix[tiles[0][0]-2-i][tiles[0][1]] == -1:
                            i-=1
                            break
                        used.append([tiles[0][0]-2-i, tiles[0][1]])
                # if the for was not interrupted, it means there are 6 token adjacent and the play is for 12 points
                if i+3==6:
                    points +=12
                    fullPlay = True

            # checks if there were tile used above the play
            if tiles[-1][1] - 1 == tiles[-2][1] and tiles[-1][0] == tiles[-2][0]:
                for i in range(4):
                    if tiles[-1][1]-2-i != size and [tiles[-1][0], tiles[-1][1]-2-i] not in tiles:
                        if matrix[tiles[-1][0]][tiles[-1][1]-2-i] == -1:
                            i-=1
                            break
                        used.append([tiles[-1][0], tiles[-1][1]-2-i])
                # if the for was not interrupted, it means there are 6 token adjacent and the play is for 12 points
                if i+3==6:
                    points +=12
                    fullPlay = True

            # checks if there were tile used bellow the play
            if tiles[0][1] - 1 == tiles[1][1] and tiles[0][0] == tiles[1][0]:
                for i in range(4):
                    if tiles[0][1]-2-i != -1 and [tiles[0][0], tiles[0][1]-2-i] not in tiles:
                        if matrix[tiles[0][0]][tiles[0][1]-2-i] == -1:
                            i-=1
                            break
                        used.append([tiles[0][0], tiles[0][1]-2-i])
                # if the for was not interrupted, it means there are 6 token adjacent and the play is for 12 points
                if i+3==6:
                    points +=12
                    fullPlay = True

        # if the play was for 6 token, it deserves 12 points
        if len(tiles) == 6:
            points += 12

        # used means the tiles with tokens that already exist in the column or line were used in the play
        if not fullPlay and len(tiles)!=1:
            points += len(tiles)+len(used)

        # for every tile in the play, it checks the surroundings of them (ignoring the tiles in the same line or column)
        for x in tiles:
            # checks the left of the tile
            if x[0] - 1 != -1:
                if matrix[x[0] - 1][x[1]] != -1 and [x[0]-1, x[1]] not in tiles and [x[0]-1, x[1]] not in used:
                    points += 2
                    # checks how many other tiles were used from that tile and add the corresponding points
                    for i in range(4):
                        if x[0] - 2 - i != -1:
                            if matrix[x[0]-2-i][x[1]] != -1:
                                points += 1
                            else:
                                i -= 1
                                break
                        else:
                            i -= 1
                            break
                    if i == 3:
                        points += 6

            # checks bellow of the tile
            if x[1] - 1 != -1:
                if matrix[x[0]][x[1]-1] != -1  and [x[0], x[1]-1] not in tiles and [x[0], x[1]-1] not in used:
                    points += 2
                    # checks how many other tiles were used from that tile and add the corresponding points
                    for i in range(4):
                        if x[1] - 2 - i != -1:
                            if matrix[x[0]][x[1]-2-i] != -1:
                                points += 1
                            else:
                                i -= 1
                                break
                        else:
                            i -= 1
                            break
                    if i == 3:
                        points += 6

            # checks the right of the tile
            if x[0] + 1 != size:
                if matrix[x[0] + 1][x[1]] != -1 and [x[0]+1, x[1]] not in tiles and [x[0]+1, x[1]] not in used:
                    points += 2
                    # checks how many other tiles were used from that tile and add the corresponding points
                    for i in range(4):
                        if x[0] + 2 + i != size:
                            if matrix[x[0] + 2 + i][x[1]] != -1:
                                points += 1
                            else:
                                i -= 1
                                break
                        else:
                            i -= 1
                            break
                    if i == 3:
                        points += 6

            # checks above the tile
            if x[1] + 1 != size:
                if matrix[x[0]][x[1]+1] != -1 and [x[0], x[1]+1] not in tiles and [x[0], x[1]+1] not in used:
                    points += 2
                    # checks how many other tiles were used from that tile and add the corresponding points
                    for i in range(4):
                        if x[1]+ 2 + i != size:
                            if matrix[x[0]][x[1]+2+i] != -1:
                                points += 1
                            else:
                                i -= 1
                                break
                        else:
                            i -= 1
                            break
                    if i == 3:
                        points += 6
        return points

# function for the end of turn for the player
def endTurn():
    global playerInv, playerButtons, playerSelection, totalTokens, icons, scoreLabel, scores, possibleMoves, easyAITimeLabel, advAITimeLabel, lastMove, aiEasyInv, aiAdvancedInv,numberOfBlankSpacesEasy, numberOfBlankSpacesAdvanced, blankIMG, whiteIMG
    playerSelection = -1
    # replenish the tokens for the player based on the amount he used
    for x in range(6):
        if playerInv[x] == -1:
            randomToken = random.randint(0, len(totalTokens) - 1)
            playerInv[x] = totalTokens[randomToken]
            totalTokens.remove(totalTokens[randomToken])
            playerButtons[x].config(command=partial(play, x), image=icons[playerInv[x]], bg="black")

    # calculates the points for the player
    if len(lastMove) != 0:
        scores[0] += calculatePointsPlay(lastMove)
        scoreLabel[0].config(text="Score: " + str(scores[0]))
        lastMove = []
    temp = possibleMoves.copy()
    # variable for ai execution time graph
    numberOfBlankSpacesEasy.append(len(possibleMoves))

    # the easy ai does its move and the calculation of its points
    startTimer = timeit.default_timer()
    answer = playEasyAI()
    endTimer = timeit.default_timer()

    # if the ai plays, changes the board and refills its inventory
    if type(answer) == list:
        updateTableToken(answer[0], answer[1])
        verifyLine()
        verifySquare()
        print("Score AI EZ: ", scores[1])
        scores[1] += answer[2]
        scoreLabel[1].config(text="Score: " + str(scores[1]))
        updateInv(aiEasyInv, answer[1], aiEasyButtons)
        updateRecentMoves(answer[1], aiEasyButtons)

    aiEasyTime.append(endTimer - startTimer)
    easyAITimeLabel.config(text=str(endTimer - startTimer))

    # variable for ai execution time graph
    numberOfBlankSpacesAdvanced.append(len(possibleMoves))

    # the advanced ai does its move and the calculation of its points
    startTimer = timeit.default_timer()
    answer = playAdvancedAI()
    endTimer = timeit.default_timer()
    if type(answer) == list:
        updateTableToken(answer[0], answer[1])
        verifyLine()
        verifySquare()
        print("Score AI ADV: ", scores[2])
        scores[2] += answer[2]
        scoreLabel[2].config(text="Score: " + str(scores[2]))
        updateInv(aiAdvancedInv, answer[1], aiAdvancedButtons)
        updateRecentMoves(answer[1], aiAdvancedButtons)

    # variable for ai execution time graph
    aiAdvancedTime.append(endTimer - startTimer)
    advAITimeLabel.config(text=str(endTimer - startTimer))

# creates an array of all the different combinations that a given inventory can do
def possibleCombination(inv):
    """ For every superior order of permutation (example: permutation of 3 token or order 3) the algorithm uses the list
        of the inferior order (in the example it would use the list of order 2) to create this permutations, in order to
        simplify the process
        The resultant array always has the form of [order 1, order 2, order 3, order 4, order 5, order 6]
    """
    result = [[], [], [], [], [], []]
    # single token possibilities
    for i in range(6):
        result[0].append(inv[i])

    # double token possibilities
    for i in range(6):
        for j in range(6):
            # checks if all the token are the same color or the same piece, without accepting the same piece
            if inv[i]!=inv[j]:
                if inv[i]//6 == inv[j]//6 or inv[i]%6 == inv[j]%6:
                    if [inv[i], inv[j]] not in result[1]:
                        result[1].append([inv[i], inv[j]])

    # triple, quad, penta and hexa token possibilities
    for i in range(4):
        # checks there were combinations before (example: for triple it needs there were combinations of two)
        if len(result[i+1]) != 0:
            # gets one combination of the previous possibilities
            for pairs in result[i+1]:
                # checks if any piece of the inventory can be placed to form a new combination of that tier
                for z in range(6):
                    if inv[z] not in pairs:
                        validColor = True
                        validType = True
                        for elements in pairs:
                            if elements//6 != inv[z]//6:
                                validColor = False
                            if elements%6 != inv[z]%6 :
                                validType = False
                            if not validColor and not validType:
                                break
                        if (validColor or validType) and pairs+[inv[z]] not in result[i+2]:
                            result[i+2].append(pairs+[inv[z]])
        else:
            break

    return result

# eliminate the blank square that are surrounded by already used tiles above and bellow or left and right
def verifySquare():
    global possibleMoves, matrix
    for i in possibleMoves:
        tileNotDone = True
        # checks if those tiles does not exceed the limits of the board above and down
        if tileNotDone and i[1]+1 != size and i[1]-1 != -1:
            # checks if the tiles are used
            if matrix[i[0]][i[1]+1] != -1 and matrix[i[0]][i[1]-1] != -1:
                # checks if it is still viable that tile (bellow and above are the same type or color)
                if (matrix[i[0]][i[1]+1]//6 != matrix[i[0]][i[1]-1]//6 and matrix[i[0]][i[1]+1]%6 == matrix[i[0]][i[1]-1]%6) or (matrix[i[0]][i[1]+1]%6 != matrix[i[0]][i[1]-1]%6 and matrix[i[0]][i[1]+1]//6 == matrix[i[0]][i[1]-1]//6):
                    continue
                else:
                    possibleMoves.remove(i)
                    tileNotDone = False

        # checks if those tiles does not exceed the limits of the board right and left
        if tileNotDone and i[0]+1 != size and i[0] - 1 != -1:
            # checks if the tiles are used
            if matrix[i[0]+1][i[1]] != -1 and matrix[i[0]-1][i[1]] != -1:
                # checks if it is still viable that tile (right and left are the same type or color)
                if (matrix[i[0] + 1][i[1]] // 6 != matrix[i[0] - 1][i[1]] // 6 and matrix[i[0] + 1][i[1]] % 6 == matrix[i[0] - 1][i[1]] % 6) or (matrix[i[0] + 1][i[1]] % 6 != matrix[i[0] - 1][i[1]] % 6 and matrix[i[0] + 1][i[1]] // 6 == matrix[i[0] - 1][i[1]] // 6):
                    continue
                else:
                    possibleMoves.remove(i)
                    tileNotDone = False

# eliminates the blank square that are at the end of a line or column
def verifyLine():
    global matrix, possibleMoves
    for tile in possibleMoves:
        tileNotDone=True
        # verifies if under that square is a column
        if tileNotDone and tile[0]-6 > -1:
            valid = True
            for j in range(6):
                if matrix[tile[0] - 1 - j][tile[1]]==-1:
                    valid = False
                    break
            if valid:
                possibleMoves.remove(tile)

        # verifies if above that square is a column
        if tileNotDone and tile[0]+6 < size:
            valid = True
            for j in range(6):
                if matrix[tile[0] + 1 + j][tile[1]] == -1:
                    valid = False
                    break
            if valid:
                possibleMoves.remove(tile)

        # verifies if at the left side of that square is a line
        if tileNotDone and tile[1]-6 > -1:
            valid = True
            for j in range(6):
                if matrix[tile[0]][tile[1] - 1 - j] == -1:
                    valid = False
                    break
            if valid:
                possibleMoves.remove(tile)

        # verifies if at the right side of that square is a line
        if tileNotDone and tile[1]+6 < size:
            valid = True
            for j in range(6):
                if matrix[tile[0]][tile[1] + 1 + j] == -1:
                    valid = False
                    break
            if valid:
                possibleMoves.remove(tile)

def playEasyAI():
    global aiEasyInv
    plays = correctPossibleMoves(aiEasyInv)
    maxPlay = []
    maxPlayTokens = []
    maxPlayPoints = 0
    for playNumber in plays:
        moveTemp=[]
        if playNumber[0][0] == playNumber[1][0]:
            if playNumber[0][1] < playNumber[1][1]:
                for y in range(abs(playNumber[0][1] - playNumber[1][1]) + 1):
                    moveTemp += [[playNumber[0][0], playNumber[0][1] + y]]
            else:
                for y in range(abs(playNumber[0][1] - playNumber[1][1]) + 1):
                    moveTemp += [[playNumber[0][0], playNumber[0][1] - y]]
        else:
            if playNumber[0][0] < playNumber[1][0]:
                for x in range(abs(playNumber[0][0] - playNumber[1][0]) + 1):
                    moveTemp += [[playNumber[0][0] + x,  playNumber[0][1]]]
            else:
                for x in range(abs(playNumber[0][0] - playNumber[1][0]) + 1):
                    moveTemp += [[playNumber[0][0] - x,  playNumber[0][1]]]
        points = calculatePointsPlay(moveTemp)
        if points > maxPlayPoints:
            maxPlay = moveTemp
            maxPlayTokens = playNumber[2]
            maxPlayPoints = points
    return [maxPlay, maxPlayTokens, maxPlayPoints]

def correctPossibleMoves(inv):
    global matrix, possibleMoves
    possibilities = possibleCombination(inv)
    sizePlay = 0
    plays = []
    for sizePlay in range(6):
        if len(possibilities[-1 - sizePlay]) != 0:
            break
    while sizePlay!=5:
        for tiles in possibleMoves:
            for possible in possibilities[5-sizePlay]:
                color = False
                if possible[0]//6 == possible[1]//6:
                    color = True

                # check the left of the blank tile
                if tiles[0] - 5 + sizePlay != -1:
                    for i in range(7-sizePlay):
                        if i == 6-sizePlay:
                            if tiles[0]-i != -1:
                                if matrix[tiles[0]-i][tiles[1]] != -1:
                                    i=-1
                                    break
                        else:
                            if matrix[tiles[0] - i][tiles[1]] != -1:
                                i = -1
                                break
                    if i == 6-sizePlay:
                        canPlace = False
                        tilesUsed = 0
                        for j in range(sizePlay+1):
                            if tiles[0] + 1 + j == size:
                                canPlace = True
                                break
                            elif matrix[tiles[0]+1+j][tiles[1]] == -1:
                                canPlace = True
                                break
                            elif j == sizePlay:
                                break
                            elif color:
                                if matrix[tiles[0]+1+j][tiles[1]]//6 != possible[0]//6 or matrix[tiles[0]+1+j][tiles[1]] in possible:
                                    break
                                else:
                                    tilesUsed+=1
                            else:
                                if matrix[tiles[0]+1+j][tiles[1]]%6 != possible[0]%6 or matrix[tiles[0]+1+j][tiles[1]] in possible:
                                    break
                                else:
                                    tilesUsed+=1
                        if canPlace:
                            if [tiles[0]-5+sizePlay, tiles[1]] not in possibleMoves:
                                validColor = True
                                validType = True
                                for token in range(6-sizePlay):
                                    if not (checkColor(possible[token], [tiles[0] - token, tiles[1]], 0, 1) and checkColor(possible[token], [tiles[0] - token, tiles[1]], 0, -1)):
                                        validColor = False
                                    if not (checkType(possible[token], [tiles[0] - token, tiles[1]], 0, 1) and checkType(possible[token], [tiles[0] - token, tiles[1]], 0, -1)):
                                        validType = False
                                if validColor or validType:
                                    plays.append([[tiles[0], tiles[1]], [tiles[0] - 5 + sizePlay, tiles[1]], possible])
                            elif tilesUsed != sizePlay:
                                canPlace = False
                                for j in range(sizePlay-tilesUsed + 1):
                                    if tiles[0] - 5 + sizePlay -1 - j == -1:
                                        canPlace = True
                                        break
                                    elif matrix[tiles[0] - 5 + sizePlay -1 - j][tiles[1]] == -1:
                                        canPlace = True
                                        break
                                    elif j == sizePlay-tilesUsed:
                                        break
                                    elif color:
                                        if matrix[tiles[0] - 5 + sizePlay -1 - j][tiles[1]] // 6 != possible[0] // 6 or matrix[tiles[0] - 5 + sizePlay -1 - j][tiles[1]] in possible:
                                            break
                                    else:
                                        if matrix[tiles[0] - 5 + sizePlay -1 - j][tiles[1]] % 6 != possible[0] % 6 or matrix[tiles[0] - 5 + sizePlay -1 - j][tiles[1]] in possible:
                                            break
                                if canPlace:
                                    validColor = True
                                    validType = True
                                    for token in range(6 - sizePlay):
                                        if not (checkColor(possible[token], [tiles[0] - token, tiles[1]], 0, 1) and checkColor(possible[token], [tiles[0] - token, tiles[1]], 0, -1)):
                                            validColor = False
                                        if not (checkType(possible[token], [tiles[0] - token, tiles[1]], 0, 1) and checkType(possible[token], [tiles[0] - token, tiles[1]], 0, -1)):
                                            validType = False
                                    if validColor or validType:
                                        plays.append([[tiles[0], tiles[1]], [tiles[0] - 5 + sizePlay, tiles[1]], possible])

                # check the right of the blank tile
                if tiles[0] + 5 - sizePlay != size:
                    for i in range(7-sizePlay):
                        if i == 6 - sizePlay:
                            if tiles[0] + i != size:
                                if matrix[tiles[0] + i][tiles[1]] != -1:
                                    i = -1
                                    break
                        else:
                            if matrix[tiles[0] + i][tiles[1]] != -1:
                                i = -1
                                break
                    if i == 6-sizePlay:
                        canPlace = False
                        tilesUsed = 0
                        for j in range(sizePlay+1):
                            if tiles[0] - 1 - j == -1:
                                canPlace = True
                                break
                            elif matrix[tiles[0]-1-j][tiles[1]] == -1:
                                canPlace = True
                                break
                            elif j == sizePlay:
                                break
                            elif color:
                                if matrix[tiles[0]-1-j][tiles[1]]//6 != possible[0]//6 or matrix[tiles[0]-1-j][tiles[1]] in possible:
                                    break
                                else:
                                    tilesUsed+=1
                            else:
                                if matrix[tiles[0]-1-j][tiles[1]]%6 != possible[0]%6 or matrix[tiles[0]-1-j][tiles[1]] in possible:
                                    break
                                else:
                                    tilesUsed+=1
                        if canPlace:
                            if [tiles[0]+5-sizePlay, tiles[1]] not in possibleMoves:
                                validColor = True
                                validType = True
                                for token in range(6-sizePlay):
                                    if not (checkColor(possible[token], [tiles[0] + token, tiles[1]], 0, 1) and checkColor(possible[token], [tiles[0] + token, tiles[1]], 0, -1)):
                                        validColor = False
                                    if not (checkType(possible[token], [tiles[0] + token, tiles[1]], 0, 1) and checkType(possible[token], [tiles[0] + token, tiles[1]], 0, -1)):
                                        validType = False
                                if validColor or validType:
                                    plays.append([[tiles[0], tiles[1]], [tiles[0] + 5 - sizePlay, tiles[1]], possible])
                            elif tilesUsed != sizePlay:
                                canPlace = False
                                for j in range(sizePlay-tilesUsed + 1):
                                    if tiles[0] + 5 - sizePlay + 1 + j == size:
                                        canPlace = True
                                        break
                                    elif matrix[tiles[0] + 5 - sizePlay + 1 + j][tiles[1]] == -1:
                                        canPlace = True
                                        break
                                    elif j == sizePlay-tilesUsed:
                                        break
                                    elif color:
                                        if matrix[tiles[0] + 5 - sizePlay + 1 + j][tiles[1]] // 6 != possible[0] // 6 or matrix[tiles[0] + 5 - sizePlay + 1 + j][tiles[1]] in possible:
                                            break
                                    else:
                                        if matrix[tiles[0] + 5 - sizePlay + 1 + j][tiles[1]] % 6 != possible[0] % 6 or matrix[tiles[0] + 5 - sizePlay + 1 + j][tiles[1]] in possible:
                                            break
                                if canPlace:
                                    validColor = True
                                    validType = True
                                    for token in range(6 - sizePlay):
                                        if not (checkColor(possible[token], [tiles[0] + token, tiles[1]], 0, 1) and checkColor(possible[token], [tiles[0] + token, tiles[1]], 0, -1)):
                                            validColor = False
                                        if not (checkType(possible[token], [tiles[0] + token, tiles[1]], 0, 1) and checkType(possible[token], [tiles[0] + token, tiles[1]], 0, -1)):
                                            validType = False
                                    if validColor or validType:
                                        plays.append([[tiles[0], tiles[1]], [tiles[0] + 5 - sizePlay, tiles[1]], possible])

                # check bellow of the blank tile
                if tiles[1] - 5 + sizePlay != -1:
                    for i in range(7-sizePlay):
                        if i == 6 - sizePlay:
                            if tiles[1] - i != -1:
                                if matrix[tiles[0]][tiles[1]- i] != -1:
                                    i = -1
                                    break
                        else:
                            if matrix[tiles[0]][tiles[1]- i] != -1:
                                i = -1
                                break
                    if i == 6-sizePlay:
                        canPlace = False
                        tilesUsed = 0
                        for j in range(sizePlay+1):
                            if tiles[1] + 1 + j == size:
                                canPlace = True
                                break
                            elif matrix[tiles[0]][tiles[1]+1+j] == -1:
                                canPlace = True
                                break
                            elif j == sizePlay:
                                break
                            elif color:
                                if matrix[tiles[0]][tiles[1]+1+j]//6 != possible[0]//6 or matrix[tiles[0]][tiles[1]+1+j] in possible:
                                    break
                                else:
                                    tilesUsed+=1
                            else:
                                if matrix[tiles[0]][tiles[1]+1+j]%6 != possible[0]%6 or matrix[tiles[0]][tiles[1]+1+j] in possible:
                                    break
                                else:
                                    tilesUsed+=1
                        if canPlace:
                            if [tiles[0], tiles[1]-5+sizePlay] not in possibleMoves:
                                validColor = True
                                validType = True
                                for token in range(6-sizePlay):
                                    if not (checkColor(possible[token], [tiles[0], tiles[1] - token], 1, 0) and checkColor(possible[token], [tiles[0], tiles[1] - token], -1, 0)):
                                        validColor = False
                                    if not (checkType(possible[token], [tiles[0], tiles[1] - token], 1, 0) and checkType(possible[token], [tiles[0] , tiles[1]- token], -1, 0)):
                                        validType = False
                                if validColor or validType:
                                    plays.append([[tiles[0], tiles[1]], [tiles[0], tiles[1] - 5 + sizePlay], possible])
                            elif tilesUsed != sizePlay:
                                canPlace = False
                                for j in range(sizePlay-tilesUsed + 1):
                                    if tiles[1] - 5 + sizePlay -1 - j == -1:
                                        canPlace = True
                                        break
                                    elif matrix[tiles[0]][tiles[1] - 5 + sizePlay -1 - j] == -1:
                                        canPlace = True
                                        break
                                    elif j == sizePlay-tilesUsed:
                                        break
                                    elif color:
                                        if matrix[tiles[0]][tiles[1] - 5 + sizePlay -1 - j] // 6 != possible[0] // 6 or matrix[tiles[0] - 5 + sizePlay -1 - j][tiles[1]] in possible:
                                            break
                                    else:
                                        if matrix[tiles[0]][tiles[1] - 5 + sizePlay -1 - j] % 6 != possible[0] % 6 or matrix[tiles[0] - 5 + sizePlay -1 - j][tiles[1]] in possible:
                                            break
                                if canPlace:
                                    validColor = True
                                    validType = True
                                    for token in range(6 - sizePlay):
                                        if not (checkColor(possible[token], [tiles[0], tiles[1] - token], 1, 0) and checkColor(possible[token], [tiles[0], tiles[1] - token], -1, 0)):
                                            validColor = False
                                        if not (checkType(possible[token], [tiles[0], tiles[1] - token], 1, 0) and checkType(possible[token], [tiles[0], tiles[1]- token], -1, 0)):
                                            validType = False
                                    if validColor or validType:
                                        plays.append([[tiles[0], tiles[1]], [tiles[0], tiles[1] - 5 + sizePlay], possible])

                # check above of the blank tile
                if tiles[1] + 5 - sizePlay != size:
                    for i in range(7-sizePlay):
                        if i == 6 - sizePlay:
                            if tiles[1] + i != size:
                                if matrix[tiles[0]][tiles[1] + i] != -1:
                                    i = -1
                                    break
                        else:
                            if matrix[tiles[0]][tiles[1] + i] != -1:
                                i = -1
                                break
                    if i == 6 - sizePlay:
                        canPlace = False
                        tilesUsed = 0
                        for j in range(sizePlay+1):
                            if tiles[1] - 1 - j == -1:
                                canPlace = True
                                break
                            elif matrix[tiles[0]][tiles[1]-1-j] == -1:
                                canPlace = True
                                break
                            elif j == sizePlay:
                                break
                            elif color:
                                if matrix[tiles[0]][tiles[1]-1-j]//6 != possible[0]//6 or matrix[tiles[0]][tiles[1]-1-j] in possible:
                                    break
                                else:
                                    tilesUsed+=1
                            else:
                                if matrix[tiles[0]][tiles[1]-1-j]%6 != possible[0]%6 or matrix[tiles[0]][tiles[1]-1-j] in possible:
                                    break
                                else:
                                    tilesUsed+=1
                        if canPlace:
                            if [tiles[0], tiles[1]+5-sizePlay] not in possibleMoves:
                                validColor = True
                                validType = True
                                for token in range(6-sizePlay):
                                    if not (checkColor(possible[token], [tiles[0], tiles[1] + token], 1, 0) and checkColor(possible[token], [tiles[0] , tiles[1]+ token], -1, 0)):
                                        validColor = False
                                    if not (checkType(possible[token], [tiles[0], tiles[1]+ token], 1, 0) and checkType(possible[token], [tiles[0] , tiles[1]+ token], -1, 0)):
                                        validType = False
                                if validColor or validType:
                                    plays.append([[tiles[0], tiles[1]], [tiles[0], tiles[1] + 5 - sizePlay], possible])
                            elif tilesUsed != sizePlay:
                                canPlace = False
                                for j in range(sizePlay-tilesUsed + 1):
                                    if tiles[1] + 5 - sizePlay + 1 + j == size:
                                        canPlace = True
                                        break
                                    elif matrix[tiles[0]][tiles[1] + 5 - sizePlay + 1 + j] == -1:
                                        canPlace = True
                                        break
                                    elif j == sizePlay-tilesUsed:
                                        break
                                    elif color:
                                        if matrix[tiles[0]][tiles[1] + 5 - sizePlay + 1 + j] // 6 != possible[0] // 6 or matrix[tiles[0]][tiles[1] + 5 - sizePlay + 1 + j] in possible:
                                            break
                                    else:
                                        if matrix[tiles[0]][tiles[1] + 5 - sizePlay + 1 + j] % 6 != possible[0] % 6 or matrix[tiles[0]][tiles[1] + 5 - sizePlay + 1 + j] in possible:
                                            break
                                if canPlace:
                                    validColor = True
                                    validType = True
                                    for token in range(6 - sizePlay):
                                        if not (checkColor(possible[token], [tiles[0], tiles[1] + token], 1, 0) and checkColor(possible[token], [tiles[0], tiles[1] + token], -1, 0)):
                                            validColor = False
                                        if not (checkType(possible[token], [tiles[0] , tiles[1]+ token], 1, 0) and checkType(possible[token], [tiles[0], tiles[1] + token], -1, 0)):
                                            validType = False
                                    if validColor or validType:
                                        plays.append([[tiles[0], tiles[1]], [tiles[0], tiles[1] + 5 - sizePlay], possible])
        sizePlay+=1

    for tiles in possibleMoves:
            for possible in possibilities[0]:
                if checkColor(possible, [tiles[0], tiles[1]], 1, 0) and checkColor(possible, [tiles[0], tiles[1]], -1, 0) and checkColor(possible, [tiles[0], tiles[1]], 0, 1) and checkColor(possible, [tiles[0], tiles[1]], 0, -1):
                    plays.append([[tiles[0], tiles[1]], [tiles[0], tiles[1]], possible])
                elif checkType(possible, [tiles[0], tiles[1]], 1, 0) and checkType(possible, [tiles[0], tiles[1]], -1, 0) and checkType(possible, [tiles[0], tiles[1]], 0, 1) and checkType(possible, [tiles[0], tiles[1]], 0, -1):
                   plays.append([[tiles[0], tiles[1]], [tiles[0], tiles[1]], possible])

    return plays

def playAdvancedAI():
    global matrix,aiAdvancedInv;
    plays = correctPossibleMoves(aiAdvancedInv)
    temp = plays.copy()
    for move in plays:
        tiles1 = 0
        tiles2 = 1
        tiles3 = 1
        if move[0][0] == move[1][0] and move[0][1] == move[1][1]:
            tiles1+=1
            for a in range(1,6):
                if size > move[0][1]+a and matrix[move[0][0]][move[0][1]+a] != -1:
                    tiles1 += 1
                else:
                    break
            if move in temp and tiles1 == 5:
                temp.remove(move)
            tiles1 = 1
            for b in range(1,6):
                if move[0][1]-b > -1 and matrix[move[0][0]][move[0][1]-b] != -1:
                    tiles1 += 1
                else:
                    break
            if move in temp and tiles1 == 5:
                temp.remove(move)
            tiles1 = 1
            for c in range(1,6):
                if size > move[0][0]+c and matrix[move[0][0]+c][move[0][1]] != -1:
                    tiles1 += 1
                else:
                    break
            if move in temp and tiles1 == 5:
                temp.remove(move)
            tiles1 = 1
            for d in range(1,6):
                if move[0][0]-d > -1 and matrix[move[0][0]-d][move[0][1]] != -1:
                    tiles1 += 1
                else:
                    break
            if move in temp and tiles1 == 5:
                temp.remove(move)
        #---------------------------------------------------------------------------#
        if move[0][0] == move[1][0]:
            # check if the left row it's 5 pts
            if move[0][1] > move[1][1]:
                tiles1 += abs(move[0][1])-abs(move[1][1]) + 1
                for x in range(1,6-tiles1):
                    if move[0][1] + x < size and matrix[move[0][0]][abs(move[0][1]) + x] != -1:
                        tiles1 += 1
                if move in temp and tiles1 == 5:
                    temp.remove(move)
                count = abs(move[1][1])
                while abs(move[0][1]) >= count:
                    for x in range(6):
                        if move[0][0]+x < size and matrix[move[0][0]+x][count] != -1:
                            tiles2 += 1
                        if move[0][0]+x > -1 and matrix[move[0][0]-x][count] != -1:
                            tiles3 += 1
                    count += 1
                    if move in temp and (tiles2 == 5 or tiles3 == 5):
                        temp.remove(move)
                        break
                    tiles2 = 1
                    tiles3 = 1
            else:
                # check if the right row it's 5 pts
                tiles1 += abs(move[1][1])-abs(move[0][1]) + 1
                for y in range(1,6-tiles1):
                    if move[1][1] - y > -1 and matrix[move[0][0]][abs(move[1][1]) - y] != -1:
                        tiles1 += 1
                if move in temp and tiles1 == 5:
                    temp.remove(move)
                count = abs(move[0][1])
                while abs(move[1][1]) >= count:
                    for x in range(6):
                        if move[0][0] + x < size and matrix[move[0][0] + x][count] != -1:
                            tiles3 += 1
                        if move[0][0] - x > -1 and matrix[move[0][0] - x][count] != -1:
                            tiles3 += 1
                    if move in temp and (tiles2 == 5 or tiles3 == 5):
                        temp.remove(move)
                        break
                    count += 1
                    tiles2 = 1
                    tiles3 = 1
        else:
            # check if the upper column it's 5 pts
            if move[0][0] > move[1][0]:
                tiles1 += abs(move[0][0])-abs(move[1][0]) + 1
                for x in range(1,6-tiles1):
                    if move[1][0]+x < size and matrix[move[1][0]+x][abs(move[0][1])] != -1:
                        tiles1 += 1
                if move in temp and tiles1 == 5:
                    temp.remove(move)
                count = abs(move[1][0])
                while abs(move[0][0]) >= count:
                    for x in range(6):
                        if move[0][1] + x < size and matrix[count][move[0][1] + x] != -1:
                            tiles2 += 1
                        if move[0][1] - x > -1 and matrix[count][move[0][1] - x]  != -1:
                            tiles3 += 1
                    count += 1
                    if move in temp and (tiles2 == 5 or tiles3 ==5):
                        temp.remove(move)
                        break
                    tiles2 = 1
                    tiles3 = 1
            else:
                # check if the down column it's 5 pts
                tiles1 += abs(move[1][0]) - abs(move[0][0]) + 1
                for y in range(1,6-tiles1):
                    if move[0][0]-y > -1 and matrix[move[0][0]-y][abs(move[0][1])] != -1:
                        tiles1 += 1
                if move in temp and tiles1 == 5:
                    temp.remove(move)
                count = abs(move[0][0])
                while abs(move[1][0]) >= count:
                    for x in range(6):
                        if move[0][1] + x < size and matrix[count][move[0][1] + x] != -1:
                            tiles2 += 1
                        if move[0][1] - x > -1 and matrix[count][move[0][1] - x] != -1:
                            tiles3 += 1
                    count += 1
                    if move in temp and (tiles2 == 5 or tiles3 ==5):
                        temp.remove(move)
                        break
                    tiles2 = 1
                    tiles3 = 1
    # ----------------------------------------------------------------------------#
    maxPlay = []
    maxPlayTokens = []
    maxPlayPoints = 0
    for playNumber in temp:
        moveTemp = []
        if playNumber[0][0] == playNumber[1][0]:
            if playNumber[0][1] < playNumber[1][1]:
                for y in range(abs(playNumber[0][1] - playNumber[1][1]) + 1):
                        moveTemp += [[playNumber[0][0], playNumber[0][1] + y]]
            else:
                for y in range(abs(playNumber[0][1] - playNumber[1][1]) + 1):
                    moveTemp += [[playNumber[0][0], playNumber[0][1] - y]]
        else:
            if playNumber[0][0] < playNumber[1][0]:
                for x in range(abs(playNumber[0][0] - playNumber[1][0]) + 1):
                    moveTemp += [[playNumber[0][0] + x, playNumber[0][1]]]
            else:
                for x in range(abs(playNumber[0][0] - playNumber[1][0]) + 1):
                    moveTemp += [[playNumber[0][0] - x, playNumber[0][1]]]
        points = calculatePointsPlay(moveTemp)
        if points > maxPlayPoints:
            maxPlay = moveTemp
            maxPlayTokens = playNumber[2]
            maxPlayPoints = points
    return [maxPlay, maxPlayTokens, maxPlayPoints]

def checkColor(token, tile, x, y):
    global matrix
    for n in range(6):
        if x>0:
            if tile[0] + x + n != size:
                if matrix[tile[0]+ x + n][tile[1]] == -1:
                    return True
                elif n == 5:
                    return False
                elif matrix[tile[0]+ x + n][tile[1]]//6 != token//6:
                    return False
                elif matrix[tile[0]+ x + n][tile[1]] == token:
                    return False
            else:
                return True
        if x<0:
            if tile[0] + x - n != -1:
                if matrix[tile[0] + x - n][tile[1]] == -1:
                    return True
                elif n == 5:
                    return False
                elif matrix[tile[0] + x - n][tile[1]]//6 != token//6:
                    return False
                elif matrix[tile[0] + x - n][tile[1]] == token:
                    return False
            else:
                return True
        if y>0:
            if tile[1] + y + n != size:
                if matrix[tile[0]][tile[1] + y + n] == -1:
                    return True
                elif n == 5:
                    return False
                elif matrix[tile[0]][tile[1]+y+n]//6 != token//6:
                    return False
                elif matrix[tile[0]][tile[1]+y+n] == token:
                    return False
            else:
                return True
        if y<0:
            if tile[1] + y - n != -1:
                if matrix[tile[0]][tile[1] + y - n] == -1:
                    return True
                elif n == 5:
                    return False
                elif matrix[tile[0]][tile[1] + y-n]//6 != token//6:
                    return False
                elif matrix[tile[0]][tile[1] + y-n] == token:
                    return False
            else:
                return True

def checkType(token, tile, x, y):
    global matrix
    for n in range(6):
        if x > 0:
            if tile[0] + x + n != size:
                if matrix[tile[0] + x + n][tile[1]] == -1:
                    return True
                elif n == 5:
                    return False
                elif matrix[tile[0] + x + n][tile[1]] % 6 != token % 6:
                    return False
                elif matrix[tile[0] + x + n][tile[1]] == token:
                    return False
            else:
                return True
        if x < 0:
            if tile[0] + x - n != -1:
                if matrix[tile[0] + x - n][tile[1]] == -1:
                    return True
                elif n == 5:
                    return False
                elif matrix[tile[0] + x - n][tile[1]] % 6 != token % 6:
                    return False
                elif matrix[tile[0] + x - n][tile[1]] == token:
                    return False
            else:
                return True
        if y > 0:
            if tile[1] + y + n != size:
                if matrix[tile[0]][tile[1] + y + n] == -1 and n == 0:
                    return True
                elif n == 5:
                    return False
                elif matrix[tile[0]][tile[1] + y + n] % 6 != token % 6:
                    return False
                elif matrix[tile[0]][tile[1] + y + n] == token:
                    return False
            else:
                return True
        if y < 0:
            if tile[1] + y - n != -1:
                if matrix[tile[0]][tile[1] + y - n] == -1 and n == 0:
                    return True
                elif n == 5:
                    return False
                elif matrix[tile[0]][tile[1] + y - n] % 6 != token % 6:
                    return False
                elif matrix[tile[0]][tile[1] + y - n] == token:
                    return False
            else:
                return True
    return True

def updateInv(inv, tokens, invButtons):
    global totalTokens
    if type(tokens) == int:
        inv.remove(tokens)
        change = random.randint(0, len(totalTokens)-1)
        inv.append(totalTokens[change])
        totalTokens.remove(totalTokens[change])
    else:
        for x in range (len(tokens)):
            if tokens[x] in inv:
                inv.remove(tokens[x])
        while len(inv) <= 6:
            change = random.randint(0,len(totalTokens)-1)
            inv.append(totalTokens[change])
            totalTokens.remove(totalTokens[change])
    for k in range(6):
        invButtons[k].config(image = icons[inv[k]])

def updateTableToken(lisTile,tokens):
    global icons, matrixButtons, matrix
    if len(lisTile) == 1:
        matrixButtons[lisTile[0][0]][lisTile[0][1]].config(image=icons[tokens])
        matrix[lisTile[0][0]][lisTile[0][1]] = tokens
        newPossibleMoves(lisTile[0][0], lisTile[0][1])
    else:
        for i in range(len(lisTile)):
            matrixButtons[lisTile[i][0]][lisTile[i][1]].config(image=icons[tokens[i]])
            matrix[lisTile[i][0]][lisTile[i][1]] = tokens[i]
            newPossibleMoves(lisTile[i][0], lisTile[i][1])

def updateRecentMoves(tokens, invButtons):
    global blankIMG
    if type(tokens) == int:
        invButtons[6].config(image=icons[tokens])
        for x in range(5):
            invButtons[x + 7].config(image=blankIMG)
    else:
        for i in range(6):
            if i < len(tokens):
                invButtons[i + 6].config(image=icons[tokens[i]])
            else:
                invButtons[i + 6].config(image=blankIMG)
# game board variables
totalTokens = []
icons = []
blankIMG = 0
whiteIMG = 0
matrixButtons = []
matrix = []

# player variables
playerButtons = []
playerInv=[]
playerSelection = -1

# ai easy variables
aiEasyInv = []
aiEasyButtons = []
easyAITimeLabel = 0

# advanced ai variables
aiAdvancedInv = []
aiAdvancedButtons = []
advAITimeLabel = 0

# calculation variables
possibleMoves = []
lastMove = []

# scores variables
scores = [0, 0, 0]
scoreLabel = []

# graph variables
aiEasyTime = []
aiAdvancedTime = []
numberOfBlankSpacesEasy = []
numberOfBlankSpacesAdvanced = []

#interface
def start():
    global matrix, matrixButtons, playerButtons, playerInv, aiEasyInv, aiAdvancedInv, icons, totalTokens, aiEasyInv, aiAdvancedInv, blankIMG, easyAITimeLabel, advAITimeLabel, whiteIMG

    screen = tk.Tk()
    screen.title("Qwirkle :D")
    screen.geometry(str(290+25*size) + "x" + str(70+25*size))

    screen.resizable(False, False)
    screen.config(bg=colorBG)

    # Tokens

    number = 0
    for color in ['_azul.png', '_Celeste.png', '_morado.png', '_Naranja.png', '_Rojo.png', '_Verde.png']:
        for token in range(6):
            icons.append(tk.PhotoImage(file='Imagenes/token' + str(token + 1) + color))
    for color in range(6):
        for token in range(6):
            for repeat in range(3):
                totalTokens.append(number + token)
        number += 6

    # Human inventory
    for i in range(6):
        randomToken = random.randint(0, len(totalTokens) - 1)
        playerInv.append(totalTokens[randomToken])
        totalTokens.remove(totalTokens[randomToken])

    # AI Easy inventory
    for i in range(6):
        randomToken = random.randint(0, len(totalTokens) - 1)
        aiEasyInv.append(totalTokens[randomToken])
        totalTokens.remove(totalTokens[randomToken])

    # AI Advanced inventory
    for i in range(6):
        randomToken = random.randint(0, len(totalTokens) - 1)
        aiAdvancedInv.append(totalTokens[randomToken])
        totalTokens.remove(totalTokens[randomToken])

    # Defines board buttons and labels
    fontTitle = font.Font(size=25)
    boardLabel = tk.Label(screen, text="Tablero", bg=colorBG, fg='#ffffff', font= fontTitle)
    boardLabel.place(x=25*(size/2-2), y=10)

    blankIMG = tk.PhotoImage(file='Imagenes/blank.png')
    whiteIMG = tk.PhotoImage(file='Imagenes/white.png')
    for i in range(size):
        matrixButtons += [[]]
        matrix += [[]]
        for j in range(size):
            matrixButtons[i].append(tk.Button(screen, bg="black", height=20, width=20,image=blankIMG, command=partial(modifyMatrixHuman, i, j)))
            matrixButtons[i][j].place(x = 10+25*i, y = 50+25*j)
            matrix[i].append(-1)

    #Player buttons and tokens
    fontInfo = font.Font(size=12)
    playerLabel = tk.Label(screen, text="Sus fichas", bg=colorBG, fg='#ffffff', font = fontInfo)
    playerLabel.place(x=110+25*size, y=50)
    scoreLabel.append(tk.Label(screen, text="Score: 0", bg=colorBG, fg='#ffffff', font=fontInfo))
    scoreLabel[0].place(x=120 + 25 * size, y=110)
    playerEndTurnButton = tk.Button(screen, command = endTurn, text="Terminar Turno")
    playerEndTurnButton.place(x=105+25*size, y=140)

    for k in range (6):
        playerButtons.append(tk.Button(screen,bg="black", height=20, width=20,command=partial(play, k), image=icons[playerInv[k]]))
        playerButtons[k].place(x=75+25*size+25*k, y=80)

    #Data info for AIs
    easyAILabel = tk.Label(screen, text="IA facil", bg=colorBG, fg='#ffffff', font=fontInfo)
    easyAILabel.place(x=125+25*size, y=180)
    easyAILabel2 = tk.Label(screen, text="Ultimo tiempo de ejecucion: ", bg=colorBG, fg='#ffffff', font=fontInfo)
    easyAILabel2.place(x=55+25*size, y=200)
    easyAITimeLabel = tk.Label(screen, bg=colorBG, fg='#ffffff', font=fontInfo, text = "0")
    easyAITimeLabel.place(x=55+25*size, y=220)
    scoreLabel.append(tk.Label(screen, text="Score: 0", bg=colorBG, fg='#ffffff', font=fontInfo))
    scoreLabel[1].place(x=120 + 25 * size, y=240)
    for k in range(6):
        aiEasyButtons.append(tk.Button(screen, bg="black", height=20, width=20, image=icons[aiEasyInv[k]]))
        aiEasyButtons[k].place(x=75 + 25 * size + 25 * k, y=265)
    easyAILabel3 = tk.Label(screen, text="Ultima jugada: ", bg=colorBG, fg='#ffffff', font=fontInfo)
    easyAILabel3.place(x=100 + 25 * size, y=295)
    for k in range(6):
        aiEasyButtons.append(tk.Button(screen, bg="black", height=20, width=20, image=blankIMG))
        aiEasyButtons[k+6].place(x=75 + 25 * size + 25 * k, y=325)
    easyAIGraphButton = tk.Button(screen, text="Mostrar Grafico", command = partial(graphs.graph, "IA facil tiempo de ejecucion", aiEasyTime,numberOfBlankSpacesEasy))
    easyAIGraphButton.place(x=105+25*size, y=360) #

    advAILabel = tk.Label(screen, text="IA avanzada", bg=colorBG, fg='#ffffff', font=fontInfo)
    advAILabel.place(x=105+25*size, y=405)
    advAILabel2 = tk.Label(screen, text="Ultimo tiempo de ejecucion: ", bg=colorBG, fg='#ffffff', font=fontInfo)
    advAILabel2.place(x=55+25*size, y=425)
    advAITimeLabel = tk.Label(screen, bg=colorBG, fg='#ffffff', font=fontInfo, text= "0")
    advAITimeLabel.place(x=55+25*size, y=455)
    scoreLabel.append(tk.Label(screen, text="Score: 0", bg=colorBG, fg='#ffffff', font=fontInfo))
    scoreLabel[2].place(x=120 + 25 * size, y=475)
    for k in range(6):
        aiAdvancedButtons.append(tk.Button(screen, bg="black", height=20, width=20, image=icons[aiAdvancedInv[k]]))
        aiAdvancedButtons[k].place(x=75 + 25 * size + 25 * k, y=500)
    advAILabel3 = tk.Label(screen, text="Ultima jugada: ", bg=colorBG, fg='#ffffff', font=fontInfo)
    advAILabel3.place(x=100 + 25 * size, y=530)
    for k in range(6):
        aiAdvancedButtons.append(tk.Button(screen, bg="black", height=20, width=20, image=blankIMG))
        aiAdvancedButtons[k + 6].place(x=75 + 25 * size + 25 * k, y=555)
    advAIGraphButton = tk.Button(screen, text="Mostrar Grafico", command = partial(graphs.graph, "IA avanzada tiempo de ejecucion", aiAdvancedTime, numberOfBlankSpacesAdvanced))
    advAIGraphButton.place(x=105+25*size, y=590)

    bothAIGraphButton = tk.Button(screen, text="Mostrar Grafico de ambos", command = partial(graphs.graphDouble, "IA facil vs IA dificil tiempo de ejecucion",aiEasyTime,numberOfBlankSpacesEasy, aiAdvancedTime, numberOfBlankSpacesAdvanced))
    bothAIGraphButton.place(x=75+25*size, y=625)

    screen.mainloop()

