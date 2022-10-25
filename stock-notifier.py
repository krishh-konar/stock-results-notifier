from calendar import calendar
from dotenv import dotenv_values
from gcsa.google_calendar import GoogleCalendar
from gcsa.calendar import Calendar
import requests
import config
import os

ENV_VARS = dotenv_values(".env")

gc = GoogleCalendar(credentials_path=config.CALENDAR_API_CREDENTIAL_PATH,
        token_path=config.CALENDAR_API_TOKEN_PATH)


def isCalendarIdPresent():
    try:
        if config.STOCK_RESULTS_CALENDAR_ID == "": return False
        else: return True
    except Exception as e:
        print(e)
        return False

def createCalendar():
    try:
        calendar = Calendar(
            'Stock Results',
            description = 'Calendar containing stock result events in your portfolio'
        )
        calendar = gc.add_calendar(calendar)
        return calendar.id

    except Exception as e:
        print(e)
        return -1
    
def loadScrips():
    pass

def fetchResults():
    results_resp = requests.get(config.BSE_RESULTS_URL)

def loadCalendar():
    try:
        if isCalendarIdPresent():
            calendar = gc.get_calendar(config.STOCK_RESULTS_CALENDAR_ID)
            return calendar
        else:
            choice = input("Calendar ID not present in config, do you want to create a new calendar (y/n): ").lower()
            if choice == "y":
                calendar_id = createCalendar()
                if calendar_id == -1:
                    print("Exception occured while creating calendar!")
                else:
                    print("Calendar created with ID: ", calendar_id)
                    print("Please add this calendar ID in config.py for future runs.")
                    return gc.get_calendar(calendar_id)

            elif choice == "n":
                print("Calendar ID is needed to run this app, please add an existing calendar ID \
                    in config or create a new calendar.")
                return -1
            else:
                print("Invalid choice!")
                return -1
            
    except:
        raise ValueError("Error loading calendar! Please check calendar id in your config.")

def main():
    # for calendar in gc.get_calendar_list():
    #     print(calendar, calendar.id)

    calendar = loadCalendar()
    print(calendar, calendar.id)

if __name__ == '__main__':
    main()