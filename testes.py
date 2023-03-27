#informações apenas para teste
km_total = 1000
itens = {'LANCHA': 10000, 'SUV': 4000, 'CARRO': 1000, 'MOTO': 1000}
peso_total_carga = sum(itens.values())
cidades = ['PORTO ALEGRE', 'VITÓRIA', 'ARACAJÚ']
distancias_cidades = {'ARACAJU - BELEM': 2079, 'BELEM - VITORIA': 3108}

#capacidade máxima de cada caminhão
capacidade_caminhoes = {'P': 1000, 'M': 4000, 'G': 10000}
#custo por km rodado de cada caminhão
custo_caminhoes = {'P': 4.87, 'M': 11.92, 'G': 27.44}

'''       DAQUI PRA BAIXO AINDA NÃO ESTÁ NO CÓDIGO GERAL ! ! ! ! ! ! ! ! ! !      '''

def distribuir_itens_caminhoes(capacidade_caminhoes, itens):
  #identifica quantidade e modelo do(s) caminhão(ões) necessário(s) para o transporte
  caminhoes_necessarios = {'P': 0, 'M': 0, 'G': 0}
  capacidade_atual_caminhoes = capacidade_caminhoes
  itens_atual_caminhoes = {'P': [], 'M': [], 'G': []}

  #começa com o peso total da carga, e depois vai reduzindo conforme alocação em caminhoes
  peso_atual_carga = sum(itens.values())
  #verificar se é possível alocar todos os itens em um único caminhão, se sim, pular loop while
  maior_capacidade = [1000, 4000, 10000]
  for capacidade_maxima in maior_capacidade:
    if peso_atual_carga <= capacidade_maxima:
      if capacidade_maxima == 1000:
        caminhoes_necessarios['P'] += 1
        capacidade_atual_caminhoes['P'] = capacidade_caminhoes['P'] - peso_atual_carga
        itens_atual_caminhoes['P'] = list(itens.keys())
      elif capacidade_maxima == 4000:
        caminhoes_necessarios['M'] += 1
        capacidade_atual_caminhoes['M'] = capacidade_caminhoes['M'] - peso_atual_carga
        itens_atual_caminhoes['M'] = list(itens.keys())
      elif capacidade_maxima == 10000:
        caminhoes_necessarios['G'] += 1
        capacidade_atual_caminhoes['G'] = capacidade_caminhoes['G'] - peso_atual_carga
        itens_atual_caminhoes['G'] = list(itens.keys())
      peso_atual_carga = 0
      break
  
  #ordena os itens por peso
  itens_ordenados_por_peso = dict(sorted(itens.items(), key=lambda x: x[1], reverse=True))
  itens_ordenados_restantes = itens_ordenados_por_peso.copy()
  
  while peso_atual_carga > 0:
    
    #itera nos itens da carga do maior ao menor peso
    for item, peso in itens_ordenados_por_peso.items():
      #tenta colocar o item no menor caminhão que ainda tem capacidade
      adicionado = False
      for modelo in ['G', 'M', 'P']:
        capacidade = capacidade_atual_caminhoes[modelo]
        if peso <= capacidade:
          #adiciona o item no caminhão, e atualiza a capacidade restante do caminhão
          peso_atual_carga -= peso
          capacidade_atual_caminhoes[modelo] -= peso
          itens_atual_caminhoes[modelo].append(item)
          #se o modelo em que o item foi incluído for G e
          #a capacidade atual ficar menor que o item restante mais leve, limpá-lo
          item_mais_leve = min(itens_ordenados_restantes.values())
          if (modelo == 'G') and (capacidade_atual_caminhoes['G'] < item_mais_leve):
            capacidade_atual_caminhoes['G'] = 10000 
            caminhoes_necessarios['G'] += 1
            itens_ordenados_restantes.pop(item)
            #exclui demais itens de 'G' em itens_ordenados_restantes e itens_atual_caminhoes
            for item_residual in list(itens_ordenados_restantes.keys()):
              if item_residual in itens_atual_caminhoes.get('G', []):
                itens_ordenados_restantes.pop(item_residual)
            itens_atual_caminhoes['G'] = []
            
          #verifica se o item já estava em outro caminhão, se sim, remove do caminhão anterior
          for tamanho, itens_array in itens_atual_caminhoes.items():
            if item in itens_array and tamanho != modelo:
              itens_array.remove(item)
              capacidade_atual_caminhoes[tamanho] += peso
  
          adicionado = True
          break
              
      #se o item não couber em nenhum dos caminhões
      if not adicionado:
        #verifica se há capacidade no caminhão G
        if peso <= capacidade_atual_caminhoes['G']:
          peso_atual_carga -= peso
          capacidade_atual_caminhoes['G'] -= peso
          itens_atual_caminhoes['G'].append(item)
          caminhoes_necessarios['G'] += 1
        #se não houver capacidade no caminhão G, transfere os itens atuais para o M ou G
        else:
          if sum(capacidade_atual_caminhoes.values()) - min(capacidade_atual_caminhoes.values()) >= peso:
            for modelo, item_no_caminhao in itens_atual_caminhoes.items():
              if modelo != 'P' and len(item_no_caminhao) > 0:
                peso_transferir = sum([itens_ordenados_por_peso[item] for item in item_no_caminhao])
                itens_transferir = itens_atual_caminhoes[modelo].copy()
                itens_atual_caminhoes[modelo] = []
                capacidade_atual_caminhoes[modelo] += peso_transferir
                itens_atual_caminhoes['P'].extend(itens_transferir)
                capacidade_atual_caminhoes['P'] += peso_transferir
              else:
                # adiciona um caminhão G em caminhoes_necessarios, remove os itens que estavam no G em itens_atual_caminhoes,
                # remove também os itens que estavam no G em itens_ordenados_por_peso, volta a capacidade_atual_caminhoes['G'] a sua
                # capacidade máxima e reinicia a verificação
                caminhoes_necessarios['G'] += 1
                itens_ordenados_por_peso = dict([(item, peso) for item, peso in itens_ordenados_por_peso.items() if item not in itens_atual_caminhoes['G']])
                itens_atual_caminhoes['G'] = []
                capacidade_atual_caminhoes['G'] = 10000
                peso_atual_carga = sum(itens_ordenados_por_peso.values())
                break
  
    itens_restantes = list(itens_ordenados_restantes)
    
    #cria dicionário com as chaves sendo os itens e valores sendo seus pesos em "itens"
    itens_restantes_dict = {} 
    for item_restante in itens_restantes: 
      itens_restantes_dict[item_restante] = itens_ordenados_restantes[item_restante]
  
    # função para adicionar a possiveis_combinacoes as diferentes quantidade de cada caminhão para transportar os itens_restantes
    def distribuir_itens_restantes(capacidade_caminhoes, itens_restantes_dict):
      possiveis_combinacoes = []
      # capacidade atual dos caminhões, que deve ser reduzida quando um item for incluso nele
      capacidade_atual_caminhoes = {'P': capacidade_caminhoes['P'], 'M': capacidade_caminhoes['M'], 'G': capacidade_caminhoes['G']}
      n = len(itens_restantes_dict)
      for i in range(n+1):
        for j in range(n+1-i):
          p = i
          m = j
          g = n-i-j
          # verificando se é possível alocar os itens nos caminhões
          for item, peso in itens_restantes_dict.items():
            if peso <= capacidade_atual_caminhoes['P'] and p > 0:
              p -= 1
            elif peso <= capacidade_atual_caminhoes['M'] and m > 0:
              m -= 1
            elif peso <= capacidade_atual_caminhoes['G'] and g > 0:
              g -= 1
          # se todos os itens foram alocados corretamente, adiciona a combinação na lista
          if p == 0 and m == 0 and g == 0:
            possiveis_combinacoes.append({'P': i, 'M': j, 'G': n-i-j})
          # restaura a capacidade dos caminhões para a próxima iteração
          capacidade_atual_caminhoes = {'P': capacidade_caminhoes['P'], 'M': capacidade_caminhoes['M'], 'G': capacidade_caminhoes['G']}
      return possiveis_combinacoes
  
    if itens_restantes_dict:    
      possiveis_combinacoes = distribuir_itens_restantes(capacidade_caminhoes, itens_restantes_dict)
      peso_atual_carga = 0
      itens_restantes_dict = {} 
      # verificando a combinação de menor valor possível para os itens restantes
      total_cada_combinacao_possivel = []
      for combinacao in possiveis_combinacoes:
        total = 0
        for caminhao in custo_caminhoes:
          total += combinacao[caminhao] * custo_caminhoes[caminhao]
        total_cada_combinacao_possivel.append(total)
      combinacao_menor_custo = min(total_cada_combinacao_possivel)
      # atualizando as quantidades necessárias de cada caminhão de acordo com a combinação de menor custo
      for index, combinacao in enumerate(possiveis_combinacoes):
        if total_cada_combinacao_possivel[index] == combinacao_menor_custo:
          for caminhao in caminhoes_necessarios:
            caminhoes_necessarios[caminhao] += combinacao[caminhao]
          break
  return caminhoes_necessarios


caminhoes_necessarios = distribuir_itens_caminhoes(capacidade_caminhoes, itens)
print(caminhoes_necessarios)

for par_cidades, distancia in distancias_cidades.items():
  print(par_cidades, distancia)

#calcula o custo total pela qtd de cada caminhão X km
lista_necessariosXcusto = []
for tamanho, quantidade in caminhoes_necessarios.items():
    lista_necessariosXcusto.append(custo_caminhoes[tamanho] * quantidade)

custo_por_trecho = 0
custo_total = sum(lista_necessariosXcusto)*km_total

'''
#imprime resultado
print(f'Saindo de {cidades[0]} até {cidades[-1]}, a distância total a ser percorrida na rota é de {km_total} km')
print(f'Para transportar os itens {list(itens.keys())},\n de forma a resultar no menor custo por km rodado., serão necessários:')
#imprime quantidade de caminhões necessários para transportar a carga
for modelo, qtd in caminhoes_necessarios.items():
  if qtd > 0:
    print(f'{qtd} caminhão(ões) de porte {modelo}')
print(f'O valor total do frete é R$ {custo_total}, sendo R$ {custo_por_trecho} o custo unitário médio por trecho.')
'''
