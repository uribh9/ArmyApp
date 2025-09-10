from typing import List, Dict


class Mission:
    """
    Represents a mission with shift schedules, authorization requirements, and personnel needs
    """

    def __init__(self, name: str, shift_hours: Dict[str, str], required_authorizations: List[str],
                 daily_personnel: int):
        self.name = name
        self.shift_hours = shift_hours  # {"Morning": "06:00-14:00", "Noon": "14:00-22:00", "Night": "22:00-06:00"}
        self.required_authorizations = required_authorizations  # Required authorizations for this mission
        self.daily_personnel = daily_personnel  # Total number of people needed per day
        self.personnel_per_shift = {}  # Will store how many people needed per shift

        # Calculate personnel distribution across shifts (can be customized later)
        self._calculate_shift_distribution()

    def _calculate_shift_distribution(self):
        """Automatically distribute personnel across shifts (equal distribution by default)"""
        shifts_count = len(self.shift_hours)
        if shifts_count > 0:
            base_per_shift = self.daily_personnel // shifts_count
            remainder = self.daily_personnel % shifts_count

            shift_names = list(self.shift_hours.keys())
            for i, shift in enumerate(shift_names):
                self.personnel_per_shift[shift] = base_per_shift + (1 if i < remainder else 0)

    def set_shift_personnel(self, shift: str, count: int):
        """Manually set personnel count for a specific shift"""
        if shift in self.shift_hours:
            self.personnel_per_shift[shift] = count
            # Update total daily personnel
            self.daily_personnel = sum(self.personnel_per_shift.values())

    def add_required_authorization(self, authorization: str):
        """Add a required authorization for this mission"""
        if authorization not in self.required_authorizations:
            self.required_authorizations.append(authorization)

    def remove_required_authorization(self, authorization: str):
        """Remove a required authorization from this mission"""
        if authorization in self.required_authorizations:
            self.required_authorizations.remove(authorization)

    def update_shift_hours(self, shift: str, hours: str):
        """Update the hours for a specific shift"""
        self.shift_hours[shift] = hours

    def get_shift_duration(self, shift: str) -> float:
        """Calculate shift duration in hours"""
        if shift not in self.shift_hours:
            return 0.0

        try:
            start_time, end_time = self.shift_hours[shift].split('-')
            start_hour, start_min = map(int, start_time.split(':'))
            end_hour, end_min = map(int, end_time.split(':'))

            start_total = start_hour + start_min / 60
            end_total = end_hour + end_min / 60

            # Handle overnight shifts
            if end_total < start_total:
                end_total += 24

            return end_total - start_total
        except (ValueError, IndexError):
            return 0.0

    def to_dict(self) -> Dict:
        """Convert mission object to dictionary for serialization"""
        return {
            'name': self.name,
            'shift_hours': self.shift_hours,
            'required_authorizations': self.required_authorizations,
            'daily_personnel': self.daily_personnel,
            'personnel_per_shift': self.personnel_per_shift
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create mission object from dictionary"""
        mission = cls(
            data['name'],
            data['shift_hours'],
            data['required_authorizations'],
            data['daily_personnel']
        )
        mission.personnel_per_shift = data.get('personnel_per_shift', {})
        return mission

    def __str__(self):
        return f"Mission: {self.name} - {self.daily_personnel} personnel/day"

    def __repr__(self):
        return f"Mission(name='{self.name}', daily_personnel={self.daily_personnel})"