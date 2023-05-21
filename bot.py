# bot.py
import os
import discord
import hashlib
import json
import time

from datetime import datetime
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
    E = 'Empty'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('DISCORD_CHANNEL')
EXPIRE_AFTER = 57600
REGION_MAP = {
    'vale' : 'Vale_Of_The_Silent',
    'silent' : 'Vale_Of_The_Silent',
    'pure' : 'Pure_Blind',
    'blind' : 'Pure_Blind',
    'perrigen' : 'Perrigen_Falls',
    'falls' : 'Perrigen_Falls',
    'etherium' : 'Etherium_Reach',
    'reach' : 'Etherium_Reach',
    'kalevala' : 'The_Kalevala_Expanse',
    'expanse' : 'The_Kalevala_Expanse',
    'spire' : 'The_Spire',
    'outer' : 'Outer_Passage',
    'passage' : 'Outer_Passage',
    'cobalt' : 'Cobalt_Edge',
    'edge' : 'Cobalt_Edge',
    'paragon' : 'Paragon_Soul',
    'soul' : 'Paragon_Soul',
    'forge' : 'The_Forge',
    'insmother' : 'Insmother',
    'period_basis' : 'Period_Basis',
    'period' : 'Period_Basis',
    'basis' : 'Period_Basis',
    'scalding_pass' : 'Scalding_Pass',
    'scalding' : 'Scalding_Pass',
    'pass' : 'Scalding_Pass',
    'fade' : 'Fade',
    'deklein' : 'Deklein',
    'deklain' : 'Deklein',
    'cloud' : 'Cloud_Ring',
    'ring' : 'Cloud_Ring',
    'cloud_ring' : 'Cloud_Ring',
    'branch' : 'Branch',
    'venal' : 'Venal',
    'tenal' : 'Tenal',
    'great' : 'Great_Wildlands',
    'wild' : 'Great_Wildlands',
    'wildlands' : 'Great_Wildlands',
    'great_wildlands' : 'Great_Wildlands'
}

