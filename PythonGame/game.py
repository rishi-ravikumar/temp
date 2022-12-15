# Resolution: 1920x1080
# Sources:
# Red Bird
# giphy.com/gifs/playkids-children-junior-junioronthejob-3ornjQQZhry6bF31CM
# Horse
# giphy.com/gifs/animation-animal-xUn3CtIpFvnSKaTVcc

# Note: comments about a function come before the function

from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import time
import os
import random
import sys

root = Tk()
root.geometry("1920x1080")
root.attributes('-fullscreen', True)
root.title("EquiKnocks")
frameCnt = 11
frames = [PhotoImage(file="giphy7.gif", format='gif -index %i' % (i))
          for i in range(frameCnt)]
frames2 = [PhotoImage(file="giphy4.gif", format='gif -index %i' % (i))
           for i in range(frameCnt)]
framesHold = [PhotoImage(file="giphy7.gif", format='gif -index %i' % (i))
              for i in range(frameCnt)]
jump_image_visible = PhotoImage(file='frame_04.gif')
jump_image_invisible = PhotoImage(
    file='frame_04_delay-0.04s.gif')
bg = PhotoImage(file='bg8.gif')
cloud = PhotoImage(file='cloud.gif')
birdCrash = PhotoImage(file='frame_53_delay-0.03s.gif')
frameCnt2 = 15
birdImgFrames = [PhotoImage(
    file='bird5.gif', format='gif -index %i' % (i)) for i in range(frameCnt2)]
bossKeyImg = PhotoImage(file='bossKey.gif')
horseJumpCount = 0
horseCrashCount = 0
pauseStatus = False
gameOver = False
barrCount = 0
startTime = 0
invisibilityStartTime = 0
score = 0
birdMove = False
upperBoundForBird = 10
lowerBoundForBird = 5
barInvisibility = False
barInvisibilityTimer = 0
barInvisibilityUsageCount = 0
decreaseBarrHeightEnable = False
increaseBarrHeightEnable = False
decreaseBarrHeightEnableTimer = 0
increaseBarrHeightEnableTimer = 0
bossKeyEnable = False
gameOverEnable = False
pauseEnable = False
mmEnable = False
name = ''
jump_binding = "Space"
pause_binding = "Return"
invisibility_binding = "I"
leaderboardEnable = False
helpPageEnable = False
reconfigEnable = False

# pause function sets the pauseStatus variable
# when the event associated with the function is called


def pause(event):
    global mmEnable
    global gameOver
    global leaderboardEnable
    global helpPageEnable
    global reconfigEnable
    if not mmEnable and not gameOver and not leaderboardEnable and\
       not helpPageEnable and not reconfigEnable:
        global pauseStatus
        if not pauseStatus:
            pauseStatus = not pauseStatus

# space function makes the horse jump when the
# associated event takes place (default: Space)


def space(event):
    global pauseStatus
    global jump_image_visible
    global jump_image_invisible
    global invisibilityStartTime
    global leaderboardEnable
    global helpPageEnable
    global reconfigEnable
    if not pauseStatus and not mmEnable and not leaderboardEnable and\
       not helpPageEnable and not reconfigEnable and not gameOver:
        global horseJumpCount
        jump_image = jump_image_visible
        if invisibilityStartTime != 0 and\
           round(time.time() * 1000) - invisibilityStartTime < 1000:
            jump_image = jump_image_invisible
        if horseJumpCount < 130:
            canvas.coords(horseImg, 0, canvas.coords(horseImg)[1] - 2.5)
            canvas.itemconfigure(horseImg, image=jump_image)
            horseJumpCount += 1
            root.after(3, space, None)
        elif horseJumpCount >= 130 and horseJumpCount <= 259:
            horseJumpCount += 1
            canvas.coords(horseImg, 0, canvas.coords(horseImg)[1] + 2.5)
            canvas.itemconfigure(horseImg, image=jump_image)
            root.after(3, space, None)
        else:
            horseJumpCount = 0

# check_contact checks if the barrier and horse are in contact


def check_contact():
    global horseCrashCount
    global gameOver
    global barInvisibility
    global barInvisibilityTimer
    global pauseStatus
    barr_coords = canvas.coords(barr)
    overlap = canvas.find_overlapping(
        barr_coords[0], barr_coords[1], barr_coords[2], barr_coords[3])
    if (round(time.time() * 1000) - barInvisibilityTimer >= 10000) and\
       barInvisibilityTimer != 0:
        barInvisibilityTimer = 0
        barInvisibility = False
    if (overlap == (1, 7, 8, 11) or overlap == (1, 6, 7, 8, 11)) and\
       not barInvisibility:
        horseCrashCount += 1
    else:
        horseCrashCount = 0
    if horseCrashCount >= 2:
        gameOver = True
        if canvas.coords(horseImg)[1] != 400:
            canvas.itemconfigure(horseImg, image=jump_image_visible)

# moves barriers and clouds during gameplay


