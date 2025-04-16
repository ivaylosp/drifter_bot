# mercenary_dens.py
import json
import os
import time
import re
import logging
from datetime import datetime
from datetime import timezone
from os.path import exists
from dotenv import load_dotenv

async def register_mercenary_den(ctx, system:str, planet_number:int, reinforcement_time:str="", owner:str=""):
    print(f"Register merc den {system}, {planet_number}, {reinforcement_time}, {owner}")

    reinforcement_time = convert_time(reinforcement_time)

    if (reinforcement_time is None):
        return await ctx.send(f"Supplied reinforcement time is invalid {reinforcement_time}")

    for mercenary_den in DATABASE:
        if (system.lower() == mercenary_den['system'].lower() and int(planet_number) == mercenary_den['planet_number']):
            column_location = ('[P' + str(mercenary_den['planet_number']).rjust(2, "0") + "] " + mercenary_den['system'])

            mercenary_den["owner"] = owner
            mercenary_den["reinforced"] = reinforcement_time
            mercenary_den["modified"] = time.time()

            persist_data()

            payload = column_location.ljust(COLUMN_LOCATION_LENGTH) + '>>  Added'
            return await ctx.send(payload)
        
    return await ctx.send(f"Could not find referenced planet in system!")

async def region_dens(ctx, region:str, reinforced:bool=False, alliance_only:bool=False):

    highlighted_systems = []
    payload = ""
    region_found = False

    if (reinforced == False):
        # Allow list by partials
        for region_name in ORDERED_REGIONS:
            if not re.search(region, region_name, re.IGNORECASE) == None:
                print(f"Found {region} in {region_name}")
                region_found = True
                region = region_name
                break;
        
        if (region_found == False):
            return await ctx.send(f"Could not find region {region}")

    #{"planet_id": 40000002, "planet_number": 1, "region": "Derelik", "system": "Tanoo", "constilation": "San Matar", "name": "Tanoo I", "owner": "", "reinforced": "", "modified": ""}
    if (reinforced == False):
        payload += '[' + region + ']' + os.linesep + os.linesep

    payload += 'Location'.ljust(COLUMN_LOCATION_LENGTH)

    if (reinforced == True):
        payload += 'Region'.ljust(COLUMN_REGION_LENGTH)

    payload += "Reinforced".ljust(COLUMN_REINFORCED_LENGTH) + "Time Left".ljust(COLUMN_TIMELEFT_LENGTH) + "Owner".ljust(COLUMN_OWNER_LENGTH) + os.linesep

    ordered_dens = []

    # Create a list with merc dens so we can order them
    for mercenary_den in DATABASE:
        if (reinforced == False and not region == mercenary_den['region']):
            continue;
        
        if (reinforced == True and mercenary_den['reinforced'] in ["","-"]):
            mercenary_den['owner'] = ''
            continue;
        
        if (alliance_only == True and mercenary_den['system'] not in ALLIANCE_SYSTEMS):
            continue;

        if (type(mercenary_den['reinforced']) == str and mercenary_den['reinforced'] == "ELAPSED"):
            mercenary_den['reinforced'] = "-"
            mercenary_den['owner'] = ''

        if (isinstance(mercenary_den['reinforced'], float) and mercenary_den['reinforced'] < time.time()):
            mercenary_den['reinforced'] = "ELAPSED"
        
        ordered_dens.append(mercenary_den)

    ordered_dens.sort(reverse=False, key=order_by_reinforcement)

    for mercenary_den in ordered_dens:
        if (mercenary_den['system'] not in highlighted_systems):
            highlighted_systems.append(mercenary_den['system'])

        time_left_value = ''

        if (isinstance(mercenary_den['reinforced'], float)):
            reinforced_column_value = datetime.fromtimestamp(mercenary_den['reinforced'], tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            time_left_value = time_left(mercenary_den['reinforced'])
        else:
            reinforced_column_value = mercenary_den['reinforced']

        column_location = ('[P' + str(mercenary_den['planet_number']).rjust(2, "0") + "] " + mercenary_den['system'])
        column_region = mercenary_den['region']
        column_reinforced = reinforced_column_value
        column_last_updated = time_left_value
        column_owner = mercenary_den['owner'] if len(mercenary_den['owner']) > 0 else '-'

        payload_line = column_location.ljust(COLUMN_LOCATION_LENGTH)

        if (reinforced == True):
            payload_line += column_region.ljust(COLUMN_REGION_LENGTH)

        payload_line += column_reinforced.ljust(COLUMN_REINFORCED_LENGTH) + column_last_updated.ljust(COLUMN_TIMELEFT_LENGTH) + column_owner.ljust(COLUMN_OWNER_LENGTH) +  os.linesep

        if ((len(payload) + len(payload_line) + BUFFER_CHARACTERS) >= MAXIMUM_CHARACTERS):
            payload = "```" + payload + "```"
            await ctx.send(payload)
            payload = ""

        payload += payload_line

    await ctx.send("```" + payload + "```")

    if (reinforced == False):
        await ctx.send("<" + DOTLAN_URL + region.replace(" ", "_") + '/' + ','.join(highlighted_systems) + ">")

async def list_regions(ctx):
    
    payload = '```[Regions]' + os.linesep + os.linesep
    column = 1

    for region in ORDERED_REGIONS:
        payload += region.ljust(COLUMN_REGION_LENGTH + COLUMN_MARGIN_LENGTH)
        if (column > 6):
            payload += os.linesep
            column = 0
        column += 1

    payload += '```'
    await ctx.send(payload)

async def clear_mercenary_den(ctx, system:str, planet_number:int):
    for mercenary_den in DATABASE:
        if (system.lower() == mercenary_den['system'].lower() and int(planet_number) == mercenary_den['planet_number']):
            column_location = ('[P' + str(mercenary_den['planet_number']).rjust(2, "0") + "] " + mercenary_den['system'])

            mercenary_den['owner'] = ''
            mercenary_den['reinforced'] = ''
            mercenary_den["modified"] = time.time()

            persist_data()
            
            payload = column_location.ljust(COLUMN_LOCATION_LENGTH) + '>>  Cleared'
            break;
        else:
            payload = "Specified target system was not found!"
    return await ctx.send(payload)

def get_ordered_regions():
    regions = []

    for region in DATABASE:
        if region['region'] not in regions:
            regions.append(region['region'])

    regions.sort()

    return regions

def convert_time(txt:str):
    txt = txt.lower()

    if (txt == ""):
        return txt

    pattern = r"(\d+)d(\d+)h(\d+)m"

    match = re.match(pattern, txt)
    if match:
        days = int(match.group(1))
        hours = int(match.group(2))
        minutes = int(match.group(3))

        current_timestamp = time.time()
        future_timestamp = current_timestamp + days*86400 + hours*3600 + minutes*60

        return future_timestamp
    else:
        return None

def persist_data():
    ## Persist data into a file
    with open(DATABASE_FILE_NAME, 'w') as file:
        json.dump(DATABASE, file)

def check_data_integrity():
    for system_default in DATABASE_DEFAULT:
        system_found = False
        for system in DATABASE:
            if (system['system'] == system_default['system']):
                system_found = True
                break

        if (system_found == False):
            print(f"Fixing data integrity for missing system {system_default['system']}")
            DATABASE.append(system_default)

def order_by_reinforcement(element):
     future_time = time.time() + 60*60*24*10
     return element['reinforced'] if isinstance(element['reinforced'], (int, float)) else future_time

def time_left(target_timestamp):
    # Get the current time
    now = datetime.now()
    
    # Convert the target timestamp (string) to a datetime object
    target_time = datetime.fromtimestamp(target_timestamp)
    
    # Calculate the difference between the target time and current time
    time_difference = target_time - now
    
    # If the target time has passed, return 0 time left
    if time_difference.total_seconds() < 0:
        return "The target time has already passed."
    
    # Calculate days, hours, and minutes
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    return f"{days}d{hours}h{minutes}m"

# Initialize environemnt varialbes
load_dotenv()

# Constants
DATABASE_DEFAULT_FILE_NAME = "data/mercenary_dens.json"
DATABASE_FILE_NAME = "database_mercenary_dens.json"
DOTLAN_URL = 'https://evemaps.dotlan.net/map/'
COLUMN_MARGIN_LENGTH = 4
COLUMN_LOCATION_LENGTH = 12 + COLUMN_MARGIN_LENGTH
COLUMN_REGION_LENGTH = 20 + COLUMN_MARGIN_LENGTH
COLUMN_REINFORCED_LENGTH = 16 + COLUMN_MARGIN_LENGTH
COLUMN_TIMELEFT_LENGTH = 9 + COLUMN_MARGIN_LENGTH
COLUMN_OWNER_LENGTH = 12 + COLUMN_MARGIN_LENGTH
MAXIMUM_CHARACTERS = 2000
BUFFER_CHARACTERS = 6

# Loading data into memory
file_exists = exists(DATABASE_DEFAULT_FILE_NAME)

logger = logging.getLogger('discord')

if (file_exists):
    logger.info("Loading default mercenary den database into memory...")
    with open(DATABASE_DEFAULT_FILE_NAME) as file:
        DATABASE_DEFAULT = json.load(file)
else:
    logger.info("No database file present. Initializing database into memory...")
    DATABASE_DEFAULT = []

file_exists = exists(DATABASE_FILE_NAME)

if (file_exists):
    logger.info("Loading main mercenary den database into memory...")
    with open(DATABASE_FILE_NAME) as file:
        DATABASE = json.load(file)
else:
    logger.info("No database file present. Initializing database into memory...")
    DATABASE = DATABASE_DEFAULT

# Defining all constants
channel = os.environ.get('DISCORD_MERCENARY_CHANNEL')

IGNORE_REGIONS = [
    11000001,11000002,11000003,11000004,11000005,11000006,11000007,
    11000008,11000009,11000010,11000011,11000012,11000013,11000014,
    11000015,11000016,11000017,11000018,11000019,11000020,11000021,
    11000022,11000023,11000024,11000025,11000026,11000027,11000028,
    11000029,11000030,11000031,11000032,11000033,12000001,12000002,
    12000003,12000004,12000005,14000001,14000002,14000003,14000004,
    14000005
]

ALLIANCE_SYSTEMS = os.environ.get('ALLIANCE_SYSTEMS')

ORDERED_REGIONS = get_ordered_regions()