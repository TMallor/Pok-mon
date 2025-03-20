import random
from pokemon import Pokemon
from move import Move

class Battle:
    def __init__(self, player_team, opponent_team):
        self.player_team = player_team
        self.opponent_team = opponent_team
        self.player_active = player_team[0] if player_team else None
        self.opponent_active = opponent_team[0] if opponent_team else None
        self.weather = None
        self.turn_count = 0
        
        # Type effectiveness chart (simplified)
        self.type_chart = {
            "normal": {"rock": 0.5, "ghost": 0, "steel": 0.5},
            "fire": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2},
            "water": {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5},
            "electric": {"water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5},
            "grass": {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5},
            "ice": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5},
            "fighting": {"normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5},
            "poison": {"grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0, "fairy": 2},
            "ground": {"fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2},
            "flying": {"electric": 0.5, "grass": 2, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5},
            "psychic": {"fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5},
            "bug": {"fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5, "dark": 2, "steel": 0.5, "fairy": 0.5},
            "rock": {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5},
            "ghost": {"normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5},
            "dragon": {"dragon": 2, "steel": 0.5, "fairy": 0},
            "dark": {"fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "fairy": 0.5},
            "steel": {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5, "fairy": 2},
            "fairy": {"fighting": 2, "poison": 0.5, "bug": 0.5, "dragon": 2, "dark": 2, "steel": 0.5}
        }
    
    def calculate_type_effectiveness(self, move_type, defender_types):
        effectiveness = 1.0
        if isinstance(defender_types, list):
            for d_type in defender_types:
                if move_type in self.type_chart and d_type in self.type_chart[move_type]:
                    effectiveness *= self.type_chart[move_type][d_type]
        else:  # Single type
            if move_type in self.type_chart and defender_types in self.type_chart[move_type]:
                effectiveness = self.type_chart[move_type][defender_types]
        return effectiveness
    
    def calculate_damage(self, attacker, defender, move):
        # Skip damage calculation for status moves
        if move.category == "status":
            return 0
            
        # Base damage formula
        level = attacker.level
        
        # Use the appropriate attack and defense stats based on move category
        if move.category == "physical":
            attack = attacker.calculate_stat("attack")
            defense = defender.calculate_stat("defense")
        else:  # Special move
            attack = attacker.calculate_stat("sp_attack")
            defense = defender.calculate_stat("sp_defense")
        
        # Calculate base damage
        base_damage = ((2 * level / 5 + 2) * move.power * attack / defense) / 50 + 2
        
        # Critical hit (1/16 chance, 1.5x damage)
        critical = 1.5 if random.randint(1, 16) == 1 else 1.0
        
        # Random factor (between 0.85 and 1.0)
        random_factor = random.uniform(0.85, 1.0)
        
        # STAB (Same Type Attack Bonus)
        stab = 1.5 if move.type in (attacker.type if isinstance(attacker.type, list) else [attacker.type]) else 1.0
        
        # Type effectiveness
        type_effectiveness = self.calculate_type_effectiveness(move.type, defender.type)
        
        # Weather effects
        weather_modifier = 1.0
        if self.weather == "sunny":
            if move.type == "fire":
                weather_modifier = 1.5
            elif move.type == "water":
                weather_modifier = 0.5
        elif self.weather == "rain":
            if move.type == "water":
                weather_modifier = 1.5
            elif move.type == "fire":
                weather_modifier = 0.5
        
        # Final damage calculation
        final_damage = int(base_damage * critical * random_factor * stab * type_effectiveness * weather_modifier)
        
        return max(1, final_damage)  # Minimum 1 damage
    
    def execute_turn(self, player_move_index, player_switch_index=None):
        """Execute a single turn of battle."""
        self.turn_count += 1
        
        # Handle player switching Pokémon
        if player_switch_index is not None and 0 <= player_switch_index < len(self.player_team):
            if not self.player_team[player_switch_index].is_fainted():
                self.player_active = self.player_team[player_switch_index]
                player_first = False  # Switching takes a turn
            else:
                return f"{self.player_team[player_switch_index].name} est K.O. et ne peut pas combattre!"
        
        # Get player's selected move
        elif player_move_index is not None and 0 <= player_move_index < len(self.player_active.moves):
            player_move = self.player_active.moves[player_move_index]
            
            # Check if the move has PP
            if player_move.current_pp <= 0:
                return f"{player_move.name} n'a plus de PP!"
                
            # Select opponent's move (random)
            opponent_moves = [m for m in self.opponent_active.moves if m.current_pp > 0]
            if not opponent_moves:
                opponent_move = None
                return "L'adversaire n'a plus de PP pour aucune attaque!"
            else:
                opponent_move = random.choice(opponent_moves)
            
            # Determine which Pokémon goes first based on speed
            player_speed = self.player_active.calculate_stat("speed")
            opponent_speed = self.opponent_active.calculate_stat("speed")
            
            # Speed tie is broken randomly
            if player_speed == opponent_speed:
                player_first = random.choice([True, False])
            else:
                player_first = player_speed > opponent_speed
                
            # Execute moves in order
            if player_first:
                player_result = self._execute_move(self.player_active, self.opponent_active, player_move)
                
                # Only execute opponent's move if they're not fainted
                if not self.opponent_active.is_fainted() and opponent_move:
                    opponent_result = self._execute_move(self.opponent_active, self.player_active, opponent_move)
                else:
                    opponent_result = f"{self.opponent_active.name} est K.O.!"
                    
                # Check if all opponent's Pokémon fainted
                if all(p.is_fainted() for p in self.opponent_team):
                    return f"{player_result}\n{opponent_result}\nTous les Pokémon adverses sont K.O. Vous avez gagné!"
                
                return f"{player_result}\n{opponent_result}"
            else:
                opponent_result = self._execute_move(self.opponent_active, self.player_active, opponent_move)
                
                # Only execute player's move if they're not fainted
                if not self.player_active.is_fainted():
                    player_result = self._execute_move(self.player_active, self.opponent_active, player_move)
                else:
                    player_result = f"{self.player_active.name} est K.O.!"
                    
                # Check if all player's Pokémon fainted
                if all(p.is_fainted() for p in self.player_team):
                    return f"{opponent_result}\n{player_result}\nTous vos Pokémon sont K.O. Vous avez perdu!"
                
                return f"{opponent_result}\n{player_result}"
        else:
            return "Choix de mouvement ou de changement invalide!"

    def _execute_move(self, attacker, defender, move):
        """Execute a single move and return the result as text."""
        # Use up a PP
        move.use()
        
        # Check for accuracy
        accuracy_check = random.randint(1, 100)
        if accuracy_check > move.accuracy:
            return f"{attacker.name} rate son attaque {move.name}!"
        
        # Calculate damage for non-status moves
        if move.category != "status":
            damage = self.calculate_damage(attacker, defender, move)
            defender.take_damage(damage)
            
            # Determine effectiveness message
            type_effectiveness = self.calculate_type_effectiveness(move.type, defender.type)
            if type_effectiveness > 1:
                effectiveness_msg = "C'est super efficace!"
            elif type_effectiveness == 0:
                effectiveness_msg = "Ça n'affecte pas le Pokémon adverse..."
            elif type_effectiveness < 1:
                effectiveness_msg = "Ce n'est pas très efficace..."
            else:
                effectiveness_msg = ""
                
            result = f"{attacker.name} utilise {move.name}! {effectiveness_msg} {damage} points de dégâts!"
            
            if defender.is_fainted():
                result += f" {defender.name} est K.O.!"
        else:
            # Handle status moves
            result = f"{attacker.name} utilise {move.name}!"
            
            # Apply status effects if applicable
            if move.status_effect and random.randint(1, 100) <= move.status_effect["chance"]:
                defender.apply_status(move.status_effect["status"])
                result += f" {defender.name} est maintenant {move.status_effect['status']}!"
                
            # Apply stat changes if applicable
            if move.stat_changes and random.randint(1, 100) <= move.stat_changes["chance"]:
                target = defender if move.stat_changes["target"] == "opponent" else attacker
                for stat, change in move.stat_changes["changes"].items():
                    if stat in target.stat_stages:
                        # Constrain stat stages to be between -6 and +6
                        target.stat_stages[stat] = max(-6, min(6, target.stat_stages[stat] + change))
                        
                        if change > 0:
                            result += f" {target.name} voit sa stat {stat} augmenter!"
                        else:
                            result += f" {target.name} voit sa stat {stat} diminuer!"
            
            # Apply weather effects if applicable
            if move.weather_effect:
                self.weather = move.weather_effect
                weather_name = {
                    "sunny": "ensoleillé",
                    "rain": "pluvieux",
                    "hail": "grêle"
                }.get(move.weather_effect, move.weather_effect)
                result += f" Le temps est maintenant {weather_name}!"
                
        return result
    
    def apply_status_effects(self):
        """Apply status effects at the end of a turn."""
        results = []
        
        # Apply status effects to player's Pokémon
        if self.player_active and not self.player_active.is_fainted():
            status_result = self._apply_status_effect(self.player_active)
            if status_result:
                results.append(status_result)
                
        # Apply status effects to opponent's Pokémon
        if self.opponent_active and not self.opponent_active.is_fainted():
            status_result = self._apply_status_effect(self.opponent_active)
            if status_result:
                results.append(status_result)
                
        return "\n".join(results) if results else "Aucun effet de statut appliqué."
    
    def _apply_status_effect(self, pokemon):
        """Apply status effect to a single Pokémon."""
        if not pokemon.status:
            return None
            
        result = None
        
        if pokemon.status == "burn":
            damage = max(1, pokemon.max_hp // 8)
            pokemon.take_damage(damage)
            result = f"{pokemon.name} perd {damage} PV à cause de sa brûlure!"
            
        elif pokemon.status == "poison":
            damage = max(1, pokemon.max_hp // 8)
            pokemon.take_damage(damage)
            result = f"{pokemon.name} perd {damage} PV à cause du poison!"
            
        elif pokemon.status == "bad_poison":
            # Bad poison damage increases each turn
            damage = max(1, pokemon.max_hp * (self.turn_count % 16) // 16)
            pokemon.take_damage(damage)
            result = f"{pokemon.name} perd {damage} PV à cause du poison violent!"
            
        elif pokemon.status == "paralysis":
            # 25% chance of not moving due to paralysis is handled during move execution
            pass
            
        elif pokemon.status == "sleep":
            # 1/3 chance of waking up
            if random.randint(1, 3) == 1:
                pokemon.cure_status()
                result = f"{pokemon.name} se réveille!"
                
        elif pokemon.status == "freeze":
            # 20% chance of thawing
            if random.randint(1, 5) == 1:
                pokemon.cure_status()
                result = f"{pokemon.name} n'est plus gelé!"
                
        # Check if the Pokémon fainted from status effects
        if pokemon.is_fainted():
            result = f"{result}\n{pokemon.name} est K.O. à cause de son statut!"
            
        return result
    
    def get_battle_state(self):
        """Get the current state of the battle."""
        player_pokemon_info = []
        for pokemon in self.player_team:
            pokemon_info = {
                "name": pokemon.name,
                "current_hp": pokemon.current_hp,
                "max_hp": pokemon.max_hp,
                "level": pokemon.level,
                "status": pokemon.status,
                "active": pokemon == self.player_active
            }
            player_pokemon_info.append(pokemon_info)
            
        opponent_pokemon_info = []
        for pokemon in self.opponent_team:
            pokemon_info = {
                "name": pokemon.name,
                "current_hp": pokemon.current_hp,
                "max_hp": pokemon.max_hp,
                "level": pokemon.level,
                "status": pokemon.status,
                "active": pokemon == self.opponent_active
            }
            opponent_pokemon_info.append(pokemon_info)
            
        # Get active Pokémon moves
        player_moves = []
        if self.player_active:
            for move in self.player_active.moves:
                move_info = {
                    "name": move.name,
                    "type": move.type,
                    "category": move.category,
                    "power": move.power,
                    "accuracy": move.accuracy,
                    "pp": f"{move.current_pp}/{move.max_pp}"
                }
                player_moves.append(move_info)
                
        return {
            "player_team": player_pokemon_info,
            "opponent_team": opponent_pokemon_info,
            "player_moves": player_moves,
            "weather": self.weather,
            "turn_count": self.turn_count
        } 