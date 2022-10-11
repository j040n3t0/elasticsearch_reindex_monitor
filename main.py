#Created by Joao Neto <joaojose.ti@gmail.com>
#Date 10/10/2021

# Importando bibliotecas
import requests, sys, urllib2, json, os, time, subprocess
from progress.bar import IncrementalBar

class SlowBar(IncrementalBar):
  suffix = '%(percent).1f%% - Tempo decorrido aprox. .: %(elapsed_minutes)dm - Finaliza em aprox. %(remaining_minutes)dm - Faltam.: %(remaining)d registros'
  @property
  def remaining_minutes(self):
    if self.eta / 60 < 1:
      return 1
    else:
      return self.eta / 60

  @property
  def elapsed_minutes(self):
    return self.elapsed / 60


def consultaTask(host,user_key,task_id):
  headers = {
      "Authorization": "Basic " + user_key,
      "Content-Type": "application/json"
  }

  url = host + "/_tasks/" + task_id

  response = requests.request("GET", url, headers=headers)
  return json.loads(response.text)


print("........... Script para monitoramento de REINDEX ...........")

# Define o host que sera pesquisado, caso nao infome nada o variavel recebe "*"
host =     raw_input("Informe o enpoint do Elasticsearch.: ")
user_key = raw_input("Informe a Basic Key de autenticacao.: ")
task_id =  raw_input("Informe o id da task.: ")

qtd_files = consultaTask(host,user_key,task_id)['task']['status']['total']

pbar = SlowBar('Reindexando', fill='@', max=qtd_files)
control = 0
controle = 0
while True:
    if control > 2:
        break
    else:
      f_new_index = consultaTask(host,user_key,task_id)['task']['status']['created']
      controle = f_new_index - controle
      if controle > 0 :
          pbar.next(controle)
      controle = f_new_index
      time.sleep(2)
      if f_new_index == qtd_files:
          control += 1

pbar.finish()
time.sleep(2)

print("\n\nO processo de reindexacao foi concluido!!")