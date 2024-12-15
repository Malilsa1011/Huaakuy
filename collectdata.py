import pandas as pd
from datetime import datetime

# Global DataFrame to store bookings
booking = pd.DataFrame(columns=["Name", "Instrumentality", "Date", "Start Time", "End Time"])

def add_booking(name, instrumentality, date, start_time, end_time):
    global booking

    # Validate input data
    if not name or not instrumentality or not date or not start_time or not end_time:
        print("Error: All fields are required.")
        return

    # Convert input times to datetime objects
    try:
        start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        print("Error: Invalid date or time format.")
        return

    if start_dt >= end_dt:
        print("Error: End time must be after start time.")
        return

    # Check for overlapping bookings
    overlapping_bookings = booking[
        (booking["Instrumentality"] == instrumentality) &
        (booking["Date"] == date) &
        (
            (start_dt < pd.to_datetime(booking["End Time"])) &
            (end_dt > pd.to_datetime(booking["Start Time"]))
        )
    ]

    if not overlapping_bookings.empty:
        print("\nError: This resource is already booked during the specified time.")
        print("Conflicting booking(s):")
        print(overlapping_bookings.to_string(index=False))
        return

    # Add booking
    new_entry = {
        "Name": name,
        "Instrumentality": instrumentality,
        "Date": date,
        "Start Time": start_time,
        "End Time": end_time,
    }
    booking.loc[len(booking)] = new_entry

    print("\nBooking added successfully!")
    print("\n--------------------")
    print("Current Booking List:")
    print(booking.sort_values(by=["Date", "Start Time"]).to_string(index=False))

def show_schedule():
    global booking
    if booking.empty:
        print("\nInstrument available.")
    else:
        print("\n----------------------")
        print("\nCurrent Schedule of Bookings:")
        print(booking.sort_values(by=["Date", "Start Time"]).to_string(index=False))

def summarize_bookings():
    global booking
    if booking.empty:
        print("\nNo bookings available for summary.")
        return
    print("\n--------------------")
    print("\nSummary of Bookings:")

    # Count bookings per instrumentality
    instrument_summary = booking["Instrumentality"].value_counts()
    print("\n--------------------")
    print("\nNumber of bookings by resource:")
    print(instrument_summary.to_string())

    # Find the most frequently booked time slots
    booking["Time Slot"] = booking["Date"] + " " + booking["Start Time"] + " to " + booking["End Time"]
    time_slot_summary = booking["Time Slot"].value_counts()
    print("\n--------------------")
    print("\nTop time slots with highest bookings:")
    print(time_slot_summary.head(5).to_string(index=True))