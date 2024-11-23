# drifter_scouts.py

import time
import json
import os
import re

from dotenv import load_dotenv
from os.path import exists
from collections.abc import Iterable
from enum import Enum
from datetime import datetime
from datetime import timezone

async def register_wormhole(ctx, system: str, wormholeType: str, endOfLife: str=''):
    try:
        wormholeType = wormholeType.upper()
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value
        eol = ''
        payload = ''

        if endOfLife == 'eol':
            eol = '*'    

        for region in DATABASE:
            if (region['system'] == system):
                if (wormholeType == 'E'):
                    region['wormholes'] = ['-']
                    payload = region['system'].ljust(COLUMN_SYSTEM_LENGTH) + '>>  Empty'
                else:
                    region['wormholes'] = [] if region['wormholes'] == ['-'] else region['wormholes']
                    region['wormholes'] += [wormholeType+eol]
                    payload = region['system'].ljust(COLUMN_SYSTEM_LENGTH) + '>>  ' + drifterWormholeDesignation
                region['modified'] = time.time()

        ## Persist data into a file
        persist_data()

        await ctx.send(payload)
    except KeyError as exception:
        await ctx.send(f"""
You entered `{wormholeType}`, which is not a valid drifter wormhole identifier.
```
Supported identifiers:

V - Vidette V928
R - Redoubt R259
S - Sentinel S877
B - Barbican B735
C - Conflux C414
```""")
        
async def region_wormholes(ctx, region:str='Paragon Soul'):

    # If the region parameter is send as one letter assume it is a drifter wormhole type search
    if len(region) == 1:  
        await search(ctx, region)
        return

    region_found = False

    # Allow list by partials
    for region_name in ORDERED_REGIONS:
        if not re.search(region, region_name, re.IGNORECASE) == None:
            print(f"Found {region} in {region_name}")
            region_found = True
            region = region_name
            break;
    
    if (region_found == False):
        return await ctx.send(f"Could not find region {region}")

    url = DOTLAN_URL + region.replace(" ", "_") + '/'

    payload = '```[' + region + ']' + os.linesep + os.linesep
    payload += 'System'.ljust(COLUMN_SYSTEM_LENGTH + 4) + 'Drifter Wormholes'.ljust(COLUMN_DRIFTERS_LENGTH) + 'Last Updated' + os.linesep

    for wormhole in DATABASE:
        if (region == wormhole['region']):
            # Expire wormholes after 16 hours
            if wormhole['modified'] != '' and wormhole['modified'] + EXPIRE_AFTER < time.time():
                wormhole['wormholes'] = []
                wormhole['modified'] = ''
            wormholes = wormhole['wormholes']
            if isinstance(wormholes, Iterable):
                wormholes = ' '.join(wormholes)
            else:
                wormholes = ''
            last_modified = datetime.fromtimestamp(wormhole['modified'], tz=timezone.utc).strftime("%Y-%m-%d %H:%M") if isinstance(wormhole['modified'], float) else '-'
            payload += wormhole['system'].ljust(COLUMN_SYSTEM_LENGTH) + '>>  ' + wormholes.ljust(COLUMN_DRIFTERS_LENGTH) + str(last_modified) +  os.linesep
            url += wormhole['system'] + ','

    payload += '```'
    payload += '<' + url[:-1] + '>'
    await ctx.send(payload)

async def remove(ctx, system: str, wormholeType: str):
    try:
        wormholeType = wormholeType.upper()
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType.replace('*', '')].value
        payload = 'Could not find drifter type ' + wormholeType + ' in ' + system

        for region in DATABASE:
            if (region['system'] == system):
                wormholes = region['wormholes']
                for index, wormhole in enumerate(wormholes):
                    if (wormhole == wormholeType):
                        wormholes.pop(index)
                        region['wormholes'] = wormholes
                        payload = region['system'].ljust(COLUMN_SYSTEM_LENGTH) + 'REMOVED  ' + drifterWormholeDesignation\

        ## Persist data into a file
        persist_data()

        await ctx.send(payload)
    except KeyError as exception:
        await ctx.send(f"""
You entered `{wormholeType}`, which is not a valid drifter wormhole identifier.
```
Supported identifiers:

V - Vidette V928
R - Redoubt R259
S - Sentinel S877
B - Barbican B735
C - Conflux C414
```""")
        
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

