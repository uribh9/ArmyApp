from typing import List, Dict
from soldier import Soldier
from mission import Mission


class Platoon:
    """
    Represents a platoon containing soldiers and assigned missions
    """

    def __init__(self, name: str):
        self.name = name
        self.soldiers = []  # List of Soldier objects
        self.weekly_missions = []  # List of assigned Mission objects for the week
        self.home_time_schedule = {}  # Weekly home time planning
        self.platoon_constraints = {}  # Platoon-level constraints and preferences

    def add_soldier(self, soldier: Soldier):
        """Add a soldier to the platoon"""
        if soldier not in self.soldiers:
            self.soldiers.append(soldier)
            # Update soldier's platoon assignment
            soldier.platoon = self.name

    def remove_soldier(self, soldier: Soldier):
        """Remove a soldier from the platoon"""
        if soldier in self.soldiers:
            self.soldiers.remove(soldier)

    def get_soldier_by_serial(self, serial_number: str) -> Soldier:
        """Find a soldier by their serial number"""
        for soldier in self.soldiers:
            if soldier.serial_number == serial_number:
                return soldier
        return None

    def get_soldiers_by_authorization(self, authorization: str) -> List[Soldier]:
        """Get all soldiers with a specific authorization"""
        return [soldier for soldier in self.soldiers if soldier.has_authorization(authorization)]

    def get_soldiers_by_preferred_shift(self, shift: str) -> List[Soldier]:
        """Get all soldiers who prefer a specific shift"""
        return [soldier for soldier in self.soldiers if soldier.preferred_shift == shift]

    def assign_mission(self, mission: Mission):
        """Assign a mission to the platoon for the week"""
        if mission not in self.weekly_missions:
            self.weekly_missions.append(mission)

    def unassign_mission(self, mission: Mission):
        """Remove a mission assignment from the platoon"""
        if mission in self.weekly_missions:
            self.weekly_missions.remove(mission)

    def can_fulfill_mission(self, mission: Mission) -> Dict[str, bool]:
        """Check if platoon can fulfill mission requirements"""
        result = {
            'can_fulfill': True,
            'missing_authorizations': [],
            'insufficient_personnel': False,
            'details': {}
        }

        # Check if we have enough personnel
        if len(self.soldiers) < mission.daily_personnel:
            result['can_fulfill'] = False
            result['insufficient_personnel'] = True

        # Check if we have soldiers with required authorizations
        for auth in mission.required_authorizations:
            soldiers_with_auth = self.get_soldiers_by_authorization(auth)
            if not soldiers_with_auth:
                result['can_fulfill'] = False
                result['missing_authorizations'].append(auth)
            result['details'][auth] = len(soldiers_with_auth)

        return result

    def set_home_time_schedule(self, week_day: str, schedule: str):
        """Set home time schedule for a specific day of the week"""
        self.home_time_schedule[week_day] = schedule

    def get_available_soldiers(self, day: str, shift: str) -> List[Soldier]:
        """Get soldiers available for a specific day and shift (considering home time)"""
        available = []
        for soldier in self.soldiers:
            # Check if soldier has home time constraint for this day
            if day in soldier.home_time_constraints:
                if soldier.home_time_constraints[day] == "home":
                    continue  # Soldier is at home this day

            # Check platoon-level home time schedule
            if day in self.home_time_schedule:
                if self.home_time_schedule[day] == "home":
                    continue  # Entire platoon is at home this day

            available.append(soldier)

        return available

    def get_soldier_count(self) -> int:
        """Get total number of soldiers in platoon"""
        return len(self.soldiers)

    def get_authorization_summary(self) -> Dict[str, int]:
        """Get summary of authorizations available in the platoon"""
        auth_count = {}
        for soldier in self.soldiers:
            for auth in soldier.authorizations:
                auth_count[auth] = auth_count.get(auth, 0) + 1
        return auth_count

    def to_dict(self) -> Dict:
        """Convert platoon object to dictionary for serialization"""
        return {
            'name': self.name,
            'soldiers': [soldier.to_dict() for soldier in self.soldiers],
            'weekly_missions': [mission.to_dict() for mission in self.weekly_missions],
            'home_time_schedule': self.home_time_schedule,
            'platoon_constraints': self.platoon_constraints
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create platoon object from dictionary"""
        platoon = cls(data['name'])

        # Add soldiers
        for soldier_data in data.get('soldiers', []):
            soldier = Soldier.from_dict(soldier_data)
            platoon.add_soldier(soldier)

        # Add missions
        for mission_data in data.get('weekly_missions', []):
            mission = Mission.from_dict(mission_data)
            platoon.assign_mission(mission)

        platoon.home_time_schedule = data.get('home_time_schedule', {})
        platoon.platoon_constraints = data.get('platoon_constraints', {})

        return platoon

    def __str__(self):
        return f"Platoon {self.name}: {len(self.soldiers)} soldiers, {len(self.weekly_missions)} missions"

    def __repr__(self):
        return f"Platoon(name='{self.name}', soldiers={len(self.soldiers)})"