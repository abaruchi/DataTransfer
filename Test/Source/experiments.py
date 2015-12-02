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
from argparse import ArgumentParser, ArgumentError

self.__contrato = contrato

class Teste(object):
    __metaclass__ = ABCMeta

    def __init__(self,duracao=60, myid='my_execution'):
        self.__duracao = duracao
        self.__myid = myid
        self.__timestamp = int(time.time())

    @property
    def duracao(self):
        return self.__duracao

    @property
    def myid(self):
        return self.__myid

    @property
    def timestamp(self):
        return self.__timestamp

    @abstractmethod
    def inicia_teste(self):
        pass

    @abstractmethod
    def finaliza_teste(self):
        pass

    @abstractmethod
    def armazena_resultado(self):
        pass

class Mem2Mem(Teste):

    def inicia_teste(self):
        print "Starting Test"

    def finaliza_teste(self):
        print "Finishing Test"

    def armazena_resultado(self):
        print "Logging Partial Results"

class Disk2Disk(Teste):

    def __init__(self, origem, destino, tamanho=5):
        self.origem = origem
        self.destino = destino
        self.tamanho = tamanho

    def cria_arquivo (self):
        print "Creating File of %s Gb" % self.tamanho

    def inicia_teste(self):
        print "Starting Test"

    def finaliza_teste(self):
        print "Finishing Test"

    def armazena_resultado(self):
        print "Logging Partial Results"


class Log (object):

    def __init__(self, arquivo, data, timestap):
        self.__arquivo = arquivo
        self.__data = data
        self.__timestamp = timestap

    def inicia_log(self):
        print "Logging Starting"

    def termina_log(self):
        print "Log Terminated"

    def atualiza_log(self):
        print "Log Updated"

