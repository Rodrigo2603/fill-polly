import pygame
import sys
from tkinter import simpledialog

class Ponto:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor

    def xy(self):
        return (self.x, self.y)

class Triangulo:
    def __init__(self, label):
        self.nome = label
        self.corAresta = (0, 0, 0)
        self.pontos = []

    def escolher_cor_aresta(self, cor):
        self.corAresta = cor

    def atualizar_rotulo(self, novo_rotulo):
        self.nome = novo_rotulo

class Main:
    def __init__(self):
        pygame.init()
        self.canvas_width = 1000
        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Fill Poly")

        self.corAtual = (0, 0, 0)
        self.listaTriangulos = []
        self.poly_selecionado = None

        self.coord_surface = pygame.Surface((400, 780))

    def handle_mouse(self):
        click_count = 0
        label_count = len(self.listaTriangulos) + 1
        novo_triangulo = Triangulo(f'T{label_count}')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos

                    if x > self.canvas_width:
                        continue

                    if click_count > 0 and (x, y) == novo_triangulo.pontos[0].xy():
                        continue
                    elif click_count > 1 and ((x, y) == novo_triangulo.pontos[1].xy() or (x, y) == novo_triangulo.pontos[0].xy) and (x == novo_triangulo.pontos[0].x == novo_triangulo.pontos[1].x) and (y == novo_triangulo.pontos[0].y == novo_triangulo.pontos[1].y):
                        continue  
                    else:
                        click_count += 1
                        ponto = Ponto(x, y, self.corAtual)
                        novo_triangulo.pontos.append(ponto)

                    if click_count >= 3:
                        self.listaTriangulos.append(novo_triangulo)
                        self.fill_poly(novo_triangulo)
                        return

            pygame.display.flip()

    def draw_all_poly(self):
        self.screen.fill((255, 255, 255))
        self.coord_surface.fill((255, 0, 0))
    
        font = pygame.font.Font(None, 30)
        y_offset = 40

        for triangulo in self.listaTriangulos:
            self.fill_poly(triangulo)
            pygame.draw.polygon(self.screen, triangulo.corAresta, [ponto.xy() for ponto in triangulo.pontos], 2)

            if triangulo == self.poly_selecionado:
                text = font.render(triangulo.nome, True, (0, 0, 0))
                self.coord_surface.blit(text, (10, y_offset))

                for i, ponto in enumerate(triangulo.pontos):
                    text = font.render(f'V{i + 1}: ({ponto.x}, {ponto.y}, {ponto.cor})', True, (0, 0, 0))
                    text_rect = text.get_rect(topleft=(10, y_offset + (i + 1) * 40))

                    if text_rect.bottom > 780:
                        text_rect.y -= text_rect.bottom - 780

                    self.coord_surface.blit(text, text_rect.topleft)

                y_offset += text_rect.bottom + 10

        pygame.draw.line(self.screen, (0, 0, 0), (self.canvas_width, 0), (self.canvas_width, 780), 2)
        self.screen.blit(self.coord_surface, (self.canvas_width, 0))

        pygame.display.flip()

    def verificar_selecao(self, x, y):
        for triangulo in reversed(self.listaTriangulos):
            if self.ponto_dentro_poligono(x, y, [ponto.xy() for ponto in triangulo.pontos]):
                self.listaTriangulos.remove(triangulo)
                self.listaTriangulos.insert(0, triangulo)
                self.poly_selecionado = triangulo
                break
            else:
                self.poly_selecionado = None

    def ponto_dentro_poligono(self, x, y, pontos):
        n = len(pontos)
        dentro = False

        j = n - 1
        for i in range(n):
            xi, yi = pontos[i]
            xj, yj = pontos[j]

            intersecta = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersecta:
                dentro = not dentro

            j = i

        return dentro
    
    def fill_poly(self, triangulo):
        if triangulo == self.poly_selecionado:
            pygame.draw.polygon(self.screen, (255, 255, 255), [ponto.xy() for ponto in triangulo.pontos])
        else:
            self.filling_poly(triangulo)

    def filling_poly(self, triangulo):
        triangulo.pontos.sort(key=lambda ponto: ponto.y)
        v0, v1, v2 = triangulo.pontos[0], triangulo.pontos[1], triangulo.pontos[2]
        v0_cor, v1_cor, v2_cor = v0.cor, v1.cor, v2.cor

        arestas = [
            {"comeco": v0, "fim": v1, "taxa_avanco": (v1.x - v0.x) / (v1.y - v0.y) if abs(v1.y - v0.y) > 1e-6 else float('inf'),
            "taxaR": (v1_cor[0] - v0_cor[0]) / (v1.y - v0.y) if abs(v1.y - v0.y) > 1e-6 else 0,
            "taxaG": (v1_cor[1] - v0_cor[1]) / (v1.y - v0.y) if abs(v1.y - v0.y) > 1e-6 else 0,
            "taxaB": (v1_cor[2] - v0_cor[2]) / (v1.y - v0.y) if abs(v1.y - v0.y) > 1e-6 else 0},
            {"comeco": v1, "fim": v2, "taxa_avanco": (v2.x - v1.x) / (v2.y - v1.y) if abs(v2.y - v1.y) > 1e-6 else float('inf'),
            "taxaR": (v2_cor[0] - v1_cor[0]) / (v2.y - v1.y) if abs(v2.y - v1.y) > 1e-6 else 0,
            "taxaG": (v2_cor[1] - v1_cor[1]) / (v2.y - v1.y) if abs(v2.y - v1.y) > 1e-6 else 0,
            "taxaB": (v2_cor[2] - v1_cor[2]) / (v2.y - v1.y) if abs(v2.y - v1.y) > 1e-6 else 0},
            {"comeco": v2, "fim": v0, "taxa_avanco": (v0.x - v2.x) / (v0.y - v2.y) if abs(v0.y - v2.y) > 1e-6 else float('inf'),
            "taxaR": (v0_cor[0] - v2_cor[0]) / (v0.y - v2.y) if abs(v0.y - v2.y) > 1e-6 else 0,
            "taxaG": (v0_cor[1] - v2_cor[1]) / (v0.y - v2.y) if abs(v0.y - v2.y) > 1e-6 else 0,
            "taxaB": (v0_cor[2] - v2_cor[2]) / (v0.y - v2.y) if abs(v0.y - v2.y) > 1e-6 else 0}
        ]

        último_x_superior, última_cor_superior, inverte_lado = 0, None, False

        for y in range(v0.y, v1.y):
            linha_atual = y - v0.y
            intervalo = [arestas[0]["comeco"].x + arestas[0]["taxa_avanco"] * linha_atual, arestas[0]["comeco"].x + arestas[2]["taxa_avanco"] * linha_atual]
            último_x_superior = intervalo[1]
            if intervalo[1] < intervalo[0]:
                intervalo[0], intervalo[1] = intervalo[1], intervalo[0]
                inverte_lado = True

            cor_inicial_superior = (
                v0_cor[0] + arestas[0]["taxaR"] * linha_atual,
                v0_cor[1] + arestas[0]["taxaG"] * linha_atual,
                v0_cor[2] + arestas[0]["taxaB"] * linha_atual
            )
            cor_final = (
                v0_cor[0] + arestas[2]["taxaR"] * linha_atual,
                v0_cor[1] + arestas[2]["taxaG"] * linha_atual,
                v0_cor[2] + arestas[2]["taxaB"] * linha_atual
            )
            última_cor_superior = cor_final
            if inverte_lado:
                cor_inicial_superior, cor_final = cor_final, cor_inicial_superior

            intervalo_linhas = intervalo[1] - intervalo[0]

            if intervalo_linhas != 0:
                taxa_variação = (
                    (cor_final[0] - cor_inicial_superior[0]) / intervalo_linhas,
                    (cor_final[1] - cor_inicial_superior[1]) / intervalo_linhas,
                    (cor_final[2] - cor_inicial_superior[2]) / intervalo_linhas
                )
            else:
                taxa_variação = (0, 0, 0)
            
            for j in range(int(intervalo[0]), int(intervalo[1])):
                main.draw_pixel(j, y, f'rgb({cor_inicial_superior[0] + taxa_variação[0] * (j - intervalo[0])}, {cor_inicial_superior[1] + taxa_variação[1] * (j - intervalo[0])}, {cor_inicial_superior[2] + taxa_variação[2] * (j - intervalo[0])})')

        inverte_lado = False

        for y in range(v1.y, v2.y):
            linha_atual = y - v1.y
            intervalo = [arestas[1]["comeco"].x + arestas[1]["taxa_avanco"] * linha_atual, último_x_superior + arestas[2]["taxa_avanco"] * linha_atual]
            if intervalo[1] < intervalo[0]:
                intervalo[0], intervalo[1] = intervalo[1], intervalo[0]
                inverte_lado = True

            cor_inicial_inferior = (
                v1_cor[0] + arestas[1]["taxaR"] * linha_atual,
                v1_cor[1] + arestas[1]["taxaG"] * linha_atual,
                v1_cor[2] + arestas[1]["taxaB"] * linha_atual
            )
            cor_final = (
                última_cor_superior[0] + arestas[2]["taxaR"] * linha_atual,
                última_cor_superior[1] + arestas[2]["taxaG"] * linha_atual,
                última_cor_superior[2] + arestas[2]["taxaB"] * linha_atual
            )
            if inverte_lado:
                cor_inicial_inferior, cor_final = cor_final, cor_inicial_inferior

            intervalo_linhas = intervalo[1] - intervalo[0]
            if intervalo_linhas != 0:    
                taxa_variação = (
                    (cor_final[0] - cor_inicial_inferior[0]) / intervalo_linhas,
                    (cor_final[1] - cor_inicial_inferior[1]) / intervalo_linhas,
                    (cor_final[2] - cor_inicial_inferior[2]) / intervalo_linhas
                )
            else:
                taxa_variação = (0, 0, 0)

            for j in range(int(intervalo[0]), int(intervalo[1])):
                main.draw_pixel(j, y, f'rgb({cor_inicial_inferior[0] + taxa_variação[0] * (j - intervalo[0])}, {cor_inicial_inferior[1] + taxa_variação[1] * (j - intervalo[0])}, {cor_inicial_inferior[2] + taxa_variação[2] * (j - intervalo[0])})')
                
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.handle_mouse()
                    elif event.key == pygame.K_r:
                        self.resetar_canvas()
                    elif event.key == pygame.K_m:
                        self.obter_cor_manual()
                    elif event.key == pygame.K_a:
                        self.obter_cor_aresta()
                    elif event.key == pygame.K_DELETE:
                        if self.poly_selecionado is not None:
                            self.remover_poly_selecionado()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        x, y = event.pos
                        self.verificar_selecao(x, y)

            self.draw_all_poly()
            pygame.display.flip()

    def draw_pixel(self, x, y, cor):
        
        r, g, b = map(float, cor[4:-1].split(','))
        
        r = int(max(0, min(255, r)))
        g = int(max(0, min(255, g)))
        b = int(max(0, min(255, b)))

        x = int(x + 0.5) + 1
        y = int(y + 0.5)

        pygame.draw.rect(self.screen, (r, g, b), (x, y, 1, 1))
    
    def resetar_canvas(self):
        self.listaTriangulos = []
        self.poly_selecionado = None

    def remover_poly_selecionado(self):
        if self.poly_selecionado in self.listaTriangulos:
            self.listaTriangulos.remove(self.poly_selecionado)
            self.poly_selecionado = None

            for i, triangulo in enumerate(self.listaTriangulos):
                novo_rotulo = f'T{i + 1}'
                triangulo.atualizar_rotulo(novo_rotulo)

    def obter_cor_manual(self):
        if self.poly_selecionado is not None:
            for i, ponto in enumerate(self.poly_selecionado.pontos):
                cor_rgb = simpledialog.askstring("Cor", f"Digite a cor para o V{i + 1} no formato R, G, B:")
                if cor_rgb:
                    try:
                        r, g, b = map(int, cor_rgb.split(','))
                        r = max(0, min(r, 255))
                        g = max(0, min(g, 255))
                        b = max(0, min(b, 255))
                        ponto.cor = (r, g, b)
                    except ValueError:
                        pass

    def obter_cor_aresta(self):
        if self.poly_selecionado is not None:
            cor_rgb = simpledialog.askstring("Cor da Aresta", "Digite a cor para a aresta no formato R, G, B:")
            if cor_rgb:
                try:
                    r, g, b = map(int, cor_rgb.split(','))
                    r = max(0, min(r, 255))
                    g = max(0, min(g, 255))
                    b = max(0, min(b, 255))
                    cor_aresta = (r, g, b)
                    self.poly_selecionado.escolher_cor_aresta(cor_aresta)
                except ValueError:
                    pass

if __name__ == "__main__":
    main = Main()
    main.run()