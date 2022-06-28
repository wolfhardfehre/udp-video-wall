from invoke import task


@task(help={'screen': 'the screen position within the defined grid'})
def client(c, suffix, screen=0):
    c.run(f'PYTHONPATH=. python client/client.py 192.168.0.{suffix} --screen={screen}')


@task
def server(c):
    c.run('PYTHONPATH=. python server/server.py')
