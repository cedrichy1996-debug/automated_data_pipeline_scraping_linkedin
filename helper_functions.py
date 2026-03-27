# import libraries
from datetime import datetime
import numpy as np
from pyjarowinkler import distance
import pandas as pd

# helper function for date transformation
def date_transform (s):
    if s == '':
        return['', '']
    lst_s = s.split(' - ')
    if len(lst_s) == 1:
        lst_s_1 = s.split (' · ')
        date_1 = datetime.strptime(lst_s_1[0], '%Y').date()
        date_2 = datetime.strptime(lst_s_1[0], '%Y').date()
        return [date_1, date_2]
    elif len(lst_s[0]) != 4:
        date_1 = datetime.strptime(lst_s[0], '%b %Y').date()
        date_2 = lst_s[1].split(' · ')[0]
        if date_2 != 'Present':
            if len(date_2) != 4:
                date_2 = datetime.strptime(date_2, '%b %Y').date()
            else:
                date_2 = datetime.strptime(date_2, '%Y').date()
    else:
        date_1 = datetime.strptime(lst_s[0], '%Y').date()
        date_2 = lst_s[1].split(' · ')[0]
        if date_2 != 'Present':
            if len(date_2) != 4:
                date_2 = datetime.strptime(date_2, '%b %Y').date()
            else:
                date_2 = datetime.strptime(date_2, '%Y').date()
    return [date_1, date_2]

# helper function to format location
def categorize_city(city_str):
    city_str = city_str.lower()
    if city_str == 'canada':
        return 'Greater Toronto Area (GTA)'
    elif city_str == 'toronto':
        return 'Greater Toronto Area (GTA)'
    elif 'ontario' in city_str:
        if 'toronto' in city_str or 'greater toronto' in city_str or 'markham' in city_str or 'scarborough' in city_str\
                or 'north york' in city_str or 'richmond hill' in city_str or 'vaughan' in city_str or 'mississauga' in city_str:
            return 'Greater Toronto Area (GTA)'
        elif 'waterloo' in city_str:
            return 'Kitchener-Waterloo Area'
        elif 'ottawa' in city_str:
            return 'Ottawa Area'
        else:
            return 'Ontario (outside GTA, Kitchener-Waterloo or Ottawa)'
    elif 'canada' in city_str:
        if 'toronto' in city_str or 'greater toronto' in city_str or 'markham' in city_str or 'scarborough' in city_str\
                or 'north york' in city_str or 'richmond hill' in city_str or 'vaughan' in city_str or 'mississauga' in city_str\
                or 'newmarket' in city_str:
            return 'Greater Toronto Area (GTA)'
        elif 'waterloo' in city_str or 'greater kitchener-cambridge-waterloo metropolitan area':
            return 'Kitchener-Waterloo Area'
        elif 'ottawa' in city_str:
            return 'Ottawa Area'
        elif 'edmonton' in city_str or 'vancouver' in city_str or 'calgary' in city_str or 'winnepeg' in city_str\
            or 'montreal' in city_str or 'fredericton' in city_str or 'kelowna' in city_str:
            return 'Canada (outside Ontario)'
        else:
            return 'Greater Toronto Area (GTA)'
    elif 'edmonton' in city_str or 'vancouver' in city_str or 'calgary' in city_str or 'winnepeg' in city_str\
            or 'montreal' in city_str or 'fredericton' in city_str:
        return 'Canada (outside Ontario)'
    elif 'usa' in city_str or 'united states' in city_str or 'san francisco' in city_str \
            or 'boston' in city_str or 'los angeles' in city_str or 'chicago' in city_str or 'seattle' in city_str\
            or 'new york' in city_str or 'dallas' in city_str:
        return 'USA'
    elif 'remote' in city_str or 'hybrid' in city_str or 'online' in city_str:
        return 'Greater Toronto Area (GTA)'
    else:
        return 'International (outside USA)'

canada_province_abbr = ['NL', 'PE', 'NS', 'NB', 'QC', 'ON', 'MB', 'SK', 'AB', 'BC', 'YT', 'NT', 'NU']
canada_province = ['Newfoundland and Labrador', 'Prince Edward Island', 'Nova Scotia', 'New Brunswick', 'Quebec',
                   'Ontario', 'Manitoba', 'Saskatchewan', 'Alberta', 'British Columbia', 'Yukon',
                   'Northwest Territories', 'Nunavut']
