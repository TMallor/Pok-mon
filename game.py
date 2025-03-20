import random
import time
import os
from data import POKEMON
from battle import Battle
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

# Type colors mapping
TYPE_COLORS = {
    "normal": Fore.WHITE,
    "fire": Fore.RED,
    "water": Fore.BLUE,
    "electric": Fore.YELLOW,
    "grass": Fore.GREEN,
    "ice": Fore.CYAN,
    "fighting": Fore.RED + Style.BRIGHT,
    "poison": Fore.MAGENTA,
    "ground": Fore.YELLOW + Style.DIM,
    "flying": Fore.CYAN + Style.BRIGHT,
    "psychic": Fore.MAGENTA + Style.BRIGHT,
    "bug": Fore.GREEN + Style.BRIGHT,
    "rock": Fore.YELLOW + Style.DIM,
    "ghost": Fore.MAGENTA + Style.DIM,
    "dragon": Fore.BLUE + Style.BRIGHT,
    "dark": Fore.BLACK + Style.BRIGHT,
    "steel": Fore.WHITE + Style.DIM,
    "fairy": Fore.MAGENTA + Style.BRIGHT
}

# Traduction des types en français
TYPE_TRANSLATION = {
    "normal": "normal",
    "fire": "feu",
    "water": "eau",
    "electric": "électrique",
    "grass": "plante",
    "ice": "glace",
    "fighting": "combat",
    "poison": "poison",
    "ground": "sol",
    "flying": "vol",
    "psychic": "psy",
    "bug": "insecte",
    "rock": "roche",
    "ghost": "spectre",
    "dragon": "dragon",
    "dark": "ténèbres",
    "steel": "acier",
    "fairy": "fée"
}

# Traduction des catégories d'attaques
CATEGORY_TRANSLATION = {
    "physical": "physique",
    "special": "spéciale",
    "status": "statut"
}

