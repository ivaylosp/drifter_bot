# bot.py
import os
import discord
import hashlib
import json

from os.path import exists
from collections.abc import Iterable
from dotenv import load_dotenv
from discord.ext import commands
from enum import Enum

class DrifterWormholeTypes(Enum):
    V = 'Vidette V928'
    R = 'Redoubt R259'
    S = 'Sentinel S877'
    B = 'Barbican B735'
    C = 'Conflux C414'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Specifying supported intents
intents = discord.Intents.default()
intents.message_content = True

# Storage
storage = [
    {'region' : 'Catch', 'system':'25S-6P', 'wormholes':[]},
    {'region' : 'Catch', 'system':'3GD6-8', 'wormholes':[]},
    {'region' : 'Catch', 'system':'4-07MU', 'wormholes':[]},
    {'region' : 'Catch', 'system':'7LHB-Z', 'wormholes':[]},
    {'region' : 'Catch', 'system':'9-8GBA', 'wormholes':[]},
    {'region' : 'Catch', 'system':'AX-DOT', 'wormholes':[]},
    {'region' : 'Catch', 'system':'B-XJX4', 'wormholes':[]},
    {'region' : 'Catch', 'system':'E3-SDZ', 'wormholes':[]},
    {'region' : 'Catch', 'system':'EX-0LQ', 'wormholes':[]},
    {'region' : 'Catch', 'system':'F4R2-Q', 'wormholes':[]},
    {'region' : 'Catch', 'system':'F9E-KX', 'wormholes':[]},
    {'region' : 'Catch', 'system':'G-AOTH', 'wormholes':[]},
    {'region' : 'Catch', 'system':'GE-94X', 'wormholes':[]},
    {'region' : 'Catch', 'system':'I-8D0G', 'wormholes':[]},
    {'region' : 'Catch', 'system':'IS-R7P', 'wormholes':[]},
    {'region' : 'Catch', 'system':'JA-O6J', 'wormholes':[]},
    {'region' : 'Catch', 'system':'JWZ2-V', 'wormholes':[]},
    {'region' : 'Catch', 'system':'L7XS-5', 'wormholes':[]},
    {'region' : 'Catch', 'system':'OGL8-Q', 'wormholes':[]},
    {'region' : 'Catch', 'system':'SNFV-I', 'wormholes':[]},
    {'region' : 'Catch', 'system':'ZQ-Z3Y', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'15U-JY', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'6F-H3W', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'7BX-6F', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'7X-02R', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'87XQ-0', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'A-HZYL', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'AC2E-3', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'CHA2-Q', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'G-UTHL', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'H-S80W', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'HMF-9D', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'I-CUVX', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'IGE-RI', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'JGOW-Y', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'KCT-0A', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'L-1SW8', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'P5-EFH', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'PXF-RF', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'Q-XEB3', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'R3W-XU', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'SPLE-Y', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'UAYL-F', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'V6-NY1', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'YRNJ-8', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'Z-YN5Y', 'wormholes':[]},
    {'region' : 'Vale', 'system':'0MV-4W', 'wormholes':[]},
    {'region' : 'Vale', 'system':'1N-FJ8', 'wormholes':[]},
    {'region' : 'Vale', 'system':'1VK-6B', 'wormholes':[]},
    {'region' : 'Vale', 'system':'1W-0KS', 'wormholes':[]},
    {'region' : 'Vale', 'system':'5T-KM3', 'wormholes':[]},
    {'region' : 'Vale', 'system':'6WW-28', 'wormholes':[]},
    {'region' : 'Vale', 'system':'7-K5EL', 'wormholes':[]},
    {'region' : 'Vale', 'system':'BR-6XP', 'wormholes':[]},
    {'region' : 'Vale', 'system':'FS-RFL', 'wormholes':[]},
    {'region' : 'Vale', 'system':'H-NOU5', 'wormholes':[]},
    {'region' : 'Vale', 'system':'JZV-F4', 'wormholes':[]},
    {'region' : 'Vale', 'system':'LS9B-9', 'wormholes':[]},
    {'region' : 'Vale', 'system':'MGAM-4', 'wormholes':[]},
    {'region' : 'Vale', 'system':'MQ-O27', 'wormholes':[]},
    {'region' : 'Vale', 'system':'O-LR1H', 'wormholes':[]},
    {'region' : 'Vale', 'system':'P3EN-E', 'wormholes':[]},
    {'region' : 'Vale', 'system':'Q-R3GP', 'wormholes':[]},
    {'region' : 'Vale', 'system':'S-NJBB', 'wormholes':[]},
    {'region' : 'Vale', 'system':'VI2K-J', 'wormholes':[]},
    {'region' : 'Vale', 'system':'XSQ-TF', 'wormholes':[]},
    {'region' : 'Vale', 'system':'Z-8Q65', 'wormholes':[]},
    {'region' : 'Vale', 'system':'ZA0L-U', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'6-I162', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'AC-7LZ', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'CJNF-J', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'FRTC-5', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'NS2L-4', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'O7-7UX', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'R-ORB7', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'U9U-TQ', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'Y-C4AL', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'Y-FZ5N', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'Y19P-1', 'wormholes':[]},
]

