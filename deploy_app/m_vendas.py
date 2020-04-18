'''
Autor:  Marcos Felipe da Silva Jardim
versão: 1.0
data:   18-04-2020
-----------------------------------------------------------
Descrição:  Cria uma rotina para fazer a construção da aplicação.

'''

from subprocess import Popen, PIPE
import shlex
import os


DIR = '/home/marcos/virtual-env/relatorio/m_vendas_1.0/'

class Mvendas:

    def __init__(self, path = DIR):
        self._path = path
        self._compose = './docker-compose.yml'
        self._nome_do_servico = 'dev_m_vendas'
        self._nome_da_pilha = 'dev'

    def pull(self):
        ''' Define o pull da aplicação, assim como o build do 
        frontend e finalmente a movimentação do arquivo gerado.

        Excessões -> FileNotFoundError, COnnectionError
        '''
        
        #Primeiro verifica se temos o git instalado
        with Popen(['which', 'git'], stdout=PIPE) as popen:
            popen.communicate()
            if popen.returncode != 0:
                raise FileNotFoundError('O executavel do git não foi encontrado')
        
        # O executavel existe, verifique se o diretorio existe
        if not os.path.exists(self._path):
            raise FileNotFoundError('O diretorio "{}" não existe'.format(self._path))

        # Veja se contém um diretório .git então vamos lançar o pull
        if not os.path.exists(os.path.join(self._path, '.git/')):
            raise FileNotFoundError('Diretorio ".git" não encontrado')
        
        # Façamos o pull da aplicação
        os.chdir(self._path)

        with Popen(['git', 'pull'], stdout=PIPE, stderr=PIPE) as popen:
            stdout, stderr = popen.communicate()
            # Deu algo errado no pull
            if popen.returncode != 0: 
                raise ConnectionError(stderr.decode())
        
        return True

    def _build(self):
        ''' Realiza o build do frontend 
        Excessões -> NotADirectoryError
        '''

        # Primeiro passo e fazer o pull
        self.pull()

        # Procure um diretorio chamado frontend
        caminho = os.path.join(self._path, 'frontend')
        if not os.path.isdir(caminho):
            raise NotADirectoryError('O path {} não é um diretório')
        
        # Acesse este diretorio
        os.chdir(caminho)

        # Veja se o comando npm esta acessivel
        with Popen(['which', 'npm']) as popen:
            popen.communicate()
            if popen.returncode != 0:
                raise FileNotFoundError('O comando npm não está disponivel')
        
        # Esta disponivel, faça a sua execucao
        with Popen(['npm', 'run', 'build'], stderr=PIPE, stdout=PIPE) as popen:
            stdout, stderr = popen.communicate()
            if popen.returncode != 0:
                raise FileNotFoundError('O comando npm run build falhou \n {}'.format(
                stderr.decode())
            )
        # Projeto foi buildado faça a movimentacao para static e templates
        if not os.path.isdir(os.path.join(self._path, 'static')):
            raise NotADirectoryError('O diretorio static não existe')

        if not os.path.isdir(os.path.join(self._path, 'templates')):
            raise NotADirectoryError('O diretorio templates não existe')
        
        # Execute o comando que vai copiar os arquivos buildados para o destino
        with Popen(['./sh/mv_deploy.sh', '../static', '../templates'], stderr=PIPE) as popen:
            _, stderr = popen.communicate()
            if popen.returncode != 0:
                raise FileNotFoundError('A movimentação dos arquivos buildados não realizada {}'.format(
            stderr.decode()))
        
        return True
        

        

    def executar(self):
        ''' Define o inicio'''

if __name__ == '__main__':
    m = Mvendas()
    m._build()