def move_barrier():
    global barrCount
    global score
    moveDistance = 50
    if barrCount < 10:
        moveDistance = 50
    elif barrCount < 20:
        moveDistance = 60
    elif barrCount < 40:
        moveDistance = 70
    elif barrCount >= 40:
        moveDistance = 75

    init_barr_coords = canvas.coords(barr)
    canvas.coords(barr, init_barr_coords[0] - moveDistance,
                  init_barr_coords[1],
                  init_barr_coords[2] - moveDistance, init_barr_coords[3])

    canvas.move(cld1, -5, 0)
    canvas.move(cld2, -5, 0)
    canvas.move(cld3, -5, 0)
    canvas.move(cld4, -5, 0)

    global increaseBarrHeightEnable
    global increaseBarrHeightEnableTimer
    global decreaseBarrHeightEnable
    global decreaseBarrHeightEnableTimer
    if increaseBarrHeightEnable and\
       round(time.time() * 1000) - increaseBarrHeightEnableTimer < 10000 and\
       increaseBarrHeightEnableTimer != 0:
        heightBarr = 420
    elif increaseBarrHeightEnable and\
            round(time.time() * 1000)\
            - increaseBarrHeightEnableTimer >= 10000 and\
            increaseBarrHeightEnableTimer != 0:
        increaseBarrHeightEnable = False
        increaseBarrHeightEnableBarrCount = 0
    elif decreaseBarrHeightEnable and\
            round(time.time() * 1000) - decreaseBarrHeightEnableTimer < 10000\
            and\
            decreaseBarrHeightEnableTimer != 0:
        heightBarr = 510
    elif decreaseBarrHeightEnable and\
            round(time.time() * 1000)-decreaseBarrHeightEnableTimer >= 10000\
            and\
            decreaseBarrHeightEnableTimer != 0:
        decreaseBarrHeightEnable = False
        decreaseBarrHeightEnableTimer = 0
    elif barrCount < 10:
        heightBarr = random.randint(480, 500)
    elif barrCount < 20:
        heightBarr = random.randint(470, 480)
    elif barrCount < 30:
        heightBarr = random.randint(450, 470)
    elif barrCount < 45:
        heightBarr = random.randint(430, 450)
    else:
        heightBarr = random.randint(420, 430)

    if init_barr_coords[2] <= 0:
        barrCount += 1
        canvas.coords(barr, 1920, heightBarr, 1950, 648)
        score += 10
        canvas.itemconfigure(scoreText, text=name + "'s score: " + str(score))

    global birdMove
    global upperBoundForBird
    global lowerBoundForBird
    if (barrCount > lowerBoundForBird and barrCount <= upperBoundForBird) or\
       (canvas.coords(bird)[0] >= 0 and
       canvas.coords(bird)[0] < 1920):
        birdMove = True
        if barrCount == upperBoundForBird:
            upperBoundForBird += 10
            lowerBoundForBird += 10
    else:
        birdMove = False

    if canvas.coords(cld1)[0] < -300:
        canvas.coords(cld1, 1920, 170)

    if canvas.coords(cld2)[0] < -300:
        canvas.coords(cld2, 1920, 250)

    if canvas.coords(cld3)[0] < -300:
        canvas.coords(cld3, 1920, 50)

    if canvas.coords(cld4)[0] < -300:
        canvas.coords(cld4, 1920, 300)

    check_contact()

# makes the horse invisible to the bird when the
# associated event takes place (default: Return)


def birdInvisibility(event):
    global leaderboardEnable
    global helpPageEnable
    global reconfigEnable
    if not leaderboardEnable and not helpPageEnable and not reconfigEnable:
        global mmEnable
        if not mmEnable:
            global gameOver
            if not gameOver:
                global frames
                global frames2
                global invisibilityStartTime
                frames = frames2
                invisibilityStartTime = round(time.time() * 1000)

# moves the bird


def move_bird(ind):
    frame = birdImgFrames[ind]
    ind += 1
    if ind == frameCnt2:
        ind = 0
    canvas.itemconfigure(bird, image=frame)

    if barrCount > 35:
        birdSpeed = 80
    else:
        birdSpeed = 70

    for i in range(0, birdSpeed):
        canvas.move(bird, -1, 0)
        canvas.move(followBird, -1, 0)

    global score

    if canvas.coords(bird)[0] < 0:
        canvas.coords(bird, 1920, 450)
        canvas.coords(followBird, 1930, 470, 1930, 470)
        score += 5
        canvas.itemconfigure(scoreText, text=name + "'s score: " + str(score))

    global invisibilityStartTime
    global gameOver

    bird_coords = canvas.coords(followBird)
    if canvas.find_overlapping(bird_coords[0],
       bird_coords[1], bird_coords[2], bird_coords[3]) == (1, 7, 9, 10):
        if invisibilityStartTime != 0 and\
           round(time.time() * 1000) - invisibilityStartTime <= 2000:
            pass
        else:
            canvas.itemconfigure(bird, image=birdCrash)
            gameOver = True

# continues game when the Continue button is clicked in the paused state


def continueGame(varSet, continueGameButton,
                 dontSaveExitButton, saveExitButton):
    global pauseStatus
    global horseJumpCount
    varSet.set(1)
    pauseStatus = not pauseStatus
    continueGameButton.destroy()
    dontSaveExitButton.destroy()
    saveExitButton.destroy()
    if canvas.coords(horseImg)[1] != 400:
        space(None)

# exits without saving the game when the corresponding
# button is clicked in the pause state


def dontSaveExit(varSet, continueGameButton,
                 dontSaveExitButton, saveExitButton):
    varSet.set(1)
    continueGameButton.destroy()
    dontSaveExitButton.destroy()
    saveExitButton.destroy()

    event_file = open("keybinding.txt", "w")
    event_file.write(jump_binding + "\n")
    event_file.write(pause_binding + "\n")
    event_file.write(invisibility_binding + "\n")
    event_file.close()

    python = sys.executable
    os.execl(python, python, * sys.argv)

# exits and saves the game when the corresponding
# button is clicked in the pause state


def saveExit(varSet, continueGameButton, dontSaveExitButton, saveExitButton):
    global score
    global barrCount
    global birdMove
    global upperBoundForBird
    global lowerBoundForBird
    global name

    varSet.set(1)
    continueGameButton.destroy()
    dontSaveExitButton.destroy()
    saveExitButton.destroy()

    saveFile = open("savedGame.txt", "w")
    saveFile.write(name+"\n")
    saveFile.write(str(score) + "\n")
    saveFile.write(str(barrCount) + "\n")
    saveFile.write(str(birdMove) + "\n")
    saveFile.write(str(upperBoundForBird) + "\n")
    saveFile.write(str(lowerBoundForBird) + "\n")
    saveFile.close()

    event_file = open("keybinding.txt", "w")
    event_file.write(jump_binding + "\n")
    event_file.write(pause_binding + "\n")
    event_file.write(invisibility_binding + "\n")
    event_file.close()

    python = sys.executable
    os.execl(python, python, * sys.argv)

# pause menu is brought up when pauseEnable is enabled
# it shows the options that are available to the player in the paused state


