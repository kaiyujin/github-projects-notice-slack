import json, os, urllib.request

result = {'statusCode': 200,'body': json.dumps('OK')}
column_dict = {
    17235572:'New issue',
    17291390:'Next milestone',
    17235434:'Current Milestone',
    17235435:'In proggress',
    17235444:'Complete UT (Waiting for deploy to dev)',
    17235486:'Completed deploy to dev(Director testing in progress) ',
    17235476:'Waiting for Release(Completed directors test)',
    17235440:'Close'
}
closed_column = 17235440
test_it_column= 17235486

def getIssue(url):
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + os.getenv('GITHUB_TOKEN'))
    req.add_header('Accept','application/vnd.github.v3+json')
    with urllib.request.urlopen(req) as res:
        return json.load(res)

def postSlack(slack_url, title, issue_url, from_column, to_column, user):
    send_data = {"username" : "Github hook", 'text' : f'<{issue_url}|{title}>\nfrom: {from_column}  to: {to_column}  by:{user}'}
    data = 'payload=' + json.dumps(send_data)
    req = urllib.request.Request(slack_url, data=data.encode("utf-8"), method='POST')
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)

def lambda_handler(event, context):
    if event['action'] != 'moved':
        print('no moved')
        return result
    column_id_from = event['changes']['column_id']['from']
    column_id_to   = event['project_card']['column_id']
    sender = event['sender']['login']
    context_api_url = event['project_card']['content_url']
    if os.getenv('repository_name') in context_api_url:
        issue = getIssue(context_api_url)
        slack_url = os.getenv('other_hook_url')
        if column_id_to == closed_column:
            slack_url = os.getenv('closed_hook_url')
        if column_id_to == test_it_column:
            slack_url = os.getenv('test_it_hook_url')
        postSlack(slack_url, issue['title'], issue['html_url'], column_dict[column_id_from], column_dict[column_id_to], sender)
    else:
        print('not target repository')
    
    return result
