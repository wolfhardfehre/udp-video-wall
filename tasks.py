from invoke import task


@task(help={'screen': 'the screen position within the defined grid'})
def client(c, ip='127.0.0.1', screen=0):
    """call client with server IP and a screen number"""
    c.run(f'PYTHONPATH=. python client/client.py {ip} --screen={screen}')       # ip=192.168.0.230


@task
def server(c):
    """start server"""
    c.run('PYTHONPATH=. python server/server.py')
