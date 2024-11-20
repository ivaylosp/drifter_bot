# generate_data.py
import requests
import json
import re
import time

from os.path import exists

ESI_BASE_URL = "https://esi.evetech.net"
ESI_ACTIVE = False
DATABASE_FILE_NAME = "mercenary_dens.json"
SYSTEMS_DATABASE_FILE_NAME = "systems.json"
CONSTELLATIONS_DATABASE_FILE_NAME = "constellations.json"
REGIONS_DATABASE_FILE_NAME = "regions.json"
PLANETS_DATABASE_FILE_NAME = "planets.json"
TEMPERATE_PLANET_TYPE_ID = 11
IGNORE_REGIONS = [
    11000001,11000002,11000003,11000004,11000005,11000006,11000007,
    11000008,11000009,11000010,11000011,11000012,11000013,11000014,
    11000015,11000016,11000017,11000018,11000019,11000020,11000021,
    11000022,11000023,11000024,11000025,11000026,11000027,11000028,
    11000029,11000030,11000031,11000032,11000033,12000001,12000002,
    12000003,12000004,12000005,14000001,14000002,14000003,14000004,
    14000005
]

# Merc Dens
file_exists = exists(DATABASE_FILE_NAME)

if (file_exists):
    print("Loading databas into memory...")
    with open(DATABASE_FILE_NAME) as file:
        STORAGE = json.load(file)
else:
    print("No database file present. Initializing database into memory...")
    STORAGE = []

# Systems
file_exists = exists(SYSTEMS_DATABASE_FILE_NAME)

if (file_exists):
    print("Loading databas into memory...")
    with open(SYSTEMS_DATABASE_FILE_NAME) as file:
        SYSTEMS = json.load(file)
else:
    print("No database file present. Initializing database into memory...")
    SYSTEMS = []

# Constellations
file_exists = exists(CONSTELLATIONS_DATABASE_FILE_NAME)

if (file_exists):
    print("Loading databas into memory...")
    with open(CONSTELLATIONS_DATABASE_FILE_NAME) as file:
        CONSTELLATIONS = json.load(file)
else:
    print("No database file present. Initializing database into memory...")
    CONSTELLATIONS = []

# Regions
file_exists = exists(REGIONS_DATABASE_FILE_NAME)

if (file_exists):
    print("Loading regions database into memory...")
    with open(REGIONS_DATABASE_FILE_NAME) as file:
        REGIONS = json.load(file)
else:
    print("No database file present. Initializing database into memory...")
    REGIONS = []

# Planets
file_exists = exists(PLANETS_DATABASE_FILE_NAME)

if (file_exists):
    print("Loading planets database into memory...")
    with open(PLANETS_DATABASE_FILE_NAME) as file:
        PLANETS = json.load(file)
else:
    print("No database file present. Initializing database into memory...")
    PLANETS = []

def fetch_all_systems_data():
    url = ESI_BASE_URL + "/latest/universe/systems"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to systems data. Status code: {response.status_code}")
        return None

def fetch_system_data(system_id):
    url = ESI_BASE_URL + "/latest/universe/systems/" + str(system_id)
    
    system = find_system(system_id)
    
    if system:
        print(f"System fetched from cache ID {system_id}")
        return system
    
    print(f"Retriving data from {url}")
    response = requests.get(f"{url}")
    if response.status_code == 200:
        system = response.json()
        SYSTEMS.append(system)
        persist_systems_data()
        return system
    else:
        print(f"Failed to retrieve system data for ID {system_id}. Status code: {response.status_code}")
        return None
    
def fetch_planet_data(planet_id):
    url = ESI_BASE_URL + "/latest/universe/planets/" + str(planet_id)

    planet = find_planet(planet_id)
    
    if planet:
        print(f"Planet fetched from cache ID {planet_id}")
        return planet
    
    print(f"Retriving data from {url}")
    response = requests.get(f"{url}")
    ESI_ACTIVE = True
    if response.status_code == 200:
        planet = response.json()
        PLANETS.append(planet)
        persist_planet_data()
        return planet
    else:
        print(f"Failed to retrieve planet data for ID {planet_id}. Status code: {response.status_code}")
        return None

def fetch_constellation_data(constellation_id):
    url = ESI_BASE_URL + "/latest/universe/constellations/" + str(constellation_id)

    constelation = find_constelation(constellation_id)

    if constelation:
        print(f"Constelation fetched from cache ID {constellation_id}")
        return constelation
    
    print(f"Retriving data from {url}")
    response = requests.get(f"{url}")

    if response.status_code == 200:
        constelation = response.json()
        CONSTELLATIONS.append(constelation)
        persist_constellations_data()
        return constelation
    else:
        print(f"Failed to retrieve constellation data for ID {constellation_id}. Status code: {response.status_code}")
        return None
    