class PokemonGame:
    def __init__(self):
        self.available_pokemon = list(POKEMON.values())
        self.player_team = []
        self.opponent_team = []
        self.battle = None
        self.multiplayer = False
        self.current_player = 1  # Pour le mode multijoueur : 1 = joueur 1, 2 = joueur 2
        
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_title(self):
        """Display the game title."""
        title = f"""{Fore.YELLOW + Style.BRIGHT}
        ____        __                                ____        __  __  __     
       / __ \____  / /_____  ____ ___  ____  ____    / __ )____ _/ /_/ /_/ /__   
      / /_/ / __ \/ //_/ _ \/ __ `__ \/ __ \/ __ \  / __  / __ `/ __/ __/ / _ \  
     / ____/ /_/ / ,< /  __/ / / / / / /_/ / / / / / /_/ / /_/ / /_/ /_/ /  __/  
    /_/    \____/_/|_|\___/_/ /_/ /_/\____/_/ /_(_)_____/\__,_/\__/\__/_/\___/   
                                                                        
                               {Fore.RED}Simulator{Style.RESET_ALL}
    """
        print(title)
        
    def display_hp_bar(self, current_hp, max_hp, width=20, player=True):
        """Display a colored HP bar."""
        ratio = current_hp / max_hp
        bar_fill = int(ratio * width)
        
        if ratio > 0.5:
            color = Fore.GREEN
        elif ratio > 0.2:
            color = Fore.YELLOW
        else:
            color = Fore.RED
            
        bar = f"{color}{'█' * bar_fill}{Fore.BLACK}{'█' * (width - bar_fill)}{Style.RESET_ALL}"
        percentage = int(ratio * 100)
        
        if player:
            return f"{bar} {current_hp}/{max_hp} ({percentage}%)"
        else:
            return f"{bar} {current_hp}/{max_hp} ({percentage}%)"
            
    def get_type_color(self, type_name):
        """Get the color for a specific type."""
        return TYPE_COLORS.get(type_name, Fore.WHITE)
        
    def colorize_type(self, type_name):
        """Return a type name with appropriate color."""
        color = self.get_type_color(type_name)
        translated_type = TYPE_TRANSLATION.get(type_name, type_name)
        return f"{color}{translated_type}{Style.RESET_ALL}"
        
    def select_game_mode(self):
        """Select game mode (solo or multiplayer)."""
        self.clear_screen()
        self.display_title()
        
        print(f"\n{Back.BLUE + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        print(f"{Back.BLUE + Fore.WHITE}" + " " * 15 + "SÉLECTION DU MODE DE JEU" + " " * 15 + Style.RESET_ALL)
        print(f"{Back.BLUE + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        
        print(f"\n{Fore.CYAN}Choisissez un mode de jeu:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}" + "-" * 60 + Style.RESET_ALL)
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} {Fore.GREEN}Mode solo{Style.RESET_ALL} - Jouer contre l'ordinateur")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} {Fore.MAGENTA}Mode multijoueur{Style.RESET_ALL} - Jouer contre un ami (sur le même appareil)")
        
        while True:
            try:
                choice = int(input(f"\n{Fore.CYAN}Sélectionnez un mode (1-2): {Style.RESET_ALL}"))
                if choice == 1:
                    self.multiplayer = False
                    print(f"\n{Fore.GREEN}Mode solo sélectionné. Vous jouerez contre l'ordinateur.{Style.RESET_ALL}")
                    time.sleep(1)
                    break
                elif choice == 2:
                    self.multiplayer = True
                    print(f"\n{Fore.MAGENTA}Mode multijoueur sélectionné. Vous jouerez à deux sur le même appareil.{Style.RESET_ALL}")
                    time.sleep(1)
                    break
                else:
                    print(f"{Fore.RED}❌ Veuillez entrer 1 ou 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Veuillez entrer un nombre valide.{Style.RESET_ALL}")

    def select_pokemon(self):
        """Let the player select their Pokémon team."""
        self.clear_screen()
        self.display_title()
        
        print(f"\n{Back.BLUE + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        
        # Modifier le titre selon le mode de jeu et le joueur actuel
        if self.multiplayer:
            print(f"{Back.BLUE + Fore.WHITE}" + f" SÉLECTION DES POKÉMON - JOUEUR {self.current_player} " + Style.RESET_ALL)
        else:
            print(f"{Back.BLUE + Fore.WHITE}" + " " * 15 + "SÉLECTION DES POKÉMON" + " " * 15 + Style.RESET_ALL)
        
        print(f"{Back.BLUE + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        
        print(f"\n{Fore.CYAN}Choisissez 3 Pokémon pour constituer votre équipe:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}" + "-" * 60 + Style.RESET_ALL)
        
        # Display Pokémon with stats in a more readable format
        for i, pokemon in enumerate(self.available_pokemon):
            if isinstance(pokemon.type, list):
                type_display = '/'.join([self.colorize_type(t) for t in pokemon.type])
            else:
                type_display = self.colorize_type(pokemon.type)
                
            name_display = f"{Fore.CYAN + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL}"
            print(f"{Fore.YELLOW}{i+1:2d}.{Style.RESET_ALL} {name_display:18} | Type: {type_display:25} | {Fore.GREEN}HP: {pokemon.max_hp:3d}{Style.RESET_ALL} | {Fore.RED}ATK: {pokemon.attack:3d}{Style.RESET_ALL} | {Fore.BLUE}DEF: {pokemon.defense:3d}{Style.RESET_ALL} | {Fore.MAGENTA}SP.ATK: {pokemon.sp_attack:3d}{Style.RESET_ALL} | {Fore.CYAN}SP.DEF: {pokemon.sp_defense:3d}{Style.RESET_ALL} | {Fore.YELLOW}SPD: {pokemon.speed:3d}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}" + "-" * 60 + Style.RESET_ALL)
        selected_indices = []
        
        while len(selected_indices) < 3:
            try:
                choice = int(input(f"\n{Fore.CYAN}Sélectionnez le Pokémon #{len(selected_indices)+1} (1-{len(self.available_pokemon)}): {Style.RESET_ALL}"))
                if 1 <= choice <= len(self.available_pokemon):
                    if choice-1 not in selected_indices:
                        pokemon = self.available_pokemon[choice-1]
                        print(f"{Fore.GREEN}✓ {pokemon.name} ajouté à votre équipe!{Style.RESET_ALL}")
                        
                        # Display the moves of the selected Pokémon
                        print(f"\n{Fore.CYAN}Attaques de {pokemon.name}:{Style.RESET_ALL}")
                        for j, move in enumerate(pokemon.moves):
                            move_type_color = self.get_type_color(move.type)
                            print(f"  {Fore.YELLOW}{j+1}.{Style.RESET_ALL} {move_type_color}{move.name}{Style.RESET_ALL} (Type: {self.colorize_type(move.type)}, Catégorie: {move.category}, Puissance: {move.power}, Précision: {move.accuracy})")
                        
                        selected_indices.append(choice-1)
                        time.sleep(1)
                    else:
                        print(f"{Fore.RED}❌ Vous avez déjà sélectionné ce Pokémon!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Veuillez entrer un nombre entre 1 et {len(self.available_pokemon)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Veuillez entrer un nombre valide.{Style.RESET_ALL}")
        
        print(f"\n{Back.GREEN + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        print(f"{Back.GREEN + Fore.WHITE}" + " " * 20 + "ÉQUIPE COMPLÈTE!" + " " * 20 + Style.RESET_ALL)
        print(f"{Back.GREEN + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        
        # Create player team
        for index in selected_indices:
            # Create a new instance of the Pokémon to avoid reference issues
            original = self.available_pokemon[index]
            pokemon_copy = POKEMON[original.name.lower()]
            self.player_team.append(pokemon_copy)
        
        print(f"\n{Fore.CYAN}Votre équipe:{Style.RESET_ALL}")
        for i, pokemon in enumerate(self.player_team):
            print(f"{Fore.YELLOW}{i+1}.{Style.RESET_ALL} {Fore.CYAN + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL}")
            
        # En mode multijoueur, on gère la sélection de l'équipe du deuxième joueur
        if self.multiplayer and self.current_player == 1:
            print(f"\n{Fore.MAGENTA}Au tour du Joueur 2 de sélectionner son équipe.{Style.RESET_ALL}")
            time.sleep(2)
            self.current_player = 2
            
            # Sauvegarder l'équipe du joueur 1
            self.player1_team = self.player_team.copy()
            self.player_team = []
            
            # Relancer la sélection pour le joueur 2
            self.select_pokemon()
            return
        
        # En mode solo, l'adversaire choisit aléatoirement
        if not self.multiplayer:
            print(f"\n{Fore.MAGENTA}L'adversaire sélectionne son équipe...{Style.RESET_ALL}")
            time.sleep(2)
            
            # Create opponent team (random selection)
            available_for_opponent = [p for i, p in enumerate(self.available_pokemon) if i not in selected_indices]
            opponent_selection = random.sample(available_for_opponent, 3)
            
            for pokemon in opponent_selection:
                # Create a new instance of the Pokémon
                pokemon_copy = POKEMON[pokemon.name.lower()]
                self.opponent_team.append(pokemon_copy)
            
            print(f"\n{Fore.RED}Équipe adverse:{Style.RESET_ALL}")
            for i, pokemon in enumerate(self.opponent_team):
                print(f"{Fore.YELLOW}{i+1}.{Style.RESET_ALL} {Fore.RED + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL}")
        else:
            # En mode multijoueur, l'équipe du joueur 2 devient l'équipe adverse
            self.opponent_team = self.player_team.copy()
            self.player_team = self.player1_team.copy()
            
            print(f"\n{Fore.CYAN}Équipe du Joueur 1:{Style.RESET_ALL}")
            for i, pokemon in enumerate(self.player_team):
                print(f"{Fore.YELLOW}{i+1}.{Style.RESET_ALL} {Fore.CYAN + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL}")
                
            print(f"\n{Fore.RED}Équipe du Joueur 2:{Style.RESET_ALL}")
            for i, pokemon in enumerate(self.opponent_team):
                print(f"{Fore.YELLOW}{i+1}.{Style.RESET_ALL} {Fore.RED + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL}")
            
        # Initialize battle
        self.battle = Battle(self.player_team, self.opponent_team)
        
        print(f"\n{Fore.CYAN}Appuyez sur Entrée pour commencer le combat...{Style.RESET_ALL}")
        input()
        
    def display_battle_state(self):
        """Display the current state of the battle."""
        self.clear_screen()
        
        # Modifier le titre en mode multijoueur
        if self.multiplayer:
            print(f"\n{Back.RED + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
            print(f"{Back.RED + Fore.WHITE}" + " " * 15 + f"BATAILLE POKÉMON - JOUEUR {self.current_player}" + " " * 15 + Style.RESET_ALL)
            print(f"{Back.RED + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        else:
            print(f"\n{Back.RED + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
            print(f"{Back.RED + Fore.WHITE}" + " " * 20 + "BATAILLE POKÉMON" + " " * 20 + Style.RESET_ALL)
            print(f"{Back.RED + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        
        # Display player's active Pokémon
        player_active = self.battle.player_active
        if isinstance(player_active.type, list):
            player_type_display = '/'.join([self.colorize_type(t) for t in player_active.type])
        else:
            player_type_display = self.colorize_type(player_active.type)
            
        print(f"\n{Fore.CYAN}➤ Votre Pokémon actif: {Fore.CYAN + Style.BRIGHT}{player_active.name}{Style.RESET_ALL} (Nv. {player_active.level}) - Type: {player_type_display}")
        print(f"  {Fore.GREEN}PV: {self.display_hp_bar(player_active.current_hp, player_active.max_hp)}")
        
        status_color = Fore.GREEN if not player_active.status else Fore.RED
        status_text = "Normal"
        if player_active.status:
            status_map = {
                "burn": "Brûlé",
                "poison": "Empoisonné",
                "bad_poison": "Gravement empoisonné",
                "paralysis": "Paralysé",
                "sleep": "Endormi",
                "freeze": "Gelé"
            }
            status_text = status_map.get(player_active.status, player_active.status)
        print(f"  {Fore.YELLOW}Statut: {status_color}{status_text}{Style.RESET_ALL}")
        
        # Display opponent's active Pokémon
        opponent_active = self.battle.opponent_active
        if isinstance(opponent_active.type, list):
            opponent_type_display = '/'.join([self.colorize_type(t) for t in opponent_active.type])
        else:
            opponent_type_display = self.colorize_type(opponent_active.type)
            
        print(f"\n{Fore.RED}➤ Pokémon adverse: {Fore.RED + Style.BRIGHT}{opponent_active.name}{Style.RESET_ALL} (Nv. {opponent_active.level}) - Type: {opponent_type_display}")
        print(f"  {Fore.GREEN}PV: {self.display_hp_bar(opponent_active.current_hp, opponent_active.max_hp, player=False)}")
        
        status_color = Fore.GREEN if not opponent_active.status else Fore.RED
        status_text = "Normal"
        if opponent_active.status:
            status_map = {
                "burn": "Brûlé",
                "poison": "Empoisonné",
                "bad_poison": "Gravement empoisonné",
                "paralysis": "Paralysé",
                "sleep": "Endormi",
                "freeze": "Gelé"
            }
            status_text = status_map.get(opponent_active.status, opponent_active.status)
        print(f"  {Fore.YELLOW}Statut: {status_color}{status_text}{Style.RESET_ALL}")
        
        # Display weather
        if self.battle.weather:
            weather_color = Fore.YELLOW
            weather_text = self.battle.weather
            if self.battle.weather == "sunny":
                weather_color = Fore.RED
                weather_text = "Ensoleillé"
            elif self.battle.weather == "rain":
                weather_color = Fore.BLUE
                weather_text = "Pluie"
            elif self.battle.weather == "hail":
                weather_color = Fore.CYAN
                weather_text = "Grêle"
                
            print(f"\n{Fore.YELLOW}➤ Météo actuelle: {weather_color}{weather_text}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}" + "-" * 60 + Style.RESET_ALL)
        # Display moves
        print(f"\n{Fore.CYAN}➤ Vos attaques disponibles:{Style.RESET_ALL}")
        for i, move in enumerate(player_active.moves):
            pp_status = f"{Fore.GREEN}✓" if move.current_pp > 0 else f"{Fore.RED}✗"
            move_type_color = self.get_type_color(move.type)
            translated_type = TYPE_TRANSLATION.get(move.type, move.type)
            translated_category = CATEGORY_TRANSLATION.get(move.category, move.category)
            print(f"  {Fore.YELLOW}{i+1}.{Style.RESET_ALL} {move_type_color}{move.name}{Style.RESET_ALL} [{pp_status}{Style.RESET_ALL}] (Type: {self.colorize_type(move.type)}, Catégorie: {translated_category}, Puissance: {move.power}, Précision: {move.accuracy}, PP: {move.current_pp}/{move.max_pp})")
            
        # Display team
        print(f"\n{Fore.CYAN}➤ Votre équipe:{Style.RESET_ALL}")
        for i, pokemon in enumerate(self.battle.player_team):
            active_marker = f" {Fore.GREEN}[ACTIF]{Style.RESET_ALL}" if pokemon == player_active else ""
            fainted_marker = f" {Fore.RED}[K.O.]{Style.RESET_ALL}" if pokemon.is_fainted() else ""
            hp_bar = self.display_hp_bar(pokemon.current_hp, pokemon.max_hp, width=10)
            print(f"  {Fore.YELLOW}{i+1}.{Style.RESET_ALL} {Fore.CYAN + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL} - PV: {hp_bar}{active_marker}{fainted_marker}")
        
        print(f"\n{Fore.CYAN}" + "-" * 60 + Style.RESET_ALL)
        
    def display_move_result(self, result):
        """Display the result of a move."""
        # Colorize the result based on keywords
        colored_result = result
        
        # Highlight effectiveness messages
        colored_result = colored_result.replace("C'est super efficace!", f"{Fore.GREEN}C'est super efficace!{Style.RESET_ALL}")
        colored_result = colored_result.replace("Ce n'est pas très efficace...", f"{Fore.YELLOW}Ce n'est pas très efficace...{Style.RESET_ALL}")
        colored_result = colored_result.replace("Ça n'affecte pas le Pokémon adverse...", f"{Fore.RED}Ça n'affecte pas le Pokémon adverse...{Style.RESET_ALL}")
        
        # Highlight K.O. messages
        if "K.O." in colored_result:
            parts = colored_result.split(" est K.O.!")
            if len(parts) > 1:
                pokemon_name = parts[0].split(" ")[-1]
                colored_result = colored_result.replace(f"{pokemon_name} est K.O.!", f"{pokemon_name} est {Fore.RED}K.O.!{Style.RESET_ALL}")
        
        # Colorize Pokémon names if found in result
        for pokemon in self.battle.player_team:
            colored_result = colored_result.replace(f"{pokemon.name} utilise", f"{Fore.CYAN + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL} utilise")
            
        for pokemon in self.battle.opponent_team:
            colored_result = colored_result.replace(f"{pokemon.name} utilise", f"{Fore.RED + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL} utilise")
        
        print("\n" + colored_result)
        time.sleep(2)  # Pause to let the player read the result
        
    def player_turn(self):
        """Handle the player's turn."""
        # Si en mode multijoueur, modifier l'affichage selon le joueur actuel
        self.display_battle_state()
        
        player_text = ""
        if self.multiplayer:
            player_text = f" - JOUEUR {self.current_player}"
            
        print(f"\n{Back.CYAN + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        print(f"{Back.CYAN + Fore.WHITE}" + " " * 20 + f"C'EST VOTRE TOUR{player_text}!" + " " * 20 + Style.RESET_ALL)
        print(f"{Back.CYAN + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        print(f"\n{Fore.CYAN}➤ Que voulez-vous faire?{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}1. {Fore.RED}👊 ATTAQUER{Style.RESET_ALL} - Utiliser une attaque")
        print(f"  {Fore.YELLOW}2. {Fore.BLUE}🔄 CHANGER{Style.RESET_ALL} - Changer de Pokémon")
        
        while True:
            try:
                choice = int(input(f"\n{Fore.CYAN}Entrez votre choix (1-2): {Style.RESET_ALL}"))
                if choice == 1:  # Fight
                    move_index = self.choose_move()
                    if move_index is not None:
                        # En mode multijoueur, on change de joueur après son tour
                        if self.multiplayer:
                            result = self.battle.execute_turn(move_index)
                            self.display_move_result(result)
                            
                            # Basculer le joueur actif
                            self.current_player = 1 if self.current_player == 2 else 2
                        else:
                            # Mode solo, comme avant
                            result = self.battle.execute_turn(move_index)
                            self.display_move_result(result)
                        
                        # Apply status effects at the end of the turn
                        status_result = self.battle.apply_status_effects()
                        if status_result != "Aucun effet de statut appliqué.":
                            status_result = status_result.replace("perd", f"{Fore.RED}perd{Style.RESET_ALL}")
                            for pokemon in self.battle.player_team + self.battle.opponent_team:
                                status_result = status_result.replace(pokemon.name, f"{Fore.CYAN + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL}")
                            print("\n" + status_result)
                            time.sleep(2)
                        
                        # Check if battle is over
                        if self.check_battle_end():
                            return
                            
                        # Check if player's active Pokémon fainted
                        if self.battle.player_active.is_fainted():
                            if not all(p.is_fainted() for p in self.battle.player_team):
                                print(f"\n{Fore.RED}{self.battle.player_active.name} est K.O.! Choisissez un autre Pokémon.{Style.RESET_ALL}")
                                self.switch_pokemon(forced=True)
                            else:
                                return  # All player's Pokémon fainted
                        break
                elif choice == 2:  # Switch
                    if self.switch_pokemon():
                        # En mode multijoueur, l'adversaire (autre joueur) ne joue pas quand on change
                        if not self.multiplayer:
                            # Apply status effects
                            status_result = self.battle.apply_status_effects()
                            if status_result != "Aucun effet de statut appliqué.":
                                status_result = status_result.replace("perd", f"{Fore.RED}perd{Style.RESET_ALL}")
                                for pokemon in self.battle.player_team + self.battle.opponent_team:
                                    status_result = status_result.replace(pokemon.name, f"{Fore.CYAN + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL}")
                                print("\n" + status_result)
                                time.sleep(2)
                        else:
                            # En mode multijoueur, changer le joueur actif
                            self.current_player = 1 if self.current_player == 2 else 2
                        
                        # Check if battle is over
                        if self.check_battle_end():
                            return
                        break
                else:
                    print(f"{Fore.RED}Veuillez entrer 1 ou 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
                
    def choose_move(self):
        """Let the player choose a move."""
        print(f"\n{Fore.CYAN}" + "-" * 60 + Style.RESET_ALL)
        print(f"{Fore.CYAN}➤ Choisissez une attaque:{Style.RESET_ALL}")
        
        # Display moves again for clarity
        for i, move in enumerate(self.battle.player_active.moves):
            pp_status = f"{Fore.GREEN}✓" if move.current_pp > 0 else f"{Fore.RED}✗"
            move_type_color = self.get_type_color(move.type)
            print(f"  {Fore.YELLOW}{i+1}.{Style.RESET_ALL} {move_type_color}{move.name}{Style.RESET_ALL} [{pp_status}{Style.RESET_ALL}] (Type: {self.colorize_type(move.type)}, PP: {move.current_pp}/{move.max_pp})")
            
        while True:
            try:
                move_index = int(input(f"\n{Fore.CYAN}Choisissez une attaque (1-4): {Style.RESET_ALL}")) - 1
                if 0 <= move_index < len(self.battle.player_active.moves):
                    move = self.battle.player_active.moves[move_index]
                    if move.current_pp > 0:
                        return move_index
                    else:
                        print(f"{Fore.RED}{move.name} n'a plus de PP! Choisissez une autre attaque.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Veuillez entrer un nombre entre 1 et 4.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
        return None
                
    def switch_pokemon(self, forced=False):
        """Let the player switch their active Pokémon."""
        # Display available Pokémon
        print(f"\n{Fore.CYAN}" + "-" * 60 + Style.RESET_ALL)
        print(f"{Fore.CYAN}➤ Choisissez un Pokémon pour remplacer votre Pokémon actif:{Style.RESET_ALL}")
        available_pokemon = []
        
        for i, pokemon in enumerate(self.battle.player_team):
            if not pokemon.is_fainted() and pokemon != self.battle.player_active:
                available_pokemon.append((i, pokemon))
                hp_bar = self.display_hp_bar(pokemon.current_hp, pokemon.max_hp, width=10)
                if isinstance(pokemon.type, list):
                    type_display = '/'.join([self.colorize_type(t) for t in pokemon.type])
                else:
                    type_display = self.colorize_type(pokemon.type)
                print(f"  {Fore.YELLOW}{len(available_pokemon)}.{Style.RESET_ALL} {Fore.CYAN + Style.BRIGHT}{pokemon.name}{Style.RESET_ALL} - Type: {type_display} - HP: {hp_bar}")
                
        if not available_pokemon:
            print(f"{Fore.RED}Aucun Pokémon disponible pour changer!{Style.RESET_ALL}")
            return False
            
        while True:
            try:
                choice = int(input(f"\n{Fore.CYAN}Choisissez un Pokémon (1-{len(available_pokemon)}): {Style.RESET_ALL}"))
                if 1 <= choice <= len(available_pokemon):
                    pokemon_index = available_pokemon[choice-1][0]
                    if forced:
                        self.battle.player_active = self.battle.player_team[pokemon_index]
                        print(f"\n{Fore.GREEN}Go, {Fore.CYAN + Style.BRIGHT}{self.battle.player_active.name}{Fore.GREEN}!{Style.RESET_ALL}")
                        time.sleep(1)
                        return True
                    else:
                        # Le changement de Pokémon
                        old_pokemon = self.battle.player_active.name
                        self.battle.player_active = self.battle.player_team[pokemon_index]
                        print(f"\n{Fore.YELLOW}Vous rappelez {Fore.CYAN + Style.BRIGHT}{old_pokemon}{Fore.YELLOW} et envoyez {Fore.CYAN + Style.BRIGHT}{self.battle.player_active.name}{Fore.YELLOW}!{Style.RESET_ALL}")
                        time.sleep(1)
                        
                        # Tour de l'adversaire après le changement
                        opponent_move_index = random.randrange(len(self.battle.opponent_active.moves))
                        opponent_move = self.battle.opponent_active.moves[opponent_move_index]
                        result = self._execute_move(self.battle.opponent_active, self.battle.player_active, opponent_move)
                        
                        if result:
                            self.display_move_result(result)
                        return True
                else:
                    print(f"{Fore.RED}Veuillez entrer un nombre entre 1 et {len(available_pokemon)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
        return False
        
    def _execute_move(self, attacker, defender, move):
        """Execute a move between two Pokémon and return the result as a string."""
        if move.current_pp <= 0:
            return f"{attacker.name} n'a plus de PP pour {move.name}!"
            
        # Use up a PP
        move.use()
        
        # Check for accuracy
        accuracy_check = random.randint(1, 100)
        if accuracy_check > move.accuracy:
            return f"{attacker.name} utilise {move.name} mais rate sa cible!"
            
        # Calculate damage for non-status moves
        if move.category != "status":
            damage = self.battle.calculate_damage(attacker, defender, move)
            defender.take_damage(damage)
            
            # Determine effectiveness message
            type_effectiveness = self.battle.calculate_type_effectiveness(move.type, defender.type)
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
            
        return result
        
    def check_battle_end(self):
        """Check if the battle has ended."""
        if all(p.is_fainted() for p in self.battle.player_team):
            print(f"\n{Back.RED + Fore.WHITE}Tous vos Pokémon sont K.O. Vous avez perdu!{Style.RESET_ALL}")
            return True
            
        if all(p.is_fainted() for p in self.battle.opponent_team):
            print(f"\n{Back.GREEN + Fore.WHITE}Tous les Pokémon adverses sont K.O. Vous avez gagné!{Style.RESET_ALL}")
            return True
            
        # Check if opponent's active Pokémon fainted
        if self.battle.opponent_active.is_fainted():
            # Find the next non-fainted Pokémon for the opponent
            for pokemon in self.battle.opponent_team:
                if not pokemon.is_fainted():
                    self.battle.opponent_active = pokemon
                    print(f"\n{Fore.RED}L'adversaire envoie {Fore.RED + Style.BRIGHT}{pokemon.name}{Fore.RED}!{Style.RESET_ALL}")
                    time.sleep(1)
                    break
                    
        return False
        
    def play(self):
        """Main game loop."""
        # Sélectionner le mode de jeu
        self.select_game_mode()
        
        # Sélectionner les Pokémon
        self.select_pokemon()
        
        self.clear_screen()
        print(f"\n{Back.RED + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        print(f"{Back.RED + Fore.WHITE}" + " " * 20 + "LA BATAILLE COMMENCE!" + " " * 20 + Style.RESET_ALL)
        print(f"{Back.RED + Fore.WHITE}" + "=" * 60 + Style.RESET_ALL)
        time.sleep(1)
        
        if self.multiplayer:
            print(f"\n{Fore.RED}➤ Le Joueur 2 envoie {Fore.RED + Style.BRIGHT}{self.battle.opponent_active.name}{Fore.RED}!{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}➤ Le Joueur 1 envoie {Fore.CYAN + Style.BRIGHT}{self.battle.player_active.name}{Fore.CYAN}!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}➤ L'adversaire envoie {Fore.RED + Style.BRIGHT}{self.battle.opponent_active.name}{Fore.RED}!{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}➤ À vous de jouer! Go, {Fore.CYAN + Style.BRIGHT}{self.battle.player_active.name}{Fore.CYAN}!{Style.RESET_ALL}")
        
        time.sleep(2)
        
        # Main battle loop
        while True:
            # En mode multijoueur, alterner entre les deux joueurs
            if self.multiplayer:
                # Pour le joueur 1
                if self.current_player == 1:
                    self.player_turn()
                # Pour le joueur 2
                else:
                    # Inverser les équipes pour que le joueur 2 joue
                    self.battle.player_team, self.battle.opponent_team = self.battle.opponent_team, self.battle.player_team
                    self.battle.player_active, self.battle.opponent_active = self.battle.opponent_active, self.battle.player_active
                    
                    self.player_turn()
                    
                    # Remettre les équipes dans le bon ordre après le tour
                    self.battle.player_team, self.battle.opponent_team = self.battle.opponent_team, self.battle.player_team
                    self.battle.player_active, self.battle.opponent_active = self.battle.opponent_active, self.battle.player_active
            else:
                # Mode solo - comme avant
                self.player_turn()
            
            # Check if battle has ended
            if all(p.is_fainted() for p in self.battle.player_team) or all(p.is_fainted() for p in self.battle.opponent_team):
                break
                
        # Afficher le résultat de la bataille
        print(f"\n{Back.YELLOW + Fore.BLACK}" + "=" * 60 + Style.RESET_ALL)
        print(f"{Back.YELLOW + Fore.BLACK}" + " " * 20 + "FIN DE LA BATAILLE" + " " * 20 + Style.RESET_ALL)
        print(f"{Back.YELLOW + Fore.BLACK}" + "=" * 60 + Style.RESET_ALL)
        
        if self.multiplayer:
            if all(p.is_fainted() for p in self.battle.player_team):
                print(f"\n{Fore.RED + Style.BRIGHT}Le Joueur 2 a gagné la bataille!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN + Style.BRIGHT}Le Joueur 1 a gagné la bataille!{Style.RESET_ALL}")
        
        # Ask if player wants to play again
        play_again = input(f"\n{Fore.CYAN}Voulez-vous rejouer? (o/n): {Style.RESET_ALL}").lower()
        if play_again == 'o':
            self.__init__()
            self.play()
            
if __name__ == "__main__":
    game = PokemonGame()
    game.play() 