def pauseMenu():
    global pauseEnable
    global continueGameButton_window
    global dontSaveExitButton_window
    global saveExitButton_window

    def on_enter(e):
        continueGameButton['background'] = 'light green'

    def on_enter2(e):
        dontSaveExitButton['background'] = 'light green'

    def on_enter3(e):
        saveExitButton['background'] = 'light green'

    def on_leave(e):
        continueGameButton['background'] = 'light yellow'
        saveExitButton['background'] = 'light yellow'
        dontSaveExitButton['background'] = 'light yellow'

    pauseEnable = True
    varSet = IntVar()
    continueGameButton = Button(
        root, text="Continue Game", font="Arial 15 bold", bg="light yellow")
    dontSaveExitButton = Button(
        root, text="Don't Save and Exit to Main Menu",
        font="Arial 15 bold", bg="light yellow")
    saveExitButton = Button(
        root, text="Save and Exit to Main Menu",
        font="Arial 15 bold", bg="light yellow")

    continueGameButton['command'] = lambda: continueGame(
        varSet, continueGameButton, dontSaveExitButton, saveExitButton)
    continueGameButton.configure(
        width=30, activebackground="#33B5E5", relief=FLAT)
    continueGameButton_window = canvas.create_window(
        650, 10, anchor=NW, window=continueGameButton)

    dontSaveExitButton['command'] = lambda: dontSaveExit(
        varSet, continueGameButton, dontSaveExitButton, saveExitButton)
    dontSaveExitButton.configure(
        width=30, activebackground="#33B5E5", relief=FLAT)
    dontSaveExitButton_window = canvas.create_window(
        650, 100, anchor=NW, window=dontSaveExitButton)

    saveExitButton['command'] = lambda: saveExit(
        varSet, continueGameButton, dontSaveExitButton, saveExitButton)
    saveExitButton.configure(width=30, activebackground="#33B5E5", relief=FLAT)
    saveExitButton_window = canvas.create_window(
        650, 190, anchor=NW, window=saveExitButton)

    continueGameButton.bind("<Enter>", on_enter)
    continueGameButton.bind("<Leave>", on_leave)
    dontSaveExitButton.bind("<Enter>", on_enter2)
    dontSaveExitButton.bind("<Leave>", on_leave)
    saveExitButton.bind("<Enter>", on_enter3)
    saveExitButton.bind("<Leave>", on_leave)

    root.wait_variable(varSet)
    pauseEnable = False

# exits to the main menu when the corresponding
# button is clicked on in the game over screen


def exitToMMFunc():
    global jump_binding
    global pause_binding
    global invisibility_binding

    event_file = open("keybinding.txt", "w")
    event_file.write(jump_binding + "\n")
    event_file.write(pause_binding + "\n")
    event_file.write(invisibility_binding + "\n")
    event_file.close()

    python = sys.executable
    os.execl(python, python, * sys.argv)

# quits the game when the corresponding
# button is clicked on in the game over screen


def exitGame():
    global startGameSet
    if os.path.exists("keybinding.txt"):
        os.remove("keybinding.txt")
    startGameSet.set(1)
    sys.exit()

# game over menu shows the player the options they have when the game is over


def gameOverMenu(ind):
    time.sleep(0.05)
    global gameOverEnable
    global exitToMM_window
    global quitGame_window
    global name
    global score
    global horseImg
    global bird
    global barr
    global frames

    gameOverEnable = True
    leaderboardFile = open("leaderboard.txt", "a")
    leaderboardFile.write(name + "," + str(score) + "\n")
    leaderboardFile.close()

    def on_enter(e):
        exitToMM['background'] = 'light green'

    def on_enter2(e):
        quitGame['background'] = 'light green'

    def on_leave(e):
        exitToMM['background'] = 'light yellow'
        quitGame['background'] = 'light yellow'

    gameOverText = canvas.create_text(
        770, 200, text="Game Over :(", font="Times 40 bold", fill="red")
    exitToMM = Button(root, text="Exit to Main Menu",
                      command=exitToMMFunc,
                      font="Arial 15 bold", bg="light yellow")
    quitGame = Button(root, text="Quit Game", command=exitGame,
                      font="Arial 15 bold", bg="light yellow")
    exitToMM.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    exitToMM_window = canvas.create_window(
        650, 300, anchor=NW, window=exitToMM)
    quitGame.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    quitGame_window = canvas.create_window(
        650, 400, anchor=NW, window=quitGame)

    exitToMM.bind("<Enter>", on_enter)
    exitToMM.bind("<Leave>", on_leave)
    quitGame.bind("<Enter>", on_enter2)
    quitGame.bind("<Leave>", on_leave)

# animates the elements of the game


def update(ind, birdInd):
    global startTime
    global pauseStatus
    global gameOver
    global invisibilityStartTime
    global frames
    global framesHold
    global birdMove
    global bossKeyEnable
    global spaceClick
    global horseJumpCount

    if invisibilityStartTime != 0 and\
       round(time.time() * 1000) - invisibilityStartTime > 1000:
        frames = framesHold
        invisibilityStartTime = 0

    if startTime == 0:
        startTime = round(time.time() * 1000)
    if not pauseStatus:
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        canvas.itemconfigure(horseImg, image=frame)
        move_barrier()
        if birdMove is True:
            move_bird(birdInd)
        birdInd += 1
        if birdInd == frameCnt2:
            birdInd = 0
    else:
        if not bossKeyEnable:
            pauseMenu()
    if not gameOver:
        root.after(50, update, ind, birdInd)
    else:
        def lowerTheHorse():
            if canvas.coords(horseImg)[1] != 400:
                global horseJumpCount
                if horseJumpCount < 130:
                    canvas.coords(horseImg, 0,
                                  canvas.coords(horseImg)[1] - 2.5)
                    horseJumpCount += 1
                    root.after(3, lowerTheHorse)
                elif (horseJumpCount >= 130 and horseJumpCount <= 259):
                    horseJumpCount += 1
                    canvas.coords(horseImg, 0,
                                  canvas.coords(horseImg)[1] + 2.5)
                    root.after(3, lowerTheHorse)

        lowerTheHorse()

        gameOverMenu(ind)

# function called when 'S' is pressed
# increases the score of the player by 100


def scoreCheat(event):
    global mmEnable
    global leaderboardEnable
    global helpPageEnable
    global reconfigEnable
    if not mmEnable and not leaderboardEnable and\
       not helpPageEnable and not reconfigEnable:
        global score
        score += 100
        canvas.itemconfigure(scoreText, text=name + "'s score: " + str(score))

# function called when 'B' is pressed
# Makes the barrier invisible to the horse for 10s


