# Fortune Cards: pick three cards from a shuffled deck and the calculator
# reads your fortune: one card for the past, one for now, one for the future.
from GHLIB import *
import random

TABLE = (55, 25, 85)
BACKC = (120, 40, 140)
FACE = (250, 240, 215)
INK = (40, 30, 50)
CW = 36
CH = 54

# name, picture, then what it means for the past, the present and the future
DECK = (
    ("The Star", "star", "You made a wish that mattered.", "Hope is shining on you.", "A wish will come true."),
    ("The Moon", "moon", "You found a way in the dark.", "Trust your dreams tonight.", "A secret will be revealed."),
    ("The Sun", "sun", "You had a really good day.", "You bring warmth to others.", "Happy days are coming."),
    ("The Key", "key", "You unlocked something new.", "An answer is close by.", "A door will open for you."),
    ("The Cat", "cat", "You were braver than you knew.", "Be curious and look around.", "You will land on your feet."),
    ("The Bridge", "bridge", "You made a new friend.", "Reach out to someone.", "Two paths will meet."),
    ("The Lantern", "lantern", "Someone helped you see.", "You are a light for a friend.", "You will find what was lost."),
    ("The Crown", "crown", "You were proud of yourself.", "Lead the way, others follow.", "You will win something."),
    ("The Wave", "wave", "A big change washed over you.", "Go with the flow today.", "An adventure is on its way."),
    ("The Mountain", "mountain", "You climbed a hard hill.", "Keep going, you are close.", "You will reach the top."),
    ("The Bird", "bird", "You heard some good news.", "Say what is on your mind.", "A message will reach you."),
    ("The Clock", "clock", "You waited for something.", "Now is the right time.", "Good things take time."),
    ("The Tree", "tree", "You grew a lot this year.", "Stay strong and steady.", "Something you plant will grow."),
    ("The Heart", "heart", "Someone was kind to you.", "You are loved more than you know.", "A friendship will get closer."),
    ("The Ship", "ship", "You left something behind.", "Set your sails, it's time.", "A trip is in your future."),
    ("The Flame", "flame", "You stood up for yourself.", "Your spark is bright today.", "You will find a new passion."),
    ("The Rainbow", "rainbow", "A storm finally ended.", "Look for the bright side.", "A happy surprise is coming."),
    ("The Book", "book", "You learned a big lesson.", "Ask, and you will find out.", "You will discover a talent."),
    ("The Owl", "owl", "You noticed what others missed.", "Listen more than you speak.", "A wise choice will pay off."),
    ("The Feather", "feather", "You let go of a worry.", "Take it easy today.", "Things will feel lighter soon."),
)
TIMES = ("PAST", "NOW", "FUTURE")


