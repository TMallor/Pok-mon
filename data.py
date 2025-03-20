from pokemon import Pokemon
from move import Move

def create_move_database():
    """Create a database of moves."""
    moves = {
        # Format: "move_name": Move(name, type, category, power, accuracy, pp)
        # Physical moves
        "tackle": Move("Charge", "normal", "physical", 40, 100, 35),
        "scratch": Move("Griffe", "normal", "physical", 40, 100, 35),
        "quick_attack": Move("Vive-Attaque", "normal", "physical", 40, 100, 30),
        "wing_attack": Move("Cru-Aile", "flying", "physical", 60, 100, 35),
        "earthquake": Move("Séisme", "ground", "physical", 100, 100, 10),
        "rock_slide": Move("Éboulement", "rock", "physical", 75, 90, 10),
        "iron_tail": Move("Queue de Fer", "steel", "physical", 100, 75, 15),
        "crunch": Move("Mâchouille", "dark", "physical", 80, 100, 15),
        "extreme_speed": Move("Vitesse Extrême", "normal", "physical", 80, 100, 5),
        "aqua_tail": Move("Hydroqueue", "water", "physical", 90, 90, 10),
        "fire_punch": Move("Poing de Feu", "fire", "physical", 75, 100, 15),
        "ice_punch": Move("Poing de Glace", "ice", "physical", 75, 100, 15),
        "thunder_punch": Move("Poing Éclair", "electric", "physical", 75, 100, 15),
        
        # Special moves
        "water_gun": Move("Pistolet à O", "water", "special", 40, 100, 25),
        "ember": Move("Flammèche", "fire", "special", 40, 100, 25),
        "thundershock": Move("Éclair", "electric", "special", 40, 100, 30),
        "confusion": Move("Choc Mental", "psychic", "special", 50, 100, 25),
        "flamethrower": Move("Lance-Flammes", "fire", "special", 90, 100, 15),
        "hydro_pump": Move("Hydrocanon", "water", "special", 110, 80, 5),
        "thunder": Move("Tonnerre", "electric", "special", 110, 70, 10),
        "psychic": Move("Psyko", "psychic", "special", 90, 100, 10),
        "ice_beam": Move("Laser Glace", "ice", "special", 90, 100, 10),
        "solar_beam": Move("Lance-Soleil", "grass", "special", 120, 100, 10),
        "hyper_beam": Move("Ultralaser", "normal", "special", 150, 90, 5),
        "shadow_ball": Move("Ball'Ombre", "ghost", "special", 80, 100, 15),
        "dragon_pulse": Move("Dracochoc", "dragon", "special", 85, 100, 10),
        
        # Status moves
        "growl": Move("Rugissement", "normal", "status", 0, 100, 40),
        "tail_whip": Move("Mimi-Queue", "normal", "status", 0, 100, 30),
        "leer": Move("Groz'Yeux", "normal", "status", 0, 100, 30),
        "sand_attack": Move("Jet de Sable", "ground", "status", 0, 100, 15),
        "thunder_wave": Move("Onde de Choc", "electric", "status", 0, 90, 20),
        "toxic": Move("Toxik", "poison", "status", 0, 90, 10),
        "will_o_wisp": Move("Feu Follet", "fire", "status", 0, 85, 15),
        "swords_dance": Move("Danse Lames", "normal", "status", 0, 100, 20),
        "calm_mind": Move("Plénitude", "psychic", "status", 0, 100, 20),
        "sunny_day": Move("Zénith", "fire", "status", 0, 100, 5),
        "rain_dance": Move("Danse Pluie", "water", "status", 0, 100, 5),
        "hail": Move("Grêle", "ice", "status", 0, 100, 10),
        "protect": Move("Abri", "normal", "status", 0, 100, 10),
    }
    
    # Set status effects for status moves
    moves["thunder_wave"].set_status_effect("paralysis", 100)
    moves["toxic"].set_status_effect("bad_poison", 100)
    moves["will_o_wisp"].set_status_effect("burn", 100)
    
    # Set stat changes for stat-changing moves
    moves["growl"].set_stat_changes({"attack": -1}, "opponent", 100)
    moves["tail_whip"].set_stat_changes({"defense": -1}, "opponent", 100)
    moves["leer"].set_stat_changes({"defense": -1}, "opponent", 100)
    moves["sand_attack"].set_stat_changes({"accuracy": -1}, "opponent", 100)
    moves["swords_dance"].set_stat_changes({"attack": 2}, "self", 100)
    moves["calm_mind"].set_stat_changes({"sp_attack": 1, "sp_defense": 1}, "self", 100)
    
    # Set weather effects
    moves["sunny_day"].set_weather_effect("sunny")
    moves["rain_dance"].set_weather_effect("rain")
    moves["hail"].set_weather_effect("hail")
    
    return moves

