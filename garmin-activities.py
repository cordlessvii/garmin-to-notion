from datetime import date, datetime
from garminconnect import Garmin
from notion_client import Client
import os

def get_icon_for_record(activity_name):
    icon_map = {
        "1K": "🥇",
        "1mi": "⚡",
        "5K": "👟",
        "10K": "⭐",
        "Longest Run": "🏃",
        "Longest Ride": "🚴",
        "Total Ascent": "🚵",
        "Max Avg Power (20 min)": "🔋",
        "Most Steps in a Day": "👣",
        "Most Steps in a Week": "🚶",
        "Most Steps in a Month": "📅",
        "Longest Goal Streak": "✔️",
        "Other": "🏅"
    }
    return icon_map.get(activity_name, "🏅")

def get_cover_for_record(activity_name):
    cover_map = {
        "1K": "https://images.unsplash.com/photo-1526676537331-7747bf8278fc",
        "1mi": "https://images.unsplash.com/photo-1638183395699-2c0db5b6afbb",
        "5K": "https://images.unsplash.com/photo-1571008887538-b36bb32f4571",
        "10K": "https://images.unsplash.com/photo-1529339944280-1a37d3d6fa8c",
        "Longest Run": "https://images.unsplash.com/photo-1532383282788-19b341e3c422",
        "Longest Ride": "https://images.unsplash.com/photo-1471506480208-91b3a4cc78be",
        "Max Avg Power (20 min)": "https://images.unsplash.com/photo-1591741535018-d042766c62eb",
        "Most Steps in a Day": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8",
        "Most Steps in a Week": "https://images.unsplash.com/photo-1602174865963-9159ed37e8f1",
        "Most Steps in a Month": "https://images.unsplash.com/photo-1580058572462-98e2c0e0e2f0",
        "Longest Goal Streak": "https://images.unsplash.com/photo-1477332552946-cfb384aeaf1c"
    }
    return cover_map.get(activity_name, "https://images.unsplash.com/photo-1471506480208-91b3a4cc78be")

def format_pace(average_speed):
    if average_speed > 0:
        pace_min_km = 1000 / (average_speed * 60)
        pace_min_mi = pace_min_km / 1.60934
        minutes = int(pace_min_mi)
        seconds = int((pace_min_mi - minutes) * 60)
        return f"{minutes}:{seconds:02d}"
    else:
        return ""

def format_garmin_value(value, activity_type, typeId):
    if typeId == 1:  # 1K
        total_seconds = round(value)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        formatted_value = f"{minutes}:{seconds:02d}"
        pace = format_pace(1000 / value) if value > 0 else ""
        return formatted_value, pace

    if typeId == 2:  # 1mile
        total_seconds = round(value)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        formatted_value = f"{minutes}:{seconds:02d}"
        return formatted_value, ""

    if typeId == 3:  # 5K
        total_seconds = round(value)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        formatted_value = f"{minutes}:{seconds:02d}"
        pace = format_pace((5000 / value)) if value > 0 else ""
        return formatted_value, pace

    if typeId == 4:  # 10K
        total_seconds = round(value)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        formatted_value = f"{hours}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes}:{seconds:02d}"
        pace = format_pace((10000 / value)) if value > 0 else ""
        return formatted_value, pace

    if typeId in [7, 8]:  # Longest Run or Ride
        value_mi = value / 1609.34
        formatted_value = f"{value_mi:.2f} mi"
        return formatted_value, ""

    if typeId == 9:
        return f"{int(value):,} m", ""
    if typeId == 10:
        return f"{round(value)} W", ""
    if typeId in [12, 13, 14]:
        return f"{round(value):,}", ""
    if typeId == 15:
        return f"{round(value)} days", ""

    minutes = int(value // 60)
    seconds = round((value / 60 - minutes) * 60, 2)
    formatted_value = f"{minutes}:{seconds:05.2f}" if value < 3600 else f"{int(value // 3600)}:{int((value % 3600) // 60):02}:{round(value % 60, 2):05.2f}"
    return formatted_value, ""

# Additional changes throughout your script should include updating any references to "Distance (km)" to "Distance (mi)"
# and converting the distance using / 1609.34 instead of / 1000.
# For example:
# "Distance (mi)": {"number": round(total_distance / 1609.34, 2)}