def fetch_region_data(region_id):
    url = ESI_BASE_URL + "/latest/universe/regions/" + str(region_id)

    region = find_region(region_id)
    
    if region:
        print(f"Region fetched from cache ID {region_id}")
        return region

    print(f"Retriving data from {url}")
    response = requests.get(f"{url}")

    if response.status_code == 200:
        region =  response.json()
        REGIONS.append(region)
        persist_regions_data()
        return region
    else:
        print(f"Failed to retrieve region data for ID {region_id}. Status code: {response.status_code}")
        return None   

def find_planet(planet_id):
    for planet in PLANETS:
        if planet['planet_id'] == planet_id:
            return planet
    return None

def find_mercenary_dens(planet_id):
    for mercenary_den in STORAGE:
        if mercenary_den['planet_id'] == planet_id:
            return mercenary_den
    return None

def find_constelation(constellation_id):
    for constellation in CONSTELLATIONS:
        if constellation['constellation_id'] == constellation_id:
            return constellation
    return None

def find_region(region_id):
    for region in REGIONS:
        if region['region_id'] == region_id:
            return region
    return None

def find_system(system_id):
    for system in SYSTEMS:
        if system['system_id'] == system_id:
            return system
    return None

def get_planet_number(planet):
    planet_name = replace_parentheses_content(planet.get("name"), '')
    planet_number_roman = planet_name.split()[-1]

    try:
        planet_number = roman_to_int(planet_number_roman)
    except:
        planet_number = planet.get("name")

    return planet_number

def persist_all_data():
    ## Persist data into a file
        with open(DATABASE_FILE_NAME, 'w') as file:
            json.dump(STORAGE, file)

        persist_planet_data()
        persist_systems_data()
        persist_regions_data()
        persist_constellations_data()

def persist_planet_data():
        with open(PLANETS_DATABASE_FILE_NAME, 'w') as file:
            json.dump(PLANETS, file)

def persist_systems_data():
        with open(SYSTEMS_DATABASE_FILE_NAME, 'w') as file:
            json.dump(SYSTEMS, file)

def persist_regions_data():
        with open(REGIONS_DATABASE_FILE_NAME, 'w') as file:
            json.dump(REGIONS, file)

def persist_constellations_data():
        with open(CONSTELLATIONS_DATABASE_FILE_NAME, 'w') as file:
            json.dump(CONSTELLATIONS, file)

def roman_to_int(roman):
    roman_values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev_value = 0

    for numeral in reversed(roman):
        current_value = roman_values[numeral]

        if current_value >= prev_value:
            total += current_value
        else:
            total -= current_value

        prev_value = current_value

    return total

def replace_parentheses_content(input_string, replacement_string):
    result = re.sub(r' \(.*?\)', replacement_string, input_string)
    
    return result

# Main function to coordinate the fetching process
def main():
    # Fetch the initial data
    systems_data = fetch_all_systems_data()
    esi_request_counter = 0
    
    if systems_data:
        for system_id in systems_data:
            system_data = fetch_system_data(system_id)
            if system_data.get("planets"):
                constellation_data = fetch_constellation_data(system_data.get("constellation_id"))
                if constellation_data is None:
                    return None
                
                try:
                    IGNORE_REGIONS.index(constellation_data.get("region_id"))
                    continue
                except ValueError as ve:
                    print(f"Region not in the ingore list")

                region_data = fetch_region_data(constellation_data.get("region_id"))
                if region_data is None:
                    return None
                
                for planet in system_data.get("planets"):
                    planet_data = fetch_planet_data(planet.get("planet_id"))
                    
                    mercenary_den = find_mercenary_dens(planet.get("planet_id"))
                    if (mercenary_den is not None):
                        print("Planet found in cache skipping...", planet_data.get("name"))
                        continue

                    # esi_request_counter += 1
                    
                    # if (esi_request_counter > 20 and ESI_ACTIVE == True):
                    #     print("Pausing for 30 seconds...")
                    #     time.sleep(30)
                    #     esi_request_counter = 0

                    # print(f"Counter at {esi_request_counter}")

                    if (planet_data.get("type_id") == TEMPERATE_PLANET_TYPE_ID):
                        print("Temperate planet found:", planet_data.get("name"))
                        storage_payload = {}
                        storage_payload["planet_id"] = planet_data.get("planet_id")
                        storage_payload["planet_number"] = get_planet_number(planet_data)
                        storage_payload["region"] = region_data.get("name")
                        storage_payload["system"] = system_data.get("name")
                        storage_payload["constellation"] = constellation_data.get("name")
                        storage_payload["name"] = planet_data.get("name")
                        storage_payload["owner"] = ""
                        storage_payload["reinforced"] = ""
                        storage_payload["modified"] = ""
                        
                        STORAGE.append(storage_payload)

                        persist_all_data()
            else:
                print("Could not fetch planets data")
    else:
        print("Systems data returned empty set")

# Call the main function
if __name__ == "__main__":
    print("Running generator...")
    main()
