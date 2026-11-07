# Lost Orbit: a short text adventure. Wake alone on a failing space station
# and find your way to the last escape pod. Up/Down pick, ENTER chooses.
from GHLIB import *

AIR = 30  # choices before the station's air runs out

# scene: (text, choices). choice: (words, next scene, needs, gives)
# needs/gives are strings of flag letters: k keycard, h helmet, c pod code,
# p power on. A choice whose flags you don't have stays hidden, and so does
# one that only gives what you already have.
S = {
    "wake": ("You wake in a sleep pod on Station Kestrel. Red lights blink. A calm voice says: Hull breach. Air failing. Please go to the escape pods. The room is empty.",
             (("Climb out of the pod", "rooms", "", ""),)),
    "rooms": ("Crew quarters. Every bed is empty and unmade. A locker hangs open. A tablet glows on the floor.",
              (("Read the tablet", "log", "", "c"), ("Search the locker", "locker", "", "kh"),
               ("Go out to the corridor", "hall", "", ""))),
    "log": ("Captain's log: Something got in through the cargo bay. Everyone to the pods. Pod code is 4-7-1. The rest is static.",
            (("Put the tablet down", "rooms", "", ""),)),
    "locker": ("Inside you find a space helmet and a keycard marked CARGO. You take them both.",
               (("Close the locker", "rooms", "", ""),)),
    "hall": ("The corridor splits. Left is the cargo bay, its door scratched from the inside. Right is the pod bay behind a blast door. A vent near the floor is open.",
             (("Open the cargo bay", "cargo", "k", ""), ("Try the pod bay door", "blast", "", ""),
              ("Crawl into the vent", "vent", "", ""), ("Back to the quarters", "rooms", "", ""))),
    "blast": ("A heavy blast door guards the pod bay. The screen beside it says: OPENS ONLY WITH MAIN POWER. SEE ENGINE ROOM.",
              (("Step back", "hall", "", ""), ("The power is on. Go in", "pods", "p", ""))),
    "vent": ("You crawl into the dark vent. Something else is moving in here too, just ahead of you. It stops when you stop.",
             (("Back out, fast", "hall", "", ""),)),
    "cargo": ("Crates lie torn open. Something has been living in here. Across the bay a hatch leads to the engine room. A soft clicking comes from behind the crates.",
              (("Sneak to the engine room", "engine", "", ""), ("Look behind the crates", "eyes", "", ""),
               ("Leave the cargo bay", "hall", "", ""))),
    "eyes": ("Dozens of shining eyes look back at you. You run! The cargo door slams shut behind you just in time.",
             (("Catch your breath", "hall", "", ""),)),
    "engine": ("The engine room. The air here is so thin it hurts to breathe. A big lever on the wall says MAIN POWER: OFF.",
               (("Wear helmet, pull lever", "power", "h", "p"), ("Pull the lever", "faint", "", ""),
                ("Go back to the cargo bay", "cargo", "", ""))),
    "faint": ("You pull, but there isn't enough air. The room spins and you have to stumble back out. You need something to breathe with.",
              (("Back to the cargo bay", "cargo", "", ""),)),
    "power": ("Lights flicker on all over the station. Far away, a blast door groans open. Behind you, the clicking gets louder.",
              (("Run for the pod bay", "pods", "", ""),)),
    "pods": ("The pod bay. One escape pod is left. Its keypad blinks: ENTER CODE.",
             (("Type 4-7-1", "home", "c", ""), ("Guess a code", "wrong", "", ""))),
    "wrong": ("WRONG CODE. The clicking is right behind you now. Think. Did anyone leave the code somewhere?",
              (("Try again", "pods", "", ""), ("Go look for the code", "hall", "", ""))),
    "home": ("The hatch seals. The pod launches into the stars just as something slams against the window... and falls away. Behind you, Station Kestrel goes dark. You made it.",
             ()),
}


def page(s, air):
    # the scene's words: drawn once, on a clear screen
    cls()
    text(4, 14, "LOST ORBIT", GOLD)
    text(236, 14, "Air " + str(air), RED if air <= 5 else GREY)
    y = 36
    for ln in wrap(s):
        text(6, y, ln)
        y += 17
    return y


def wrap(s, n=31):
    out = []
    line = ""
    for w in s.split(" "):
        if line and len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


def pick(opts, y0):
    # the choices under the words; Up/Down moves the gold one, so only the
    # two lines that change colour are drawn again
    sel = 0
    y0 = max(y0 + 6, 206 - 20 * len(opts))
    for i in range(len(opts)):
        text(20, y0 + i * 20, opts[i], GOLD if i == sel else WHITE)
    text(6, y0, ">", GOLD)
    while True:
        k = wkey()
        old = sel
        if k == UP:
            sel = (sel - 1) % len(opts)
        elif k == DOWN:
            sel = (sel + 1) % len(opts)
        elif k == OK:
            return sel
        elif k == CLR:
            return -1
        if sel != old:
            rect(6, y0 + old * 20 - 12, 10, 16, BLACK)
            text(20, y0 + old * 20, opts[old], WHITE)
            text(6, y0 + sel * 20, ">", GOLD)
            text(20, y0 + sel * 20, opts[sel], GOLD)


def game():
    have = ""
    air = AIR
    at = "wake"
    while True:
        words, choices = S[at]
        if not choices:
            y = page(words, air)
            ctext(max(y + 10, 186), "THE END", GOLD)
            ctext(206, "ENTER", GREY)
            while wkey() not in (OK, CLR):
                pass
            return
        show = [c for c in choices if all(f in have for f in c[2]) and not (c[3] and all(f in have for f in c[3]))]
        y = page(words, air)
        i = pick([c[0] for c in show], y)
        if i < 0:
            if message(["ENTER: quit the story", "CLEAR: keep playing"], "Quit?") == OK:
                return
            continue
        c = show[i]
        for f in c[3]:
            if f not in have:
                have += f
        at = c[1]
        air -= 1
        if air <= 0:
            cls()
            message(["The air runs out.", "Station Kestrel goes", "quiet. Try again!"], "Out of air")
            return


RULES = "You wake alone on a failing space station. Read each scene and pick what to do. Find the last escape pod before the air runs out."
KEYS = ["Up/Down: pick a choice", "ENTER: do it", "CLEAR: quit"]


def main():
    while True:
        c = home("GHSPACE", "LOST ORBIT", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