can_province_dict = {'NL': 'Newfoundland and Labrador',
                         'PE': 'Prince Edward Island',
                         'NS': 'Nova Scotia',
                         'NB': 'New Brunswick',
                         'QC': 'Quebec',
                         'ON': 'Ontario',
                         'MB': 'Manitoba',
                         'SK': 'Saskatchewan',
                         'AB': 'Alberta',
                         'BC': 'British Columbia',
                         'YT': 'Yukon',
                         'NT': 'Northwest Territories',
                         'NU': 'Nunavut'}
major_cities_canada = {
    "Alberta": ["Edmonton", "Calgary"],
    "British Columbia": ["Vancouver", "Victoria", "Burnaby"],
    "Manitoba": ["Winnipeg"],
    "New Brunswick": ["Saint John", "Moncton", "Fredericton"],
    "Newfoundland and Labrador": ["St. John's"],
    "Northwest Territories": ["Yellowknife"],
    "Nova Scotia": ["Halifax"],
    "Nunavut": ["Iqaluit"],
    "Ontario": ["Toronto", "Hamilton", "Kitchener", "London", "Ottawa", "Oshawa", "Windsor", 'Markham', 'Scarborough',
                'North York', 'Richmond Hill', 'Vaughan', 'Mississauga'],
    "Prince Edward Island": ["Charlottetown"],
    "Quebec": ["Montreal", "Quebec City", "Sherbrooke"],
    "Saskatchewan": ["Saskatoon", "Regina"],
    "Yukon": ["Whitehorse"]
}
canada_cities_to_provinces = {
    "Toronto": "Ontario",
    "North York": "Ontario",
    "Mississauga": "Ontario",
    "Markham": "Ontario",
    "Vaughan": "Ontario",
    "Brampton": "Ontario",
    "Richmond Hill": "Ontario",
    "Oakville": "Ontario",
    "Burlington": "Ontario",
    "Brampton": "Ontario",
    "Hamilton": "Ontario",
    "Kitchener": "Ontario",
    "London": "Ontario",
    "Ottawa": "Ontario",
    "Oshawa": "Ontario",
    "Windsor": "Ontario",
    "Montreal": "Quebec",
    "Quebec City": "Quebec",
    "Sherbrooke": "Quebec",
    "Vancouver": "British Columbia",
    "Surrey": "British Columbia",
    "Burnaby": "British Columbia",
    "Richmond": "British Columbia",
    "Abbotsford": "British Columbia",
    "Coquitlam": "British Columbia",
    "Delta": "British Columbia",
    "Langley": "British Columbia",
    "North Vancouver": "British Columbia",
    "Maple Ridge": "British Columbia",
    "New Westminster": "British Columbia",
    "Port Coquitlam": "British Columbia",
    "Port Moody": "British Columbia",
    "Pitt Meadows": "British Columbia",
    "White Rock": "British Columbia",
    "Victoria": "British Columbia",
    "Calgary": "Alberta",
    "Edmonton": "Alberta",
    "Regina": "Saskatchewan",
    "Saskatoon": "Saskatchewan",
    "Winnipeg": "Manitoba",
    "Fredericton": "New Brunswick",
    "Moncton": "New Brunswick",
    "Saint John": "New Brunswick",
    "Charlottetown": "Prince Edward Island",
    "Halifax": "Nova Scotia",
    "St. John's": "Newfoundland and Labrador",
    "Yellowknife": "Northwest Territories",
    "Iqaluit": "Nunavut",
    "Whitehorse": "Yukon"
}

us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
             'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
             'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
             'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
             'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
             'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
             'Wisconsin', 'Wyoming']
us_states_abbr  = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
                   'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                   'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
                   'WI', 'WY']

