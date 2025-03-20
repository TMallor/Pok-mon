class Move:
    def __init__(self, name, move_type, category, power, accuracy, pp):
        self.name = name
        self.type = move_type
        self.category = category  # "physical", "special", or "status"
        self.power = power
        self.accuracy = accuracy
        self.max_pp = pp
        self.current_pp = pp
        self.status_effect = None
        self.stat_changes = None
        self.weather_effect = None
        
    def use(self):
        """Use the move, reducing PP by 1."""
        if self.current_pp > 0:
            self.current_pp -= 1
            return True
        return False
    
    def restore_pp(self, amount=None):
        """Restore PP by the given amount or to max."""
        if amount:
            self.current_pp = min(self.current_pp + amount, self.max_pp)
        else:
            self.current_pp = self.max_pp
        return self.current_pp
    
    def set_status_effect(self, status, chance=100):
        """Set a status effect that the move can cause, with a chance percentage."""
        self.status_effect = {"status": status, "chance": chance}
        
    def set_stat_changes(self, stat_changes, target="opponent", chance=100):
        """Set stat changes that the move applies."""
        self.stat_changes = {"changes": stat_changes, "target": target, "chance": chance}
        
    def set_weather_effect(self, weather):
        """Set a weather effect that the move causes."""
        self.weather_effect = weather
        
    def __str__(self):
        return f"{self.name} ({self.type}, {self.category}, PP: {self.current_pp}/{self.max_pp})" 