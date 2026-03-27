# import libraries
import gspread
import pandas as pd
import numpy as np
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from pyjarowinkler import distance
from helper_functions import date_transform
from helper_functions import format_location
from helper_functions import map_string
from helper_functions import is_in
from helper_functions import generate_aliases
from helper_functions import categorize_program
from categorize_job_titles import categorize_job_title

# pandas display option
pd.set_option('display.max_columns', 10)

# define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('linkedinupdate-28ab8d2b40be.json', scope)
# print(creds)

# authorize the clientsheet
client = gspread.authorize(creds)

# get the instance of LinkedIn scrape
raise_scrape = client.open('Oct 2025 - VSAI All Time Scrape')

# read LinkedIn scrape data
linkedin_instance = raise_scrape.get_worksheet(0)
# print(linkedin_instance)

# get all the records of LinkedIn data
linkedin_data = linkedin_instance.get_all_values()
# for i in range(10):
#     print(linkedin_data[i])

# convert to dataframe
headers = linkedin_data[0]
linkedin_df = pd.DataFrame.from_records(linkedin_data[1:], columns=headers, index='baseUrl')
# linkedin_df = linkedin_df.reset_index()
# print(linkedin_df.head())
# print(linkedin_df.columns)

# read raise gsheet
raise_outcome_gsheet = client.open('All-time VSAI Scrape List')

# get the Researcher Outcomes sheet of the Spreadsheet
raise_outcome = raise_outcome_gsheet.get_worksheet(0)

# get all the records of the data
raise_data = raise_outcome.get_all_values()
# print(researcher_data)

# convert to dataframe
headers = raise_data[0]
raise_df = pd.DataFrame.from_records(raise_data[1:], columns=headers)
# researcher_df = researcher_df.reset_index()
# print(researcher_df.head())
# print(researcher_df.describe())

# get the HQP Role Category sheet
hqp_role_categories = raise_outcome_gsheet.get_worksheet(1)

# get all the records of the data
hqp_data = hqp_role_categories.get_all_values()

# convert to dataframe
headers = hqp_data[0]
hqp_df = pd.DataFrame.from_records(hqp_data[1:], columns=headers)
# print(hqp_df.head())

# get the Employer Details sheet
employer_details = raise_outcome_gsheet.get_worksheet(2)

# get all the records of the data
employer_data = employer_details.get_all_values()

# convert to dataframe
headers = employer_data[0]
employer_df = pd.DataFrame.from_records(employer_data[1:], columns=headers)
# print(employer_df.head())

# # Update Start Date and End Date for former raises
# for index, row in raise_df.iterrows():
#     if row['Linkedin'] in linkedin_df.index:
#         employer_record = row['Employer']
#         employer_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'company'].values[0]
#         employer_second_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'company2'].values[0]
#         job_title_record = row['Job Title']
#         job_title_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobTitle'].values[0]
#         job_title_second_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobTitle2'].values[0]
#         job_date_range_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobDateRange'].values[0]
#         job_date_range_second_latest = \
#             linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobDateRange2'].values[0]
#         if employer_latest == employer_record and distance.get_jaro_distance(map_string(job_title_latest), job_title_record) > 0.75:
#             start_date = date_transform(job_date_range_latest)[0]
#             end_date = date_transform(job_date_range_latest)[1]
#             row['start_date'] = start_date
#             row['end_date'] = end_date
#         elif employer_second_latest == employer_record and distance.get_jaro_distance(map_string(job_title_second_latest), job_title_record) > 0.75:
#             start_date = date_transform(job_date_range_second_latest)[0]
#             end_date = date_transform(job_date_range_second_latest)[1]
#             row['start_date'] = start_date
#             row['end_date'] = end_date

print('Updating Employer and Job Title...')
print('...')
print('...')
print('Update Started...')
print("----------")

