'''
Autor:  Marcos
data:   17-04-2020
versão: 1.0
--------------------------------------------------------------------
Funções: 
 - exec_backup_mysql(arquivos: list)
 - comprimir(arquivos: list, nome = 'backup-mysql')
 - remover_arquivos(list)

--------------------------------------------------------------------
Descrição: Este script usa o modulo subprocess para realizar backup
das bases de dados MySQL.
--------------------------------------------------------------------
Historico:
v1.0:   17-04-2020  Função exec_backup_mysql recebe uma lista de
                    bases de dados e então faz o backup de cada base
                    retornando um dicionario com o status

v1.1:   17-04-2020  Função comprimir criada para gerar um arquivo .zip
                    com compressão dos arquivos .sql que foram gerados

v1.2:   17-04-2020  Função para remover o "lixo" ou seja os arquivos 
                    que forem repassados
'''

from subprocess import PIPE 
from subprocess import Popen 
import shlex
import zipfile
import os
from config import config

# Informa as bases de dados que serão feitos backups
databases = [
    'relatorios',
    'apptech',
    'relatorios_floripa',
]

def exec_backup_mysql(args: list):
    ''' Função que recebe as bases de dados e cria um arquivo .sql 
    para cada base de dados, retornando um dicionario com o status 
    de cada base de dados solicitada para backup'''

    db_dict = {}
    
    for db in args:    
        cmd = 'mysqldump -u %s --password=%s %s' % (
            config['mysql']['usuario'], config['mysql']['senha'], db
        )
        attrs = {'stdout': PIPE}

        with Popen(shlex.split(cmd), **attrs) as popen:
            stdout, _ = popen.communicate()
            if popen.returncode != 0:
                db_dict[db] = {'status': False}
            else:
                nome = '.'.join((db,'sql'))
                with open(nome, 'w') as arq:
                    arq.write(stdout.decode())
                    db_dict[db] = {'status': True, 'arquivo': nome}
    
    return db_dict

def comprimir(args:list, nome = 'backup-mysql', destino = './'):
    ''' Cria um arquivo .zip com todos os arquivos repassados na lista'''
    
    nome = 'backup-mysql' if len(nome) == 0 else nome

    with zipfile.ZipFile(os.path.join(destino, '.'.join((nome,'zip'))),
     'w', compression=zipfile.ZIP_BZIP2) as zp:
        for arquivo in args:
            zp.write(arquivo)
    
    return True

def remover_arquivos(args: list):
    ''' Remoção simples de todos os arquivos informados '''
    for arq in args:
        try:
            os.remove(arq)
        except FileNotFoundError:
            pass
    
    return True

if __name__ == '__main__':
    resp = exec_backup_mysql(databases) # Realiza o backup
    # Separa os arquivos para compressão
    backups = [resp[key]['arquivo'] for key in resp.keys() if resp[key]['status'] == True]
    comprimir(backups, '') # Comprime todos os arquivos
    # Remove todos os arquivos gerados
    remover_arquivos(backups)
    