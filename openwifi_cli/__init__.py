import click
from click_shell import shell
import requests
import requests.exceptions
from .basic import generate_basic_functions, json_parsable

JSON_PARSABLE = json_parsable()

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

@main.group()
@click.pass_context
def services(ctx):
    pass

service_options = ['--name', {'name' : '--queries', 'type': JSON_PARSABLE} ,\
                   '--capability_script', '--capability_match']
generate_basic_functions(services, '/service', service_options)

@main.group()
@click.pass_context
def access(ctx):
    pass

access_options = ['--userid', '--apikeyid', '--access_all_nodes/--no-access_all_nodes', {'name' : '--data', 'type': JSON_PARSABLE},
                  {'name': '--nodes', 'type':list}]
generate_basic_functions(access, '/access', access_options)