# Update Employer and Job Title
check_list = []
for index, row in raise_df.iterrows():
    if row['Linkedin'] in check_list:
        pass
    else:
        check_list.append(row['Linkedin'])
        if row['Linkedin'] in linkedin_df.index:
            employer_record = row['Employer']
            employer_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'company'].values[0]
            employer_second_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'company2'].values[0]
            job_title_record = row['Job Title']
            job_title_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobTitle'].values[0]
            job_title_second_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobTitle2'].values[0]
            job_date_range_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobDateRange'].values[0]
            job_date_range_second_latest = \
            linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobDateRange2'].values[0]
            location_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobLocation'].values
            location_second_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobLocation2'].values
            location_profile = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'location'].values
            if row['Linkedin'] != 'No Linkedin Found':
                if employer_latest == '' and employer_second_latest == '':
                    print(f"No LinkedIn Candidate Found -- {row['Full Name']}")
                    print("----------")
                else:
                    if str(employer_latest) != employer_record:
                        raise_df.loc[index, 'Historical Record?'] = 'Yes'
                        print(f"New employer found for {row['Full Name']} -- {str(employer_latest)}")
                        print("...")
                        print(
                            f"Adding new employer and job title for {row['Full Name']} -- {str(employer_latest)}, {str(job_title_latest)}")
                        print("...")
                        start_date = date_transform(job_date_range_latest)[0]
                        end_date = date_transform(job_date_range_latest)[1]
                        if (row['start_date'] != '') and (
                                row['end_date'] == 'Present' or row['end_date'] == 'present' or row['end_date'] == '') \
                                and (start_date > datetime.strptime(row['start_date'], '%Y-%m-%d').date()):
                            raise_df.loc[index, 'end_date'] = start_date
                            print(f"existing role info updated for {row['Full Name']}")
                        raise_df = pd.concat([raise_df, pd.DataFrame({'Contact ID': [row['Contact ID']],
                                                                        'First Name': [row['First Name']],
                                                                        'Last Name': [row['Last Name']],
                                                                        'Pref Name': [row['Pref Name']],
                                                                        'Full Name': [row['Full Name']],
                                                                        'Full Preferred Name': [
                                                                            row['Full Preferred Name']],
                                                                        'Email': [row['Email']],
                                                                        'Linkedin': [row['Linkedin']],
                                                                        'University': [row['University']],
                                                                        'Degree Level': [row['Degree Level']],
                                                                        'Program Name': [row['Program Name']],
                                                                        'Core or Complementary?': [
                                                                            row['Core or Complementary?']],
                                                                        'Cohort': [row['Cohort']],
                                                                        'Scrape Month': ['x'],
                                                                        'Affiliation to Vector': [
                                                                            row['Affiliation to Vector']],
                                                                        'VSAI Recipient': [row['VSAI Recipient']],
                                                                        'Employed?': [row['Employed?']],
                                                                        'Employer': [employer_latest],
                                                                        'Employer Type': [''],
                                                                        'Employer Size': [''],
                                                                        'Category': [''],
                                                                        'Job Title': [job_title_latest],
                                                                        'Standard Job Title': [''],
                                                                        'Standard Job Group': [''],
                                                                        'HQP Role': [''],
                                                                        'Status': [''],
                                                                        'Location': [location_latest[
                                                                                         0] if location_latest.size != 0 else
                                                                                     location_profile[0]],
                                                                        'Location Formatted': [''],
                                                                        'start_date': [start_date],
                                                                        'end_date': [end_date],
                                                                        'sector_of_interest': [''],
                                                                        'Formula (Location of Employment)': [''],
                                                                        'Historical Record?': ['']})],
                                              ignore_index=True)
                        print(f"New employer and job title added for {row['Full Name']}")
                        print("----------")
                    else:
                        if job_title_latest == '':
                            pass
                        elif distance.get_jaro_distance(map_string(job_title_latest), job_title_record) < 0.75:
                            raise_df.loc[index, 'Historical Record?'] = 'Yes'
                            print(f"New employer found for {row['Full Name']} -- {str(employer_latest)}")
                            print("...")
                            print(
                                f"Adding new employer and job title for {row['Full Name']} -- {str(employer_latest)}, {str(job_title_latest)}")
                            print("...")
                            start_date = date_transform(job_date_range_latest)[0]
                            end_date = date_transform(job_date_range_latest)[1]
                            if (row['start_date'] != '') and (
                                    row['end_date'] == 'Present' or row['end_date'] == 'present' or row[
                                'end_date'] == '') and (start_date > datetime.strptime(row['start_date'], '%Y-%m-%d').date()):
                                raise_df.loc[index, 'end_date'] = start_date
                                print(f"existing role info updated for {row['Full Name']}")
                            raise_df = pd.concat([raise_df, pd.DataFrame({'Contact ID': [row['Contact ID']],
                                                                            'First Name': [row['First Name']],
                                                                            'Last Name': [row['Last Name']],
                                                                            'Pref Name': [row['Pref Name']],
                                                                            'Full Name': [row['Full Name']],
                                                                            'Full Preferred Name': [
                                                                                row['Full Preferred Name']],
                                                                            'Email': [row['Email']],
                                                                            'Linkedin': [row['Linkedin']],
                                                                            'University': [row['University']],
                                                                            'Degree Level': [row['Degree Level']],
                                                                            'Program Name': [row['Program Name']],
                                                                            'Core or Complementary?': [
                                                                                row['Core or Complementary?']],
                                                                            'Cohort': [row['Cohort']],
                                                                            'Scrape Month': ['x'],
                                                                            'Affiliation to Vector': [
                                                                                row['Affiliation to Vector']],
                                                                            'VSAI Recipient': [row['VSAI Recipient']],
                                                                            'Employed?': [row['Employed?']],
                                                                            'Employer': [employer_latest],
                                                                            'Employer Type': [''],
                                                                            'Employer Size': [''],
                                                                            'Category': [''],
                                                                            'Job Title': [job_title_latest],
                                                                            'Standard Job Title': [''],
                                                                            'Standard Job Group': [''],
                                                                            'HQP Role': [''],
                                                                            'Status': [''],
                                                                            'Location': [location_latest[
                                                                                             0] if location_latest.size != 0 else
                                                                                         location_profile[0]],
                                                                            'Location Formatted': [''],
                                                                            'start_date': [start_date],
                                                                            'end_date': [end_date],
                                                                            'sector_of_interest': [''],
                                                                            'Formula (Location of Employment)': [''],
                                                                            'Historical Record?': ['']})],
                                                  ignore_index=True)
                            print(f"New employer and job title added for {row['Full Name']}")
                            print("----------")
                        else:
                            print(f"No new job found for {row['Full Name']}")
                            print("----------")
            else:
                print(f"No LinkedIn Candidate Found -- {row['Full Name']}")
                print("----------")
        else:
            print(f"Candidate not found -- {row['Full Name']}")
            print("----------")

