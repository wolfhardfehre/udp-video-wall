from invoke import task


@task(help={'screen': 'the screen position within the defined grid'})
def client(c, ip, screen=0):
    c.run(f'PYTHONPATH=. python client/client.py {ip} --screen={screen}')


@task
def server(c):
    c.run('PYTHONPATH=. python server/server.py')