COLUMN_MARGIN_LENGTH = 2
COLUMN_REGION_LENGTH = 20 + COLUMN_MARGIN_LENGTH
COLUMN_SYSTEM_LENGTH = 9 + COLUMN_MARGIN_LENGTH
COLUMN_DRIFTERS_LENGTH = 17 + COLUMN_MARGIN_LENGTH

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
    {'region' : 'Vale_Of_The_Silent', 'system':'0MV-4W', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'1N-FJ8', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'1VK-6B', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'1W-0KS', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'5T-KM3', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'6WW-28', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'7-K5EL', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'BR-6XP', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'FS-RFL', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'H-NOU5', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'JZV-F4', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'LS9B-9', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'MGAM-4', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'MQ-O27', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'O-LR1H', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'P3EN-E', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'Q-R3GP', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'S-NJBB', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'VI2K-J', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'XSQ-TF', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'Z-8Q65', 'wormholes':[], 'modified':''},
    {'region' : 'Vale_Of_The_Silent', 'system':'ZA0L-U', 'wormholes':[], 'modified':''},
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
    {'region' : 'The_Kalevala_Expanse', 'system':'6FS-CZ', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'86L-9F', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'BM-VYZ', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'BVRQ-O', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'C3J0-O', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'EPCD-D', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'HD-HOZ', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'HPV-RJ', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'J-OAH2', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'JT2I-7', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'K76A-3', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'LE-67X', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'R1O-GN', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'SH6X-F', 'wormholes':[], 'modified':''},
    {'region' : 'The_Kalevala_Expanse', 'system':'TA9T-P', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'B9EA-G', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'C6C-K9', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'E-BFLT', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'ETO-OT', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'GTB-O4', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'H4X-0I', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'HIK-MC', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'K-XJJT', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'K-YL9T', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'KPI-OW', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'M-NP5O', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'OTJ9-E', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'P65-TA', 'wormholes':[], 'modified':''},
    {'region' : 'The_Spire', 'system':'RXA-W1', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'0-4VQL', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'2ULC-J', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'2WU-XT', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'4AZV-W', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'4O-ZRI', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'8-AA98', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'CNHV-M', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'J7X-VN', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'KGCF-5', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'MC4C-H', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'N-I024', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'QFRV-2', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'QHH-13', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'QOK-SX', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'TFPT-U', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'WIO-OL', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'XUPK-Z', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'YQM-P1', 'wormholes':[], 'modified':''},
    {'region' : 'Outer_Passage', 'system':'ZZK-VF', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'3-JG3X', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'6U-MFQ', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'DGDT-3', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'HO4E-Q', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'IG-4OF', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'IO-R2S', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'JXQJ-B', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'KED-2O', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'MZLW-9', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'RJBC-I', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'U-RELP', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'U9SE-N', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'X-CYNC', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'X-Z4JW', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'XKM-DE', 'wormholes':[], 'modified':''},
    {'region' : 'Oasa', 'system':'Y-770C', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'39-DGG', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'4-CUM5', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'4K0N-J', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'6L78-1', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'B-F1MI', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'BWF-ZZ', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'D-I9HJ', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'FDZ4-A', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'HKYW-T', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'K42-IE', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'L-TOFR', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'LX-ZOJ', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'O2O-2X', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'QKTR-L', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'SR-KBB', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'TDE4-H', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'TJM-JJ', 'wormholes':[], 'modified':''},
    {'region' : 'Geminate', 'system':'WH-2EZ', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'1GT-MA', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'5E-EZC', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'5ED-4E', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'5HN-D6', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'87-1PM', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'CHP-76', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'DK0-N8', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'E-B957', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'E-BYOS', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'FV-YEA', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'FV1-RQ', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'HB-5L3', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'L-Z9NB', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'X-41DA', 'wormholes':[], 'modified':''},
    {'region' : 'Cobalt_Edge', 'system':'Y-RAW3', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'2-F3OE', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'2UK4-N', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'3-BADZ', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'6O-XIO', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'CL-J9W', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'DUU1-K', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'I9-ZQZ', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'K-X5AX', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'OXC-UL', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'P8-BKO', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'PO-3QW', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'QK-CDG', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'U-BXU9', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'UB5Z-3', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'UD-VZW', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'X6-J6R', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'Z-PNIA', 'wormholes':[], 'modified':''},
    {'region' : 'Feythabolis', 'system':'ZID-LE', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'6EK-BV', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'C-PEWN', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'CR-0E5', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'D-FVI7', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'F-UVBV', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'G-4H4C', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'G-YZUX', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'G2-INZ', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'HHE5-L', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'IPX-H5', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'JAUD-V', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'NIZJ-0', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'P9F-ZG', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'PE-H02', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'Q1-R7K', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'R-ARKN', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'SN9S-N', 'wormholes':[], 'modified':''},
    {'region' : 'Esoteria', 'system':'YRV-MZ', 'wormholes':[], 'modified':''},
    {'region' : 'Paragon_Soul', 'system':'3PPT-9', 'wormholes':[], 'modified':''},
    {'region' : 'Paragon_Soul', 'system':'ARBX-9', 'wormholes':[], 'modified':''},
    {'region' : 'Paragon_Soul', 'system':'GQ2S-8', 'wormholes':[], 'modified':''},
    {'region' : 'Paragon_Soul', 'system':'H8-ZTO', 'wormholes':[], 'modified':''},
    {'region' : 'Paragon_Soul', 'system':'LD-2VL', 'wormholes':[], 'modified':''},
    {'region' : 'Paragon_Soul', 'system':'O-MCZR', 'wormholes':[], 'modified':''},
    {'region' : 'Paragon_Soul', 'system':'O-N589', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Ahtulaima', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Akkio', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Akora', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Jakanerva', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Mahtista', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Nomaa', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Nuken', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Obanen', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Ohkunen', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Osaa', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Otomainen', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Outuni', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Shihuken', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Ukkalen', 'wormholes':[], 'modified':''},
    {'region' : 'The_Forge', 'system':'Uoyonen', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'0-VG7A', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'1ZF-PJ', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'4CJ-AC', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'5-2PQU', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'5C-RPA', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'88A-RA', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'B-II34', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'C1G-XC', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'EKPB-3', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'EUU-4N', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'F3-8X2', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'F39H-1', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'GDHN-K', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'GK5Z-T', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'HL-VZX', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'KD-KPR', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'L5-UWT', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'MOCW-2', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'N-O53U', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'N7-BIY', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'O-7LAI', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'RD-FWY', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'V-QXXK', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'VBPT-T', 'wormholes':[], 'modified':''},
    {'region' : 'Insmother', 'system':'XQP-9C', 'wormholes':[], 'modified':''},
    {'region' : 'Period_Basis', 'system':'08S-39', 'wormholes':[], 'modified':''},
    {'region' : 'Period_Basis', 'system':'E-DOF2', 'wormholes':[], 'modified':''},
    {'region' : 'Period_Basis', 'system':'RYQC-I', 'wormholes':[], 'modified':''},
    {'region' : 'Period_Basis', 'system':'TCAG-3', 'wormholes':[], 'modified':''},
    {'region' : 'Period_Basis', 'system':'VQE-CN', 'wormholes':[], 'modified':''},
    {'region' : 'Period_Basis', 'system':'Z-M5A1', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'1QZ-Y9', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'2-KPW6', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'4E-EZS', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'6-KPAB', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'9PX2-F', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'F2-NXA', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'FYD-TO', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'GN-PDU', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'H5N-V7', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'IAK-JW', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'JLO-Z3', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'K7-LDX', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'LBC-AW', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'LQ-OAI', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'NSBE-L', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'Q-K2T7', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'Q-NA5H', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'U2-28D', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'V-F6DQ', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'WFFE-4', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'WV0D-1', 'wormholes':[], 'modified':''},
    {'region' : 'Scalding_Pass', 'system':'X9V-15', 'wormholes':[], 'modified':''},
    {'region' : 'Fade', 'system':'0-ARFO', 'wormholes':[], 'modified':''},
    {'region' : 'Fade', 'system':'O1Y-ED', 'wormholes':[], 'modified':''},
    {'region' : 'Fade', 'system':'X36Y-G', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'33RB-O', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'3JN9-Q', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'5W3-DG', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'E-FIC0', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'MXX5-9', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'MZ1E-P', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'N-TFXK', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'S-DN5M', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'TXME-A', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'U-TJ7Y', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'XCBK-X', 'wormholes':[], 'modified':''},
    {'region' : 'Deklein', 'system':'ZOYW-O', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'28O-JY', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'6-4V20', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'77-KDQ', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'8R-RTB', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'G8AD-C', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'MJYW-3', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'O-IVNH', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'OU-X3P', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'QA1-BT', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'X-M9ON', 'wormholes':[], 'modified':''},
    {'region' : 'Cloud_Ring', 'system':'XT-R36', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'2B7A-3', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'4DTQ-K', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'52G-NZ', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'AH-B84', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'BU-IU4', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'C-LP3N', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'C-VGYO', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'CX-1XF', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'I-7JR4', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'J52-BH', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'KMC-WI', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'LRWD-B', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'M-HU4V', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'NEH-CS', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'O-JPKH', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'P7Z-R3', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'Q-NJZ4', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'SVB-RE', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'T-Q2DD', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'W-4FA9', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'YG-82V', 'wormholes':[], 'modified':''},
    {'region' : 'Branch', 'system':'Z-K495', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'0-XIDJ', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'2PLH-3', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'4RX-EE', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'9-266Q', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'92K-H2', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'9IPC-E', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'AJCJ-1', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'EK2-ET', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'HBD-CC', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'K3JR-J', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'M2-2V1', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'N-Q5PW', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'N5Y-4N', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'OJ-CT4', 'wormholes':[], 'modified':''},
    {'region' : 'Venal', 'system':'Y6-HPG', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'3DR-CR', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'5-O8B1', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'6OYQ-Z', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'7D-PAT', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'A1RR-M', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'EOY-BG', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'KMV-CQ', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'PNS7-J', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'Q1U-IU', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'S-1LIO', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'SZ6-TA', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'T-K10W', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'WV-0R2', 'wormholes':[], 'modified':''},
    {'region' : 'Tenal', 'system':'ZK-YQ3', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'4M-P1I', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'7Q-8Z2', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'8DL-CP', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'B-VIP9', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'DE71-9', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'F5-CGW', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'HB-1NJ', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'IX8-JB', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'N-RAEL', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'NE-3GR', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'QM-20X', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'QQ3-YI', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'R-ESG0', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'TET3-B', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'UNJ-GX', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'UT-UZB', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'V89M-R', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'Y4-GQV', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'YUY-LM', 'wormholes':[], 'modified':''},
    {'region' : 'Great_Wildlands', 'system':'ZM-DNR', 'wormholes':[], 'modified':''},
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
    if CHANNEL not in ctx.message.channel.name: return

    try:
        wormholeType = wormholeType.upper()
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value

        for region in storage:
            if (region['system'] == system):
                if (wormholeType == 'E'):
                    region['wormholes'] = ['-']
                    payload = region['system'].ljust(COLUMN_SYSTEM_LENGTH) + '>>  Empty'
                else:
                    region['wormholes'] = [] if region['wormholes'] == ['-'] else region['wormholes']
                    wormholes = region['wormholes']
                    region['wormholes'] += [wormholeType]
                    payload = region['system'].ljust(COLUMN_SYSTEM_LENGTH) + '>>  ' + drifterWormholeDesignation
                region['modified'] = time.time()

        ## Persist data into a file
        with open("database.json", 'w') as file:
            json.dump(storage, file)

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

