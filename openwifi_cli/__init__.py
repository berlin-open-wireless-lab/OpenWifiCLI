import click
from click_shell import shell
import requests
import requests.exceptions
import pprint
from .basic import generate_basic_functions, json_parsable, generate_show

JSON_PARSABLE = json_parsable()

@shell(prompt='openwifi-shell >')
@click.option('--server', default='http://localhost', help='Full URL-Path to the OpenWifi Server')
@click.option('--user', default=None, help='Username')
@click.option('--password', default=None, help='Password')
@click.pass_context
def main(ctx, server, user, password):
    if len(server) < 7 or\
       server[:7] != 'http://' or\
       server[:8] != 'https://':
        server = 'http://'+server

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

@nodes.command()
@click.pass_context
@click.argument('uuid', nargs=-1)
def get_diff(ctx, uuid):
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

    #import pdb
    #pdb.set_trace()
    pretty = pprint.pformat(ctx.obj['result'], indent=4)
    click.echo(pretty)
    #click.echo(ctx.obj['result'])

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
                  {'name': '--nodes', 'type': JSON_PARSABLE}]
generate_basic_functions(access, '/access', access_options)

@main.group()
@click.pass_context
def settings(ctx):
    pass

settings_optios = ['--key', '--value']
generate_basic_functions(settings, '/settings', settings_optios)
