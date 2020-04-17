'''
Autor:  Marcos Felipe da Silva
versão: 1.0
data:   17-04-2020
--------------------------------------------------------------
Funções: 
 - exec_backup_mongo()
 - comprimir(nome = 'backup-mysql')
--------------------------------------------------------------
Descrição:  Faz a extração das bases de dados mongodb e realiza
a compactação dos arquivos
--------------------------------------------------------------
Historico:
v1.0    17-04-2020  Faz o backup de todas as colecoes no mongodb

'''

from subprocess import PIPE
from subprocess import Popen
import shlex
import shutil
import os
from config import config

DIR = 'mongo'

def exec_backup_mongo():
    ''' Faz backup de todas as bases de dados da instancia mongodb '''

    cmd = 'mongodump -u %s -p %s --out %s' % (
        config['mongo']['usuario'], config['mongo']['senha'], DIR
    )
    
    attrs = {'stdout': PIPE, 'stderr': PIPE}
    with Popen(shlex.split(cmd), **attrs) as popen:
        popen.communicate()
    
    return True

def comprimir(nome = 'backup-mongo', destino = './'):
    ''' Cria um arquivo .zip dos diretorios gerados pelo mongodb'''
        
    # Executa o comando e cria um arquivo zipado 
    cmd = 'tar -zcvf %s.tar.gz %s' % (os.path.join(destino, nome), DIR)
    
    attrs = {'stdout': PIPE, 'stderr': PIPE}
    with Popen(shlex.split(cmd), **attrs) as popen:
        std, stderr = popen.communicate()

    # Removendo o diretorio do mongo
    shutil.rmtree(DIR)
    
    return True


if __name__ == "__main__":
    exec_backup_mongo() # Executa o backup das bases de dados
    comprimir() # Cria o arquivo de compressão inserindo os arquivos 

