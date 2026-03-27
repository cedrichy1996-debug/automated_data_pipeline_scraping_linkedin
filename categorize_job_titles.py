# import libraries
import pandas as pd

# Define your own categories
categories = ["Business Intelligence Analyst",
              "Data Scientist",
              "Technical Architect",
              "Other",
              "Senior Data Scientist",
              "Manager, AI-Related Department",
              "Software Developer",
              "Data Analyst",
              "Senior Manager, AI-Related Department",
              "Senior Analyst",
              "Analyst",
              "Data Engineer",
              "ML Researcher",
              "Director, AI-Related Department",
              "Software Analyst",
              "Postdoctoral Fellowship",
              "ML Engineer",
              "Research Engineer",
              "Business Analyst",
              "Software Engineer",
              "Technical Business Analyst",
              "Research Scientist",
              "Business Development",
              "ML Scientist",
              "Systems Administrator",
              "Data Architect",
              "Product Engineer",
              "Product Manager",
              "Team Lead, AI Related Department",
              "Data Governance Specialist",
              "Research Analyst",
              "Computational Biologist",
              "Administrative Assistant/Coordinator",
              "Database Analyst",
              "Senior Business Intelligence Analyst",
              "Researcher",
              "Project Manager",
              "Fraud Strategist",
              "Senior Consultant",
              "Consultant",
              "Senior Business Analyst",
              "Senior Data Analyst",
              "Course Instructor/Professor",
              "Senior Fraud Strategist",
              "Senior Software Developer",
              "Engineer"]

std_job_group = {
    'Data or Business Analyst':
        ['Business Intelligence Analyst',
         'Data Analyst',
         'Senior Analyst',
         'Analyst',
         'Software Analyst',
         'Business Analyst',
         'Technical Business Analyst',
         'Business Development',
         'Data Architect',
         'Database Analyst',
         'Senior Business Intelligence Analyst',
         'Fraud Strategist',
         'Senior Consultant',
         'Senior Business Analyst',
         'Senior Data Analyst',
         'Senior Fraud Strategist'],
    'Researcher or Scientist':
        ['Data Scientist',
         'Senior Data Scientist',
         'ML Researcher',
         'Postdoctoral Fellowship',
         'Research Engineer',
         'Research Scientist',
         'ML Scientist',
         'Research Analyst',
         'Computational Biologist',
         'Researcher'],
    'Engineer':
        ['Technical Architect',
         'Data Engineer',
         'ML Engineer',
         'Software Engineer',
         'Product Engineer',
         'Engineer'],
    'Management Role':
        ['Manager, AI-Related Department',
         'Senior Manager, AI-Related Department',
         'Director, AI-Related Department',
         'Product Manager',
         'Team Lead, AI Related Department',
         'Project Manager'],
    'Software Developer':
        ['Software Developer',
         'Senior Software Developer'],
    'Other':
        ['Other',
         'Systems Administrator',
         'Data Governance Specialist',
         'Administrative Assistant/Coordinator',
         'Consultant',
         'Course Instructor/Professor']}


