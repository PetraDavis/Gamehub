# Lost Orbit: a text adventure. Wake alone on a failing space station
# and find your way to the last escape pod. Up/Down pick, ENTER chooses.
from GHLIB import *

AIR = 30  # choices before the station's air runs out
TANK = 10  # extra air from the oxygen tank

# scene: (text, choices). choice: (words, next scene, needs, gives)
# needs/gives are strings of flag letters: k keycard, h helmet, c first part
# of the pod code, d last part, p power on, t oxygen tank, f flare gun,
# s creatures scared off, x tried the lever without air, w one wrong code.
# A capital letter in needs means you must NOT have that flag. A choice
# whose flags don't fit stays hidden, and so does one that only gives what
# you already have. Scenes in DEAD end the game badly.
S = {
    "wake": ("You wake in a sleep pod on Station Kestrel. Red lights blink. A calm voice says: Hull breach. Air failing. Please go to the escape pods. The room is empty.",
             (("Climb out of the pod", "rooms", "", ""),)),
    "rooms": ("Crew quarters. Every bed is empty and unmade. A locker hangs open. A tablet glows on the floor.",
              (("Read the tablet", "log", "", "c"), ("Search the locker", "locker", "", "kh"),
               ("Go out to the corridor", "hall", "", ""))),
    "log": ("Captain's log: Something got in through the cargo bay. Everyone to the pods. The pod code starts 4-7. I hid the last number on the bridge. The rest is static.",
            (("Put the tablet down", "rooms", "", ""),)),
    "locker": ("Inside you find a space helmet and a keycard marked CARGO. You take them both.",
               (("Close the locker", "rooms", "", ""),)),
    "hall": ("Corridor. Doors to the cargo bay, pod bay and med bay. A ladder goes up. A vent is open.",
             (("Open the cargo bay", "cargo", "k", ""), ("Try the pod bay door", "blast", "", ""),
              ("Go into the med bay", "med", "", ""), ("Climb the ladder", "bridge", "", ""),
              ("Crawl into the vent", "vent", "", ""), ("Back to the quarters", "rooms", "", ""))),
    "blast": ("A heavy blast door guards the pod bay. The screen beside it says: OPENS ONLY WITH MAIN POWER. SEE ENGINE ROOM.",
              (("Step back", "hall", "", ""), ("The power is on. Go in", "pods", "p", ""))),
    "vent": ("You crawl into the dark vent. Something else is moving in here too, just ahead of you. It stops when you stop.",
             (("Back out, fast", "hall", "", ""), ("Keep crawling", "ventend", "", ""))),
    "med": ("The med bay. Broken glass covers the floor. An oxygen tank sits on a shelf, and a red box on the wall says EMERGENCY FLARE. A soft bed looks very comfy.",
            (("Take the oxygen tank", "tank", "", "t"), ("Open the red box", "flarebox", "", "f"),
             ("Lie down for a moment", "nap", "", ""), ("Back to the corridor", "hall", "", ""))),
    "tank": ("You strap on the oxygen tank and take a deep breath. That's better. You have more air now.",
             (("Look around the med bay", "med", "", ""),)),
    "flarebox": ("Inside is a flare gun with one shot. Bright light might scare off things that like the dark.",
                 (("Take it and look around", "med", "", ""),)),
    "bridge": ("The bridge. Stars shine through cracked glass. The captain's chair is turned away from you. A big red button glows on the main desk.",
               (("Turn the chair around", "chair", "", "d"), ("Press the red button", "button", "", ""),
                ("Climb back down", "hall", "", ""))),
    "chair": ("Nobody is in the chair, but a note is taped to it: Last number of the pod code is 1. Good luck.",
              (("Put the note away", "bridge", "", ""),)),
    "cargo": ("Crates lie torn open. Something has been living in here. Across the bay a hatch leads to the engine room. A soft clicking comes from behind the crates.",
              (("Sneak to the engine room", "engine", "", ""), ("Fire the flare at the crates", "flare", "fS", "s"),
               ("Look behind the crates", "eyes", "S", ""), ("Leave the cargo bay", "hall", "", ""))),
    "flare": ("The flare bursts into blinding light. Dozens of shining eyes squeeze shut, and the creatures scramble away into the vents, shrieking.",
              (("Go on", "cargo", "", ""),)),
    "engine": ("The engine room. The air here is so thin it hurts to breathe. A big lever on the wall says MAIN POWER: OFF.",
               (("Wear helmet, pull lever", "power", "hP", "p"), ("Pull the lever", "faint", "P", "x"),
                ("Try the lever again", "gasp", "xP", ""), ("Go back to the cargo bay", "cargo", "", ""))),
    "faint": ("You pull, but there isn't enough air. The room spins and you have to stumble back out. You need something to breathe with. Trying that again would be a bad idea.",
              (("Back to the cargo bay", "cargo", "", ""),)),
    "power": ("Lights flicker on all over the station. Far away, a blast door groans open. Behind you, something is clicking.",
              (("Run for the pod bay", "pods", "s", ""), ("Run for the pod bay", "swarm", "S", ""))),
    "swarm": ("Creatures pour out of the cargo bay and fill the corridor, clicking and hissing. They are between you and the pod bay!",
              (("Fire the flare gun", "scare", "f", "s"), ("Push through them", "caught", "", ""),
               ("Hide in the med bay", "hide", "", ""))),
    "scare": ("Blinding light fills the corridor. The creatures shriek and scatter. The way to the pod bay is clear!",
              (("Run!", "pods", "", ""),)),
    "hide": ("You hold your breath behind the med bay door. Claws scrape past outside... and fade away. That took a lot of air.",
             (("Sneak to the pod bay", "pods", "", ""),)),
    "pods": ("The pod bay. One escape pod is left. Its keypad blinks: ENTER CODE. A sign says: 2 WRONG TRIES LOCK THE PAD.",
             (("Type 4-7-1", "home", "cd", ""), ("Guess a code", "wrong", "", "w"),
              ("Guess one more time", "lockout", "w", ""), ("Go look for the code", "hall", "", ""))),
    "wrong": ("WRONG CODE. One more wrong try will lock the keypad. Did anyone leave the code somewhere?",
              (("Think it over", "pods", "", ""),)),
    "home": ("The hatch seals. The pod launches into the stars just as something slams against the window... and falls away. Behind you, Station Kestrel goes dark. You made it!",
             ()),
    "ventend": ("You keep going. The thing ahead turns around. Its eyes shine in the dark, and it is much bigger than you.", ()),
    "nap": ("You close your eyes for just a moment. The air keeps leaking out while you sleep... and you never wake up.", ()),
    "button": ("A voice says: SELF DESTRUCT. TEN SECONDS. There is no off button. Never press the big red button.", ()),
    "eyes": ("Dozens of shining eyes look back at you. You run, but they are much faster than you.", ()),
    "gasp": ("You pull and pull, but there is no air left to breathe. The room goes black.", ()),
    "caught": ("You try to push past, but there are far too many of them. The clicking closes in around you.", ()),
    "lockout": ("WRONG CODE. KEYPAD LOCKED. The pod will not open now, and the clicking is right behind you.", ()),
}
DEAD = ("ventend", "nap", "button", "eyes", "gasp", "caught", "lockout")


def fits(c, have):
    # needs: small letters you must have, capital letters you must not
    for f in c[2]:
        if (f.lower() in have) == f.isupper():
            return False
    return not (c[3] and all(f in have for f in c[3]))


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
            ctext(max(y + 10, 186), "GAME OVER" if at in DEAD else "THE END", RED if at in DEAD else GOLD)
            ctext(206, "ENTER", GREY)
            while wkey() not in (OK, CLR):
                pass
            return
        show = [c for c in choices if fits(c, have)]
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
                if f == "t":
                    air += TANK
        at = c[1]
        air -= 3 if at == "hide" else 1
        if air <= 0:
            cls()
            message(["The air runs out.", "Station Kestrel goes", "quiet. Try again!"], "Out of air")
            return


RULES = "You wake alone on a failing space station. Pick what to do in each scene. Find the pod code and escape before the air runs out. Choose carefully!"
KEYS = ["Up/Down: pick a choice", "ENTER: do it", "CLEAR: quit"]


def main():
    while True:
        c = home("GHSPACE", "LOST ORBIT", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
