import requests
import folium
import webbrowser

# Response Codes:
#1XX: Hold On
#2XX: Here you go
#3XX: Go Away, not authorized
#4XX: Couldn't find what you're looking for
#5XX: I messed something up


# Function to get the current ISS position
def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    longitude = data["iss_position"]["longitude"]
    latitude = data["iss_position"]["latitude"]
    return float(latitude), float(longitude)

# Function to get a human-readable location from latitude and longitude
def get_location_name(latitude, longitude, api_key):
    geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={api_key}"
    response = requests.get(geocode_url)
    response.raise_for_status()
    data = response.json()

    if data['results']:
        # Extract the formatted location name
        location = data['results'][0]['formatted']
    else:
        # Fallback if no location is found
        location = "over an unknown location"

    return location

# Function to generate a map with the ISS position
def generate_iss_map(latitude, longitude, location_name):
    # Create a folium map centered at the ISS location
    iss_map = folium.Map(location=[latitude, longitude], zoom_start=4)

    # Add a marker for the ISS
    folium.Marker(
        location=[latitude, longitude],
        popup=f"ISS Location: {location_name}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(iss_map)

    # Save the map to an HTML file
    map_filename = "iss_location_map.html"
    iss_map.save(map_filename)

    return map_filename

# Main Program
def main():
    # Replace with your OpenCage API key
    api_key = "99518f43d9e54ed6a4f3a8cd0fbefab7"

    # Get the current ISS position
    latitude, longitude = get_iss_position()

    # Get the human-readable location name
    location = get_location_name(latitude, longitude, api_key)

    # Print the ISS location details
    print(f"The ISS is currently at latitude: {latitude}, longitude: {longitude}, which is near {location}.")

    # Generate the map
    map_file = generate_iss_map(latitude, longitude, location)

    # Open the map in the default web browser
    webbrowser.open(map_file)

if __name__ == "__main__":
    main()