print('Employer and Job Title Update Finished.')
print('...')
print('...')
print('Standardizing EmployerID...')
print('...')
print('...')
print('Update Started...')
print("----------")

raise_df['Employer Standardized'] = raise_df.apply(lambda _: '', axis = 1)
for index, row in raise_df.iterrows():
    if row['Employer'] == '':
        pass
    else:
        employer_std = employer_df[employer_df['Employer'] == row['Employer']]['Employer']
        if employer_std.size != 0:
            row['Employer Standardized'] = employer_std.values[0]
            print(f"Updating Employer for {row['Full Name']} -- {row['Employer']}")
            print("----------")
        else:
            alias = generate_aliases(row['Employer'])
            for i, r in employer_df.iterrows():
                if distance.get_jaro_distance(r['Employer'], row['Employer']) >= 0.75 and is_in(alias, r['Alias']):
                    employer_std = r['Employer']
                    row['Employer Standardized'] = employer_std
                    print(f"Updating Employer for {row['Full Name']} -- {row['Employer']}")
                    print("----------")

print('Employer Update Finished.')
print('...')
print('...')
print('Updating Employed?...')
print('...')
print('...')
print('Update Started...')
print("----------")


# Update Employed?, Employer Type, Employer Size, and sector_of_interest
for index, row in raise_df.iterrows():
    employer_type = employer_df[employer_df['Employer'] == row['Employer Standardized']]['Employer Type']
    employer_size = employer_df[employer_df['Employer'] == row['Employer Standardized']]['Employer Size']
    sector_of_interest = employer_df[employer_df['Employer'] == row['Employer Standardized']]['sector_of_interest']
    # # Add Employer Type
    # if row['Employer Type'] == '':
    #     if employer_type.size > 0:
    #         print(f"Adding Employer Type for {row['Full Name']} -- {row['Employer Standardized']}")
    #         row['Employer Type'] = employer_type.values[0]
    #         print(f"Employer Type added for {row['Full Name']}")
    #         print("----------")
    #     else:
    #         print(f"Employer Type not found for {row['Full Name']} -- {row['Employer Standardized']}")
    #         print("----------")
    # else:
    #     print(f"Employer Type for {row['Full Name']} already filled -- {row['Employer Standardized']}")
    #     print("----------")
    # # Add Employer Size
    # if row['Employer Size'] == '':
    #     if employer_size.size > 0:
    #         print(f"Adding Employer Size for {row['Full Name']} -- {row['Employer Standardized']}")
    #         row['Employer Size'] = employer_size.values[0]
    #         print(f"Employer Size added for {row['Full Name']}")
    #         print("----------")
    #     else:
    #         print(f"Employer Size not found for {row['Full Name']} -- {row['Employer Standardized']}")
    #         print("----------")
    # else:
    #     print(f"Employer Size for {row['Full Name']} already filled -- {row['Employer Standardized']}")
    #     print("----------")
    # # Add sector_of_interest
    # if row['sector_of_interest'] == '':
    #     if sector_of_interest.size > 0:
    #         print(f"Adding sector_of_interest for {row['Full Name']} -- {row['Employer Standardized']}")
    #         row['sector_of_interest'] = sector_of_interest.values[0]
    #         print(f"sector_of_interest added for {row['Full Name']}")
    #         print("----------")
    #     else:
    #         print(f"sector_of_interest not found for {row['Full Name']} -- {row['Employer Standardized']}")
    #         print("----------")
    # else:
    #     print(f"sector_of_interest for {row['Full Name']} already filled -- {row['Employer Standardized']}")
    #    print("----------")
    # Add Employed?
    if row['Employer'] != '':
        if row['end_date'] != 'Present':
            print(f"Adding Employed? for {row['Full Name']}")
            raise_df.loc[index, 'Employed?'] = 'Unemployed'
            print(f"Employed? added for {row['Full Name']}")
            print("----------")
        else:
            print(f"Adding Employed? for {row['Full Name']}")
            raise_df.loc[index, 'Employed?'] = 'Employed'
            print(f"Employed? added for {row['Full Name']}")
            print("----------")
    else:
        if row['Employed?'] == '':
            print(f"Adding Employed? for {row['Full Name']}")
            raise_df.loc[index, 'Employed?'] = 'Unemployed'
            print(f"Employed? added for {row['Full Name']}")
            print("----------")
        else:
            print(f"Employed? for {row['Full Name']} already filled")