def barInvisibilityCheat(event):
    global mmEnable
    global leaderboardEnable
    global helpPageEnable
    global reconfigEnable
    if not mmEnable and not leaderboardEnable and\
       not helpPageEnable and not reconfigEnable:
        global barInvisibility
        global barInvisibilityTimer
        global barInvisibilityUsageCount
        if barInvisibility is False and barInvisibilityUsageCount < 3:
            barInvisibility = True
            barInvisibilityTimer = round(time.time() * 1000)
            barInvisibilityUsageCount += 1

# function called when 'Shift' is pressed
# decreases barrier height for 10s


def decreaseBarrHeight(event):
    global mmEnable
    global leaderboardEnable
    global helpPageEnable
    global reconfigEnable
    if not mmEnable and not leaderboardEnable and\
       not helpPageEnable and not reconfigEnable:
        global decreaseBarrHeightEnable
        global decreaseBarrHeightEnableTimer
        global increaseBarrHeightEnable
        global increaseBarrHeightEnableTimer
        decreaseBarrHeightEnable = True
        decreaseBarrHeightEnableTimer = round(time.time() * 1000)
        if increaseBarrHeightEnable:
            increaseBarrHeightEnable = False
            increaseBarrHeightEnableTimer = 0

# function called when 'Ctrl' is pressed
# increases barrier height for 10s


def increaseBarrHeight(event):
    global mmEnable
    global leaderboardEnable
    global helpPageEnable
    global reconfigEnable
    if not mmEnable and not leaderboardEnable and\
       not helpPageEnable and not reconfigEnable:
        global increaseBarrHeightEnable
        global increaseBarrHeightEnableTimer
        global decreaseBarrHeightEnable
        global decreaseBarrHeightEnableTimer
        global name
        increaseBarrHeightEnable = True
        increaseBarrHeightEnableTimer = round(time.time() * 1000)
        if decreaseBarrHeightEnable:
            decreaseBarrHeightEnable = False
            decreaseBarrHeightEnableTimer = 0

# starts the gameplay when the start button is clicked


def startGame(button, button2, button3, lbButton,
              helpButton, reconfigureButton, titleText):
    global startGameSet
    global name
    global keepLooping
    startGameSet.set(1)
    button.destroy()
    button2.destroy()
    button3.destroy()
    lbButton.destroy()
    helpButton.destroy()
    reconfigureButton.destroy()
    try:
        os.remove("savedGame.txt")
    except:
        pass

    while name == '':
        name = askstring('', 'What is your name?')
        if name == '':
            showinfo('', 'Please enter a name.')
    if name is None:
        name = 'guest'

    keepLooping = 1
    canvas.itemconfigure(titleText, state='hidden')

# continues a previous game when the continue game button is clicked


def continueGameMainMenu(button, button2, button3, lbButton,
                         helpButton, reconfigureButton, titleText):
    global startGameSet
    global score
    global barrCount
    global birdMove
    global upperBoundForBird
    global lowerBoundForBird
    global name
    global keepLooping
    keepLooping = 1
    startGameSet.set(1)
    saveFile = open("savedGame.txt", "r")
    name = saveFile.readline().strip()
    score = int(saveFile.readline().strip())
    barrCount = int(saveFile.readline().strip())
    birdMove = bool(saveFile.readline().strip())

    upperBoundForBird = int(saveFile.readline().strip())
    lowerBoundForBird = int(saveFile.readline().strip())
    saveFile.close()

    os.remove("savedGame.txt")

    button.destroy()
    button2.destroy()
    button3.destroy()
    lbButton.destroy()
    helpButton.destroy()
    reconfigureButton.destroy()

    canvas.itemconfigure(titleText, state='hidden')

# brings player back to the main menu from another page


def bMMfunc(lbTable, bMMButton, lbSet, titleText, lbHeadline):
    global button_window
    global button2_window
    global button3_window
    global lbButton_window
    global helpButton_window
    global reconfigureButton_window
    global lbTable2

    canvas.itemconfigure(titleText, state='normal')

    lbSet.set(1)
    canvas.itemconfigure(lbTable, state='hidden')
    try:
        canvas.itemconfigure(lbTable2, state='hidden')
    except:
        pass
    canvas.itemconfigure(lbHeadline, state='hidden')
    canvas.itemconfigure(button_window, state='normal')
    canvas.itemconfigure(button2_window, state='normal')
    try:
        canvas.itemconfigure(button3_window, state='normal')
    except:
        pass
    canvas.itemconfigure(lbButton_window, state='normal')
    canvas.itemconfigure(helpButton_window, state='normal')
    canvas.itemconfigure(reconfigureButton_window, state='normal')
    bMMButton.destroy()

# presents the leaderboard to the player


def leaderboard(titleText):
    global button_window
    global button2_window
    global button3_window
    global lbButton_window
    global helpButton_window
    global reconfigureButton_window
    global leaderboardEnable
    global mmEnable
    global bMMButton_window
    global lbHeadline
    global lbTable
    global lbTable2

    leaderboardEnable = True
    mmEnable = False

    canvas.itemconfigure(titleText, state='hidden')

    lbSet = IntVar()

    canvas.itemconfigure(button_window, state='hidden')
    canvas.itemconfigure(button2_window, state='hidden')
    try:
        canvas.itemconfigure(button3_window, state='hidden')
    except:
        pass
    canvas.itemconfigure(lbButton_window, state='hidden')
    canvas.itemconfigure(helpButton_window, state='hidden')
    canvas.itemconfigure(reconfigureButton_window, state='hidden')

    leaderboardFile = open("leaderboard.txt", "r")
    leaderboardData = [x.strip() for x in leaderboardFile.readlines()]
    leaderboardDataDict = dict()
    for data in leaderboardData:
        points = data.split(",")[1]
        name = data.split(",")[0]
        if name in leaderboardDataDict:
            leaderboardDataDict[name].append(int(points))
        else:
            leaderboardDataDict[name] = [int(points)]
    for item in leaderboardDataDict.items():
        leaderboardDataDict[item[0]] = max(item[1])

    leaderboardDataDict = dict(
        sorted(leaderboardDataDict.items(),
               key=lambda item: item[1], reverse=True))
    lbText = "\n\n\n"
    lbText2 = "\n\n\n"
    loopCount = 0
    for index, item in enumerate(list(leaderboardDataDict.items())):
        lbText += str(index + 1) + ". " + item[0] + "\n"
        lbText2 += str(item[1]) + "\n"
        loopCount += 1
        if loopCount > 9:
            break

    leaderboardFile.close()

    lbHeadline = canvas.create_text(
        800, 170, font="Times 25 bold underline",
        fill="#660066", text="Leaderboard", tags="lb")
    lbTable = canvas.create_text(
        720, 330, font="Times 20 bold", fill="#004d4d", text=lbText, tags="lb")
    lbTable2 = canvas.create_text(
        920, 330, font="Times 20 bold",
        fill="#004d4d", text=lbText2, tags="lb")

    def on_enter(e):
        bMMButton['background'] = 'light green'

    def on_leave(e):
        bMMButton['background'] = 'light yellow'

    bMMButton = Button(root, text="Main Menu",
                       font="Arial 15 bold", bg="light yellow")
    bMMButton['command'] = lambda: bMMfunc(
        lbTable, bMMButton, lbSet, titleText, lbHeadline)
    bMMButton.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    bMMButton_window = canvas.create_window(
        670, 580, anchor=NW, window=bMMButton)
    bMMButton.bind("<Enter>", on_enter)
    bMMButton.bind("<Leave>", on_leave)
    canvas.pack()
    root.wait_variable(lbSet)
    leaderboardEnable = False
    mmEnable = True