def art(kind, x, y, s=1):
    # each picture is a few shapes centred on x, y; s = 2 draws it bigger
    def r(a, b, w, h, c):
        rect(x + a * s, y + b * s, w * s, h * s, c)
    if kind == "star":
        col(GOLD)
        fill_poly([x, x + 3 * s, x + 10 * s, x + 4 * s, x + 6 * s, x, x - 6 * s, x - 4 * s, x - 10 * s, x - 3 * s],
                  [y - 10 * s, y - 3 * s, y - 3 * s, y + 2 * s, y + 9 * s, y + 5 * s, y + 9 * s, y + 2 * s, y - 3 * s, y - 3 * s])
    elif kind == "moon":
        circ(x, y, 9 * s, (230, 225, 170))
        circ(x + 4 * s, y - 2 * s, 8 * s, FACE)
    elif kind == "sun":
        r(-11, -1, 22, 2, (250, 170, 30))
        r(-1, -11, 2, 22, (250, 170, 30))
        circ(x, y, 6 * s, (250, 200, 40))
    elif kind == "key":
        circ(x - 5 * s, y, 5 * s, GOLD)
        r(-1, -1, 12, 3, GOLD)
        r(7, 2, 2, 4, GOLD)
        circ(x - 5 * s, y, 2 * s, FACE)
    elif kind == "cat":
        col(INK)
        fill_poly([x - 7 * s, x - 7 * s, x - 2 * s], [y - 4 * s, y - 11 * s, y - 6 * s])
        fill_poly([x + 7 * s, x + 7 * s, x + 2 * s], [y - 4 * s, y - 11 * s, y - 6 * s])
        circ(x, y, 7 * s, INK)
        r(-4, -2, 2, 2, (120, 220, 90))
        r(2, -2, 2, 2, (120, 220, 90))
    elif kind == "bridge":
        r(-12, -2, 24, 3, (140, 90, 50))
        r(-10, 1, 3, 8, (140, 90, 50))
        r(7, 1, 3, 8, (140, 90, 50))
        r(-12, 6, 24, 4, (80, 140, 220))
    elif kind == "lantern":
        r(-5, -6, 10, 13, (250, 210, 80))
        r(-6, -8, 12, 2, INK)
        r(-6, 7, 12, 2, INK)
        r(-2, -11, 4, 3, INK)
    elif kind == "crown":
        col(GOLD)
        fill_poly([x - 10 * s, x - 10 * s, x - 5 * s, x, x + 5 * s, x + 10 * s, x + 10 * s],
                  [y + 6 * s, y - 6 * s, y, y - 8 * s, y, y - 6 * s, y + 6 * s])
        r(-2, 1, 4, 3, RED)
    elif kind == "wave":
        circ(x - 4 * s, y + 2 * s, 7 * s, (60, 130, 220))
        circ(x + 6 * s, y + 4 * s, 5 * s, (60, 130, 220))
        r(-12, 6, 24, 4, (60, 130, 220))
    elif kind == "mountain":
        col((110, 110, 130))
        fill_poly([x - 12 * s, x, x + 12 * s], [y + 9 * s, y - 10 * s, y + 9 * s])
        col(WHITE)
        fill_poly([x - 4 * s, x, x + 4 * s], [y - 4 * s, y - 10 * s, y - 4 * s])
    elif kind == "bird":
        circ(x, y, 6 * s, (230, 90, 70))
        col((230, 90, 70))
        fill_poly([x - 3 * s, x - 13 * s, x - 2 * s], [y - 2 * s, y - 8 * s, y + 3 * s])
        col(GOLD)
        fill_poly([x + 5 * s, x + 10 * s, x + 5 * s], [y - 2 * s, y, y + 2 * s])
        r(1, -3, 2, 2, INK)
    elif kind == "tree":
        r(-2, 2, 4, 9, (130, 80, 40))
        circ(x, y - 3 * s, 8 * s, (60, 150, 70))
    elif kind == "heart":
        circ(x - 4 * s, y - 3 * s, 5 * s, RED)
        circ(x + 4 * s, y - 3 * s, 5 * s, RED)
        col(RED)
        fill_poly([x - 9 * s, x + 9 * s, x], [y - 1 * s, y - 1 * s, y + 9 * s])
    elif kind == "ship":
        col((80, 140, 220))
        fill_poly([x - 1 * s, x - 1 * s, x - 9 * s], [y - 11 * s, y + 2 * s, y + 2 * s])
        fill_poly([x + 1 * s, x + 1 * s, x + 8 * s], [y - 8 * s, y + 2 * s, y + 2 * s])
        col((140, 90, 50))
        fill_poly([x - 11 * s, x + 11 * s, x + 7 * s, x - 7 * s], [y + 4 * s, y + 4 * s, y + 9 * s, y + 9 * s])
    elif kind == "flame":
        col((240, 110, 30))
        fill_poly([x, x + 7 * s, x + 6 * s, x - 6 * s, x - 7 * s], [y - 11 * s, y, y + 8 * s, y + 8 * s, y])
        col((250, 210, 60))
        fill_poly([x, x + 4 * s, x + 3 * s, x - 3 * s, x - 4 * s], [y - 4 * s, y + 3 * s, y + 8 * s, y + 8 * s, y + 3 * s])
    elif kind == "rainbow":
        for i, c in enumerate(((220, 50, 50), (245, 150, 30), (240, 210, 50), (70, 170, 80), (60, 120, 220))):
            circ(x, y + 5 * s, (12 - 2 * i) * s, c)
        circ(x, y + 5 * s, 2 * s, FACE)
        r(-13, 5, 27, 13, FACE)
    elif kind == "book":
        r(-11, -7, 22, 15, (60, 90, 170))
        r(-10, -6, 9, 13, WHITE)
        r(1, -6, 9, 13, WHITE)
        r(-8, -3, 5, 1, GREY)
        r(3, -3, 5, 1, GREY)
        r(-8, 0, 5, 1, GREY)
        r(3, 0, 5, 1, GREY)
    elif kind == "owl":
        circ(x, y + 1 * s, 9 * s, (140, 95, 60))
        circ(x - 4 * s, y - 1 * s, 3 * s, WHITE)
        circ(x + 4 * s, y - 1 * s, 3 * s, WHITE)
        r(-5, -2, 2, 2, INK)
        r(3, -2, 2, 2, INK)
        col(GOLD)
        fill_poly([x - 2 * s, x + 2 * s, x], [y + 2 * s, y + 2 * s, y + 5 * s])
    elif kind == "feather":
        col((90, 170, 160))
        fill_poly([x + 8 * s, x + 4 * s, x - 6 * s, x - 9 * s, x - 3 * s], [y - 10 * s, y - 2 * s, y + 7 * s, y + 9 * s, y - 2 * s])
        r(-8, 6, 2, 4, INK)
    elif kind == "clock":
        circ(x, y, 9 * s, INK)
        circ(x, y, 7 * s, WHITE)
        r(-1, -6, 2, 7, INK)
        r(0, -1, 5, 2, INK)