# print(researcher_df[researcher_df['Full Name'] == 'Alex Gao'][['Employer', 'Job Title', 'Employed?', 'Employer Type', 'Employer Size', 'sector_of_interest', 'Location']])

# print(linkedin_df.loc[linkedin_df.index == 'https://www.linkedin.com/in/aditi-maheshwari/', 'jobLocation'].values)

print('Employed? Update Finished.')
print('...')
print('...')
print('Updating Location Formatted...')
print('...')
print('...')
print('Update Started...')
print("----------")

# fill location for existing records
for index, row in raise_df.iterrows():
    if row['Employed?'] == 'Unemployed' and row['Employer'] == '':
        pass
    else:
        if row['Linkedin'] in linkedin_df.index:
            location_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobLocation'].values
            location_second_latest = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'jobLocation2'].values
            location_profile = linkedin_df.loc[linkedin_df.index == row['Linkedin'], 'location'].values
            # print(location_latest)
            # print(location_second_latest)
            # print(location_profile)
            if row['Location'] == '':
                if np.any(location_latest==['']):
                    if np.any(location_second_latest == ['']):
                        if np.any(location_profile == ['']):
                            raise_df.loc[index, 'Location'] = 'Canada'
                        else:
                           raise_df.loc[index, 'Location'] = location_profile[0]
                    else:
                        raise_df.loc[index, 'Location'] = location_second_latest[0]
                else:
                    raise_df.loc[index, 'Location'] = location_latest[0]
            else:
                pass
        else:
            pass

