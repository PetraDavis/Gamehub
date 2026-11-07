# Detective Case: something was stolen and one of five suspects did it.
# Search rooms for clues (always true) and question suspects (the thief
# lies). You have 6 moves, then name the thief. Every case is new.
from GHLIB import *
import random

BG = (35, 30, 55)
SKIN = ((240, 200, 160), (200, 150, 110), (150, 100, 70), (250, 215, 185))
HAIR = ((200, 70, 40), (30, 30, 30), (240, 210, 90), (170, 170, 175))
HAIRN = ("red", "black", "blond", "grey")
SHIRT = ((60, 120, 230), (200, 60, 70), (70, 170, 90), (230, 150, 40), (150, 90, 200))
NAMES = ("Rosa", "Hugo", "Basil", "Lily", "Rex", "Ada", "Tom", "Mia", "Otto", "Ivy", "Max", "Nell", "Finn", "Zoe", "Gus")
LOOT = ("the golden cupcake", "the museum diamond", "Grandma's recipe", "the mayor's hat", "the prize pumpkin", "the royal crown")
PLACE = ("Maple Manor", "the town museum", "the bakery", "the castle", "the county fair")
ROOMS = ("Kitchen", "Library", "Garden", "Attic", "Ballroom")
MOVES = 6


class Case:
    pass


def new_case():
    c = Case()
    c.names = sample(NAMES, 5)
    while True:
        # each suspect: hair, hat, glasses
        c.t = [(random.randint(0, 3), random.randint(0, 1), random.randint(0, 1)) for i in range(5)]
        c.thief = random.randint(0, 4)
        if c.t.count(c.t[c.thief]) == 1:
            break
    c.skin = [random.randint(0, 3) for i in range(5)]
    c.shirt = sample(range(5), 5)
    c.loot = random.choice(LOOT)
    c.place = random.choice(PLACE)
    # three rooms hold one true clue each, two hold nothing
    rooms = sample(range(5), 5)
    c.room = [None] * 5
    for k in range(3):
        c.room[rooms[k]] = k
    c.searched = [False] * 5
    c.asked = [False] * 5
    c.notes = []
    c.moves = MOVES
    return c


def clue(c, k, true=True):
    # trait k of the thief in a few words; true=False tells a lie
    h, hat, gl = c.t[c.thief]
    if k == 0:
        if not true:
            h = (h + random.randint(1, 3)) % 4
        return HAIRN[h] + " hair"
    if k == 1:
        return "a hat" if hat == true else "no hat"
    return "glasses" if gl == true else "no glasses"


def room_text(c, k):
    h, hat, gl = c.t[c.thief]
    if k == 0:
        return ["You find a " + HAIRN[h] + " hair", "caught on the window."]
    if k == 1:
        return ["A hat left a ring in", "the dust."] if hat else ["Muddy hand prints on", "a hat stand: no hat."]
    return ["A glasses lens lies", "under a chair."] if gl else ["A note in tiny writing", "read without glasses."]


