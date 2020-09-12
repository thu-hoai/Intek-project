import re

# Regular express pattern
START_TIME_PATTERN = re.compile(r"Log Started at (.*)")
CONSOLE_VARIABLES_PATTERN = re.compile(r'Lua cvar: \((.*)\)')
MODES_PATTERN = re.compile(r'Loading level Levels\/(.*), mission (\w+)')
FRAGS_PATTERN = re.compile(r'<(.*)> <Lua> (.*) killed (.*)(?:itself| with )(\w*)')
START_GAME_SESSION = re.compile(r"<(.*)>  Level (.*) loaded in (.*) seconds")
END_TIME_PATTERN = re.compile(r"<(.*)> == Statistics")
END_TIME_ERROR_PATTERN = re.compile(r"<(.*)> ERROR: \$3#SCRIPT ERROR File: =C, Function: _ERRORMESSAGE,")

# Emojis:
BLUE_CAR = u"🚙"
PISTOL = u"🔫"
BOMB = u"💣"
ROCKET = u"🚀"
KNIFE = u"🔪"
SPEEDBOAT = u"🚤"
FACE_WITH_TONGUE = u"😛"
FROWNING_FACE = u"😦"
SKULL_AND_CROSSBONES = u"☠️"

# Weapon Codes
WEAPONS_DICT = {
    "Vehicle": BLUE_CAR,
    "Falcon": PISTOL,
    "Shotgun": PISTOL,
    "P90": PISTOL,
    "MP5": PISTOL,
    "M4": PISTOL,
    "AG36": PISTOL,
    "OICW": PISTOL,
    "SniperRifle": PISTOL,
    "M249": PISTOL,
    "MG": PISTOL,
    "VehicleMountedAutoMG": PISTOL,
    "VehicleMountedMG": PISTOL,
    "HandGrenade": BOMB,
    "StickyExplosive": BOMB,
    "AG36Grenade": ROCKET,
    "OICWGrenade": ROCKET,
    "Rocket": ROCKET,
    "VehicleMountedRocketMG": ROCKET,
    "VehicleRocket": ROCKET,
    "Machete": KNIFE,
    "Boat": SPEEDBOAT
}

# SQL


SQLITE_MATCH = """INSERT INTO match (start_time, end_time, game_mode, map_name)
                VALUES (?, ?, ?, ?)"""
SQLITE_KILL_OTHER = """INSERT INTO match_frag (match_id, frag_time,
    killer_name, victim_name, weapon_code) VALUES(?, ?, ?, ?, ?)"""
SQLITE_KILL_ITSELF = """INSERT INTO match_frag (match_id, frag_time, killer_name)
    VALUES(?, ?, ?)"""

POSTGRES_MATCH = """INSERT INTO match
            (start_time, end_time, game_mode, map_name)
            VALUES (%s, %s, %s, %s) RETURNING match_id;"""
POSTGRES_KILL_OTHER = """INSERT INTO match_frag (match_id, frag_time,
    killer_name, victim_name, weapon_code) VALUES(%s, %s, %s, %s, %s)"""
POSTGRES_KILL_ITSELF = """INSERT INTO match_frag
    (match_id, frag_time, killer_name) VALUES(%s, %s, %s)"""