@bot.command(help='Remove a drifter wormhole from the database')
async def remove(ctx, system: str, wormholeType: str):
    if CHANNEL not in ctx.message.channel.name: return

    try:
        wormholeType = wormholeType.upper()
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value
        payload = 'Could not find drifter type ' + wormholeType + ' in ' + system

        for region in storage:
            if (region['system'] == system):
                wormholes = region['wormholes']
                for index, wormhole in enumerate(wormholes):
                    if (wormhole == wormholeType):
                        wormholes.pop(index)
                        region['wormholes'] = wormholes
                        payload = region['system'].ljust(COLUMN_SYSTEM_LENGTH) + 'REMOVED  ' + drifterWormholeDesignation\

        ## Persist data into a file
        with open("database.json", 'w') as file:
            json.dump(storage, file)

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

@bot.command(help='List all drifter wormholes for a region with Paragon Soul as default')
async def list(ctx, region:str='Paragon_Soul'):
    if CHANNEL not in ctx.message.channel.name: return

    # If the region parameter is send as one letter assume it is a drifter wormhole type search
    if len(region) == 1:  
        await search(ctx, region)
        return

    # Allow list by partials
    if region.lower() in REGION_MAP:
        region = REGION_MAP[region.lower()]

    region = region.title().replace(" ","_")
    url = dotlanUrl + region.replace(" ", "_") + '/'

    payload = '```[' + region + ']' + os.linesep + os.linesep
    payload += 'System'.ljust(COLUMN_SYSTEM_LENGTH + 4) + 'Drifter Wormholes'.ljust(COLUMN_DRIFTERS_LENGTH) + 'Last Updated' + os.linesep

    for wormhole in storage:
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
            last_modified = '' if wormhole['modified'] == '' else datetime.utcfromtimestamp(wormhole['modified'])
            payload += wormhole['system'].ljust(COLUMN_SYSTEM_LENGTH) + '>>  ' + wormholes.ljust(COLUMN_DRIFTERS_LENGTH) + str(last_modified) +  os.linesep
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

