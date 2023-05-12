import pandas as pd
import requests

# Read the input excel file
input_df = pd.read_excel('input.xlsx')

# Define the GraphQL endpoint URL
url = 'https://leetcode.com/graphql'

# Define the GraphQL query
query = """
query ($username: String!) {
  matchedUser(username: $username) {
    username
    userCalendar {
      activeYears
    }
    profile {
      ranking
      aboutMe
      realName
    }
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
}
"""

# Define a function to execute GraphQL queries
def execute_query(query, variables):
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()['data']

# Loop over each row of the input dataframe and fetch data for each user
results = []
for i, row in input_df.iterrows():
    username = row['Username']
    variables = {'username': username}
    result = execute_query(query, variables)
    if result.get('matchedUser'):
        results.append(result['matchedUser'])
    else:
        results.append({'username': username, 'userCalendar': {'activeYears': None}, 'profile': {'ranking': None, 'aboutMe': None, 'realName': None}, 'submitStatsGlobal': {'acSubmissionNum': None}})

# Convert the list of results to a dataframe
output_df = pd.json_normalize(results)

# Save the output dataframe to a new Excel file
output_df.to_excel('updated-sheet.xlsx', index=False)