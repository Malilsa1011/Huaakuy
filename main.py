import pandas as pd
from collectdata import add_booking, show_schedule, summarize_bookings

def main_menu():
    print("Welcome to the hospital booking system!")

    while True:
        print("\n--------------------")
        print("\nHospital Booking System")
        print("1. Book a resource")
        print("2. View available bookings (schedule)")
        print("3. Summarize bookings")
        print("4. Exit")
        choice = input("Choose your option: ").strip()

        if choice == "1":
            # Collect user details
            name = input("Enter your name: ").strip()
            if not name:
                print("Error: Name cannot be empty.")
                continue

            instrument_type = ["Bed", "Ventilator", "Ultrasound", "Electrocardiograph"]
            print("Choose 1 for Bed, 2 for Ventilator, 3 for Ultrasound, 4 for Electrocardiograph.")
            instr_choice = input("Enter your choice (1-4): ").strip()

            if instr_choice not in ["1", "2", "3", "4"]:
                print("Invalid choice! Please enter a number between 1 and 4.")
                continue

            instrument = instrument_type[int(instr_choice) - 1]
            date = input("Enter date [YYYY-MM-DD]: ").strip()
            start_time = input("Enter start time [HH:MM]: ").strip()
            end_time = input("Enter end time [HH:MM]: ").strip()

            add_booking(name, instrument, date, start_time, end_time)

        elif choice == "2":
            # Show schedule
            show_schedule()

        elif choice == "3":
            # Summarize bookings
            summarize_bookings()

        elif choice == "4":
            print("Exiting the system. Goodbye!")
            print("\n--------------------")
            break
            
        else:
            print("Invalid choice! Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main_menu()