@bot.command(help='Search for systems with specific wormhole type')
async def search(ctx, wormholeType:str=""):
    if CHANNEL not in ctx.message.channel.name: return

    try:
        wormholeType = wormholeType.upper()
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value

        found_result = False
        payload = '```' + 'Region'.ljust(COLUMN_REGION_LENGTH) + 'System'.ljust(COLUMN_SYSTEM_LENGTH) + 'Drifter Wormholes'.ljust(COLUMN_DRIFTERS_LENGTH) + 'Last Updated' + os.linesep

        for wormhole in storage:
            # Expire wormholes after 16 hours
            if wormhole['modified'] != '' and wormhole['modified'] + EXPIRE_AFTER < time.time():
                wormhole['wormholes'] = []
                wormhole['modified'] = ''

            if (wormholeType in wormhole['wormholes']):
                found_result = True
                last_modified = '' if wormhole['modified'] == '' else datetime.utcfromtimestamp(wormhole['modified'])
                payload += wormhole['region'].ljust(COLUMN_REGION_LENGTH) + wormhole['system'].ljust(COLUMN_SYSTEM_LENGTH) + wormholeType.ljust(COLUMN_DRIFTERS_LENGTH) + str(last_modified) +  os.linesep

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

@bot.command(help='Alias for search')
async def find(ctx, wormholeType:str=""):
    await search(ctx, wormholeType)

try:
    bot.run(TOKEN)
except:
    print(f"Something went wrong!")

