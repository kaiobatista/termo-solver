alfabeto = 'abcdefghijklmnopqrstuvwxyz'

arquivo = './palavras_disponiveis.txt'


def contar_letras(lista):
    letras_c = dict()
    for l in alfabeto:
        letras_c[l] = 0
    for word in lista:
        word = word.replace('\n', '')
        for l in alfabeto:
            if l in word:
                letras_c[l] += 1
    
    return letras_c


def organizar_dict(dicio):
    value_key_pairs = [(k, v) for (v, k) in dicio.items()]
    sorted_value_key_pairs = sorted(value_key_pairs, reverse=True)
    sorted_dicio = {k: v for v, k in sorted_value_key_pairs}

    return sorted_dicio

letras_count = dict()
for l in alfabeto:
    letras_count[l] = 0
total_de_palavras = 6026
principais_palavras = list()

palavra_alvo = {0:'', 1:'', 2:'', 3:'', 4:''}
letras_certas = list()
letras_erradas = list()

with open(arquivo, 'r') as f:
    for word in f.readlines():
        word = word.replace('\n', '')
        for l in alfabeto:
            if l in word:
                letras_count[l] += 1


value_key_pairs = [(k, v) for (v, k) in letras_count.items()]
sorted_value_key_pairs = sorted(value_key_pairs, reverse=True)

letras_count = {k: v for v, k in sorted_value_key_pairs}

with open(arquivo, 'r') as f:
    for word in f.readlines():
        counter = 0
        word = word.replace('\n', '')
        for l in list(letras_count.keys())[:6]:
            if l in word:
                counter += 1
        if counter == 5:
            principais_palavras.append(word)
        if len(principais_palavras) >= 20:
            break

principais_palavras = list(set(principais_palavras[:]))
print(principais_palavras)

print(f'Palavras iniciais recomendadas: {", ".join(principais_palavras)}')

count = 0

while True:
    print('Qual palavra você usou?')
    palavra_usada = input('>> ')
    print('Você descobriu quantas letras do alvo?')
    n_letras = int(input('>> '))
    for i in range(0, n_letras):
        print(f'Digite a {i + 1}ª letra descoberta e a posição [pos 0 = nao sabe a posicao]: ')
        lt, pos = input('>> ').split(' ')
        letras_certas.append(lt)
        if int(pos) > 0: palavra_alvo[int(pos) - 1] = lt
    for l in palavra_usada:
        if l not in letras_certas:
            letras_erradas.append(l)
    letras_erradas = list(set(letras_erradas))

    palavras_possiveis = list()
    with open(arquivo, 'r') as f:
        for word in f.readlines():
            word = word.replace('\n', '')
            tem_letra_errada = None
            for l in letras_erradas:
                if l in word:
                    tem_letra_errada = True
            if not tem_letra_errada:
                qnt_certas_na_palavra = 0
                for l  in letras_certas:
                    if l in word:
                        qnt_certas_na_palavra += 1
                if qnt_certas_na_palavra == len(letras_certas):
                    if ''.join(list(palavra_alvo.values())) in '        ':
                            palavras_possiveis.append(word)
                    else:
                        qnt_certas_na_palavra = 0
                        for k, v in palavra_alvo.items():    
                            if word[k] == v:
                                qnt_certas_na_palavra += 1

                        if qnt_certas_na_palavra == len([x for x in palavra_alvo.values() if x != '']):        
                            palavras_possiveis.append(word)
    
    palavras_possiveis = list(set(palavras_possiveis))
    letras_count = contar_letras(palavras_possiveis)
    for l in palavra_usada:
        if l in list(letras_count.keys()):
            letras_count.pop(l)
    letras_count = organizar_dict(letras_count)
    sis_pontuacao = {k: list(letras_count.keys()).index(k) + 1 for k in letras_count.keys()}
    palavra_pontuacao = list()
    for p in palavras_possiveis:
        pontos = 0
        for k, v in sis_pontuacao.items():
            if k in p: pontos += 1/v
        palavra_pontuacao.append((round(pontos, 4), p))
    
    palavra_pontuacao = sorted(palavra_pontuacao, reverse=True)
    

    print(palavra_pontuacao)
    print('Podem ser', len(palavras_possiveis), 'palavras')
    print(f'Fomação da palavra alvo: {"".join(list(palavra_alvo.values()))}')