us_state_dict = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}
us_state_cities = {
    'Alabama': ['Birmingham', 'Montgomery', 'Mobile', 'Huntsville'],
    'Alaska': ['Anchorage', 'Fairbanks', 'Juneau', 'Sitka'],
    'Arizona': ['Phoenix', 'Tucson', 'Mesa', 'Chandler'],
    'Arkansas': ['Little Rock', 'Fort Smith', 'Fayetteville', 'Springdale'],
    'California': ['San Francisco', 'Mountain View', 'Los Angeles', 'San Diego', 'San Jose'],
    'Colorado': ['Denver', 'Colorado Springs', 'Aurora', 'Fort Collins'],
    'Connecticut': ['Bridgeport', 'New Haven', 'Hartford', 'Stamford'],
    'Delaware': ['Wilmington', 'Dover', 'Newark', 'Middletown'],
    'Florida': ['Miami', 'Tampa', 'Orlando', 'Jacksonville'],
    'Georgia': ['Atlanta', 'Savannah', 'Columbus', 'Athens'],
    'Hawaii': ['Honolulu', 'Hilo', 'Kailua', 'Kapolei'],
    'Idaho': ['Boise', 'Nampa', 'Meridian', 'Idaho Falls'],
    'Illinois': ['Chicago', 'Aurora', 'Rockford', 'Joliet'],
    'Indiana': ['Indianapolis', 'Fort Wayne', 'Evansville', 'South Bend'],
    'Iowa': ['Des Moines', 'Cedar Rapids', 'Davenport', 'Sioux City'],
    'Kansas': ['Wichita', 'Overland Park', 'Kansas City', 'Topeka'],
    'Kentucky': ['Louisville', 'Lexington', 'Bowling Green', 'Owensboro'],
    'Louisiana': ['New Orleans', 'Baton Rouge', 'Shreveport', 'Lafayette'],
    'Maine': ['Portland', 'Lewiston', 'Bangor', 'South Portland'],
    'Maryland': ['Baltimore', 'Frederick', 'Rockville', 'Gaithersburg'],
    'Massachusetts': ['Boston', 'Worcester', 'Springfield', 'Cambridge'],
    'Michigan': ['Detroit', 'Grand Rapids', 'Ann Arbor', 'Lansing'],
    'Minnesota': ['Minneapolis', 'St. Paul', 'Rochester', 'Duluth'],
    'Mississippi': ['Jackson', 'Gulfport', 'Southaven', 'Hattiesburg'],
    'Missouri': ['Kansas City', 'St. Louis', 'Springfield', 'Independence'],
    'Montana': ['Billings', 'Missoula', 'Great Falls', 'Bozeman'],
    'Nebraska': ['Omaha', 'Lincoln', 'Bellevue', 'Grand Island'],
    'Nevada': ['Las Vegas', 'Reno', 'Henderson', 'North Las Vegas'],
    'New Hampshire': ['Manchester', 'Nashua', 'Concord', 'Dover'],
    'New Jersey': ['Jersey City', 'Newark', 'Paterson', 'Elizabeth'],
    'New Mexico': ['Albuquerque', 'Las Cruces', 'Rio Rancho', 'Santa Fe'],
    'New York': ['New York', 'Buffalo', 'Rochester', 'Yonkers'],
    'North Carolina': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham'],
    'North Dakota': ['Fargo', 'Bismarck', 'Grand Forks', 'Minot'],
    'Ohio': ['Columbus', 'Cleveland', 'Cincinnati', 'Dayton'],
    'Oklahoma': ['Oklahoma City', 'Tulsa', 'Norman', 'Broken Arrow'],
    'Oregon': ['Portland', 'Eugene', 'Salem', 'Gresham'],
    'Pennsylvania': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Erie'],
    'Rhode Island': ['Providence', 'Warwick', 'Cranston', 'Pawtucket'],
    'South Carolina': ['Columbia', 'Charleston', 'Greenville', 'Rock Hill'],
    'South Dakota': ['Sioux Falls', 'Rapid City', 'Aberdeen', 'Brookings'],
    'Tennessee': ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga'],
    'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
    'Utah': ['Salt Lake City', 'West Valley City', 'Provo', 'West Jordan'],
    'Vermont': ['Burlington', 'South Burlington', 'Rutland', 'Montpelier'],
    'Virginia': ['Virginia Beach', 'Norfolk', 'Chesapeake', 'Richmond'],
    'Washington': ['Seattle', 'Spokane', 'Tacoma', 'Vancouver'],
    'West Virginia': ['Charleston', 'Huntington', 'Morgantown', 'Parkersburg'],
    'Wisconsin': ['Milwaukee', 'Madison', 'Green Bay', 'Kenosha'],
    'Wyoming': ['Cheyenne', 'Casper', 'Laramie', 'Gillette']}

