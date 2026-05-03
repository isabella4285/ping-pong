from PPlay.window import *
from PPlay.sprite import *
from PPlay.collision import *
import pygame

em_jogo = True
wx, wy = 1000, 700
pontos = [0, 0] #jogador, ia
pygame.mixer.init()
colisao_som = pygame.mixer.Sound("pong.mp3")
buzzer_som = pygame.mixer.Sound("buzzer.mp3")
get_piece = pygame.mixer.Sound("get_piece.mp3")

colisoes = 0

#variacoes = [0, 10, 20, 50]

janela = Window(wx, wy)
janela.set_title("ping pong")
janela.set_background_color((100, 0, 90))  

bola=Sprite("bola.png")
barra1 = Sprite("barra.png")
barra2 = Sprite("barra.png")

barra1.set_position(0, wy/2-barra1.height/2)
barra2.set_position(wx-barra2.width, wy/2-barra2.height/2)

bola.x = (janela.width)/2 - (bola.width)/2
bola.y = (janela.height)/2 - (bola.height)/2

velx, vely = 300, 300

#controlar as colisoes
colisao_parede = False
colisao_barra = False

while True:
    janela.set_background_color((100, 0, 90))

    if em_jogo:
        bola.x += velx*janela.delta_time()
        bola.y += vely*janela.delta_time()
        #colisoes com margens horizontais
        if bola.y <= 0:
            bola.y = 0 #corrige a posicao
            if not colisao_parede:
                vely *= -1
                colisao_parede = True
        elif bola.y >= wy - bola.height:
            bola.y = wy - bola.height #corrige a posicao
            if not colisao_parede:
                vely *= -1
                colisao_parede = True
        else:
            colisao_parede = False #resetar quando nao esta colidindo
    
    

        #verificar pontos depois q a bola sai da tela
        if bola.x > wx: #direita-> ponto do jogador
            get_piece.play()
            pontos[0] += 1
            print(pontos)
            em_jogo = False
            bola.set_position((wx)/2-bola.width/2, (wy)/2-bola.height/2)
            barra1.set_position(0, wy/2-bola.height/2)

        elif bola.x < -bola.width:
            buzzer_som.play()
            pontos[1] += 1
            print(pontos)
            em_jogo = False
            bola.set_position((wx)/2-bola.width/2, (wy)/2-barra1.height/2)
            barra1.set_position(0, wy/2-barra1.height/2)
            

        #colisoes com margens horizontais
        if bola.y <= 0 or bola.y >= wy - bola.height:
            vely *= -1
        
        #movendo a barra esquerda
        keyboard = janela.get_keyboard()
        if keyboard.key_pressed("UP") and barra1.y > 0:
            barra1.y -= 400 * janela.delta_time()
        if keyboard.key_pressed("DOWN") and barra1.y < wy - barra1.height:
            barra1.y += 400 * janela.delta_time()
        
        
        #movendo a barra direita - ia
        velocidade_ia = 350  # velocidade da IA, um pouco menor que a bola
        if barra2.y + barra2.height/2 < bola.y and barra2.y < wy - barra2.height:
            barra2.y += velocidade_ia * janela.delta_time()
        elif barra2.y + barra2.height/2 > bola.y and barra2.y > 0:
            barra2.y -= velocidade_ia * janela.delta_time()
        
        

        #adicionando colisao
        if Collision.collided(bola, barra2) and not colidiu_barra:
            #corrigir a posicao para nao ficar entrando na barra
            bola.x = barra2.x - bola.width
            velx *= -1
            colisoes += 1
            colisao_som.play()
            colidiu_barra = True
            
        elif Collision.collided(bola, barra1) and not colidiu_barra:
            #corrige a posicao para nao ficar entrando na barra
            bola.x = barra1.x + barra1.width
            velx *= -1
            colisoes +=1
            colisao_som.play()
            #adicionar som de colisao, o pong.mp3
            
            colidiu_barra = True
            
        else:
            if not Collision.collided(bola, barra1) and not Collision.collided(bola, barra2):
                colidiu_barra = False #resetar quando nao esta colidindo

    else: #espera espaco para resetar
        if janela.get_keyboard().key_pressed("space"):
            #colocar musica de bzzer
            bola.set_position((wx)/2-bola.width/2, (wy)/2-bola.height/2)
            barra1.set_position(0, wy/2-barra1.height/2)
            velx, vely = 300, 300
            em_jogo = True
            colidiu_barra = False
            colidiu_parede = False

    if colisoes >= 3:
        velx *= 1.1
        vely *= 1.1
        colisoes = 0

    #desenhar tudo
    bola.draw()
    barra1.draw()
    barra2.draw()
    
    janela.update()
    


        