# presents the How to Play page to the player


def helpPage(titleText):
    global button_window
    global button2_window
    global button3_window
    global lbButton_window
    global helpButton_window
    global reconfigureButton_window
    global bMMButton_window
    global helpTextObj
    global helpPageEnable
    global mmEnable

    mmEnable = False
    helpPageEnable = True

    canvas.itemconfigure(titleText, state='hidden')

    lbSet = IntVar()

    canvas.itemconfigure(button_window, state='hidden')
    canvas.itemconfigure(button2_window, state='hidden')
    try:
        canvas.itemconfigure(button3_window, state='hidden')
    except:
        pass
    canvas.itemconfigure(lbButton_window, state='hidden')
    canvas.itemconfigure(helpButton_window, state='hidden')
    canvas.itemconfigure(reconfigureButton_window, state='hidden')

    helpText = "How To Play (Default Settings)\n\n1. To dodge the barriers,"
    helpText += " the horse must jump. Hit the SPACE BAR"
    helpText += " to jump.\n2. To avoid the bird, the horse"
    helpText += " must be invisible to the bird. To enable"
    helpText += " bird invisibility, hit 'I'.\n3. To pause"
    helpText += " the game, hit ENTER.\n4. Hit 'H' to hide the"
    helpText += " game and fool your Boss into thinking"
    helpText += " you're working.\n5. Cheats: 'S' increases"
    helpText += " the score by 100, 'B' gives barrier"
    helpText += " invisibility for 10s,\n   'SHIFT' increases barrier"
    helpText += " height for 10s and 'CTRL' decreases barrier height for 10s."
    helpTextObj = canvas.create_text(
        800, 300, font="Times 20 bold",
        text=helpText, tags="ht", fill="#3333ff")

    def on_enter(e):
        bMMButton['background'] = 'light green'

    def on_leave(e):
        bMMButton['background'] = 'light yellow'

    bMMButton = Button(root, text="Main Menu",
                       font="Arial 15 bold", bg="light yellow")
    bMMButton['command'] = lambda: bMMfunc(
        helpTextObj, bMMButton, lbSet, titleText, None)
    bMMButton.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    bMMButton_window = canvas.create_window(
        600, 500, anchor=NW, window=bMMButton)
    bMMButton.bind("<Enter>", on_enter)
    bMMButton.bind("<Leave>", on_leave)

    root.wait_variable(lbSet)
    helpPageEnable = False
    mmEnable = True

# brings the user back to the main menu from the Settings page


def bMMfromConfig(jumpSet_window, invSet_window, pauseSet_window,
                  jumpText, invText, pauseText,
                  bMMButton, doTheConfigButton, configSet, titleText, restore):
    global button_window
    global button2_window
    global button3_window
    global lbButton_window
    global helpButton_window
    global reconfigureButton_window

    configSet.set(1)
    canvas.itemconfigure(jumpSet_window, state='hidden')
    canvas.itemconfigure(invSet_window, state='hidden')
    canvas.itemconfigure(pauseSet_window, state='hidden')
    canvas.itemconfigure(jumpText, state='hidden')
    canvas.itemconfigure(invText, state='hidden')
    canvas.itemconfigure(pauseText, state='hidden')

    canvas.itemconfigure(button_window, state='normal')
    canvas.itemconfigure(button2_window, state='normal')
    try:
        canvas.itemconfigure(button3_window, state='normal')
    except:
        pass
    canvas.itemconfigure(lbButton_window, state='normal')
    canvas.itemconfigure(helpButton_window, state='normal')
    canvas.itemconfigure(reconfigureButton_window, state='normal')
    canvas.itemconfigure(titleText, state='normal')
    bMMButton.destroy()
    doTheConfigButton.destroy()
    restore.destroy()

# reconfigures the keybinding based on player input


def reconfig(jumpVariable, invVariable, pauseVariable):
    global jump_binding
    global pause_binding
    global invisibility_binding

    if jumpVariable == invVariable:
        showinfo(
            '',
            'Jump and Invisibility cannot' +
            ' be associated with the same key press!')
        return
    else:
        if jumpVariable == "Space":
            canvas.unbind("<space>")
            canvas.bind("<space>", space)
            jump_binding = "Space"
        elif jumpVariable == "Left Click":
            canvas.unbind("<space>")
            canvas.bind("<Button-1>", space)
            jump_binding = "Button-1"
        if pauseVariable == "Return":
            canvas.unbind("<Return>")
            canvas.bind("<Return>", pause)
            pause_binding = "Return"
        elif pauseVariable == "Left Alt":
            canvas.unbind("<Return>")
            canvas.bind("<Alt_L>", pause)
            pause_binding = "Left Alt"
        if invVariable == "I":
            canvas.unbind("<i>")
            canvas.bind("<i>", birdInvisibility)
            invisibility_binding = "I"
        elif invVariable == "Space":
            canvas.unbind("<i>")
            canvas.bind("<space>", birdInvisibility)
            invisibility_binding = "Space"

        showinfo('', 'Reconfiguration Done!')

