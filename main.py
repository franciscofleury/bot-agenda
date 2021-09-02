

from ast import literal_eval
import discord
import asyncio
from discord.ext import commands
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from discord_components import *
#intents = discord.Intents.all()
cred = credentials.Certificate('./turma-cred.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

def agendaBackup():
    db.collection('AGENDA').document('Agenda').set(deveres)

client = commands.Bot(command_prefix='?')




calendario_escola = {'SEGUNDA':['Física DIONE','Física DIONE','Inglês','Biologia FRED','Matemática SÉRGIO','Matemática SÉRGIO'],'TERÇA':['Biologia LEO','História KAPA','Literatura','Matemática Rapha','Redação','Química Jeosafá'],'QUARTA':['Português','Espanhol','Biologia LEO','Biologia LEO','Literatura','Química RODRIGO'],'QUINTA':['SOE','Geografia','Geografia','Português','História KAPA','História KAPA','Espanhol','Química RODRIGO','Redação','Física DIONE'],'SEXTA':['Química JEOSAFÁ','Matemática RAPHA','Matemática RAPHA','Física CADU','Física CADU','História GAUI'],'SABADO':['Sociologia','Química RODRIGO','Filosofia','Matemática RAPHA','História GAUI','Biologia FRED']}
def read_token():
    with open("token.txt",'r') as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
def transDever(lista):
    new_lista = {}
    counting_list = []
    for key, i in lista.items():
        newNumber = int(i['dataEnd'][0:2]) + (int(i['dataEnd'][3:5]) * 100) + (int(i['dataEnd'][6:10])* 10000)
        if newNumber in counting_list:
            counting_list.append(newNumber)
            new_lista[newNumber+(counting_list.count(newNumber)*0.01)] = i
        else:
            counting_list.append(newNumber)
            new_lista[newNumber] = i
    
    return new_lista
@client.command(name = 'clear')
async def limpar(context):
    deveres.clear()
    agendaBackup()
    await  context.message.channel.send("A agenda foi limpa!")

@client.command(name ='add')
async def add(context, dever='none', prazo='none'):
    getAgenda()
    print(dever)
    print(prazo)
    materia = 'none'
    plat = 'none'
    if dever !='none' and prazo != 'none':
        await context.send('Insira a matéria e a plataforma:',components=[Select(placeholder='Matéria',options=[SelectOption(label='Matemática 1',value='Matemática 1'),SelectOption(label='Matemática 2',value='Matemática 2'),SelectOption(label='Matemática 3', value='Matemática 3'),SelectOption(label='Física 1', value='Física 1'),SelectOption(label='Física 2', value='Física 2'),SelectOption(label='Geografia', value='Geografia'),SelectOption(label='História 1', value='História 1'),SelectOption(label='História 2', value='História 2'),SelectOption(label='Filosofia', value='Filosofia'),SelectOption(label='Sociologia', value='Sociologia'),SelectOption(label='Português', value='Português'),SelectOption(label='Redação', value='Redação'),SelectOption(label='Inglês', value='Inglês'),SelectOption(label='Literatura', value='Literatura'),SelectOption(label='Biologia 1', value='Biologia 1'),SelectOption(label='Biologia 2', value='Biologia 2'),SelectOption(label='Química 1', value='Química 1'),SelectOption(label='Química 2', value='Química 2')], custom_id='materia'),Select(placeholder='Plataforma',options=[SelectOption(label='Geekie',value='Geekie'),SelectOption(label='Teams',value='Teams'),SelectOption(label='Rede y', value='Rede y')], custom_id='plataforma'),
        Button(style=ButtonStyle.green, label="CONFIRMAR", id="go")])
        while True:
            select1 = await client.wait_for('select_option',check=None)
            if select1.custom_id == 'materia':
                materia = select1.values[0]
                print(materia)
                await select1.respond(type=7, content='Insira a plataforma:')
                break
            elif select1.custom_id == 'plataforma':
                plat = select1.values[0]
                print(plat)
                await select1.respond(type=7, content='Insira a matéria:')
                break
        while True:
            select2 = await client.wait_for('select_option',check=None)
            if select2.custom_id == 'materia':
                materia = select2.values[0]
                print(materia)
                await select2.respond(type=7,content='Confirme!')
                break
            elif select2.custom_id == 'plataforma':
                plat = select2.values[0]
                print(plat)
                await select2.respond(type=7, content='Confirme!')
                break
        while True:
            button = await client.wait_for('button_click',check=None)
            deveres[dever] = {'nome':dever,'materia':materia, 'plataforma':plat,'dataEnd': prazo}
            await button.send('DEVER ADICIONADO COM SUCESSO!', ephemeral=True)
        #await select1.send('ITEM ADICIONADO COM SUCESSO!',ephemeral=True)
            agendaBackup()
    else:
        await context.message.channel.send('POR FAVOR USE O FORMATO ?ADD DEVER * PLATAFORMA * MATERIA * DATA')


@client.command(name ='del')
async def delete(context):
    getAgenda()
    elemento = context.message.content[5:]
    try:
        deveres.pop(elemento)
        await context.message.channel.send("ITEM REMOVIDO COM SUCESSO!")
        agendaBackup()
    except:
        await context.message.channel.send('ESSE ITEM NÃO EXISTE, POR FAVOR INSIRA UM ITEM VÁLIDO')
    
    
@client.command(name = 'agenda')
async def lista(context):
    getAgenda()
    hasFilter = False
    if len(context.message.content) >8:
        hasFilter = True
        filtro = context.message.content[8:].lower()
    if len(deveres) > 0:
        teste_deveres = transDever(deveres).items()
        new_deveres = sorted(teste_deveres)
        emb = discord.Embed(title='Agenda')
        print(new_deveres)
        for key, tu in enumerate(new_deveres):
            print(key)
            print(tu)
            value = tu[1]
            if hasFilter:
                
                if value['plataforma'].lower() == filtro:
                    emb.add_field(name='**{}**'.format(value['nome']), value="> plataforma: {}\n> materia: {}\n> data: {}".format(value['plataforma'],value['materia'],value['dataEnd']),inline=False)
            else:
                emb.add_field(name='**{}**'.format(value['nome']), value="> plataforma: {}\n> materia: {}\n> data: {}".format(value['plataforma'],value['materia'],value['dataEnd']),inline=False)
        await context.message.channel.send(embed=emb)
    else:
        await context.message.channel.send("Não há deveres na agenda")
@client.command(name = 'calendario')
async def calendario(context):
    if len(context.message.content) > 11:
        dia = context.message.content[12:].upper()
        if dia == 'HOJE':
            semana_dia = datetime.date.today().weekday()
            if semana_dia == 0:
                dia = 'SEGUNDA'
            elif semana_dia == 1:
                dia = 'TERÇA'
            elif semana_dia == 2:
                dia = 'QUARTA'
            elif semana_dia == 3:
                dia = 'QUINTA'
            elif semana_dia == 4:
                dia = 'SEXTA'
            elif semana_dia == 5:
                dia = 'SABADO'
            else:
                dia = 'HOJE NÃO TEM AULA'
        await context.message.channel.send('**'+dia+'**'+'\n\n')
        to_print = ''
        for tempo in calendario_escola[dia]:
            to_print += tempo+'\n'
        print(to_print)
        await context.message.channel.send(to_print)
    else:
        for key, value in calendario_escola.items():
            await context.message.channel.send('**'+key+'**')
            to_print = ''
            for tempo in value:
                to_print += tempo+'\n'
            await context.message.channel.send(to_print)

def getAgenda():
    doc = db.collection('AGENDA').document('Agenda').get()
    if doc.exists:

        global deveres
        deveres = doc.to_dict()
        
    else:
        print('nao')


@client.event
async def on_ready():
    DiscordComponents(client)
    print('Informações básicas:')
    print('Nome do bot: {0}'.format(client.user.name))
    print('Id: {0}'.format(client.user.id))
    print('Server: {0}'.format(client.guilds))
    print('-------------------------------------------------------------------------------')
    getAgenda()
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Guardando os deveres da 3C"))


client.run(token)