def create_pokemon_database(moves):
    """Create a database of Pokémon with moves."""
    pokemon = {
        # Format: "pokemon_name": Pokemon(name, type, level, hp, attack, defense, sp_attack, sp_defense, speed)
        "pikachu": Pokemon("Pikachu", "electric", 25, 35, 55, 40, 50, 50, 90),
        "charizard": Pokemon("Charizard", ["fire", "flying"], 36, 78, 84, 78, 109, 85, 100),
        "blastoise": Pokemon("Blastoise", "water", 36, 79, 83, 100, 85, 105, 78),
        "venusaur": Pokemon("Venusaur", ["grass", "poison"], 36, 80, 82, 83, 100, 100, 80),
        "jolteon": Pokemon("Jolteon", "electric", 30, 65, 65, 60, 110, 95, 130),
        "alakazam": Pokemon("Alakazam", "psychic", 30, 55, 50, 45, 135, 95, 120),
        "gengar": Pokemon("Gengar", ["ghost", "poison"], 30, 60, 65, 60, 130, 75, 110),
        "dragonite": Pokemon("Dragonite", ["dragon", "flying"], 35, 91, 134, 95, 100, 100, 80),
        "snorlax": Pokemon("Snorlax", "normal", 30, 160, 110, 65, 65, 110, 30),
        "tyranitar": Pokemon("Tyranitar", ["rock", "dark"], 35, 100, 134, 110, 95, 100, 61),
    }
    
    # Assign moves to Pokémon
    pokemon["pikachu"].add_move(moves["thundershock"])
    pokemon["pikachu"].add_move(moves["quick_attack"])
    pokemon["pikachu"].add_move(moves["thunder_wave"])
    pokemon["pikachu"].add_move(moves["thunder"])
    
    pokemon["charizard"].add_move(moves["flamethrower"])
    pokemon["charizard"].add_move(moves["dragon_pulse"])
    pokemon["charizard"].add_move(moves["wing_attack"])
    pokemon["charizard"].add_move(moves["sunny_day"])
    
    pokemon["blastoise"].add_move(moves["water_gun"])
    pokemon["blastoise"].add_move(moves["hydro_pump"])
    pokemon["blastoise"].add_move(moves["ice_beam"])
    pokemon["blastoise"].add_move(moves["rain_dance"])
    
    pokemon["venusaur"].add_move(moves["solar_beam"])
    pokemon["venusaur"].add_move(moves["toxic"])
    pokemon["venusaur"].add_move(moves["swords_dance"])
    pokemon["venusaur"].add_move(moves["sunny_day"])
    
    pokemon["jolteon"].add_move(moves["thundershock"])
    pokemon["jolteon"].add_move(moves["thunder"])
    pokemon["jolteon"].add_move(moves["thunder_wave"])
    pokemon["jolteon"].add_move(moves["quick_attack"])
    
    pokemon["alakazam"].add_move(moves["psychic"])
    pokemon["alakazam"].add_move(moves["shadow_ball"])
    pokemon["alakazam"].add_move(moves["calm_mind"])
    pokemon["alakazam"].add_move(moves["thunder_punch"])
    
    pokemon["gengar"].add_move(moves["shadow_ball"])
    pokemon["gengar"].add_move(moves["psychic"])
    pokemon["gengar"].add_move(moves["toxic"])
    pokemon["gengar"].add_move(moves["will_o_wisp"])
    
    pokemon["dragonite"].add_move(moves["dragon_pulse"])
    pokemon["dragonite"].add_move(moves["extreme_speed"])
    pokemon["dragonite"].add_move(moves["thunder_punch"])
    pokemon["dragonite"].add_move(moves["ice_punch"])
    
    pokemon["snorlax"].add_move(moves["earthquake"])
    pokemon["snorlax"].add_move(moves["crunch"])
    pokemon["snorlax"].add_move(moves["thunder_punch"])
    pokemon["snorlax"].add_move(moves["ice_punch"])
    
    pokemon["tyranitar"].add_move(moves["crunch"])
    pokemon["tyranitar"].add_move(moves["rock_slide"])
    pokemon["tyranitar"].add_move(moves["earthquake"])
    pokemon["tyranitar"].add_move(moves["fire_punch"])
    
    return pokemon

# Initialize databases
MOVES = create_move_database()
POKEMON = create_pokemon_database(MOVES) 