# restores controls to defaults


def restoreDefaults(jumpVariable, invVariable, pauseVariable):
    global jump_binding
    global pause_binding
    global invisibility_binding
    if os.path.exists("keybinding.txt"):
        os.remove("keybinding.txt")
    if invisibility_binding == "Space":
        canvas.unbind("<space>")
        canvas.bind("<i>", birdInvisibility)
    if jump_binding == "Button-1":
        canvas.unbind("<Button-1>")
        canvas.bind("<space>", space)
        jump_binding = "Space"
    if pause_binding == "Left Alt":
        canvas.unbind("<Alt_L>")
        canvas.bind("<Return>", pause)
        pause_binding = "Return"
        invisibility_binding = "I"
    showinfo('', 'Controls have been set to Default.')

# brings up the reconfigure keybindings page


def reconfigure(titleText):
    global button_window
    global button2_window
    global button3_window
    global lbButton_window
    global helpButton_window
    global reconfigureButton_window
    global mmEnable
    global reconfigEnable
    global jumpText
    global jumpSet_window
    global invText
    global invSet_window
    global pauseText
    global pauseSet_window
    global bMMButton_window
    global doTheConfigButton_window
    global restore_window

    mmEnable = False
    reconfigEnable = True

    canvas.itemconfigure(titleText, state='hidden')

    configSet = IntVar()

    canvas.itemconfigure(button_window, state='hidden')
    canvas.itemconfigure(button2_window, state='hidden')
    try:
        canvas.itemconfigure(button3_window, state='hidden')
    except:
        pass
    canvas.itemconfigure(lbButton_window, state='hidden')
    canvas.itemconfigure(helpButton_window, state='hidden')
    canvas.itemconfigure(reconfigureButton_window, state='hidden')

    jumpVariable = StringVar(root)
    jumpVariable.set("Space")
    jumpSet = OptionMenu(root, jumpVariable, "Space", "Left Click")
    jumpSet.configure(width=50)
    jumpText = canvas.create_text(
        500, 220, font="Times 20 bold", fill="#4d4d4d", text="Jump")
    jumpSet_window = canvas.create_window(800, 200, anchor=NW, window=jumpSet)

    invVariable = StringVar(root)
    invVariable.set("I")
    invSet = OptionMenu(root, invVariable, "I", "Space")
    invSet.configure(width=50)
    invText = canvas.create_text(
        500, 320, font="Times 20 bold",
        fill="#4d4d4d", text="Horse Invisibility")
    invSet_window = canvas.create_window(800, 300, anchor=NW, window=invSet)

    pauseVariable = StringVar(root)
    pauseVariable.set("Enter")
    pauseSet = OptionMenu(root, pauseVariable, "Return", "Left Alt")
    pauseSet.configure(width=50)
    pauseText = canvas.create_text(
        500, 420, font="Times 20 bold", fill="#4d4d4d", text="Pause")
    pauseSet_window = canvas.create_window(
        800, 400, anchor=NW, window=pauseSet)

    def on_enter(e):
        doTheConfigButton['background'] = 'light green'

    def on_enter2(e):
        bMMButton['background'] = 'light green'

    def on_enter3(e):
        restore['background'] = 'light green'

    def on_leave(e):
        doTheConfigButton['background'] = 'light yellow'
        bMMButton['background'] = 'light yellow'
        restore['background'] = 'light yellow'

    doTheConfigButton = Button(root, text="Reconfigure", font="Arial 15 bold",
                               bg="light yellow",
                               command=lambda: reconfig(jumpVariable.get(),
                                                        invVariable.get(),
                                                        pauseVariable.get()))
    doTheConfigButton.configure(
        width=20, activebackground="#33B5E5", relief=FLAT)
    doTheConfigButton_window = canvas.create_window(
        800, 500, anchor=NW, window=doTheConfigButton)
    doTheConfigButton.bind("<Enter>", on_enter)
    doTheConfigButton.bind("<Leave>", on_leave)
    restore = Button(root, text="Restore to Defaults",
                     font="Arial 15 bold", bg="light yellow")
    restore['command'] = lambda: restoreDefaults(jumpVariable,
                                                 invVariable, pauseVariable)
    restore.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    restore_window = canvas.create_window(
        1100, 500, anchor=NW, window=restore)
    restore.bind("<Enter>", on_enter3)
    restore.bind("<Leave>", on_leave)

    bMMButton = Button(root, text="Main Menu",
                       font="Arial 15 bold", bg="light yellow")
    bMMButton['command'] = lambda: bMMfromConfig(
        jumpSet_window, invSet_window, pauseSet_window,
        jumpText, invText, pauseText, bMMButton,
        doTheConfigButton, configSet, titleText, restore)
    bMMButton.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    bMMButton_window = canvas.create_window(
        500, 500, anchor=NW, window=bMMButton)
    bMMButton.bind("<Enter>", on_enter2)
    bMMButton.bind("<Leave>", on_leave)

    root.wait_variable(configSet)
    mmEnable = True
    reconfigEnable = False

# presents the main menu to the user


