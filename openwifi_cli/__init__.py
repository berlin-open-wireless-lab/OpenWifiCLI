import click
from click_shell import shell
import requests
import requests.exceptions
from .basic import generate_basic_functions

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

@main.group()
@click.pass_context
def users(ctx):
    pass

users_options = ['--login', '--password', '--admin/--no-admin']
generate_basic_functions(users, '/users', users_options)

@main.group()
@click.pass_context
def nodes(ctx):
    pass

nodes_options = ['--name', '--address', '--distribution', '--version', '--login', '--password']
generate_basic_functions(nodes, '/nodes', nodes_options)
