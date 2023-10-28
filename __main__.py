import pygame
import time

class Nodo:
    def __init__(self, posicao, pai=None):
        self.posicao = posicao
        self.pai = pai
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, outro):
        return self.posicao == outro.posicao

def busca_a_estrela(mapa, inicio, fim):
    lista_aberta = []
    lista_fechada = []

    nodo_inicio = Nodo(inicio)
    nodo_fim = Nodo(fim)

    lista_aberta.append(nodo_inicio)

    while lista_aberta:
        nodo_atual = lista_aberta[0]
        indice_atual = 0

        for indice, item in enumerate(lista_aberta):
            if item.f < nodo_atual.f:
                nodo_atual = item
                indice_atual = indice

        lista_aberta.pop(indice_atual)
        lista_fechada.append(nodo_atual)

        if nodo_atual == nodo_fim:
            caminho = []
            atual = nodo_atual
            while atual is not None:
                caminho.append(atual.posicao)
                atual = atual.pai
            return caminho[::-1]

        filhos = []
        movimentos = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for novo_movimento in movimentos:
            posicao_nova = (nodo_atual.posicao[0] + novo_movimento[0], nodo_atual.posicao[1] + novo_movimento[1])

            if (0 <= posicao_nova[0] < len(mapa)) and (0 <= posicao_nova[1] < len(mapa[0])) and mapa[posicao_nova[0]][posicao_nova[1]] == ' ':
                novo_nodo = Nodo(posicao_nova, nodo_atual)
                filhos.append(novo_nodo)

        for filho in filhos:
            for filho_fechado in lista_fechada:
                if filho == filho_fechado:
                    continue

            filho.g = nodo_atual.g + 1
            filho.h = ((filho.posicao[0] - nodo_fim.posicao[0]) ** 2) + ((filho.posicao[1] - nodo_fim.posicao[1]) ** 2)
            filho.f = filho.g + filho.h

            for nodo_aberto in lista_aberta:
                if filho == nodo_aberto and filho.g > nodo_aberto.g:
                    continue

            lista_aberta.append(filho)

def desenhar_labirinto(tela, mapa):
    tamanho_celula = 30
    cor_parede = (0, 0, 0)
    cor_caminho = (255, 255, 255)
    for indice_linha, linha in enumerate(mapa):
        for indice_coluna, celula in enumerate(linha):
            if celula == '▓':
                pygame.draw.rect(tela, cor_parede, (indice_coluna * tamanho_celula, indice_linha * tamanho_celula, tamanho_celula, tamanho_celula))
            elif celula == ' ':
                pygame.draw.rect(tela, cor_caminho, (indice_coluna * tamanho_celula, indice_linha * tamanho_celula, tamanho_celula, tamanho_celula))

def main():
    pygame.init()

    labirinto = [['▓', '▓', '▓', '▓', '▓'],
                ['▓', ' ', ' ', '$', '▓'],
                ['▓', ' ', '▓', ' ', '▓'],
                ['▓', '☺', ' ', '$', '▓'],
                ['▓', '▓', '▓', '▓', '▓']]

    inicio = (3, 1)
    fim = (1, 3)

    caminho = busca_a_estrela(labirinto, inicio, fim)

    if caminho is None:
        print("Não foi encontrado um caminho válido.")
        return

    largura_tela = len(labirinto[0]) * 30
    altura_tela = len(labirinto) * 30

    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Resolutor de Labirinto A*")

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        for passo in caminho:
            labirinto[passo[0]][passo[1]] = "☺"
            desenhar_labirinto(tela, labirinto)
            pygame.display.update()
            time.sleep(0.5)

    pygame.quit()

if __name__ == '__main__':
    main()