def mainMenu():
    global startGameSet
    global mmEnable
    global button_window
    global button2_window
    global button3_window
    global lbButton_window
    global helpButton_window
    global reconfigureButton_window
    global keepLooping

    def on_enter(e):
        button['background'] = 'light green'

    def on_enter2(e):
        button2['background'] = 'light green'

    def on_enter3(e):
        button3['background'] = 'light green'

    def on_enter4(e):
        lbButton['background'] = 'light green'

    def on_enter5(e):
        helpButton['background'] = 'light green'

    def on_enter6(e):
        reconfigureButton['background'] = 'light green'

    def on_leave(e):
        button['background'] = 'light yellow'
        button2['background'] = 'light yellow'
        button3['background'] = 'light yellow'
        lbButton['background'] = 'light yellow'
        helpButton['background'] = 'light yellow'
        reconfigureButton['background'] = 'light yellow'

    keepLooping = 0
    mmEnable = True
    button = Button(root, text="Start Game")
    button2 = Button(root, text="Quit Game", command=exitGame)
    titleText = canvas.create_text(
        750, 375, text="EquiKnocks", font="Helvetica 70 bold", fill="#9900cc")
    lbButton = Button(root, text="View Leaderboard", font="Arial 15 bold",
                      command=lambda: leaderboard(titleText),
                      bg="light yellow")
    helpButton = Button(root, text="How to Play", font="Arial 15 bold",
                        command=lambda: helpPage(titleText), bg="light yellow")
    reconfigureButton = Button(root, text="Game Settings",
                               font="Arial 15 bold",
                               command=lambda: reconfigure(titleText),
                               bg="light yellow")

    button3 = Button()

    if os.path.exists("savedGame.txt"):
        button3 = Button(root, text="Continue Game", font="Arial 15 bold",
                         bg="light yellow",
                         command=lambda:
                             continueGameMainMenu(
                                                  button,
                                                  button2,
                                                  button3,
                                                  lbButton,
                                                  helpButton,
                                                  reconfigureButton,
                                                  titleText))
        button3.configure(width=20, activebackground="#33B5E5", relief=FLAT)
        button3_window = canvas.create_window(
            1200, 150, anchor=NW, window=button3)
        button3.bind("<Enter>", on_enter3)
        button3.bind("<Leave>", on_leave)

    button = Button(root, text="Start Game",
                    font="Arial 15 bold", bg="light yellow")
    button2 = Button(root, text="Quit Game", font="Arial 15 bold",
                     command=exitGame, bg="light yellow")

    button['command'] = lambda: startGame(
        button, button2, button3, lbButton,
        helpButton, reconfigureButton, titleText)

    button.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    button_window = canvas.create_window(1200, 225, anchor=NW, window=button)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    button2.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    button2_window = canvas.create_window(1200, 300, anchor=NW, window=button2)
    button2.bind("<Enter>", on_enter2)
    button2.bind("<Leave>", on_leave)

    lbButton.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    lbButton_window = canvas.create_window(
        1200, 375, anchor=NW, window=lbButton)
    lbButton.bind("<Enter>", on_enter4)
    lbButton.bind("<Leave>", on_leave)

    helpButton.configure(width=20, activebackground="#33B5E5", relief=FLAT)
    helpButton_window = canvas.create_window(
        1200, 450, anchor=NW, window=helpButton)
    helpButton.bind("<Enter>", on_enter5)
    helpButton.bind("<Leave>", on_leave)

    reconfigureButton.configure(
        width=20, activebackground="#33B5E5", relief=FLAT)
    reconfigureButton_window = canvas.create_window(
        1200, 525, anchor=NW, window=reconfigureButton)
    reconfigureButton.bind("<Enter>", on_enter6)
    reconfigureButton.bind("<Leave>", on_leave)

    def animateMM(indCnt, indCnt2):
        if keepLooping == 0:
            frame = frames[indCnt]
            indCnt += 1
            if indCnt == frameCnt:
                indCnt = 0
            canvas.itemconfigure(horseImg, image=frame)
            canvas.move(cld1, -5, 0)
            canvas.move(cld2, -5, 0)
            canvas.move(cld3, -5, 0)
            canvas.move(cld4, -5, 0)

            if canvas.coords(cld1)[0] < -300:
                canvas.coords(cld1, 1920, 170)

            if canvas.coords(cld2)[0] < -300:
                canvas.coords(cld2, 1920, 250)

            if canvas.coords(cld3)[0] < -300:
                canvas.coords(cld3, 1920, 50)

            if canvas.coords(cld4)[0] < -300:
                canvas.coords(cld4, 1920, 300)

            frame = birdImgFrames[indCnt2]
            indCnt2 += 1
            if indCnt2 == frameCnt2:
                indCnt2 = 0
            canvas.itemconfigure(bird, image=frame)

            for i in range(0, 25):
                canvas.move(bird, -1, 0)

            if canvas.coords(bird)[0] < -100:
                canvas.coords(bird, 1920, 30)

            root.after(50, animateMM, indCnt, indCnt2)

    canvas.pack()
    canvas.coords(bird, 1920, 30)
    root.after(0, animateMM, 0, 0)

    root.wait_variable(startGameSet)

    mmEnable = False
    canvas.itemconfigure(bird, image=None)
    canvas.coords(bird, 1920, 450)

# hides the game with an image when 'H' is pressed


