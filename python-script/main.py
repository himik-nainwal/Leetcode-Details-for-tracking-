import time
import pandas as pd
import requests
# Install these 3 
# Read the input Excel file into a pandas DataFrame
input_df = pd.read_excel('input.xlsx')

# API endpoint URL
url = 'https://leetcode.com/graphql'

# GraphQL query to fetch user information
query = """
query ($username: String!) {
  matchedUser(username: $username) {
    username
    userCalendar {
      activeYears
    }
    githubUrl
    contributions {
      points
      questionCount
      testcaseCount
    }
    profile {
      skillTags
      ranking
      aboutMe
      realName
      reputation
      countryName
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

# Function to execute a GraphQL query using the requests library
def execute_query(query, variables):
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()['data']

results = []
counter = 0

# Iterate over each row in the input DataFrame
for i, row in input_df.iterrows():
    username = row['Username']
    variables = {'username': username}
    
    # Execute the GraphQL query for the current username
    result = execute_query(query, variables)
    
    if result.get('matchedUser'):
        # Process the user data if a match is found
        for x in result["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]:
            # Add difficulty count in the format "count/submissions"
            result["matchedUser"][x["difficulty"]] = str(x["count"]) + "/" + str(x["submissions"])

        # Extract and reorganize relevant user information
        result["matchedUser"]["ranking"] = result["matchedUser"]["profile"]["ranking"]
        result["matchedUser"]["country"] = result["matchedUser"]["profile"]["countryName"]
        result["matchedUser"]["reputation"] = result["matchedUser"]["profile"]["reputation"]
        result["matchedUser"]["contribution-points"] = result["matchedUser"]["contributions"]["points"]
        result["matchedUser"]["githubUrl"] = result["matchedUser"]["githubUrl"]
        # POP is used to drop some objects which are not in need
        # make sure to extract from that
        # object before. And look at that query for variables, adding and 
        # deleting/droping can be done. [Case Sensitive ]
        result["matchedUser"].pop("profile")
        result["matchedUser"].pop("contributions")
        result["matchedUser"].pop("submitStatsGlobal")
        result["matchedUser"].pop("userCalendar")

        # Create a dictionary to store the combined data
        result_dict = {}
        for col in input_df.columns:
            if col != 'Username':
                result_dict[col] = row[col]
        for col in result["matchedUser"]:
            result_dict[col] = result["matchedUser"][col]
        
        # Append the combined data to the results list
        results.append(result_dict)
    else:
        # If no match is found, create a dictionary with the username only
        result_dict = {'username': username}
        for col in input_df.columns:
            if col != 'Username':
                result_dict[col] = row[col]
        results.append(result_dict)

    counter += 1
    
    # Delay execution every 150 records to avoid IP blocking
    if counter % 150 == 0:
        print(f"Processed {counter} records. Waiting for 10 seconds...To avoid IP block")
        time.sleep(10)

# Convert the results list to a pandas DataFrame
output_df = pd.json_normalize(results)

# Write the output DataFrame to an Excel file
output_df.to_excel('updated-sheet.xlsx', index=False)
