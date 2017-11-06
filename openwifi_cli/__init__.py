import click
from click_shell import shell
import requests
import requests.exceptions

#@click.group()
@shell(prompt='openwifi-shell >')
@click.option('--server', default='http://localhost', help='Full URL-Path to the OpenWifi Server')
@click.option('--user', default=None, help='Username')
@click.option('--password', default=None, help='Password')
@click.pass_context
def main(ctx, server, user, password):
    try:
        r = requests.get(server)
    except requests.exceptions.ConnectionError:
        click.echo('ERROR server not reachable')
        exit(1)

    login = requests.get(server+'/login')
    if not login.json():
        if user == None:
            user = click.prompt('Please enter the username')
        if password == None:
            password = click.prompt('Please enter the password', hide_input=True)
        login = requests.post(server+'/login', json={'login':user, 'password':password}, allow_redirects=False)

        if login.status_code != 302:
            click.echo('ERROR wrong credentials')
            exit(1)

        ctx.obj = {}
        ctx.obj['cookies'] = login.cookies
        ctx.obj['server'] = server

@main.command()
@click.pass_context
@click.option('--id', default=None)
def users(ctx, id):
    jar = ctx.obj['cookies']
    server = ctx.obj['server']

    if id:
        users_request = requests.get(server+'/users/'+id, cookies=jar)
    else:
        users_request = requests.get(server+'/users', cookies=jar)

    click.echo(users_request.json())

@main.command()
@click.pass_context
@click.option('--uuid', default=None)
def nodes(ctx, uuid):
    jar = ctx.obj['cookies']
    server = ctx.obj['server']

    if uuid:
        nodes_request = requests.get(server+'/nodes/'+uuid, cookies=jar)
    else:
        nodes_request = requests.get(server+'/nodes', cookies=jar)

    click.echo(nodes_request.json())
