#!/bin/bash

# ARQUIVO SIMPLES QUE EXECUTA AS ROTINAS DE BACKUP DAS BASES DE DADOS

python3 backup/backup_mongo_hora.py . # backup base de dados mongodb
python3 backup/backup_mysql_hora.py . # backup base de dados mysql