from typing import List, Dict, Optional
from platoon import Platoon
from mission import Mission
from soldier import Soldier


class Company:
    """
    Represents a military company containing multiple platoons and managing missions
    """

    def __init__(self, name: str = "Default Company"):
        self.name = name
        self.platoons = []  # List of Platoon objects
        self.missions = []  # List of all available Mission objects
        self.weekly_assignments = {}  # Week-based mission assignments
        self.company_policies = {}  # Company-wide policies and constraints

    def add_platoon(self, platoon: Platoon):
        """Add a platoon to the company"""
        if platoon not in self.platoons:
            self.platoons.append(platoon)

    def remove_platoon(self, platoon: Platoon):
        """Remove a platoon from the company"""
        if platoon in self.platoons:
            self.platoons.remove(platoon)

    def get_platoon_by_name(self, name: str) -> Optional[Platoon]:
        """Find a platoon by name"""
        for platoon in self.platoons:
            if platoon.name == name:
                return platoon
        return None

    def add_mission(self, mission: Mission):
        """Add a mission to the company's mission list"""
        if mission not in self.missions:
            self.missions.append(mission)

    def remove_mission(self, mission: Mission):
        """Remove a mission from the company"""
        if mission in self.missions:
            self.missions.remove(mission)
            # Also remove from all platoon assignments
            for platoon in self.platoons:
                platoon.unassign_mission(mission)

    def get_mission_by_name(self, name: str) -> Optional[Mission]:
        """Find a mission by name"""
        for mission in self.missions:
            if mission.name == name:
                return mission
        return None

    def assign_mission_to_platoon(self, mission_name: str, platoon_name: str, week: str = "current") -> bool:
        """Assign a specific mission to a specific platoon for a given week"""
        mission = self.get_mission_by_name(mission_name)
        platoon = self.get_platoon_by_name(platoon_name)

        if not mission or not platoon:
            return False

        # Check if platoon can fulfill the mission
        capability_check = platoon.can_fulfill_mission(mission)
        if not capability_check['can_fulfill']:
            return False

        # Assign the mission
        platoon.assign_mission(mission)

        # Track in weekly assignments
        if week not in self.weekly_assignments:
            self.weekly_assignments[week] = {}

        if platoon_name not in self.weekly_assignments[week]:
            self.weekly_assignments[week][platoon_name] = []

        if mission_name not in self.weekly_assignments[week][platoon_name]:
            self.weekly_assignments[week][platoon_name].append(mission_name)

        return True

    def get_all_soldiers(self) -> List[Soldier]:
        """Get all soldiers from all platoons"""
        all_soldiers = []
        for platoon in self.platoons:
            all_soldiers.extend(platoon.soldiers)
        return all_soldiers

    def get_soldier_by_serial(self, serial_number: str) -> Optional[Soldier]:
        """Find a soldier by serial number across all platoons"""
        for platoon in self.platoons:
            soldier = platoon.get_soldier_by_serial(serial_number)
            if soldier:
                return soldier
        return None

    def get_company_statistics(self) -> Dict:
        """Get comprehensive company statistics"""
        stats = {
            'total_platoons': len(self.platoons),
            'total_soldiers': len(self.get_all_soldiers()),
            'total_missions': len(self.missions),
            'platoon_details': {},
            'mission_coverage': {},
            'authorization_distribution': {}
        }

        # Platoon details
        for platoon in self.platoons:
            stats['platoon_details'][platoon.name] = {
                'soldier_count': platoon.get_soldier_count(),
                'assigned_missions': len(platoon.weekly_missions),
                'authorizations': platoon.get_authorization_summary()
            }

        # Mission coverage analysis
        for mission in self.missions:
            capable_platoons = []
            for platoon in self.platoons:
                if platoon.can_fulfill_mission(mission)['can_fulfill']:
                    capable_platoons.append(platoon.name)
            stats['mission_coverage'][mission.name] = {
                'capable_platoons': capable_platoons,
                'personnel_required': mission.daily_personnel,
                'required_authorizations': mission.required_authorizations
            }

        # Authorization distribution across company
        auth_dist = {}
        for soldier in self.get_all_soldiers():
            for auth in soldier.authorizations:
                auth_dist[auth] = auth_dist.get(auth, 0) + 1
        stats['authorization_distribution'] = auth_dist

        return stats

    def optimize_weekly_schedule(self, week: str = "current") -> Dict:
        """Basic optimization for weekly mission assignments"""
        optimization_result = {
            'assignments': {},
            'conflicts': [],
            'recommendations': []
        }

        # Simple algorithm: assign missions to most capable platoons
        available_platoons = self.platoons.copy()

        for mission in self.missions:
            best_platoon = None
            best_score = -1

            for platoon in available_platoons:
                capability = platoon.can_fulfill_mission(mission)
                if capability['can_fulfill']:
                    # Score based on available personnel and authorization coverage
                    score = platoon.get_soldier_count()
                    # Bonus for having required authorizations
                    for auth in mission.required_authorizations:
                        soldiers_with_auth = platoon.get_soldiers_by_authorization(auth)
                        score += len(soldiers_with_auth) * 2

                    if score > best_score:
                        best_score = score
                        best_platoon = platoon

            if best_platoon:
                optimization_result['assignments'][mission.name] = best_platoon.name
                # Remove platoon from available list to avoid double assignment
                if best_platoon in available_platoons:
                    available_platoons.remove(best_platoon)
            else:
                optimization_result['conflicts'].append({
                    'mission': mission.name,
                    'issue': 'No capable platoon available'
                })

        return optimization_result

    def export_home_time_options(self, platoon_name: str, week: str = "current") -> Dict:
        """Generate home time options for a specific platoon based on mission requirements"""
        platoon = self.get_platoon_by_name(platoon_name)
        if not platoon:
            return {}

        home_time_options = {
            'platoon': platoon_name,
            'week': week,
            'soldier_options': {},
            'conflicts': [],
            'recommendations': []
        }

        # Analyze each soldier's constraints and mission requirements
        for soldier in platoon.soldiers:
            soldier_options = {
                'name': soldier.name,
                'preferred_shift': soldier.preferred_shift,
                'possible_home_days': [],
                'blocked_days': [],
                'constraints': soldier.home_time_constraints
            }

            # Check each day of the week
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for day in days:
                # Check if soldier is needed for missions this day
                needed_for_missions = False
                for mission in platoon.weekly_missions:
                    # Simplified check - in real implementation, this would be more complex
                    if soldier.has_authorization(
                            mission.required_authorizations[0] if mission.required_authorizations else ""):
                        # Check if this soldier is critical for the mission
                        available_soldiers = platoon.get_soldiers_by_authorization(
                            mission.required_authorizations[0] if mission.required_authorizations else "")
                        if len(available_soldiers) <= mission.daily_personnel:
                            needed_for_missions = True
                            break

                if not needed_for_missions:
                    soldier_options['possible_home_days'].append(day)
                else:
                    soldier_options['blocked_days'].append(day)

            home_time_options['soldier_options'][soldier.serial_number] = soldier_options

        return home_time_options

    def to_dict(self) -> Dict:
        """Convert company object to dictionary for serialization"""
        return {
            'name': self.name,
            'platoons': [platoon.to_dict() for platoon in self.platoons],
            'missions': [mission.to_dict() for mission in self.missions],
            'weekly_assignments': self.weekly_assignments,
            'company_policies': self.company_policies
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create company object from dictionary"""
        company = cls(data.get('name', 'Default Company'))

        # Add platoons
        for platoon_data in data.get('platoons', []):
            platoon = Platoon.from_dict(platoon_data)
            company.add_platoon(platoon)

        # Add missions
        for mission_data in data.get('missions', []):
            mission = Mission.from_dict(mission_data)
            company.add_mission(mission)

        company.weekly_assignments = data.get('weekly_assignments', {})
        company.company_policies = data.get('company_policies', {})

        return company

    def __str__(self):
        return f"Company {self.name}: {len(self.platoons)} platoons, {len(self.missions)} missions, {len(self.get_all_soldiers())} total soldiers"

    def __repr__(self):
        return f"Company(name='{self.name}', platoons={len(self.platoons)}, missions={len(self.missions)})"