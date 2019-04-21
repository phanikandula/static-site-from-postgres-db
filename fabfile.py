import os
from fabric import task
from models import *

def get_states():
	"""
	Retrieves list of all state and capital as tuples from the remote db.
	"""
	return ([(s.state_name, s.capital_name) for s in Usa.select()])

@task
def dev_show_states(c):
	"""
	Prints a list of all states and capitals retrieved from remote db.
	"""
	print(get_states())

@task
def dev_add_state(c, state, capital):
	"""
	Provide CLI way to add new entries into remote DB.
	"""
	print('Got state={0}, capital={1}'.format(state, capital))
	s = Usa.create(state_name=state, capital_name=capital)
	print('Added to DB.')

@task
def dev_trigger_build(c):
	"""
	Provides a way to trigger build on remote netlify server using webhook.
	Using this we can rebuild our static site without pushing any changes
	to the git repo of static site.
	"""
	c.run('curl -X POST -d {} ' + os.environ['DEMO_DB_BUILD_TRIGGER_URL'])
	print('Build on Netlify triggered')

template= '''
<html>
<title>List of states so far!</title>

<body>
This is what we have in Postgres DB
<br>
<pre>
{states}
</pre>
</body>
</html>
'''

def format_state(index, state_tuple):
	"""
	Formats a state capital tuple with index number prefixed.
	"""
	return str(index+1) + ' ' + str(state_tuple)

def create_index_html_from_db():
	"""
	Gets list of states and capitals from the remote DB.
	Formats and inserts them into the html template
	"""
	all_states = get_states()
	formatted_states = '\n'.join(format_state(i, st) for i, st in enumerate(all_states))
	return template.format(states=formatted_states)

@task
def build_website(c):
	"""
	Get all states and capitals and generate new index.html
	Creates output directory if not present.
	Puts the latest generated index.html into that directory.
	Overwrites existing index.html if present.
	"""
	c.run('mkdir -p output')
	with open('output/index.html', 'w+') as f:
		f.write(create_index_html_from_db())
	
