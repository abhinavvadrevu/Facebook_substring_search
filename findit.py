from facepy import GraphAPI
from facepy import exceptions
import time

oauth_access_token = "AAACEdEose0cBAKZBs7SySfsvtZCZAZCH8ZBkmi2XOEgmRsVSqz6CuOSlXUjNxnYc8eQ1Bz9KCk5dxNAvmkpZBfXsinELUwof9z5PBw1ruR0QZDZD"
no_of_threads = 10 #note the script parses 50 times this number of threads
messages_per_thread = 5 #note the script parses 50 times this number of messages

def wait():
        print 'UGH ERROR -.-'
        for i in range(9):
            print "waiting " + str(10-i) + " mins"
            time.sleep(60)
        time.sleep(2)

graph = GraphAPI(oauth_access_token)\
thread_ids = []

for i in list(map(lambda x:x*50, range(1,no_of_threads))):
    query = "SELECT thread_id FROM thread WHERE folder_id = 0 Limit 50 Offset " + str(i)
    json_output = None
    try:
        json_output = graph.fql(query)
    except exceptions.OAuthError:
        """
        we got kicked out by facebook for making too many method calls.
        ugh.
        just wait about 10 mins and try again.
        """
        wait()
        json_output = graph.fql(query)
    out = [x['thread_id'] for x in json_output['data']]
    thread_ids += out

messages = []
for thread_id in thread_ids:
    for i in list(map(lambda x:x*50, range(1,messages_per_thread))):
        query = "SELECT thread_id, body, author_id, created_time FROM message WHERE thread_id = " + thread_id + " Limit 50 Offset " + str(i)
        json_output = None
        try:
            json_output = graph.fql(query)
        except exceptions.OAuthError:
            """
            we got kicked out by facebook for making too many method calls.
            ugh.
            just wait about 10 mins and try again.
            """
            wait()
            json_output = graph.fql(query)
        for x in json_output['data']:
            messages.append([x['body'],x['author_id']])

for x in messages:
    if '=]' in x[0]:
        print x