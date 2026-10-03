import random
import time


def blank():
    print()


def radio(msg):
    print('[RADIO] "' + msg + '"')


def countdown():
    print("--- COUNTDOWN ---")
    print("15 min to qualifying...")
    time.sleep(0.3)
    print("10 min to qualifying...")
    time.sleep(0.3)
    print("5 min to qualifying...")
    time.sleep(0.3)
    radio("Five minutes to qualifying.")
    blank()


def ask(prompt, valid):
    vals = []
    for v in valid:
        vals.append(v.lower())
    while True:
        ans = input(prompt).strip().lower()
        if ans in vals:
            return ans
        print("Invalid. Enter: " + ", ".join(sorted(vals)) + ".")
        blank()


def ask_name(prompt, default):
    raw = input(prompt + " [default: " + default + "]: ")
    parts = raw.strip().split()
    name = " ".join(parts)
    if name == "":
        return default
    return name


def pick_circuit():
    tracks = []
    tracks.append({"name": "Velora Park", "desc": "fast, long straights", "answer": "1"})
    tracks.append({"name": "Kazemiro Bay", "desc": "twisty street circuit", "answer": "3"})
    tracks.append({"name": "Mount Auris", "desc": "balanced layout", "answer": "2"})
    return random.choice(tracks)


def pick_weather():
    options = []
    options.append({"label": "Hot 47C, high wear", "tyre": "hard"})
    options.append({"label": "Mild 29C, balanced", "tyre": "medium"})
    options.append({"label": "Cool 21C, low grip", "tyre": "soft"})
    return random.choice(options)