us_cities_states = {
    'San Francisco': 'California',
    'San Jose': 'California',
    'Oakland': 'California',
    'Irvine': 'California',
    'Los Angeles': 'California',
    'San Diego': 'California',
    'Long Beach': 'California',
    'Anaheim': 'California',
    'Riverside': 'California',
    'Santa Ana': 'California',
    'Bakersfield': 'California',
    'Fresno': 'California',
    'Sacramento': 'California',
    'Mountain View': 'California',
    'New York': 'New York',
    'New York City': 'New York',
    'Brooklyn': 'New York',
    'Queens': 'New York',
    'Manhattan': 'New York',
    'Staten Island': 'New York',
    'Alameda': 'California',
    'Albany': 'New York',
    'Berkeley': 'California',
    'Boston': 'Massachusetts',
    'Buffalo': 'New York',
    'Cambridge': 'Massachusetts',
    'Chicago': 'Illinois',
    'Cleveland': 'Ohio',
    'Dallas': 'Texas',
    'Austin': 'Texas',
    'Denver': 'Colorado',
    'Detroit': 'Michigan',
    'Houston': 'Texas',
    'Miami': 'Florida',
    'Minneapolis': 'Minnesota',
    'New Orleans': 'Louisiana',
    'Philadelphia': 'Pennsylvania',
    'Pittsburgh': 'Pennsylvania',
    'Portland': 'Oregon',
    'Salt Lake City': 'Utah',
    'Seattle': 'Washington',
    'Washington DC': 'District of Columbia',
    'Stanford': 'California'
}

country_capitals = {
    'Argentina': 'Buenos Aires',
    'Australia': 'Canberra',
    'Brazil': 'Brasilia',
    'China': 'Beijing',
    'Denmark': 'Copenhagen',
    'Finland': 'Helsinki',
    'France': 'Paris',
    'Germany': 'Berlin',
    'Greece': 'Athens',
    'Hungary': 'Budapest',
    'India': 'New Delhi',
    'Indonesia': 'Jakarta',
    'Iran': 'Tehran',
    'Israel': 'Jerusalem',
    'Italy': 'Rome',
    'Japan': 'Tokyo',
    'Mexico': 'Mexico City',
    'Netherlands': 'Amsterdam',
    'New Zealand': 'Wellington',
    'Norway': 'Oslo',
    'Poland': 'Warsaw',
    'Portugal': 'Lisbon',
    'Russia': 'Moscow',
    'Saudi Arabia': 'Riyadh',
    'South Korea': 'Seoul',
    'Spain': 'Madrid',
    'Sweden': 'Stockholm',
    'Switzerland': 'Zurich',
    'Thailand': 'Bangkok',
    'Turkey': 'Ankara',
    'United Kingdom': 'London',
    'Senegal': 'Dakar',
    'Rwanda': 'Kigali',
    'Slovenia': 'Ljubljana',
    'England': 'London',
    'Egypt': 'Cairo',
    'Pakistan': 'Islamabad'

}

# helper function to check if any of the element in a list is in another list
def is_in(lst1, lst2):
    for element in lst1:
        if element in lst2:
            return True
    return False

