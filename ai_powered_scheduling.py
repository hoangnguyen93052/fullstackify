import datetime
import json
import random
from collections import defaultdict
from typing import List, Dict, Any, Tuple


class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.schedule = []

    def add_event(self, event):
        self.schedule.append(event)

    def get_schedule(self) -> List[Dict[str, Any]]:
        return self.schedule


class Event:
    def __init__(self, title: str, start_time: datetime.datetime, end_time: datetime.datetime):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.participants = []

    def add_participant(self, user: User):
        self.participants.append(user)

    def get_details(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'participants': [user.name for user in self.participants],
        }


class Scheduler:
    def __init__(self):
        self.users = {}
        self.events = []

    def add_user(self, user_id: str, name: str):
        user = User(user_id, name)
        self.users[user_id] = user

    def create_event(self, title: str, start_time: datetime.datetime, end_time: datetime.datetime, user_ids: List[str]):
        event = Event(title, start_time, end_time)
        for user_id in user_ids:
            if user_id in self.users:
                user = self.users[user_id]
                event.add_participant(user)
                user.add_event(event)
        self.events.append(event)

    def get_user_schedule(self, user_id: str) -> List[Dict[str, Any]]:
        if user_id in self.users:
            return self.users[user_id].get_schedule()
        return []

    def suggest_time_slot(self, duration: int, user_ids: List[str]) -> Tuple[datetime.datetime, datetime.datetime]:
        busy_slots = defaultdict(list)
        for user_id in user_ids:
            if user_id in self.users:
                user_schedule = self.get_user_schedule(user_id)
                for event in user_schedule:
                    busy_slots[user_id].append((event['start_time'], event['end_time']))

        # Find a suitable time slot
        current_time = datetime.datetime.now()
        while True:
            end_time = current_time + datetime.timedelta(minutes=duration)
            if all(not self.is_time_conflicted(current_time, end_time, busy_slots[user_id]) for user_id in user_ids):
                return current_time, end_time
            current_time += datetime.timedelta(minutes=30)

    @staticmethod
    def is_time_conflicted(start_time: datetime.datetime, end_time: datetime.datetime, busy_times: List[Tuple[str, str]]) -> bool:
        for busy_start, busy_end in busy_times:
            busy_start, busy_end = datetime.datetime.fromisoformat(busy_start), datetime.datetime.fromisoformat(busy_end)
            if (start_time < busy_end) and (end_time > busy_start):
                return True
        return False

    def export_schedule(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump(self.events, file, default=str)

    def load_schedule(self, file_name: str):
        with open(file_name, 'r') as file:
            events = json.load(file)
            for event_data in events:
                title = event_data['title']
                start_time = datetime.datetime.fromisoformat(event_data['start_time'])
                end_time = datetime.datetime.fromisoformat(event_data['end_time'])
                self.create_event(title, start_time, end_time, event_data['participants'])

    def random_event_generator(self, num_events: int, user_ids: List[str]):
        for _ in range(num_events):
            title = f"Meeting {random.randint(1, 100)}"
            start_time = datetime.datetime.now() + datetime.timedelta(days=random.randint(0, 10), hours=random.randint(0, 23))
            duration = random.randint(30, 120)
            end_time = start_time + datetime.timedelta(minutes=duration)
            self.create_event(title, start_time, end_time, random.sample(user_ids, random.randint(1, len(user_ids))))

    def generate_schedule_report(self) -> Dict[str, Any]:
        report = {}
        for user_id, user in self.users.items():
            report[user.name] = user.get_schedule()
        return report


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.add_user("1", "Alice")
    scheduler.add_user("2", "Bob")
    scheduler.add_user("3", "Charlie")
    
    scheduler.random_event_generator(5, ["1", "2", "3"])
    
    event_details = scheduler.get_user_schedule("1")
    print(f"Alice's Schedule: {event_details}")

    scheduler.export_schedule("schedule.json")
    scheduler.load_schedule("schedule.json")

    suggested_slot = scheduler.suggest_time_slot(60, ["1", "2"])
    print(f"Suggested Time Slot for Alice and Bob: {suggested_slot[0]} - {suggested_slot[1]}")

    report = scheduler.generate_schedule_report()
    print("Schedule Report:")
    print(json.dumps(report, indent=2))