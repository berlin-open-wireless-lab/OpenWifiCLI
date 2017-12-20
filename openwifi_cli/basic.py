import click
import requests
import json

class json_parsable(click.ParamType):
    name = 'json'

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except ValueError:
            self.fail('%s is not a valid json string.' % value, param, ctx)


def generate_show(group, path):
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

def generate_delete(group, path):
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

def generate_basic_functions(group, path, options):

    generate_show(group, path)
    generate_delete(group, path)

    @group.command()
    @click.pass_context
    def add(ctx, *args, **kwargs):
        jar = ctx.obj['cookies']
        server = ctx.obj['server']

        nodes_request = requests.post(server+path, cookies=jar, json=kwargs)
        ctx.obj['result'] = nodes_request.text

        click.echo(ctx.obj['result'])

    def decorate_with_options(f, ignore_prompt=False, prompt=True):
        for option in options:
            if type(option) == dict:
                option_name = option['name']

                try:
                    option_type = option['type']
                except:
                    option_type = str
                try:
                    if not ignore_prompt:
                        option_prompt = option['prompt']
                    else:
                        option_prompt = False
                except:
                    option_prompt = True

                f = click.option(option_name, prompt=option_prompt, type=option_type)(f)
            else:
                f = click.option(option, prompt=prompt)(f)
        return f

    decorate_with_options(add)

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
    
    decorate_with_options(mod, True, False)
