from datetime import timedelta
import datetime

def Expiry_Date():
    # Calculate the date after 7 days
    future_date = datetime.datetime.strptime("2023-12-21", "%Y-%m-%d") + timedelta(days=7)

    # Print the year, month, and day separately
    return future_date.year, future_date.month, future_date.day


def Monthly_Expiry():
    # Calculate the date after 7 days
    future_date = datetime.datetime.strptime("2023-12-21", "%Y-%m-%d") + timedelta(days=7)

    # Print the year, month, and day separately
    return future_date.year, future_date.month, future_date.day


def Nifty_Expiry_Date():
    # Calculate the date after 7 days
    future_date = datetime.datetime.strptime("2023-12-14", "%Y-%m-%d") + timedelta(days=7)

    # Print the year, month, and day separately
    return future_date.year, future_date.month, future_date.day


def Nifty_Monthly_Expiry():
    # Calculate the date after 7 days
    future_date = datetime.datetime.strptime("2023-12-21", "%Y-%m-%d") + timedelta(days=7)

    # Print the year, month, and day separately
    return future_date.year, future_date.month, future_date.day


def Fin_Nifty_Expiry_Date():
    # Calculate the date after 7 days
    future_date = datetime.datetime.strptime("2023-10-31", "%Y-%m-%d") + timedelta(days=7)

    # Print the year, month, and day separately
    return future_date.year, future_date.month, future_date.day


def Fin_Nifty_Monthly_Expiry():
    # Calculate the date after 7 days
    future_date = datetime.datetime.strptime("2023-11-21", "%Y-%m-%d") + timedelta(days=7)

    # Print the year, month, and day separately
    return future_date.year, future_date.month, future_date.day


def Midcp_Nifty_Expiry_Date():
    # Calculate the date after 7 days
    future_date = datetime.datetime.strptime("2023-10-09", "%Y-%m-%d") + timedelta(days=7)

    # Print the year, month, and day separately
    return future_date.year, future_date.month, future_date.day


def Midcp_Nifty_Monthly_Expiry():
    # Calculate the date after 7 days
    future_date = datetime.datetime.strptime("2023-10-30", "%Y-%m-%d") + timedelta(days=7)

    # Print the year, month, and day separately
    return future_date.year, future_date.month, future_date.day