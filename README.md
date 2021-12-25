# github-projects-notice-slack
Notify slack when a column in Github projects is moved.

# Usage
- Create API Gateway and Lambda function to AWS.
- Paste this code into the Lambda you created.
- Change the values of column_dict, closed_column, and test_it_column.
- Set the environment variables for Lambda.
- Set up a Github webhook.
  - Set the Payload URL to the URL of the API Gateway.
  - For trigger, set 'Let me select individual events' and specify 'Project cards'.

## environment variables
| Key | Description |
| ------------- | ------------- |
| GITHUB_TOKEN  | your github api token  |
| repository_name  | Part of the repository name you want to be notified about  |
|closed_hook_url|Notification when an issue is closed.|
|test_it_hook_url|Notifications to testers.|
|other_hook_url|Others|
