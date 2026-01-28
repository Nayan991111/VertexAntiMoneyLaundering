from rapidfuzz import process, fuzz
from typing import Tuple

class WatchlistService:
    def __init__(self):
        # SIMULATION: In a real bank, this loads daily from XML/CSV (OFAC/UN/EU).
        # We load this into memory for O(1) speed during transactions.
        self.sanctions_list = [
            "Ivan Drago",              # The specific test case
            "Gennady Golovkin",        # High risk individual
            "North Korea State Bank",  # Sanctioned Entity
            "Syrian General Intelligence",
            "Pablo Escobar",
            "Vladimir Makarov",
            "Osama Bin Laden"
        ]
        # STRICTNESS: 80% similarity means "Ivan Dragg" (90%) will be caught.
        self.threshold = 80.0

    def check_sanction(self, name: str) -> Tuple[bool, str, float]:
        """
        Screens a name against the sanctions list using Token Sort Ratio.
        Token Sort Ratio handles reordering (e.g. "Doe John" vs "John Doe").
        
        Returns: (is_hit, matched_name, score)
        """
        if not name:
            return False, "", 0.0

        # process.extractOne finds the best single match in the list efficiently
        result = process.extractOne(
            name, 
            self.sanctions_list, 
            scorer=fuzz.token_sort_ratio
        )
        
        # Result format is (match, score, index)
        if result:
            match_name, score, _ = result
            if score >= self.threshold:
                return True, match_name, score
        
        return False, "", 0.0

# Singleton Instance
watchlist_service = WatchlistService()