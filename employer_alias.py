import pandas as pd
from graduate_outcomes_linkedin_employment_update import employer_df

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

alias_list = []
for index, row in employer_df.iterrows():
    alias_list.append(generate_aliases(row['Employer']))

employer_df['Alias'] = alias_list

# print(employer_df.head()['Alias'])

# save the new researcher data locally
employer_df.to_csv('Employer Details Updated.csv')