dotlanUrl = 'https://evemaps.dotlan.net/map/'

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

file_exists = exists('database.json')

if (file_exists):
    with open("database.json") as file:
        storage = json.load(file)

@bot.command(help='Register new drifter wormhole to the database')
async def add(ctx, system: str, wormholeType: str):
    try:
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value
        wormholeType = wormholeType.capitalize()

        for region in storage:
            if (region['system'] == system):
                wormholes = region['wormholes']
                region['wormholes'] += [wormholeType]
                payload = region['system'] + '    >>    ' + drifterWormholeDesignation

        ## Persist data into a file
        with open("database.json", 'w') as file:
            json.dump(storage, file)

        await ctx.send(payload)
    except KeyError as exception:
        await ctx.send(f"""
You entered `{wormhole_type}`, which is not a valid drifter wormhole identifier.
```
Supported identifiers:

V - Vidette V928
R - Redoubt R259
S - Sentinel S877
B - Barbican B735
C - Conflux C414
```""")

@bot.command(help='Register new drifter wormhole to the database')
async def remove(ctx, system: str, wormholeType: str):
    try:
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value
        wormholeType = wormholeType.capitalize()
        payload = 'Could not find drifter type ' + wormholeType + ' in ' + system

        for region in storage:
            if (region['system'] == system):
                wormholes = region['wormholes']
                for index, wormhole in enumerate(wormholes):
                    if (wormhole == wormholeType):
                        wormholes.pop(index)
                        region['wormholes'] = wormholes
                        payload = region['system'] + '    REMOVED    ' + drifterWormholeDesignation\

        ## Persist data into a file
        with open("database.json", 'w') as file:
            json.dump(storage, file)

        await ctx.send(payload)
    except KeyError as exception:
        await ctx.send(f"""
You entered `{wormhole_type}`, which is not a valid drifter wormhole identifier.
```
Supported identifiers:

V - Vidette V928
R - Redoubt R259
S - Sentinel S877
B - Barbican B735
C - Conflux C414
```""")

@bot.command(help='List all drifter wormholes in the database')
async def list(ctx, region:str='Catch'):
    region = region.capitalize()
    url = dotlanUrl + region + '/'

    payload = '```[' + region + ']' + os.linesep + os.linesep

    for wormhole in storage:
        if (region == wormhole['region']):
            wormholes = wormhole['wormholes']
            if isinstance(wormholes, Iterable):
                wormholes = ' '.join(wormholes)
            else:
                wormholes = ''
            payload += wormhole['system'] + '    >>    ' + wormholes + os.linesep
            url += wormhole['system'] + ','

    payload += '```'
    payload += '<' + url[:-1] + '>'
    await ctx.send(payload)

@bot.command(help='Initialize datastore')
async def init(ctx, password:str):
    env_password = os.getenv('ADMIN_PASSWORD')
    if (env_password == password):
        with open("database.json", 'w') as file:
            json.dump(storage, file)

@bot.command(help='Lists all supported regions')
async def regions(ctx):
    regions = []
    payload = '```[Regions]' + os.linesep + os.linesep

    for region in storage:
        if region['region'] not in regions:
            regions.append(region['region'])
            payload += region['region'] + os.linesep

    payload += '```'
    await ctx.send(payload)

try:
    bot.run(TOKEN)
except:
    print(f"Something went wrong!")