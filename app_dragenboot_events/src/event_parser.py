import requests
from bs4 import BeautifulSoup

def parse_dragenboat_online_events(event_name, race_cup_id, qualifiers_name):
    # URL of the website you want to scrape
    url = f"https://germany.dragonboat.online/event/{event_name}?race_cupId={race_cup_id}&race_pageSize=999"

    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a dictionary to store the accumulated time for each team
    team_times = {}

    # Find all div elements with class 'race-box-wrapper'
    race_boxes = soup.find_all('div', class_='race-box-wrapper')

    # Iterate over the race boxes to extract race information
    races = []
    for race_box in race_boxes:
        if [ele for ele in qualifiers_name if(ele in race_box.find('div', class_='race-header').find('div', class_='race-info').text.strip())]:
            race = {}
            race_header = race_box.find('div', class_='race-header')
            race['number'] = race_header.find('div', class_='race-number').text.strip()
            race['name'] = race_header.find('div', class_='cup-name').text.strip()
            race['info'] = race_header.find('div', class_='race-info').text.strip()
            race_time = race_header.find('div', class_='race-time-wrapper')
            race['date'] = race_time.find('div', class_='date').text.strip()
            race['time'] = race_time.find('div', class_='time').text.strip()
            race_participants = race_box.find('div', class_='race-participants-wrapper')
            race['participants'] = []
            participant_rows = race_participants.find_all('div', class_='race-participant')
            for row in participant_rows:
                if 'race-participant-header' not in row.attrs['class']:
                    participant = {}
                    lane_info = row.find('div', class_='lane-number')
                    participant['lane'] = lane_info.text.strip() if lane_info else ''

                    team_info = row.find('div', class_='team')
                    if team_info and team_info.find('span', class_='team-name'):
                        participant['team'] = team_info.find('span', class_='team-name').text.strip()
                    elif team_info and team_info.find('a', class_='team-name'):
                        participant['team'] = team_info.find('a', class_='team-name').text.strip()
                    else:  participant['team'] = 'N/A'

                    position_info = row.find('div', class_='position')
                    participant['position'] = position_info.text.strip() if position_info else ''
                    time_info = row.find('div', class_='time')
                    participant['time'] = time_info.text.strip() if time_info.text.strip() else '00:00,00'
                    race['participants'].append(participant)
            races.append(race)

    # Print the extracted race information
    for race in races:
        for participant in race['participants']:
            teamname=participant['team']
            time=participant['time']
        
            # Split the time string into minutes, seconds, and hundredths of a second
            time_parts = time.split(":")
            if len(time_parts) != 2:
                continue

            minutes, seconds = time_parts
            if not minutes.isdigit() or not seconds:
                continue

            # Parse the minutes and seconds into integers
            minutes = int(minutes)
            seconds_parts = seconds.split(",")
            if len(seconds_parts) != 2:
                continue

            seconds = seconds_parts[0]
            hundredths = seconds_parts[1]
            if not seconds.isdigit() or not hundredths.isdigit():
                continue

            seconds = int(seconds)
            hundredths = int(hundredths)

            # Calculate the total time in hundredths of a second
            total_hundredths = minutes * 60 * 100 + seconds * 100 + hundredths

            # Accumulate the time for the team
            if teamname in team_times:
                team_times[teamname].append(total_hundredths)
            else:
                team_times[teamname] = [total_hundredths]

    # Sort the accumulated times in ascending order
    sorted_times = sorted(team_times.items(), key=lambda x: sum(x[1]))
    
    return sorted_times
    
def max_num_races(race_list):
    max_races= max((x[1]) for x in race_list)
    max_num_races = len(max_races)
    
    return max_num_races