# Format the locations for raise data
for index, row in raise_df.iterrows():
    if row['Employed?'] == 'Unemployed' and row['Employer'] == '':
        pass
    else:
        if row['Location Formatted'] == '':
            if row['Location'] != '':
                raise_df.loc[index, 'Location Formatted'] = format_location(row['Location'])
                print(f"Location formatted for {row['Full Name']}")
                print("----------")
            else:
                print(f"Location missing for {row['Full Name']}")
                print("----------")
                pass
        else:
            print(f"Location already formatted for {row['Full Name']}")
            print("----------")
            pass

print('Location Formatted Update Finished.')
print('...')
print('...')
print('Updating Category, Status...')
print('...')
print('...')
print('Update Started...')
print("----------")

# Update Category (Permanent/Contract) and Status (Full-time/Part-time)
for index, row in raise_df.iterrows():
    job_title = row['Job Title'].lower()
    if row['Employed?'] == 'Unemployed' and row['Employer'] == '':
        pass
    else:
        if row['Category'] == '':
            if 'graduate student' in job_title or 'phd student' in job_title or 'master thesis student' in job_title or\
                'master student' in job_title or 'capstone project student' in job_title or 'project student' in job_title:
                raise_df.loc[index, 'Category'] = 'Undefined'
                print(f"Updating job category for {row['Full Name']} -- Undefined")
                print("----------")
            elif 'intern' in job_title or 'summer' in job_title or 'co-op' in job_title or 'student' in job_title:
                raise_df.loc[index, 'Category'] = 'Internship/Co-op'
                print(f"Updating job category for {row['Full Name']} -- raiseship/Co-op")
                print("----------")
            elif 'contract' in job_title or 'postdoc' in job_title or 'post doc' in job_title\
                    or 'teaching assistant' in job_title:
                raise_df.loc[index, 'Category'] = 'Contract'
                print(f"Updating job category for {row['Full Name']} -- Contract")
                print("----------")
            else:
                raise_df.loc[index, 'Category'] = 'Permanent'
                print(f"Updating job category for {row['Full Name']} -- Permanent")
                print("----------")
        if row['Status'] == '':
            if 'part' in job_title or 'part-time' in job_title or 'part time' in job_title \
                    or 'teaching assistant' in job_title or 'undergrad researcher' in job_title or\
                    'student researcher' in job_title or 'research student' in job_title:
                raise_df.loc[index, 'Status'] = 'Part-Time (Less Than 30 Hours)'
                print(f"Updating job status for {row['Full Name']} -- Part-Time")
                print("----------")
            else:
                raise_df.loc[index, 'Status'] = 'Full-Time (30 Hours or More)'
                print(f"Updating job status for {row['Full Name']} -- Full-Time")
                print("----------")

