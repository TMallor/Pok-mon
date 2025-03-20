class Pokemon:
    def __init__(self, name, pokemon_type, level, hp, attack, defense, sp_attack, sp_defense, speed, moves=None):
        self.name = name
        self.type = pokemon_type  # Can be a list for dual-type Pokémon
        self.level = level
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.moves = moves if moves else []
        self.status = None  # For status conditions like poisoned, burned, etc.
        self.stat_stages = {
            "attack": 0,
            "defense": 0,
            "sp_attack": 0,
            "sp_defense": 0,
            "speed": 0,
            "accuracy": 0,
            "evasion": 0
        }
        
    def add_move(self, move):
        if len(self.moves) < 4:
            self.moves.append(move)
            return True
        return False
    
    def is_fainted(self):
        return self.current_hp <= 0
    
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        return self.current_hp
    
    def heal(self, amount):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        return self.current_hp
    
    def calculate_stat(self, stat_name):
        """Calculate the actual stat value based on stat stages."""
        base_stat = getattr(self, stat_name)
        stage = self.stat_stages.get(stat_name, 0)
        
        # Stat modifier formula based on stages (-6 to +6)
        if stage >= 0:
            modifier = (2 + stage) / 2
        else:
            modifier = 2 / (2 - stage)
            
        return int(base_stat * modifier)
    
    def apply_status(self, status):
        """Apply a status condition to the Pokémon."""
        self.status = status
        
    def cure_status(self):
        """Remove any status condition."""
        self.status = None
    
    def __str__(self):
        return f"{self.name} (Lv. {self.level}) - HP: {self.current_hp}/{self.max_hp}" 