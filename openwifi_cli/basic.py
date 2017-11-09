import click
import requests

def generate_basic_functions(group, path, options):

    @group.command()
    @click.pass_context
    @click.argument('uuid', nargs=-1, required=False)
    def show(ctx, uuid):
        jar = ctx.obj['cookies']
        server = ctx.obj['server']

        ctx.obj['result'] = []
        for uid in uuid:
            nodes_request = requests.get(server+path+'/'+uid, cookies=jar)
            ctx.obj['result'].append(nodes_request.json())

        if not uuid:
            nodes_request = requests.get(server+path, cookies=jar)
            ctx.obj['result'] = nodes_request.json()

        click.echo(ctx.obj['result'])

    @group.command()
    @click.pass_context
    @click.argument('uuids', nargs=-1)
    def delete(ctx, uuids):
        jar = ctx.obj['cookies']
        server = ctx.obj['server']

        ctx.obj['result'] = []
        for uuid in uuids:
            nodes_request = requests.delete(server+path+'/'+uuid, cookies=jar)
            ctx.obj['result'].append(nodes_request.json())

        click.echo(ctx.obj['result'])

    @group.command()
    @click.pass_context
    def add(ctx, *args, **kwargs):
        jar = ctx.obj['cookies']
        server = ctx.obj['server']

        nodes_request = requests.post(server+path, cookies=jar, json=kwargs)
        ctx.obj['result'] = nodes_request.text

        click.echo(ctx.obj['result'])

    for option in options:
        add = click.option(option, prompt=True)(add)

    @group.command()
    @click.pass_context
    @click.argument('ids', nargs=-1)
    def mod(ctx, ids, *args, **kwargs):

        kwargs = dict(filter(lambda x: x[1] != None, kwargs.items()))
        jar = ctx.obj['cookies']
        server = ctx.obj['server']

        ctx.obj['result'] = []
        for id in ids:
            nodes_request = requests.post(server+path+'/'+id, cookies=jar, json=kwargs)
            ctx.obj['result'].append(nodes_request.text)

        click.echo(ctx.obj['result'])

    for option in options:
        mod = click.option(option)(mod)