def back(x, y):
    # a face-down card: plain purple with a gold dot
    rect(x, y, CW, CH, BACKC)
    rect(x + CW // 2 - 3, y + CH // 2 - 3, 6, 6, GOLD)


def face(x, y, i):
    rect(x, y, CW, CH, FACE)
    art(DECK[i][1], x + CW // 2, y + CH // 2)


def frame(x, y, c):
    # a 2-pixel outline just outside a card, drawn as 4 strips
    rect(x - 3, y - 3, CW + 6, 2, c)
    rect(x - 3, y + CH + 1, CW + 6, 2, c)
    rect(x - 3, y - 1, 2, CH + 2, c)
    rect(x + CW + 1, y - 1, 2, CH + 2, c)


def spot(i):
    return 14 + i * 42, 40


def reading():
    deck = list(range(len(DECK)))
    shuffle(deck)
    # seven cards face down; a picked card is replaced by the next one from
    # the deck, so there are always seven to choose from
    row = deck[:7]
    nxt = 7
    cards = []
    cls(TABLE)
    ctext(22, "Pick 3 cards", GOLD)
    for i in range(7):
        back(spot(i)[0], spot(i)[1])
    for t in range(3):
        x = 50 + t * 90
        rect(x, 120, CW + 20, CH + 20, dk(TABLE, 0.8))
        text(x + 28 - len(TIMES[t]) * 5, 208, TIMES[t], GREY)
    sel = 0
    frame(spot(sel)[0], spot(sel)[1], GOLD)
    while len(cards) < 3:
        k = wkey()
        old = sel
        if k == CLR:
            return False
        if k in (LEFT, RIGHT):
            sel = (sel + (1 if k == RIGHT else -1)) % 7
        elif k == OK:
            # the card lands face up in its spot and a new one is dealt
            x = 50 + len(cards) * 90 + 10
            cards.append(row[sel])
            rect(spot(sel)[0], spot(sel)[1], CW, CH, TABLE)
            face(x, 130, row[sel])
            if len(cards) < 3:
                row[sel] = deck[nxt]
                nxt += 1
                pause(0.25)
                back(spot(sel)[0], spot(sel)[1])
            continue
        if sel != old:
            frame(spot(old)[0], spot(old)[1], TABLE)
            frame(spot(sel)[0], spot(sel)[1], GOLD)
    for t in range(3):
        name, kind = DECK[cards[t]][0], DECK[cards[t]][1]
        cls(TABLE)
        ctext(20, TIMES[t], GREY)
        rect(124, 34, 72, 92, FACE)
        art(kind, 160, 80, 2)
        ctext(148, name, GOLD)
        ctext(172, DECK[cards[t]][2 + t])
        ctext(206, "ENTER: next" if t < 2 else "ENTER: done", GREY)
        if wkey() == CLR:
            return False
    cls(TABLE)
    ctext(26, "YOUR FORTUNE", GOLD)
    y = 60
    for t in range(3):
        text(10, y, TIMES[t], GREY)
        y += 18
        text(10, y, DECK[cards[t]][2 + t])
        y += 26
    ctext(206, "ENTER: new reading  CLEAR: stop", GREY)
    return wkey() != CLR


def game():
    while reading():
        pass


RULES = "Shuffle the deck, pick three cards and find out what they say about your past, your present and your future. Just for fun!"
KEYS = ["Left/Right: choose a card", "ENTER: pick it / next", "CLEAR: stop"]


def main():
    while True:
        c = home("GHFORTUN", "FORTUNE CARDS", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