# define the function of categorize job titles to standard job titles
def categorize_job_title(title):
    title = title.lower()
    if 'analyst' in title:
        if 'business intelligence' in title or 'bi' in title:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Business Intelligence Analyst'
            else:
                return 'Business Intelligence Analyst'
        elif 'business' in title:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Business Analyst (Technical)'
            else:
                return 'Business Analyst (Technical)'
        elif 'financial' in title or 'finance' in title:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Financial Analyst'
            else:
                return 'Financial Analyst'
        elif 'data' in title:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Data Analyst'
            elif 'junior' in title or 'jr.' in title or 'jr' in title:
                return 'Junior Data Analyst'
            else:
                return 'Data Analyst'
        elif 'technical' in title:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Technical Analyst'
            else:
                return 'Technical Analyst'
        elif 'project' in title:
            return 'Project Analyst'
        elif 'research' in title:
            return 'Research Analyst'
        else:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Analyst (Technical)'
            else:
                return 'Analyst (Technical)'
    elif 'engineer' in title:
        if 'data' in title:
            return 'Data Engineer'
        elif 'software' in title:
            return 'Software Engineer'
        elif 'machine learning' in title or 'ML' in title or 'deep learning' in title or 'ai' in title or 'nlp' in title:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior ML Engineer'
            else:
                return 'ML Engineer'
        else:
            return 'Engineer'
    elif 'developer' in title:
        if 'junior' in title or 'jr.' in title or 'jr' in title:
            return 'Junior Software Developer'
        elif 'senior' in title or 'sr.' in title or 'sr' in title:
            return 'Senior Software Developer'
        else:
            return 'Software Developer'
    elif 'scientist' in title:
        if 'data' in title:
            if 'junior' in title:
                return 'Junior Data Scientist'
            elif 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Data Scientist'
            else:
                return 'Data Scientist'
        elif 'machine learning' in title or 'ML' in title or 'deep learning' in title or 'ai' in title or 'nlp' in title:
            return 'ML Scientist'
        elif 'research' in title:
            return 'Research Scientist'
    elif 'consultant' in title or 'advisor' in title:
        if 'data' in title or 'sap' in title or 'software' in title or 'ml' in title or 'innovation' in title \
                or 'digital' in title or 'it' in title or 'crm' in title or 'salesforce' in title or 'ai' in title \
                or 'artifical intelligence' in title or 'analytics' in title:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Consultant (Technical)'
            else:
                return 'Consultant (Technical)'
        else:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior Consultant (Non-Technical)'
            else:
                return 'Consultant (Non-Technical)'
    elif 'assistant' in title:
        if 'teaching' in title:
            return 'Teaching Assistant'
        elif 'research' in title:
            return 'Research Assistant'
    elif 'manager' in title or 'lead' in title or 'head' in title or 'supervisor' in title:
        if 'product' in title:
            return 'Product Manager'
        elif 'project' in title:
            return 'Project Manager'
        elif 'program' in title:
            if 'data' in title or 'sap' in title or 'software' in title or 'ml' in title or 'innovation' in title \
                    or 'digital' in title or 'it' in title or 'crm' in title or 'salesforce' in title or 'ai' in title \
                    or 'artifical intelligence' in title or 'analytics' in title:
                return 'Program Manager (Technical)'
            else:
                return 'Program Manager (Non-Technical)'
        elif 'operations' in title or 'ops' in title or 'op' in title:
            return 'Operations Manager'
        else:
            if 'data' in title or 'sap' in title or 'software' in title or 'ml' in title or 'innovation' in title \
                    or 'digital' in title or 'it' in title or 'crm' in title or 'salesforce' in title or 'ai' in title \
                    or 'artifical intelligence' in title or 'analytics' in title:
                return 'Manager (Technical)'
            else:
                return 'Manager (Non-Technical)'
    elif 'director' in title or 'vp' in title or 'vice-president' in title:
        if 'data' in title or 'sap' in title or 'software' in title or 'ml' in title or 'innovation' in title \
                or 'digital' in title or 'it' in title or 'crm' in title or 'salesforce' in title or 'ai' in title \
                or 'artifical intelligence' in title:
            return 'Director (Technical)'
        else:
            return 'Director (Non-Technical)'
    elif 'ceo' in title or 'founder' in title or 'partner' in title or 'chief' in title or 'president' in title:
        return 'Founder/Co-Founder (Technical)'
    elif 'coordinator' in title:
        return 'Coordinator'
    elif 'researcher' in title:
        if 'machine learning' in title or 'ML' in title or 'deep learning' in title or 'ai' in title:
            if 'senior' in title or 'sr.' in title or 'sr' in title:
                return 'Senior ML Researcher'
            else:
                return 'ML Researcher'
    elif 'architect' in title:
        if 'data' in title or 'sap' in title or 'software' in title or 'ml' in title or 'innovation' in title \
                    or 'digital' in title or 'it' in title or 'crm' in title or 'salesforce' in title or 'ai' in title \
                    or 'tech' in title or 'artifical intelligence' in title or 'analytics' in title:
            return 'Technical Architect'
        else:
            return 'Other (Non-Technical)'
    elif 'specialist' in title:
        if 'ux' in title or 'ui' in title or 'design' in title:
            return 'Design Specialist'
        elif 'data' in title:
            if 'governance' in title:
                if 'senior' in title or 'sr.' in title or 'sr' in title:
                    return 'Senior Data Governance Specialist'
                else:
                    return 'Data Governance Specialist'
            else:
                return 'Other (Technical)'
        else:
            return 'Other (Non-Technical)'
    elif 'instructor' in title or 'professor' in title or 'teacher' in title:
        return 'Course Instructor/Professor'
    elif 'fraud' in title:
        return 'fraud strategist'
    elif 'business' in title:
        if 'development' in title:
            return 'Business Development'
        else:
            return 'Other (Non-Technical)'
    elif 'postdoc' in title:
        return 'Postdoctoral Fellowship'
    elif 'intern' in title:
        if 'data' in title:
            return 'Data Intern'
        else:
            return 'Other (Technical)'
    else:
        if 'data' in title or 'sap' in title or 'software' in title or 'ml' in title or 'innovation' in title \
                    or 'digital' in title or 'it' in title or 'crm' in title or 'salesforce' in title or 'ai' in title \
                    or 'tech' in title or 'artifical intelligence' in title or 'analytics' in title:
            return 'Other (Technical)'
        else:
            return 'Other (Non-Technical)'



# data = pd.read_csv('Job Trending Analysis.csv')
# for index, row in data.iterrows():
#     data.loc[index, 'Standard Job Title'] = categorize_job_title(str(row['Job Title']))

# # for index, row in data.iterrows():
# #     for key in std_job_group.keys():
# #         if row['Standard Job Title'] in std_job_group[key]:
# #             data.loc[index, 'Standard Job Group'] = key



# # save the new researcher data locally
# data.to_csv('Job Trending Analysis.csv')
