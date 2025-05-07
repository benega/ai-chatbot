import pandas as pd

class ScheduleManager:
    def __init__(self, csv_path="data/schedule.csv"):
        self.csv_path = csv_path
        self.schedule = self.load_schedule()

    def load_schedule(self):
        """Loads the schedule from the CSV file using pandas."""
        try:
            df = pd.read_csv(self.csv_path)
            return df
        except FileNotFoundError:
            print(f"Error: Schedule file not found at {self.csv_path}")
            return pd.DataFrame()  # Return an empty DataFrame

    def check_availability(self, class_type, date, time):
        """Checks the availability of a class at a given date and time."""
        available = self.schedule[
            (self.schedule["class_type"] == class_type)
            & (self.schedule["date"] == date)
            & (self.schedule["time"] == time)
            & (self.schedule["availability"] == True)
        ]
        return not available.empty

    def get_schedule(self):
        """Returns the schedule."""
        return self.schedule

if __name__ == "__main__":
    # Example usage
    schedule_manager = ScheduleManager()
    schedule = schedule_manager.get_schedule()
    print(schedule)

    # Example availability check
    is_available = schedule_manager.check_availability("Yoga", "2023-12-25", "10:00")
    print(f"Is Yoga available on 2023-12-25 at 10:00? {is_available}")
