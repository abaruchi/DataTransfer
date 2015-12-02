#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#          - Artur Baruchi <abaruchi AT ncc DOT unesp DOT br>
#
# -*- coding: utf-8 -*-


from abc import ABCMeta, abstractmethod
import time
import tempfile
from ConfigParser import SafeConfigParser
import subprocess
import os
import re
from paramiko import SSHClient


class Teste(object):
    '''
    Classe Abstrata que implementa os Testes.
    '''
    __metaclass__ = ABCMeta

    def __init__(self, duracao='60', clientes='1', myid='first_test'):
        self.__duracao = duracao
        self.__clientes = clientes
        self.__myid = myid
        self.__timestamp = int(time.time())

    @property
    def duracao(self):
        return self.__duracao

    @property
    def clientes(self):
        return self.__clientes

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def myid(self):
        return self.__myid

    def inicia_server(self):
        print "Server started"

    def finaliza_teste(self):
        print "Tests Finished"

    @abstractmethod
    def inicia_clientes(self):
        pass


class Mem2Mem(Teste):
    '''
    Classe que implementa testes Memory2Memory.
    '''

    def inicia_clientes(self):
        print "Starting Test"
        print "Number of Clients: %s" % self.clientes


class Disk2Disk(Teste):
    '''
    Classe que implementa testes Disk2Disk.
    '''

    def __init__(self, arquivo_origem, arquivo_destino, tamanho=5):
        self.arquivo_origem = arquivo_origem
        self.arquivo_destino = arquivo_destino
        self.arquivo_tamanho = tamanho

    def cria_arquivo (self):
        print "Creating File of %s Gb" % self.tamanho

    def inicia_clientes(self):
        print "Starting Test"


class Parametros(object):
    '''
    Classe que recupera os parametros para execucao dos testes de um arquivo
    .ini.
    '''

    def __init__(self, conf_file='test.ini'):
        self.__conf_file = conf_file
        self.__parser = SafeConfigParser()

    @property
    def parser(self):
        return self.__parser

    @property
    def conf_file(self):
        return self.__conf_file

    @property
    def tipo_experimento(self):
        self.parser.read(self.conf_file)
        return self.parser.get('Experiment','type')

    @property
    def servidor(self):
        self.parser.read(self.conf_file)
        return self.parser.get('Server','IP')

    @property
    def log_servidor(self):
        self.parser.read(self.conf_file)
        return self.parser.get('Server','LogFile')

    @property
    def qtde_cliente(self):
        self.parser.read(self.conf_file)
        return self.parser.get('Client','Number')

    @property
    def log_cliente(self):
        self.parser.read(self.conf_file)
        return self.parser.get('Client','Number')

    @property
    def disk_tam_arquivo(self):
        self.parser.read(self.conf_file)
        return self.parser.get('Disk2Disk','FileSize')

    @property
    def disk_path_arquivo(self):
        self.parser.read(self.conf_file)
        return self.parser.get('Disk2Disk','Path')


class Log (object):
    '''
    Classe que implementa o registro dos Logs no decorrer dos testes.
    '''

    def __init__(self, arquivo, timestap):
        self.__arquivo = arquivo
        self.__timestamp = timestap

    def inicia_log(self):
        print "Logging Starting"

    def termina_log(self):
        print "Log Terminated"

    def atualiza_log(self):
        print "Log Updated"


if __name__ == '__main__':

    teste_parametros = Parametros()
    print teste_parametros.conf_file
    print teste_parametros.disk_path_arquivo

    meu_teste01 = Mem2Mem()
    print meu_teste01.inicia_server()

    meu_teste02 = Disk2Disk(teste_parametros.disk_path_arquivo,
                            teste_parametros.disk_path_arquivo)
    print meu_teste02.inicia_clientes()
    print meu_teste02.inicia_server()
