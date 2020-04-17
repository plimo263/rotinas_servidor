'''
Autor:  Marcos Felipe da Silva
versão: 1.0
data:   17-04-2020
-----------------------------------------------------------
Descrição:  Este modulo realiza o backup e compressão das 
bases de dados do mongodb registrando a hora (hh:mm)

'''

from datetime import datetime
import backup_mongo # exec_backup_mongo, comprimir
import sys

if __name__ == '__main__':
    # DIRETORIO DE DESTINO PARA O ARQUIVO DE BACKUP DO MONGODB
    DIR_DEST = './' if len(sys.argv) < 2 else sys.argv[1]
    HORA = datetime.now().strftime('%H_%M')
    nome = '-'.join(('backup-mongo', HORA))
    backup_mongo.exec_backup_mongo()
    backup_mongo.comprimir(nome, DIR_DEST)