async def search(ctx, wormholeType:str=""):
    try:
        wormholeType = wormholeType.upper()
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value

        found_result = False
        payload = '```' + 'Region'.ljust(COLUMN_REGION_LENGTH) + 'System'.ljust(COLUMN_SYSTEM_LENGTH) + 'Drifter Wormholes'.ljust(COLUMN_DRIFTERS_LENGTH) + 'Last Updated' + os.linesep

        for wormhole in DATABASE:
            # Expire wormholes after 16 hours
            if wormhole['modified'] != '' and wormhole['modified'] + EXPIRE_AFTER < time.time():
                wormhole['wormholes'] = []
                wormhole['modified'] = ''

            eol = ''

            if (wormholeType + '*' in wormhole['wormholes']):
                eol = '*'

            if (wormholeType in wormhole['wormholes'] or eol == '*'):
                found_result = True
                last_modified = datetime.fromtimestamp(wormhole['modified'], tz=timezone.utc).strftime("%Y-%m-%d %H:%M") if isinstance(wormhole['modified'], float) else '-'
                payload += wormhole['region'].ljust(COLUMN_REGION_LENGTH) + wormhole['system'].ljust(COLUMN_SYSTEM_LENGTH) + (wormholeType+eol).ljust(COLUMN_DRIFTERS_LENGTH) + str(last_modified) +  os.linesep

        payload  += '```'

        if (found_result == False):
            payload = 'Search did not yeld any results'

        await ctx.send(payload)
    except KeyError as exception:
        await ctx.send(f"""
You entered `{wormholeType}`, which is not a valid drifter wormhole identifier.
```
Supported identifiers:

V - Vidette V928
R - Redoubt R259
S - Sentinel S877
B - Barbican B735
C - Conflux C414
```""")

def get_ordered_regions():
    regions = []

    for region in DATABASE:
        if region['region'] not in regions:
            region['region'] = region['region'].replace("_"," ")
            regions.append(region['region'])

    regions.sort()

    return regions

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

def persist_data():
    ## Persist data into a file
    with open(DATABASE_FILENAME, 'w') as file:
        json.dump(DATABASE, file)

# Initialize environemnt varialbes
load_dotenv()

# Loading databases in memory
DATABASE_DEFAULT_FILENAME = 'data\drifter_scouts.json'
DATABASE_FILENAME = 'database_drifter_scouts.json'

file_exists = exists(DATABASE_DEFAULT_FILENAME)

if (file_exists):
    print("Loading default drifter scouts database into memory...")
    with open(DATABASE_DEFAULT_FILENAME) as file:
        DATABASE_DEFAULT = json.load(file)
else:
    DATABASE_DEFAULT = []

file_exists = exists(DATABASE_FILENAME)

if (file_exists):
    print("Loading main drifter scouts database into memory...")
    with open(DATABASE_FILENAME) as file:
        DATABASE = json.load(file)
else:
    DATABASE = []

check_data_integrity()

DOTLAN_URL = 'https://evemaps.dotlan.net/map/'
channel = os.getenv('DISCORD_CHANNEL')

EXPIRE_AFTER = 57600
COLUMN_MARGIN_LENGTH = 2
COLUMN_REGION_LENGTH = 20 + COLUMN_MARGIN_LENGTH
COLUMN_SYSTEM_LENGTH = 9 + COLUMN_MARGIN_LENGTH
COLUMN_DRIFTERS_LENGTH = 17 + COLUMN_MARGIN_LENGTH

ORDERED_REGIONS = get_ordered_regions()

class DrifterWormholeTypes(Enum):
    V = 'Vidette V928'
    R = 'Redoubt R259'
    S = 'Sentinel S877'
    B = 'Barbican B735'
    C = 'Conflux C414'
    E = 'Empty'