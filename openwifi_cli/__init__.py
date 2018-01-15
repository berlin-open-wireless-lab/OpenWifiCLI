""" main file for openwifi cli """

import pprint
import click
from click_shell import shell
import requests
import requests.exceptions
from .basic import generate_basic_functions, JsonParsable, generate_show

JSON_PARSABLE = JsonParsable()

@shell(prompt='openwifi-shell >')
@click.option('--server', default='http://localhost', help='Full URL-Path to the OpenWifi Server')
@click.option('--user', default=None, help='Username')
@click.option('--password', default=None, help='Password')
@click.pass_context
def main(ctx, server, user, password):
    """ main function for openwifi cli """

    if len(server) < 7 or\
       server[:7] != 'http://' or\
       server[:8] != 'https://':
        server = 'http://'+server

    try:
        requests.get(server)
    except requests.exceptions.ConnectionError:
        click.echo('ERROR server not reachable')
        exit(1)

    login = requests.get(server+'/login')
    if not login.json():
        if user is None:
            user = click.prompt('Please enter the username')
        if password is None:
            password = click.prompt('Please enter the password', hide_input=True)
        login = requests.post(server+'/login', json={'login':user, 'password':password}\
                , allow_redirects=False)

        if login.status_code != 302:
            click.echo('ERROR wrong credentials')
            exit(1)

        ctx.obj = {}
        ctx.obj['cookies'] = login.cookies
        ctx.obj['server'] = server

@main.group()
def users():
    """ group for user related actions """

    pass

USERS_OPTIONS = ['--login', '--password', '--admin/--no-admin']
generate_basic_functions(users, '/users', USERS_OPTIONS)

@main.group()
def nodes():
    """ group for nodes related actions """

    pass

NODES_OPTIONS = ['--name', '--address', '--distribution', '--version', '--login', '--password']
generate_basic_functions(nodes, '/nodes', NODES_OPTIONS)

@nodes.command()
@click.pass_context
@click.argument('uuid', nargs=-1)
def get_diff(ctx, uuid):
    """ get and print all diffs of a given node """

    jar = ctx.obj['cookies']
    server = ctx.obj['server']

    ctx.obj['result'] = []
    for uid in uuid:
        nodes_request = requests.get(server+'/nodes/'+uid+'/diff', cookies=jar)
        from ast import literal_eval
        data = literal_eval(nodes_request.text)
        print(type(data))
        data = literal_eval(data)
        print(type(data))
        ctx.obj['result'].append(data)

    pretty = pprint.pformat(ctx.obj['result'], indent=4)
    click.echo(pretty)

@main.group()
def services():
    """ group for service related actions """

    pass

SERVICE_OPTIONS = ['--name', {'name' : '--queries', 'type': JSON_PARSABLE},\
                   '--capability_script', '--capability_match']
generate_basic_functions(services, '/service', SERVICE_OPTIONS)

@main.group()
def access():
    """ group for access related actions """

    pass

ACCESS_OPTIONS = ['--userid', '--apikeyid', '--access_all_nodes/--no-access_all_nodes',\
                  {'name' : '--data', 'type': JSON_PARSABLE},\
                  {'name': '--nodes', 'type': JSON_PARSABLE}]
generate_basic_functions(access, '/access', ACCESS_OPTIONS)

@main.group()
def settings():
    """ group for settings related actions """

    pass

SETTINGS_OPTIOS = ['--key', '--value']
generate_basic_functions(settings, '/settings', SETTINGS_OPTIOS)

@main.command()
@click.pass_context
@click.option('--name', prompt=True)
def generate_apikey(ctx, name):
    """ this functions triggers the generation of an api keys and returns it """

    jar = ctx.obj['cookies']
    server = ctx.obj['server']
    nodes_request = requests.post(server+'/get_apikey', json={"key":name}, cookies=jar)
    click.echo(nodes_request.text)

@main.group()
def master_config():
    """ group for master config related actions """

    pass

MASTER_CONFIG_OPTIONS = []
generate_basic_functions(master_config, '/masterConfig', MASTER_CONFIG_OPTIONS, has_mod=False)
