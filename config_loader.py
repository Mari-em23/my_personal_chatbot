# config_loader.py
def load_config():
    mission = ""
    rules = ""
    
    try:
        with open("configuration_data/mission.txt", "r", encoding="utf-8") as f:
            mission = f.read().strip()
    except FileNotFoundError:
        pass
    
    try:
        with open("configuration_data/rules.txt", "r", encoding="utf-8") as f:
            rules = f.read().strip()
    except FileNotFoundError:
        pass
    
    return mission, rules