print('Category and Status Update Finished.')
print('...')
print('...')
# print('Updating SchoolID, FacultyID, DepartmentID, ProgramID...')
# print('...')
# print('...')
# print('Update Started...')
# print("----------")

# # update SchoolID
# raise_df['SchoolID'] = raise_df.apply(lambda _: '', axis = 1)
# raise_df['School Name'] = raise_df.apply(lambda _: '', axis = 1)
# for index, row in raise_df.iterrows():
#     if row['University'] == '':
#         pass
#     else:
#         for i, r in employer_df.iterrows():
#             if 'University' in r['Account Name'] or 'College' in r['Account Name'] or 'Institute' in r['Account Name']:
#                 if 'University of ' + row['University'] == r['Account Name'] or row['University'] + ' University' == r['Account Name']:
#                     row['School Name'] = r['Account Name']
#                     row['SchoolID'] = r['Account ID']
#                     print(f"Updating SchoolID for {row['Full Name']} -- {r['Account Name']}")
#                     print("----------")
#
# print('SchoolID Update Finished.')
# print('...')
# print('...')
# print('Updating FacultyID, DepartmentID, ProgramID...')
# print('...')
# print('...')
# print('Update Started...')
# print("----------")
# # update FacultyID, DepartmentID, ProgramID
# raise_df['FacultyID'] = raise_df.apply(lambda _: '', axis = 1)
# raise_df['Faculty Name'] = raise_df.apply(lambda _: '', axis = 1)
# raise_df['DepartmentID'] = raise_df.apply(lambda _: '', axis = 1)
# raise_df['Department'] = raise_df.apply(lambda _: '', axis = 1)
# raise_df['ProgramID'] = raise_df.apply(lambda _: '', axis = 1)
# for index, row in raise_df.iterrows():
#     if row['University'] == '':
#         pass
#     else:
#         merge = row['School Name'] + row['Program Name']
#         faculty_id = academic_df[academic_df['Merge'] == merge]['Faculty ID']
#         faculty = academic_df[academic_df['Merge'] == merge]['Faculty Name']
#         department_id = academic_df[academic_df['Merge'] == merge]['Department ID']
#         department = academic_df[academic_df['Merge'] == merge]['Department Name']
#         program_id = academic_df[academic_df['Merge'] == merge]['Program ID']
#         if faculty_id.size != 0:
#             row['FacultyID'] = faculty_id.values[0]
#             row['Faculty Name'] = faculty.values[0]
#             row['DepartmentID'] = department_id.values[0]
#             row['Department'] = department.values[0]
#             row['ProgramID'] = program_id.values[0]
#             print(f"Updating FacultyID, DepartmentID, ProgramID for {row['Full Name']}")
#             print("----------")
#
# print('FacultyID, DepartmentID, ProgramID Update Finished.')
# print('...')
# print('...')

print('...')
print('...')
print('Updating Formula (Location of Employment)')
print('...')
print('...')
print('Update Started...')
print("----------")

# update Location of Employement
for index, row in raise_df.iterrows():
    if row['Employed?'] == 'Unemployed' and row['Employer'] == '':
        pass
    else:
        if row['Location Formatted'] == '':
            raise_df.loc[index, 'Formula (Location of Employment)'] = 'Employed in Ontario'
            print(f"Updating Formula (Location of Employment) for {row['Full Name']}")
            print("----------")
        elif row['Location Formatted'] == 'Greater Toronto Area (GTA)' or \
           raise_df.loc[index, 'Formula (Location of Employment)'] == 'Ontario (outside GTA, Kitchener-Waterloo or Ottawa)' or \
            row['Location Formatted'] == 'Kitchener-Waterloo Area' or \
            row['Location Formatted'] == 'Ontario (outside GTA, Kitchener-Waterloo or Ottawa)' or \
            row['Location Formatted'] == 'Ottawa Area':
            raise_df.loc[index, 'Formula (Location of Employment)'] = 'Employed in Ontario'
            print(f"Updating Formula (Location of Employment) for {row['Full Name']}")
            print("----------")
        elif row['Location Formatted'] == 'Canada (outside Ontario)':
            raise_df.loc[index, 'Formula (Location of Employment)'] = 'Employed in Canada, Not Ontario'
            print(f"Updating Formula (Location of Employment) for {row['Full Name']}")
            print("----------")
        elif row['Location Formatted'] == 'USA':
            raise_df.loc[index, 'Formula (Location of Employment)'] = 'Employed in the United States'
            print(f"Updating Formula (Location of Employment) for {row['Full Name']}")
            print("----------")
        else:
            raise_df.loc[index, 'Formula (Location of Employment)'] = 'Employed Internationally, Not in the United States'
            print(f"Updating Formula (Location of Employment) for {row['Full Name']}")
            print("----------")