def face(c, i, x, y, big=1):
    # a suspect: shirt, face, hair, maybe a hat, maybe glasses
    h, hat, gl = c.t[i]
    r = 14 * big
    rect(x - r, y + r - 2, 2 * r, r, SHIRT[c.shirt[i]])
    circ(x, y, r, SKIN[c.skin[i]])
    rect(x - r, y - r, 2 * r, r // 2 + 1, HAIR[h])
    rect(x - r, y - r // 2, 3 * big, r // 2 + 2, HAIR[h])
    rect(x + r - 3 * big, y - r // 2, 3 * big, r // 2 + 2, HAIR[h])
    if hat:
        rect(x - r - 3 * big, y - r - 1, 2 * r + 6 * big, 3 * big, DARK)
        rect(x - r + 3 * big, y - r - 9 * big, 2 * r - 6 * big, 9 * big, DARK)
    if gl:
        for dx in (-6 * big, 2 * big):
            rect(x + dx, y - 2 * big, 5 * big, 4 * big, BLACK)
            rect(x + dx + big, y - big, 3 * big, 2 * big, (200, 230, 255))
        rect(x - big, y - big, 3 * big, big, BLACK)
    else:
        rect(x - 5 * big, y - big, 2 * big, 2 * big, BLACK)
        rect(x + 3 * big, y - big, 2 * big, 2 * big, BLACK)
    rect(x - 3 * big, y + 6 * big, 6 * big, big + 1, (150, 60, 60))


def lineup(c, title, sel=None):
    # all five suspects; with sel, Left/Right picks one and ENTER returns it
    cls(BG)
    ctext(22, title, GOLD)
    for i in range(5):
        x = 32 + i * 64
        face(c, i, x, 90)
        text(x - len(c.names[i]) * 5, 140, c.names[i], WHITE)
        if c.asked[i]:
            text(x - 15, 160, "asked", GREY)
    text(6, 186, "Moves left: " + str(c.moves), WHITE)
    if sel is None:
        text(6, 204, "ENTER: back", GREY)
        while wkey() not in (OK, CLR):
            pass
        return -1
    text(6, 204, "Left/Right, ENTER: pick", GREY)
    while True:
        x = 32 + sel * 64
        rbox(x - 30, 52, 60, 96, 6, GOLD, 2, BG, False)
        k = wkey()
        if k == OK:
            return sel
        if k == CLR:
            return -1
        if k in (LEFT, RIGHT):
            rbox(x - 30, 52, 60, 96, 6, BG, 2, BG, False)
            sel = (sel + (1 if k == RIGHT else -1)) % 5


def notebook(c):
    lines = c.notes[-6:] or ["No clues yet."]
    message(lines, "Notebook")


def search(c):
    opts = [ROOMS[i] + (" (done)" if c.searched[i] else "") for i in range(5)]
    i = choose("Search which room?", opts + ["Back"])
    if i < 0 or i >= 5 or c.searched[i]:
        return
    c.searched[i] = True
    c.moves -= 1
    k = c.room[i]
    cls(BG)
    if k is None:
        message(["You search everywhere,", "but find nothing useful."], ROOMS[i])
        c.notes.append(ROOMS[i] + ": nothing")
        return
    message(room_text(c, k), ROOMS[i] + ": a clue!")
    c.notes.append(ROOMS[i] + ": " + clue(c, k))


def question(c):
    i = lineup(c, "Question who?", 0)
    if i < 0:
        return
    if c.asked[i]:
        cls(BG)
        message(["You already asked " + c.names[i] + "."])
        return
    c.asked[i] = True
    c.moves -= 1
    k = random.randint(0, 2)
    s = clue(c, k, i != c.thief)
    cls(BG)
    face(c, i, 160, 46, 2)
    room = random.choice(ROOMS)
    message(["I was in the " + room + ".", "I saw the thief! They", "had " + s + "."], c.names[i] + " says")
    c.notes.append(c.names[i] + " says: " + s)


def accuse(c):
    i = lineup(c, "Who is the thief?", 0)
    if i < 0:
        return False
    cls(BG)
    face(c, c.thief, 160, 70, 2)
    t = c.names[c.thief]
    h, hat, gl = c.t[c.thief]
    why = [HAIRN[h] + " hair, " + ("a hat," if hat else "no hat,"), ("glasses." if gl else "no glasses.")]
    if i == c.thief:
        message(["You caught " + t + "!"] + why + ["Case closed. Great work!"], "SOLVED")
    else:
        message([c.names[i] + " is innocent.", "It was " + t + ":"] + why, "Wrong person!")
    return True


def play():
    c = new_case()
    cls(BG)
    message(["Someone stole", c.loot, "at " + c.place + "!", "Room clues are true,", "but the thief will lie."], "NEW CASE")
    while True:
        if c.moves <= 0:
            cls(BG)
            message(["Out of moves!", "Time to name the thief."], "Hurry")
            if accuse(c):
                return
            continue
        o = choose("Moves left: " + str(c.moves), ["Search a room", "Question someone", "See suspects", "Notebook", "Name the thief!"])
        if o == 0:
            search(c)
        elif o == 1:
            question(c)
        elif o == 2:
            lineup(c, "The suspects")
        elif o == 3:
            notebook(c)
        elif o == 4:
            if accuse(c):
                return
        else:
            cls(BG)
            if message(["ENTER: quit this case", "CLEAR: keep going"], "Quit?") == OK:
                return


RULES = "Something was stolen! Search rooms for clues and question the 5 suspects, then name the thief. Clues in rooms are always true, but the thief lies. You only have 6 moves. Every case is different."
KEYS = ["Up/Down + ENTER: choose", "Left/Right: pick a suspect", "CLEAR: back"]


def main():
    while True:
        c = home("GHDETECT", "DETECTIVE CASE", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        play()
