# bot.py
import os
import discord
import hashlib
import json
import time

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
    - = 'Empty'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('DISCORD_CHANNEL')

# Specifying supported intents
intents = discord.Intents.default()
intents.message_content = True

# Storage
storage = [
    {'region' : 'Catch', 'system':'25S-6P', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'3GD6-8', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'4-07MU', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'7LHB-Z', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'9-8GBA', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'AX-DOT', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'B-XJX4', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'E3-SDZ', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'EX-0LQ', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'F4R2-Q', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'F9E-KX', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'G-AOTH', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'GE-94X', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'I-8D0G', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'IS-R7P', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'JA-O6J', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'JWZ2-V', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'L7XS-5', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'OGL8-Q', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'SNFV-I', 'wormholes':[], 'modified':''},
    {'region' : 'Catch', 'system':'ZQ-Z3Y', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'15U-JY', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'6F-H3W', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'7BX-6F', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'7X-02R', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'87XQ-0', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'A-HZYL', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'AC2E-3', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'CHA2-Q', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'G-UTHL', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'H-S80W', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'HMF-9D', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'I-CUVX', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'IGE-RI', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'JGOW-Y', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'KCT-0A', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'L-1SW8', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'P5-EFH', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'PXF-RF', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'Q-XEB3', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'R3W-XU', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'SPLE-Y', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'UAYL-F', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'V6-NY1', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'YRNJ-8', 'wormholes':[], 'modified':''},
    {'region' : 'Fountain', 'system':'Z-YN5Y', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'0MV-4W', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'1N-FJ8', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'1VK-6B', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'1W-0KS', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'5T-KM3', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'6WW-28', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'7-K5EL', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'BR-6XP', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'FS-RFL', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'H-NOU5', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'JZV-F4', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'LS9B-9', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'MGAM-4', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'MQ-O27', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'O-LR1H', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'P3EN-E', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'Q-R3GP', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'S-NJBB', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'VI2K-J', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'XSQ-TF', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'Z-8Q65', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_of_the_Silent', 'system':'ZA0L-U', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'6-I162', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'AC-7LZ', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'CJNF-J', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'FRTC-5', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'NS2L-4', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'O7-7UX', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'R-ORB7', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'U9U-TQ', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'Y-C4AL', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'Y-FZ5N', 'wormholes':[], 'modified':''},
    {'region' : 'Immensea', 'system':'Y19P-1', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'2V-CS5', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'8P9-BM', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'9UY4-H', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'D-6WS1', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'FSW-3C', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'GN7-XY', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'HP-6Z6', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'I-MGAB', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'K1Y-5H', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'MH9C-S', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'N-RMSH', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'OXIY-V', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'QBL-BV', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'QR-K85', 'wormholes':[], 'modified':''},
    {'region' : 'Providence', 'system':'TU-O0T', 'wormholes':[], 'modified':''},
    {'region' : 'Curse', 'system':'ES-UWY', 'wormholes':[], 'modified':''},
    {'region' : 'Curse', 'system':'G-G78S', 'wormholes':[], 'modified':''},
    {'region' : 'Curse', 'system':'J7A-UR', 'wormholes':[], 'modified':''},
    {'region' : 'Curse', 'system':'K-MGJ7', 'wormholes':[], 'modified':''},
    {'region' : 'Curse', 'system':'V7D-JD', 'wormholes':[], 'modified':''},
    {'region' : 'Curse', 'system':'Y-K50G', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'C2X-M5', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'C8VC-S', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'F-749O', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'NJ4X-S', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'S8-NSQ', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'SH1-6P', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'V0DF-2', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'W-UQA5', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'WH-JCA', 'wormholes':[], 'modified':''},
    {'region' : 'Tribute', 'system':'XD-TOV', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'12YA-2', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'4-ABS8', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'5ZXX-K', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'JC-YX8', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'KQK1-2', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'R-2R0G', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'RORZ-H', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'RZC-16', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'S-MDYI', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'U-INPD', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'UC3H-Y', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'UI-8ZE', 'wormholes':[], 'modified':''},
    {'region' : 'Pure_Blind', 'system':'WW-KGD', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'1PF-BC', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'3IK-7O', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'4-QDIX', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'89-JPE', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'8KE-YS', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'9P-870', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'CT8K-0', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'F69O-M', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'IRD-HU', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'KGT3-6', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'KMH-J1', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'RO-0PZ', 'wormholes':[], 'modified':''},
    {'region' : 'Etherium_Reach', 'system':'WPV-JN', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'0-U2M4', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'4-1ECP', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'9-ZA4Z', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'A1F-22', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'BEG-RL', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'E-WMT7', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'H-29TM', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'J9A-BH', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'JPEZ-R', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'JZ-UQC', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'LW-YEW', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'M4-KX5', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'MJ-5F9', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'MTO2-2', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'O-QKSM', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'OP7-BP', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'PE-SAM', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'PFV-ZH', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'RY-2FX', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'SY-OLX', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'TAL1-3', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'VWES-Y', 'wormholes':[], 'modified':''},
    {'region' : 'Perrigen_Falls', 'system':'XU7-CH', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'8F-TK3', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'D-W7F0', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'F-9PXR', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'HM-XR2', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'IP6V-X', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'KBAK-I', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'M-SRKS', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'QY6-RK', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'YZ9-F6', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'Z3V-1W', 'wormholes':[], 'modified':''},
    {'region' : 'Delve', 'system':'ZXB-VC', 'wormholes':[], 'modified':''},
]
# perrigan falls
dotlanUrl = 'https://evemaps.dotlan.net/map/'

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

file_exists = exists('database.json')

if (file_exists):
    with open("database.json") as file:
        storage = json.load(file)

@bot.command(help='Register new drifter wormhole to the database')
async def add(ctx, system: str, wormholeType: str):
    if CHANNEL not in ctx.message.channel.name: return

    try:
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value
        wormholeType = wormholeType.capitalize()

        for region in storage:
            if (region['system'] == system):
                wormholes = region['wormholes']
                region['wormholes'] += [wormholeType]
                payload = region['system'] + '    >>    ' + drifterWormholeDesignation
                region['modified'] = time.time()

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

@bot.command(help='Remove a drifter wormhole from the database')
async def remove(ctx, system: str, wormholeType: str):
    if CHANNEL not in ctx.message.channel.name: return

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

@bot.command(help='List all drifter wormholes for a region with Catch as default')
async def list(ctx, region:str='Catch'):
    if CHANNEL not in ctx.message.channel.name: return

    region = region.title().replace(" ","_")
    url = dotlanUrl + region.replace(" ", "_") + '/'

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
    if CHANNEL not in ctx.message.channel.name: return

    env_password = os.getenv('ADMIN_PASSWORD')
    if (env_password == password):
        with open("database.json", 'w') as file:
            json.dump(storage, file)

@bot.command(help='Lists all supported regions')
async def regions(ctx):
    if CHANNEL not in ctx.message.channel.name: return

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