def make_time(base, extra):
    total = base + extra
    m = int(total // 60)
    rest = total - m * 60
    s = int(rest)
    ms = int(round((rest - s) * 1000))
    if ms == 1000:
        s = s + 1
        ms = 0
    if s < 10:
        return str(m) + ":0" + str(s) + "." + str(ms).zfill(3)
    return str(m) + ":" + str(s) + "." + str(ms).zfill(3)


def to_seconds(lap):
    lap = lap.strip()
    left, right = lap.split(":")
    sec, milli = right.split(".")
    return int(left) * 60 + int(sec) + int(milli) / 1000.0


def tyre_room(game):
    blank()
    print("=== TYRE ROOM ===")
    print(game["circuit"]["name"] + " | " + game["weather"]["label"])
    blank()
    radio("What rubber do we bolt on?")
    print("  1) SOFT - grip, fast wear")
    print("  2) MEDIUM - balanced")
    print("  3) HARD - durable")
    blank()
    print("Pick (1/2/3 or name):")
    choice = ask("> ", ["1", "2", "3", "soft", "medium", "hard"])
    picked = choice
    if choice == "1":
        picked = "soft"
    if choice == "2":
        picked = "medium"
    if choice == "3":
        picked = "hard"
    game["tyre"] = picked
    blank()
    if picked == game["weather"]["tyre"]:
        print("Correct. " + picked.upper() + " fits. +1 prep.")
        if "tyres" not in game["done"]:
            game["done"].add("tyres")
            game["prep"] = game["prep"] + 1
    else:
        print("Wrong choice. No point.")
        game["penalties"] = game["penalties"] + 1
    blank()
    print("Tyre: " + picked.upper() + " | Prep: " + str(game["prep"]) + "/3")
    input("Enter to continue...")
    game["location"] = "garage"


def sim_room(game):
    blank()
    print("=== SIMULATOR ===")
    print(game["circuit"]["name"] + " (" + game["circuit"]["desc"] + ")")
    blank()
    radio("Losing time. Fix the aero.")
    print("  1) LOW - fast straights")
    print("  2) BALANCED")
    print("  3) HIGH - fast corners")
    blank()
    print("Pick (1/2/3):")
    choice = ask("> ", ["1", "2", "3"])
    blank()
    if choice == game["circuit"]["answer"]:
        print("Correct. +1 prep.")
        if "sim" not in game["done"]:
            game["done"].add("sim")
            game["prep"] = game["prep"] + 1
    else:
        print("Wrong setup. No point.")
        game["penalties"] = game["penalties"] + 1
    blank()
    print("Prep: " + str(game["prep"]) + "/3")
    input("Enter to continue...")
    game["location"] = "garage"


def telemetry_room(game):
    blank()
    print("=== TELEMETRY ===")
    base = random.uniform(86.5, 88.5)
    t1 = make_time(base, random.uniform(0.4, 0.9))
    t2 = make_time(base, 0.0)
    t3 = make_time(base, random.uniform(0.2, 0.6))
    laps = [("Run A", t1), ("Run B", t2), ("Run C", t3)]
    random.shuffle(laps)
    for lap in laps:
        print("  " + lap[0] + ": " + lap[1])
    best = laps[0]
    for lap in laps:
        if to_seconds(lap[1]) < to_seconds(best[1]):
            best = lap
    blank()
    radio("Which run was quickest?")
    n = 1
    for lap in laps:
        print("  " + str(n) + ") " + lap[0] + " (" + lap[1] + ")")
        n = n + 1
    blank()
    print("Pick (1/2/3):")
    choice = ask("> ", ["1", "2", "3"])
    blank()
    got = laps[int(choice) - 1]
    if got[0] == best[0]:
        print("Correct. " + best[0] + " " + best[1] + ". +1 prep.")
        if "telemetry" not in game["done"]:
            game["done"].add("telemetry")
            game["prep"] = game["prep"] + 1
    else:
        print("Wrong. Fastest was " + best[0] + " " + best[1] + ".")
        game["penalties"] = game["penalties"] + 1
    blank()
    print("Prep: " + str(game["prep"]) + "/3")
    input("Enter to continue...")
    game["location"] = "garage"


def pit_wall(game):
    blank()
    print("=== PIT WALL ===")
    tyre = game["tyre"]
    if tyre is None:
        tyre = "NONE"
    print("Prep: " + str(game["prep"]) + "/3 | Tyre: " + tyre.upper())
    blank()
    if game["prep"] >= 3:
        print("Car ready.")
        print("  1) Go to Qualifying Grid")
        print("  2) Back to Garage")
        c = ask("> ", ["1", "2"])
        if c == "1":
            game["location"] = "grid"
            countdown()
        else:
            game["location"] = "garage"
    else:
        left = 3 - game["prep"]
        print("Need " + str(left) + " more point(s).")
        input("Enter to go back...")
        game["location"] = "garage"


def quali_grid(game):
    blank()
    print("=== QUALIFYING GRID ===")
    radio(game["driver"] + ": 'Let's go.'")
    blank()
    print("Final call:")
    print("  1) Light fuel, fresh softs, late push")
    print("  2) Heavy fuel, used mediums")
    print("  3) Wait in garage")
    blank()
    print("Pick (1/2/3):")
    c = ask("> ", ["1", "2", "3"])
    good = False
    if c == "1":
        good = True
    if not good:
        game["penalties"] = game["penalties"] + 1
    blank()
    bonus = 0
    if good:
        bonus = 0.4
    lap = make_time(87.5 - game["prep"] * 0.25 - bonus + game["penalties"] * 0.15 + random.uniform(-0.15, 0.15), 0)
    print(game["driver"] + " - " + lap)
    blank()
    extra = 0
    if good:
        extra = 1
    score = game["prep"] + extra - 0.5 * game["penalties"]
    if score >= 3.5:
        pos = random.choice([1, 2, 3])
        radio("P-POLE! What a lap!")
    elif score >= 2.0:
        pos = random.choice([4, 5, 6, 7])
        radio("Good job. Strong position.")
    elif score >= 1.0:
        pos = random.choice([8, 9, 10, 11, 12])
        radio("Tough one. We'll review.")
    else:
        pos = random.choice([14, 15, 17, 19])
        radio("We missed the window.")
    print("P" + str(pos) + " | Lap: " + lap + " | Prep: " + str(game["prep"]) + "/3")
    blank()
    game["running"] = False
    game["location"] = "done"
    print("--- GAME OVER ---")
    again = ask("Again? (y/n): ", ["y", "n", "yes", "no"])
    if again == "y" or again == "yes":
        game["restart"] = True
    else:
        game["restart"] = False


def main():
    print("PIT WALL: F1 GARAGE CHALLENGE")
    blank()
    play = True
    while play:
        print("--- SETUP ---")
        driver = ask_name("Driver name", "Kade Morell #27")
        car = ask_name("Car name", "Falcon F-26")
        blank()
        game = {}
        game["location"] = "garage"
        game["prep"] = 0
        game["tyre"] = None
        game["done"] = set()
        game["running"] = True
        game["penalties"] = 0
        game["team"] = "Northpeak Falcon"
        game["driver"] = driver
        game["car"] = car
        game["circuit"] = pick_circuit()
        game["weather"] = pick_weather()
        game["restart"] = False
        print(game["team"] + " | " + driver + " | " + car)
        print(game["circuit"]["name"] + " - " + game["weather"]["label"])
        blank()
        radio("Losing time in the fast section.")
        radio("Copy. Check telemetry.")
        blank()
        print("Get 3 prep points, then Pit Wall -> Grid.")
        blank()
        while game["running"]:
            loc = game["location"]
            if loc == "garage":
                print("=== GARAGE ===")
                t = game["tyre"]
                if t is None:
                    t = "NONE"
                print("Prep: " + str(game["prep"]) + "/3 | Tyre: " + t.upper())
                print("  1) Tyres  2) Sim  3) Telemetry  4) Pit Wall  5) Quit")
                blank()
                print("Pick (1-5):")
                c = ask("> ", ["1", "2", "3", "4", "5"])
                blank()
                if c == "1":
                    game["location"] = "tyres"
                elif c == "2":
                    game["location"] = "sim"
                elif c == "3":
                    game["location"] = "telemetry"
                elif c == "4":
                    game["location"] = "pitwall"
                else:
                    print("Shift over.")
                    game["running"] = False
                    game["restart"] = False
                    break
            elif loc == "tyres":
                tyre_room(game)
            elif loc == "sim":
                sim_room(game)
            elif loc == "telemetry":
                telemetry_room(game)
            elif loc == "pitwall":
                pit_wall(game)
            elif loc == "grid":
                quali_grid(game)
            elif loc == "done":
                break
            else:
                game["location"] = "garage"
        if game["restart"]:
            blank()
            print("New weekend.")
            blank()
        else:
            play = False
    print("Thanks for playing.")


main()
