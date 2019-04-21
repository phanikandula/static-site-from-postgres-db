from fabric import task
from models import *

def get_states():
	return ([(s.state_name, s.capital_name) for s in Usa.select()])

@task
def dev_show_states(c):
	print(get_states())

@task
def dev_add_state(c, state, capital):
	print('Got state={0}, capital={1}'.format(state, capital))
	s = Usa.create(state_name=state, capital_name=capital)
	print('Added to DB.')

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
	return str(index+1) + ' ' + str(state_tuple)

def create_index_html_from_db():
	all_states = get_states()
	formatted_states = '\n'.join(format_state(i, st) for i, st in enumerate(all_states))
	return template.format(states=formatted_states)

@task
def build_website(c):
	c.run('mkdir -p output')
	with open('output/index.html', 'w+') as f:
		f.write(create_index_html_from_db())
	
