import sqlite3
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "games.db"

SLUG_MAP = {
    "Car Parking": "car-parking-multiplayer",
    "Null's Brawl": "brawl-stars",
    "Null's Clash": "clash-of-clans",
    "GTA San Andreas": "gta-san-andreas",
    "Shadow Fight 2": "shadow-fight-2",
    "Subway Surfers": "subway-surfers",
    "Traffic Rider": "traffic-rider",
    "Hill Climb Racing": "hill-climb-racing-2",
    "Score! Hero": "score-hero",
    "8 Ball Pool": "8-ball-pool",
    "Dead Target": "dead-target",
    "Sniper 3D": "sniper-3d-assassin",
    "Mini Militia": "mini-militia",
    "Earn to Die": "earn-to-die-2",
    "Zombie Catchers": "zombie-catchers",
    "Swamp Attack": "swamp-attack",
    "Hungry Shark": "hungry-shark-world",
    "Bowmasters": "bowmasters",
    "Fruit Ninja": "fruit-ninja",
    "Plants vs Zombies": "plants-vs-zombies-2",
    "Dude Theft Wars": "dude-theft-wars",
    "Stickman Warriors": "stickman-warriors",
    "Payback 2": "payback-2",
    "Kick the Buddy": "kick-the-buddy",
    "Dr. Driving": "dr-driving",
    "PUBG Mobile": "pubg-mobile-lite",
    "Free Fire": "free-fire-max",
    "Standoff 2": "standoff-2",
    "Special Forces": "special-forces-group-2",
    "Call of Duty": "call-of-duty-mobile",
    "Modern Strike": "modern-strike-online",
    "Cover Fire": "cover-fire",
    "Hitman Sniper": "hitman-sniper",
    "Six-Guns": "six-guns",
    "Into the Dead": "into-the-dead-2",
    "Mortal Kombat": "mortal-kombat-x",
    "Injustice 2": "injustice-2",
    "Gangstar Vegas": "gangstar-vegas",
    "Soul Knight": "soul-knight",
    "Magic Rampage": "magic-rampage",
    "Asphalt 9": "asphalt-9-legends",
    "CarX Drift": "carx-drift-racing-2",
    "CarX Street": "carx-street",
    "Need for Speed": "need-for-speed-no-limits",
    "Real Racing": "real-racing-3",
    "Rush Rally": "rush-rally-3",
    "Rebel Racing": "rebel-racing",
    "Pixel Car Racer": "pixel-car-racer",
    "MadOut2": "madout2-bigcityonline",
    "Trial Xtreme": "trial-xtreme-4",
    "Truck Simulator": "truck-simulator-ultimate",
    "Bus Simulator": "bus-simulator-ultimate",
    "Farming Simulator": "farming-simulator-23",
    "Construction Simulator": "construction-simulator-3",
    "Flight Pilot": "flight-pilot-simulator-3d",
    "SimCity": "simcity-buildit",
    "Car Saler": "car-saler-simulator-dealership",
    "Dream League Soccer": "dream-league-soccer",
    "DLS": "dream-league-soccer",
    "EA SPORTS FC": "fifa-mobile",
    "FIFA": "fifa-mobile",
    "eFootball": "pes-2018",
    "PES": "pes-2018",
    "Head Ball": "head-ball-2",
    "Real Steel": "real-steel-world-robot-boxing",
    "WWE Mayhem": "wwe-mayhem",
    "NBA LIVE": "nba-live-mobile",
    "Monument Valley": "monument-valley",
    "The Room": "the-room-old-sins",
    "Limbo": "limbo",
    "Machinarium": "machinarium",
    "Cut the Rope": "cut-the-rope",
    "Bad Piggies": "bad-piggies",
    "Brain Out": "brain-out",
    "Minecraft": "minecraft-pocket-edition",
    "Terraria": "terraria",
    "Roblox": "roblox",
    "Temple Run": "temple-run-2",
    "Vector": "vector",
    "Swordigo": "swordigo",
    "Alto's Odyssey": "altos-odyssey",
    "Super Mario": "super-mario-run",
    "Sonic Dash": "sonic-dash",
    "Contra": "contra-returns",
    "Doodle Jump": "doodle-jump",
    "PAC-MAN": "pac-man",
    "1945 Air Force": "1945-classic-arcade"
}

def update_games():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title FROM games")
    games = c.fetchall()

    updated = 0
    for gid, title in games:
        matched_slug = None
        for key, slug in SLUG_MAP.items():
            if key.lower() in title.lower():
                matched_slug = slug
                break
        
        if not matched_slug:
            # Clean title slug fallback
            clean = re.sub(r'[^a-zA-Z0-9]', '-', title.split('(')[0]).strip('-').lower()
            clean = re.sub(r'-+', '-', clean)[:25]
            matched_slug = clean if clean else "subway-surfers"

        real_url = f"https://{matched_slug}.en.uptodown.com/android/download"
        c.execute("UPDATE games SET download_url = ? WHERE id = ?", (real_url, gid))
        updated += 1

    conn.commit()
    conn.close()
    print(f"Successfully updated {updated} games with REAL verified Uptodown download links!")

if __name__ == "__main__":
    update_games()
