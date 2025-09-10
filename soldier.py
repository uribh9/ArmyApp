from typing import List, Dict


class Soldier:
    """
    Represents a soldier with personal information, preferences, and authorizations
    """

    def __init__(self, name: str, serial_number: str, platoon: str, preferred_shift: str, authorizations: List[str]):
        self.name = name
        self.serial_number = serial_number
        self.platoon = platoon
        self.preferred_shift = preferred_shift  # "Morning", "Noon", "Night"
        self.authorizations = authorizations  # List of authorized duties
        self.home_time_constraints = {}  # Will store weekly home time preferences

    def add_home_time_constraint(self, day: str, constraint: str):
        """Add a home time constraint for a specific day"""
        self.home_time_constraints[day] = constraint

    def has_authorization(self, required_auth: str) -> bool:
        """Check if soldier has a specific authorization"""
        return required_auth in self.authorizations

    def add_authorization(self, authorization: str):
        """Add a new authorization to the soldier"""
        if authorization not in self.authorizations:
            self.authorizations.append(authorization)

    def remove_authorization(self, authorization: str):
        """Remove an authorization from the soldier"""
        if authorization in self.authorizations:
            self.authorizations.remove(authorization)

    def to_dict(self) -> Dict:
        """Convert soldier object to dictionary for serialization"""
        return {
            'name': self.name,
            'serial_number': self.serial_number,
            'platoon': self.platoon,
            'preferred_shift': self.preferred_shift,
            'authorizations': self.authorizations,
            'home_time_constraints': self.home_time_constraints
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create soldier object from dictionary"""
        soldier = cls(
            data['name'],
            data['serial_number'],
            data['platoon'],
            data['preferred_shift'],
            data['authorizations']
        )
        soldier.home_time_constraints = data.get('home_time_constraints', {})
        return soldier

    def __str__(self):
        return f"Soldier: {self.name} ({self.serial_number}) - Platoon {self.platoon}"

    def __repr__(self):
        return f"Soldier(name='{self.name}', serial='{self.serial_number}', platoon='{self.platoon}')"