def bossKey(event):
    global bossKeyImgObj
    global pauseStatus
    global mmEnable
    global startGameSet
    global button_window
    global button2_window
    global button3_window
    global bossKeyEnable
    global pauseEnable
    global gameOverEnable
    global exitToMM_window
    global quitGame_window
    global continueGameButton_window
    global dontSaveExitButton_window
    global saveExitButton_window
    global lbButton_window
    global helpButton_window
    global reconfigureButton_window
    global leaderboardEnable
    global bMMButton_window
    global lbHeadline
    global lbTable
    global lbTable2
    global helpPageEnable
    global helpTextObj
    global reconfigEnable
    global jumpText
    global jumpSet_window
    global invText
    global invSet_window
    global pauseText
    global pauseSet_window
    global doTheConfigButton_window
    global restore_window

    if not bossKeyEnable:
        canvas.itemconfigure(bossKeyImgObj, image=bossKeyImg)
        canvas.tag_raise(bossKeyImgObj)
        canvas.pack()
        bossKeyEnable = True
        if not pauseEnable:
            pauseStatus = True
        if mmEnable:
            canvas.itemconfigure(button_window, state='hidden')
            canvas.itemconfigure(button2_window, state='hidden')
            try:
                canvas.itemconfigure(button3_window, state='hidden')
            except:
                pass
            canvas.itemconfigure(lbButton_window, state='hidden')
            canvas.itemconfigure(helpButton_window, state='hidden')
            canvas.itemconfigure(reconfigureButton_window, state='hidden')

        if leaderboardEnable:
            canvas.itemconfigure(bMMButton_window, state='hidden')
            canvas.itemconfigure(lbHeadline, state='hidden')
            canvas.itemconfigure(lbTable, state='hidden')
            canvas.itemconfigure(lbTable2, state='hidden')

        if helpPageEnable:
            canvas.itemconfigure(bMMButton_window, state='hidden')
            canvas.itemconfigure(helpTextObj, state='hidden')

        if reconfigEnable:
            canvas.itemconfigure(bMMButton_window, state='hidden')
            canvas.itemconfigure(doTheConfigButton_window, state='hidden')
            canvas.itemconfigure(jumpText, state='hidden')
            canvas.itemconfigure(jumpSet_window, state='hidden')
            canvas.itemconfigure(invText, state='hidden')
            canvas.itemconfigure(invSet_window, state='hidden')
            canvas.itemconfigure(pauseText, state='hidden')
            canvas.itemconfigure(pauseSet_window, state='hidden')
            canvas.itemconfigure(restore_window, state='hidden')

        if pauseEnable:
            canvas.itemconfigure(continueGameButton_window, state='hidden')
            canvas.itemconfigure(dontSaveExitButton_window, state='hidden')
            canvas.itemconfigure(saveExitButton_window, state='hidden')

        if gameOverEnable:
            canvas.itemconfigure(exitToMM_window, state='hidden')
            canvas.itemconfigure(quitGame_window, state='hidden')

    elif bossKeyEnable:
        canvas.delete("bK")
        bossKeyImgObj = canvas.create_image(
            0, 0, image=None, anchor="nw", tags="bK")
        canvas.pack()
        bossKeyEnable = False
        if not pauseEnable:
            pauseStatus = False
        if mmEnable:
            canvas.itemconfigure(button_window, state='normal')
            canvas.itemconfigure(button2_window, state='normal')
            try:
                canvas.itemconfigure(button3_window, state='normal')
            except:
                pass
            canvas.itemconfigure(lbButton_window, state='normal')
            canvas.itemconfigure(helpButton_window, state='normal')
            canvas.itemconfigure(reconfigureButton_window, state='normal')

        if leaderboardEnable:
            canvas.itemconfigure(bMMButton_window, state='normal')
            canvas.itemconfigure(lbHeadline, state='normal')
            canvas.itemconfigure(lbTable, state='normal')
            canvas.itemconfigure(lbTable2, state='normal')

        if helpPageEnable:
            canvas.itemconfigure(bMMButton_window, state='normal')
            canvas.itemconfigure(helpTextObj, state='normal')

        if reconfigEnable:
            canvas.itemconfigure(bMMButton_window, state='normal')
            canvas.itemconfigure(doTheConfigButton_window, state='normal')
            canvas.itemconfigure(jumpText, state='normal')
            canvas.itemconfigure(jumpSet_window, state='normal')
            canvas.itemconfigure(invText, state='normal')
            canvas.itemconfigure(invSet_window, state='normal')
            canvas.itemconfigure(pauseText, state='normal')
            canvas.itemconfigure(pauseSet_window, state='normal')
            canvas.itemconfigure(restore_window, state='normal')

        if pauseEnable:
            canvas.itemconfigure(continueGameButton_window, state='normal')
            canvas.itemconfigure(dontSaveExitButton_window, state='normal')
            canvas.itemconfigure(saveExitButton_window, state='normal')

        if gameOverEnable:
            canvas.itemconfigure(exitToMM_window, state='normal')
            canvas.itemconfigure(quitGame_window, state='normal')

# keybindings updated when the game is refreshed


def updateBindings():
    global jump_binding
    global pause_binding
    global invisibility_binding

    if os.path.exists("keybinding.txt"):
        bindings_file = open("keybinding.txt", "r")
        bindingsArr = [x.strip() for x in bindings_file.readlines()]
        for index, binding in enumerate(bindingsArr):
            if index == 0 and binding == "Space":
                canvas.unbind("<space>")
                canvas.bind("<space>", space)
                jump_binding = "Space"
            elif index == 0 and binding == "Button-1":
                canvas.unbind("<space>")
                canvas.bind("<Button-1>", space)
                jump_binding = "Button-1"
            elif index == 1 and binding == "Return":
                canvas.unbind("<Return>")
                canvas.bind("<Return>", pause)
                pause_binding = "Return"
            elif index == 1 and binding == "Left Alt":
                canvas.unbind("<Return>")
                canvas.bind("<Alt_L>", pause)
                pause_binding = "Left Alt"
            elif index == 2 and binding == "I":
                canvas.unbind("<i>")
                canvas.bind("<i>", birdInvisibility)
                invisibility_binding = "I"
            elif index == 2 and binding == "Space":
                canvas.unbind("<i>")
                canvas.bind("<space>", birdInvisibility)
                invisibility_binding = "Space"
            canvas.focus_set()


canvas = Canvas(root, bg="light yellow", width="1920", height="1080")
canvas.create_image(0, 0, image=bg, anchor="nw")
bossKeyImgObj = canvas.create_image(0, 0, image=None, anchor="nw", tags="bK")
cld1 = canvas.create_image(1920, 170, image=cloud, anchor="nw")
cld2 = canvas.create_image(1000, 250, image=cloud, anchor="nw")
cld3 = canvas.create_image(100, 50, image=cloud, anchor="nw")
cld4 = canvas.create_image(500, 300, image=cloud, anchor="nw")
canvas.bind("<s>", scoreCheat)
canvas.bind("<b>", barInvisibilityCheat)
canvas.bind("<Control_L>", decreaseBarrHeight)
canvas.bind("<Shift_L>", increaseBarrHeight)
canvas.bind("<h>", bossKey)
canvas.bind("<space>", space)
canvas.bind("<Return>", pause)
canvas.bind("<i>", birdInvisibility)
canvas.focus_set()

horseImg = canvas.create_image(0, 400, anchor="nw", image=None)
barr = canvas.create_rectangle(2500, 500, 2530, 648, fill="#b36b00")
followBird = canvas.create_rectangle(1930, 470, 1930, 470)
bird = canvas.create_image(1920, 450, anchor="nw", image=None)
canvas.create_rectangle(0, 648, 1920, 1080, fill="#00cc00")
startGameSet = IntVar()
updateBindings()
mainMenu()
scoreText = canvas.create_text(
    770, 700, text=name + "'s score: " + str(score), font="Times 20 bold")
canvas.pack()

root.after(0, update, 0, 0)

root.mainloop()
