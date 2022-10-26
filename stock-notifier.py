from gcsa.google_calendar import GoogleCalendar
from gcsa.calendar import Calendar
import requests
import config
import sys
from SQLStore import SQLStore
from datetime import datetime

# Initializing objects to be used within the script
gc = GoogleCalendar(credentials_path=config.CALENDAR_API_CREDENTIAL_PATH,
        token_path=config.CALENDAR_API_TOKEN_PATH)

db = SQLStore(config.SQLITE_DB_PATH + config.SQLITE_DB_NAME)


# Helper functions
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
    try:
        db_data = []
        scrip_results = requests.get(config.BSE_RESULTS_URL).json()
        for scrip in scrip_results:
            db_data.append((
                int(scrip["scrip_Code"]),
                scrip["short_name"],
                scrip["Long_Name"],
                scrip["meeting_date"],
                scrip["URL"],
            ))
            
        db.insertIntoTable("stocks_db", 5, db_data)

    except Exception as e:
        print("Failed fetching data from BSE API!")
        print(e)
        sys.exit(-1)

def createCalendarEvent(scrip):
    pass

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
                    sys.exit(-1)
                else:
                    print("Calendar created with ID: ", calendar_id)
                    print("Please add this calendar ID in config.py for future runs.")
                    return gc.get_calendar(calendar_id)

            elif choice == "n":
                print("Calendar ID is needed to run this app, please add an existing calendar ID \
                    in config or create a new calendar.")
                sys.exit(-1)
            else:
                print("Invalid choice!")
                sys.exit(-1)
            
    except:
        raise ValueError("Error loading calendar! Please check calendar id in your config.")


def main():
    # calendar = loadCalendar()
    # print(calendar, calendar.id)
    
    fetchResults()
    db.testQuery()

if __name__ == '__main__':
    main()