# format locations into salesforce format
def format_location(str):
    location_list = str.split(', ')
    if 'Canada' in location_list:
        if len(location_list) == 3:
            if len(location_list[1]) == 2:
                return location_list[0] + ', ' + can_province_dict[location_list[1]] + ', ' + location_list[2]
            else:
                return location_list[0] + ', ' + location_list[1] + ', ' + location_list[2]
        else:
            if len(location_list) == 1:
                return 'Toronto, Ontario, Canada'
            else:
                if location_list[0] in canada_province:
                    return major_cities_canada[location_list[0]][0] + ', ' + location_list[0] + ', ' + location_list[1]
                elif location_list[0] in canada_province_abbr:
                    return major_cities_canada[can_province_dict[location_list[0]]][0] + ', ' + \
                        can_province_dict[location_list[0]] + ', ' + location_list[1]
                elif 'Greater Toronto Area' in location_list:
                    return 'Toronto, Ontario, Canada'
                elif 'Greater Montreal Metropolitan Area' in location_list:
                    return 'Montreal, Quebec, Canada'
                elif 'Greater Vancouver Metropolitan Area' in location_list:
                    return 'Vancouver, British Columbia, Canada'
                elif 'Greater Ottawa Metropolitan Area' in location_list:
                    return 'Ottawa, Ontario, Canada'
                elif is_in(location_list, canada_cities_to_provinces.keys()):
                    return location_list[0] + ', ' + canada_cities_to_provinces[location_list[0]] + ', ' + 'Canada'
    elif 'Greater Toronto Area' in location_list:
        return 'Toronto, Ontario, Canada'
    elif 'Greater Montreal Metropolitan Area' in location_list:
        return 'Montreal, Quebec, Canada'
    elif 'Greater Vancouver Metropolitan Area' in location_list:
        return 'Vancouver, British Columbia, Canada'
    elif 'Greater Ottawa Metropolitan Area' in location_list:
        return 'Ottawa, Ontario, Canada'
    elif is_in(location_list, canada_province):
        if len(location_list) == 1:
            return major_cities_canada[location_list[0]][0] + ', ' + location_list[0] + ', ' + 'Canada'
        else:
            return location_list[0] + ', ' + location_list[1] + ', ' + 'Canada'
    elif is_in(location_list, canada_province_abbr):
        if len(location_list) == 1:
            return major_cities_canada[can_province_dict[location_list[0]]][0] + ', ' + can_province_dict[location_list[0]] + ', ' + 'Canada'
        else:
            return location_list[0] + ', ' + can_province_dict[location_list[1]] + ', ' + 'Canada'
    elif 'United States' in location_list or 'United States of America' in location_list or 'USA' in location_list\
        or 'US' in location_list:
        if len(location_list) == 3:
            if len(location_list[1]) == 2:
                return location_list[0] + ', ' + us_state_dict[location_list[1]] + ', ' + 'United States'
            else:
                return location_list[0] + ', ' + location_list[1] + ', ' + 'United States'
        else:
            if len(location_list) == 1:
                return 'New York, New York, United States'
            else:
                if location_list[0] in us_states:
                    return us_state_cities[location_list[0]][0] + ', ' + location_list[0] + ', ' + 'United States'
                elif location_list[0] in us_states_abbr:
                    return us_state_cities[us_state_dict[location_list[0]]][0] + ', ' + \
                        us_state_dict[location_list[0]] + ', ' + 'United States'
                elif is_in(location_list, us_cities_states.keys()):
                    return location_list[0] + ', ' + us_cities_states[location_list[0]] + ', ' + 'United States'
    elif is_in(location_list, us_states):
        if len(location_list) == 1:
            return us_state_cities[location_list[0]][0] + ', ' + location_list[0] + ', ' + 'United States'
        else:
            return location_list[0] + ', ' + location_list[1] + ', ' + 'United States'
    elif is_in(location_list, us_states_abbr):
        if len(location_list) == 1:
            return us_state_cities[us_state_dict[location_list[0]]][0] + ', ' + us_state_dict[
                location_list[0]] + ', ' + 'United States'
        else:
            return location_list[0] + ', ' + us_state_dict[location_list[1]] + ', ' + 'United States'
    elif is_in(location_list, us_cities_states.keys()):
        return location_list[0] + ', ' + us_cities_states[location_list[0]] + ', ' + 'United States'
    elif 'Greater Boston' in location_list:
        return 'Boston, Massachusetts, United States'
    elif 'San Francisco Bay Area' in location_list:
        return 'San Francisco, California, United States'
    elif 'Greater New York City Area' in location_list:
        return 'New York, New York, United States'
    elif location_list == [''] or location_list == []:
        return ''
    elif is_in(location_list, country_capitals.keys()):
        if len(location_list) == 1:
            return country_capitals[location_list[0]] + ', ' + location_list[0]
        elif len(location_list) == 2:
            return country_capitals[location_list[1]] + ', ' + location_list[1]
        else:
            return country_capitals[location_list[2]] + ', ' + location_list[2]
    else:
        return 'Toronto, Ontario, Canada'

# data = pd.read_csv('Job Trending Analysis.csv')
# for index, row in data.iterrows():
#     data.loc[index, 'Formatted Location'] = format_location(str(row['Location']))
#     print(row)


# # save the new researcher data locally
# data.to_csv('Job Trending Analysis.csv')


