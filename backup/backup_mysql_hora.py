'''
Autor:  Marcos Felipe da Silva
versão: 1.0
data:   17-04-2020
------------------------------------------------------------
Descrição:  Este modulo faz backup das bases de dados Mysql
colocando registro de horas para cada arquivo .zip gerado
------------------------------------------------------------
Historico:
v1.0    17-04-2020  Cria e nomeia um arquivo .zip com a hora
                    (hh:mm) que ele foi criado

'''

import backup_mysql # exec_backup_mysql, comprimir, remover_arquivos
from datetime import datetime
import os
import sys


if __name__ == '__main__':
    DIR_DEST = './' if len(sys.argv) < 2 else sys.argv[1]
    # gerando hora
    HORA = datetime.now().strftime('%H_%M')

    # executando o backup
    resp = backup_mysql.exec_backup_mysql(backup_mysql.databases)

    # Recuperando o nome dos arquivos
    arquivos = [resp[key]['arquivo'] for key in resp.keys() if resp[key]['status'] == True]

    # Realizando a compressão dos arquivos
    backup_mysql.comprimir(arquivos, '-'.join(('backup-mysql', HORA)), DIR_DEST)

    # Remove todos os arquivos que foram criados
    backup_mysql.remover_arquivos(arquivos)