print('Formula (Location of Employment) Update Finished.')
print('...')
print('...')
print('Create new records for unemployed people')
print('...')
print('...')
print('Update Started...')
print("----------")

# create new records for unemployed people
# for index, row in raise_df.iterrows():
#     if row['Employed?'] == 'Unemployed' and row['Employer'] != '':
#         raise_df.loc[index, 'Historical Record?'] = 'Yes'
#         raise_df = pd.concat([raise_df, pd.DataFrame({'Contact ID': [row['Contact ID']],
#                                                       'First Name': [row['First Name']],
#                                                       'Last Name': [row['Last Name']],
#                                                       'Pref Name': [row['Pref Name']],
#                                                       'Full Name': [row['Full Name']],
#                                                       'Full Preferred Name': [
#                                                           row['Full Preferred Name']],
#                                                       'Email': [row['Email']],
#                                                       'Linkedin': [row['Linkedin']],
#                                                       'University': [row['University']],
#                                                       'Degree Level': [row['Degree Level']],
#                                                       'Program Name': [row['Program Name']],
#                                                       'Core or Complementary?': [
#                                                           row['Core or Complementary?']],
#                                                       'Cohort': [row['Cohort']],
#                                                       'Scrape Month': ['6'],
#                                                       'Affiliation to Vector': [
#                                                           row['Affiliation to Vector']],
#                                                       'VSAI Recipient': [row['VSAI Recipient']],
#                                                       'Employed?': [row['Employed?']],
#                                                       'Employer': [''],
#                                                       'Employer Type': [''],
#                                                       'Employer Size': [''],
#                                                       'Category': [''],
#                                                       'Job Title': [''],
#                                                       'Standard Job Title': [''],
#                                                       'Standard Job Group': [''],
#                                                       'HQP Role': [''],
#                                                       'Status': [''],
#                                                       'Location': [''],
#                                                       'Location Formatted': [''],
#                                                       'start_date': [''],
#                                                       'end_date': [''],
#                                                       'sector_of_interest': [''],
#                                                       'Formula (Location of Employment)': [''],
#                                                       'Historical Record?': [''],
#                                                       'Employer Standardized': ['']})],
#                              ignore_index=True)
#         print(f"Creating new records for {row['Full Name']}")
#         print(print("----------"))

# print('Update finished.')
# print('...')
# print('...')
# print('Updating Core or Complementary?...')
# print('...')
# print('...')
# print('Update Started...')
# print("----------")

# # update Core or Complementary?
# for index, row in raise_df.iterrows():
#     raise_df.loc[index, 'Core or Complementary?'] = categorize_program(row['Program Name'])
#     print(f"Core or Complementary? updated for {row['Full Name']}")
#     print("----------")
# print('Core or Complementary Update Finished.')

# update Standard Job Title
for index, row in raise_df.iterrows():
    raise_df.loc[index, 'Standard Job Title'] = categorize_job_title(str(row['Job Title']))


# save the new researcher data locally
raise_df.to_csv('All-time VSAI Scrape.csv')