# print(format_location('Toronto, ON, Canada'))
# print(format_location('Toronto, Ontario, Canada'))
# print(format_location('Ontario, Canada'))
# print(format_location('Greater Toronto Area, Canada'))
# print(format_location('Canada'))
# print(format_location('Quebec, Canada'))
# print(format_location('Halifax, NS, Canada'))
# print(format_location('North York, Canada'))
# print(format_location('QC, Canada'))
# print(format_location('Winnipeg, Manitoba, Canada'))
# print(format_location('Greater Montreal Metropolitan Area'))
# print(format_location('Greater Vancouver Metropolitan Area'))
# print(format_location('Greater Toronto Area'))
# print(format_location('Nova Scotia'))
# print(format_location('Montreal, Quebec'))
# print(format_location('Edmonton, AB'))
# print(format_location('AB'))
# print(format_location('Fredericton, New Brunswick, Canada'))
# print(format_location('Texas, USA'))
# print(format_location('Austin, USA'))
# print(format_location('Boston, USA'))
# print(format_location('Massachusetts, USA'))
# print(format_location('Cambridge, MA'))
# print(format_location('California, USA'))
# print(format_location('Mountain View, USA'))
# print(format_location('New York City, USA'))
# print(format_location('New York, New York, United States'))
# print(format_location('New York, USA'))
# print(format_location('United States'))
# print(format_location('USA'))
# print(format_location('New Jersey, USA'))
# print(format_location('Philadelphia, USA'))
# print(format_location('San Francisco, USA'))
# print(format_location('San Francisco, USA, USA'))
# print(format_location('Washington, USA'))
# print(format_location('Seattle, USA'))
# print(format_location('Standford, USA'))
# print(format_location('Champaign, Illinois, United States'))
# print(format_location('Italy'))
# print(format_location(''))
# print(format_location('Switzerland'))
# print(format_location('Remote'))
# print(format_location('500+ connections'))
# print(format_location('Greater Boston'))
# print(format_location('Mountain View'))
# print(format_location('San Francisco Bay Area'))
# print(format_location('TÃ¼bingen, Baden-WÃ¼rttemberg, Germany'))
# print(format_location('Greater New York City Area'))
# print(format_location('Senegal'))
# print(format_location('Rwanda'))
# print(format_location('Slovenia'))
# print(format_location('England'))

# helper function for mapping job titles

# Define a common abbreviations mapping
common_abbreviations = {
    "Artificial Intelligence": "AI",
    "Machine Learning": "ML",
    "Management": "Mgmt",
    "Engineer": "Eng",
    "Developer": "Dev",
    "Product": "Prod",
    "Marketing": "Mktg",
    "Customer": "Cust",
    "Technical": "Tech",
    "Project Management": "PM"
}


# Define a mapping function
def map_string(string):
    # Split the job title into individual words
    words = string.split()

    # Loop through each word and replace with the abbreviated version if available
    for i, word in enumerate(words):
        for abbreviation, abbreviated_word in common_abbreviations.items():
            if distance.get_jaro_distance(word.lower(), abbreviation.lower()) > 0.9:
                words[i] = abbreviated_word

    # Join the words back together to form the new job title
    new_title = " ".join(words)
    return new_title

# print(distance.get_jaro_distance('Applied ML Intern', 'Applied Machine Learning Intern'))
# print(distance.get_jaro_distance('SME', 'SME Program Design Intern'))
# print(distance.get_jaro_distance('AI Engineer', 'Artificial Intelligence'))
# print(distance.get_jaro_distance('Project Management Intern', 'AI Project Management Intern'))
# print(distance.get_jaro_distance('Scotia Insurance', 'Scotiabank'))
# print(distance.get_jaro_distance('RBC', 'Royal Bank of Canada'))

def generate_aliases(company_name):
    company_name = company_name.strip()
    words = company_name.split()
    alias_list = []

    # Generate all possible combinations of words
    for i in range(len(words)):
        alias = " ".join(words[0:i + 1])
        alias_list.append(alias)

    # Check for common abbreviations
    if "Bank" in words:
        if "TD" in alias_list:
            alias_list.append("TD")
            alias_list.append("TD Bank")
    if "Montreal" in words:
        if "BMO" in alias_list:
            alias_list.append("BMO")
    if "Financial" in words:
        if "BMO" in alias_list:
            alias_list.append("BMOF")

    # Generate the first alphabet of each word
    if len(words) > 1:
        first_alphabets = "".join([word[0] for word in words])
        alias_list.append(first_alphabets)

    return alias_list

# helper function to categorize program
def categorize_program(s):
    program = s.lower()
    if 'engineering' in program or 'science' in program or 'data' in program or 'technology' in program \
            or 'mathematics' in program or 'health' in program:
        return 'Core Technical'
    else:
        return 'Complementary'

