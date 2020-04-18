'''
Autor:  Marcos Felipe da Silva
versao: 1.0
------------------------------------------------------------
Descrição: Testes no modulo m_vendas
'''

import unittest
import sys
sys.path.insert(0, '../')
import m_vendas

class TestMVendas(unittest.TestCase):

    def __init__(self, *args, **kargs):
        super(TestMVendas, self).__init__(*args, **kargs)
    
    def test_a_diretorio_inexistente(self):
        ''' Faz um teste esperando uma excessão para um diretorio que não existe '''
        m = m_vendas.Mvendas('/tmpax')
        # Espera um FileNotFoundError
        with self.assertRaises(FileNotFoundError): m.pull()
    
    def test_b_diretorio_nao_e_um_projeto_git(self):
        ''' Testa para ver se o diretorio contem um arquivo .git '''
        m = m_vendas.Mvendas('/tmp')
        # Espera um FileNotFoundError
        with self.assertRaises(FileNotFoundError): m.pull()
        

if __name__ == '__main__':
    unittest.main()