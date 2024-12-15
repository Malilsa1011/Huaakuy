from datetime import datetime, time
from collections import defaultdict

class Booking:
    def __init__(self, booking_id, requester, requester_id, resource_type, date, start_time, end_time):
        self.booking_id = booking_id
        self.requester = requester
        self.requester_id = requester_id
        self.resource_type = resource_type
        self.date = date
        self.start_time = datetime.strptime(start_time, "%H:%M").time()
        self.end_time = datetime.strptime(end_time, "%H:%M").time()

    def __str__(self):
        return f"Requester: {self.requester} ({self.requester_id}), Resource: {self.resource_type}, Date: {self.date}, Time: {self.start_time} - {self.end_time}"

class Resource:
    def __init__(self, resource_type, max_capacity=100):
        self.resource_type = resource_type
        self.bookings = []
        self.max_capacity = max_capacity

    def add_booking(self, booking):
        if len(self.bookings) < self.max_capacity:
            self.bookings.append(booking)
            return True
        else:
            return False

    def is_available(self, date, start_time_str, end_time_str):
        if start_time_str is None and end_time_str is None:
            # Check if any booking exists for the entire day
            for booking in self.bookings:
                if booking.date == date:
                    return False
            return True

        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

        for booking in self.bookings:
            if booking.date == date:
                if (start_time >= booking.start_time and start_time < booking.end_time) or \
                   (end_time > booking.start_time and end_time <= booking.end_time):
                    return False
        return True

    def get_unavailable_timeslots(self, date):
        unavailable_slots = defaultdict(list)
        for booking in self.bookings:
            if booking.date == date:
                unavailable_slots[f"{booking.start_time.strftime('%H:%M')}-{booking.end_time.strftime('%H:%M')}"] \
                    .append(f"{booking.requester} ({booking.requester_id})")
        return unavailable_slots

    def get_current_usage(self):
        return len(self.bookings)

# Initialize resources
resources = {
    1: Resource("Bed", 100),
    2: Resource("Ventilator", 50),
    3: Resource("Ultrasound", 50),
    4: Resource("Electrocardiograph", 50)
}

resource_names = {
    1: "Bed",
    2: "Ventilator",
    3: "Ultrasound",
    4: "Electrocardiograph"
}

booking_id_counter = 1

def book_resource():
    global booking_id_counter
    requester = input("Enter your name: ")
    requester_id = input("Enter your ID number: ")
    resource_type = input("Enter resource type (1: Bed, 2: Ventilator, 3: Ultrasound, 4: Electrocardiograph): ")
    try:
        resource_type = int(resource_type)
        if resource_type not in resources:
            print("Invalid resource type. Please enter a number between 1 and 4.")
            return
    except ValueError:
        print("Invalid resource type. Please enter a number.")
        return

    resource_amount = int(input("Enter the amount of resources needed: ")) 
    date = input("Enter date (YYYY-MM-DD): ")
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")

    if resources.get(resource_type):
        resource = resources[resource_type]
        available_resources = resource.max_capacity - len(resource.bookings)
        if resource.is_available(date, start_time, end_time) and resource_amount <= available_resources:
            for _ in range(resource_amount):
                new_booking = Booking(booking_id_counter, requester, requester_id, resource_names[resource_type], date, start_time, end_time)
                if resource.add_booking(new_booking):
                    booking_id_counter += 1
                else:
                    print(f"Maximum capacity for {resource_names[resource_type]} reached.")
                    break
            print("Booking Successful!")
            print("------------------------")
            print(f"Name: {requester}")
            print(f"ID: {requester_id}")
            print(f"Resource: {resource_names[resource_type]}")
            print(f"Date: {date}")
            print(f"Time: {start_time} - {end_time}")
            print(f"Amount: {resource_amount}")
            print(f"{resource_names[resource_type]} Left: {available_resources - resource_amount}") 
            print("------------------------")
        else:
            if resource_amount > available_resources:
                print(f"Booking failed. Exceeded maximum capacity for {resource_names[resource_type]}.")
            else:
                print(f"{resource_names[resource_type]} is not available at the specified time.")
    else:
        print(f"Invalid resource type. Please enter a number between 1 and 4.")

def view_available_resources():
    date = input("Enter date (YYYY-MM-DD): ")
    print(f"Available Resources on {date}:")
    print("------------------------")
    for resource_id, resource in resources.items():
        print(f"{resource_names[resource_id]}:")
        available_count = resource.max_capacity - len(resource.bookings)
        print(f"  - Available: {available_count}/{resource.max_capacity}")
        unavailable_slots = resource.get_unavailable_timeslots(date)
        if unavailable_slots:
            print(f"  - Unavailable time:")
            for slot, users in unavailable_slots.items():
                if len(users) > 1:
                    print(f"    - {slot} (Used by {len(users)} users)")
                else:
                    print(f"    - {slot} (Used by {users[0]})") 
        else:
            print("  - Available all day")
    print("------------------------")

def view_resource_usage():
    print("Resource Usage:")
    print("------------------------")
    for resource_id, resource in resources.items():
        current_usage = resource.get_current_usage()
        print(f"{resource_names[resource_id]}: {current_usage}/{resource.max_capacity}")
    print("------------------------")

while True:
    print("\n1. Book Resource")
    print("2. View Available Resources")
    print("3. View Resource Usage")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        book_resource()
    elif choice == '2':
        view_available_resources()
    elif choice == '3':
        view_resource_usage()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

print("Exiting...")