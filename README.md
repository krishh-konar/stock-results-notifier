# Stock Results Notifier
Get notifications for upcoming results for companies listed on BSE.

This script creates a new secondary calendar in your Google Calendar and adds event for results in that calendars for selected scrips.

### Dependencies

This tool mainly uses the [Google Calendar Simple API](https://github.com/kuzmoyev/google-calendar-simple-api) package to make API calls to Google Calendar.

You can install requirements using `requirements.txt`.

```
pip install -r requirements.txt
```

### Authentication

This app requires authentication with Google OAuth in order to read/add/update google calendar events. 

You can follow the detailed steps [here](https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html#credentials) to get the crendentials.

>   1. Create a new Google Cloud Platform (GCP) project.
>   Note: You will need to enable the “Google Calendar API” for your project.
>
>   2. Configure the OAuth consent screen.
>
>   3. Create a OAuth client ID credential and download the `credentials.json` file.
>
>   4. Put downloaded `credentials.json` file into `~/.credentials/` directory.

Once credentials are downloaded and stored, update `CALENDAR_API_CREDENTIAL_PATH` and `CALENDAR_API_TOKEN_PATH` in `config.py` to point to your credentials and location where the token will be created.

> Note: Make sure you have `Read` access for your credentials file and `Read/Write` access for token file/directory.

### Usage

* Edit the `config.py` file and add `CALENDAR_API_CREDENTIAL_PATH` and `CALENDAR_API_TOKEN_PATH` from the previous step and save.

* Add `STOCK_RESULTS_CALENDAR_ID` if you already have a dedicated calendar for saving these result events. If not added, the app will ask to create one for you.

* Add ticker symbols for all the stocks you want to create events for in `portfolio_stocks.txt`, one stock per line.

* Run the script.

```
    python stock-notifier.py
```