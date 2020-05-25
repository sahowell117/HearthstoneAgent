#!/usr/bin/env python2.7
#-*-coding:Latin-1 -*

#Open Source Hearthstone bot
#Python2 / OpenCV


import autopy #sudo pip2.7 install autopy
import time
import numpy as np
import cv2 #sudo pacman -S opencv
import os
import argparse
import imutils
from pprint import pprint
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect, FindWindowEx
import json
from threading import *
from low_lvl import *
from gauge import *
from PIL import Image
from database_manager import *
from fight_manager import *

def whoseTurnIsIt() :
    print("scanning turn button")    
    whnd = FindWindowEx(None, None, None, 'Hearthstone')
    if not (whnd == 0):
        print('FOUND!')

    print(GetWindowRect(whnd))
    winX = (GetWindowRect(whnd))
    rect = ((max(0, winX[0]),winX[1]),(winX[2], winX[3]))
    autopy.bitmap.capture_screen(rect).save('src/screengrab.png')
    img_rgb = cv2.imread('src/screengrab.png')
    template = cv2.imread('src/ingame/enemy_turn.PNG')
    w, h = template.shape[:-1]
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .71

    if (np.amax(res) > threshold) :
        return 0

    template = cv2.imread('src/ingame/my_turn.PNG')
    w, h = template.shape[:-1]

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .71

    if (np.amax(res) > threshold) :
        return 1

def howManyCardsDoIHave() :
    print("scanning hand")         #offset is therefore 180 and  560
    rect=((180,560),(390,80))   #first tuple is top left point, next touple is width, height
    autopy.bitmap.capture_screen(rect).save('src/my_hand.png')
    img_rgb = cv2.imread('src/my_hand.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('src/cards_img/OasisSnapJaw.PNG',0)         #template is what we are looking for
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where( res >= threshold)
    if (np.amax(res) > threshold) :
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        autopy.mouse.smooth_move(pt[0] + 180, pt[1] + 560)    #moves mouse to the card
        print("found Oasis Snapjaw")
        cv2.imwrite('res.png',img_rgb)

    #zero_mana_rgb = cv2.imread('src/mana/mana0.png')
    #one_mana_rgb = cv2.imread('src/mana/1mana.PNG')
    #two_mana_rgb = cv2.imread('src/mana/mana2.png')
    #three_mana_rgb = cv2.imread('src/mana/3mana.PNG')
    #four_mana_rgb = cv2.imread('src/mana/mana4.png')
    #five_mana_rgb = cv2.imread('src/mana/mana5.png')
    #six_mana_rgb = cv2.imread('src/mana/mana6.png')
    #seven_mana_rgb = cv2.imread('src/mana/mana7.png')
    #eight_mana_rgb = cv2.imread('src/mana/mana8.png')
    #nine_mana_rgb = cv2.imread('src/mana/mana9.png')
   #
    #mana_images.append(zero_mana_rgb)
    #mana_images.append(one_mana_rgb)
    #mana_images.append(two_mana_rgb)
    #mana_images.append(three_mana_rgb)
    #mana_images.append(four_mana_rgb)
    #mana_images.append(five_mana_rgb)
    #mana_images.append(six_mana_rgb)
    #mana_images.append(seven_mana_rgb)
    #mana_images.append(eight_mana_rgb)
    #mana_images.append(nine_mana_rgb)
#
#
#
#
    #numberOfCards = 0
    #w, h = img_rgb.shape[:-1]
    #for mana in mana_images :
    #    print("testing for ")
    #    print(mana)
    #    res = cv2.matchTemplate(img_rgb, mana, cv2.TM_CCOEFF_NORMED)
    #    threshold = .4
    #    loc = np.where(res >= threshold)
    #    for pt in zip(*loc[::-1]):  # Switch collumns and rows
    #        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
#
    #    cv2.imwrite('result.png', img_rgb)
    #    if (np.amax(res) > threshold) :
    #       print("found a card")
    #       numberOfCards += 1
#
    #print(numberOfCards)       


#howManyCardsDoIHave()
#findRotatedObject('src/mana/9mana.png')
#detectRotatedAndScaledImage('src/mana/9mana.png')


#mapBoard()
###########GLOBAL############
#Data = Data_manager() #La database doit pouvoir etre utiliser par toutes les fonctions
#############################

class Game_manager :
    #Classe principale"""
    #def __init__(self):
    #    #self.k_pick,self.k_board,self.k_hand=init_scale()# get the right ratios
    #    self.name = "hunter"
    #    self.mode = "agressive"
    #    self.throwThresh = 2
    #    self.turnNb = 0 #compteur de tour
    #    self.mana = 1 # compteur de mana
    #    self.cardsNb = 0
    #    self.bot_turn = 0 # 1-actuellement au bot de jouer
    #    self.hand = []
    #    self.coin = 0
    #    self.board = []
    #    self.board_ennemy = []
    #    self.board_priority = []
    #    self.fight = Fight_manager

    def start(self) : #cherche le bouton play et lance la game
        print("Bot look for play button...")
        img_template = cv2.imread('src/ingame/play.PNG',0)
        play_button=findone(img_template)
        return clickone(play_button)

    def earlygame(self): #s'occupe de toute les actions avant le tour 1 A OPTIMISER !
        print("Bot look for confirm button...")
        found_ok = 0
        confirm_button = ([],[])
        sec = 0
        pb=progressbarClass(60,"/")
        while (tuple_test(confirm_button)==0 and sec < 60):
            pb.progress(sec)
            img_template=cv2.imread('src/ingame/confirm.PNG',0)
            confirm_button=findone(img_template)
            time.sleep(1) #on attend 1 sec
            clickone(confirm_button)
            sec = sec +1
        time.sleep(9) #time to change cards    
      #  if self.pick_cards() == 1 : # identify card on hand
      #      clickone(start_button)
      #      time.sleep(8) #time to change cards
      #      heroes_list = ["Rogue","Warlock","Warrior","Shaman","Priest","Druid","Hunter","Mage","Paladin"]         //commenting out as dont know how to pick cards or mulligan at start of game 4/15/2020
      #      #Recherche de la classe de l'adversaire
      #      for i in range(len(heroes_list)) :
      #          template = cv2.imread('src/heroes/'+heroes_list[i]+'.png',0)
      #          result=findone(template,1)
      #          if tuple_test(result)!=0 :
      #              w = tuple_zip(result)
      #              self.ennemy =heroes_list[i],w
      #      self.fight = Fight_manager(self.ennemy,Data)
      #  else :
      #      print ("Fail de la fonction early game")

        #Fonction qui permet de savoir  qui commence à jouer

        print ("Bot whoes turn it is ...")
        template = cv2.imread('src/ingame/my_turn.PNG',0)
        result=findone(template)
        if tuple_test(result)!=0 :
            print ("its my_turn.png")
            self.bot_turn = 1 #passe notre tour
            return clickone(result)
        else :
            template = cv2.imread('src/ingame/green_end.PNG',0)
            result=findone(template)
            if tuple_test(result)!=0 :
                print ("its green_end.png")
                self.bot_turn = 1 #tour du bot
                return clickone(result)
            else :
                template = cv2.imread('src/ingame/enemy_turn.PNG',0)
                result=findone(template)
                if tuple_test(result)!=0 :
                    self.bot_turn = 0 #passe notre tour
                    print ("its enemy_turn.png")
                    self.bot_turn = 0
                    return clickone(result)
                else :
                    print ("FACK, idk")

    #Fonction elementaire qui permet le choix des cartes au debut de la partie
   # def pick_cards(self):
   #     pick = []
   #     print("\nBot try to identify your hand ...")
   #     tps1 = time.process_time()
   #     interest= Data.search_database({u'indeck' : 1})# liste de dictionnaire des cartes interessantes
   #     result =card_identification(interest,0,u'pic_pick',0,1)
   #     if result != [] :
   #         for entity in result :
   #             pick.append(entity) # ajout de la carte
   #     for t in pick : #click
   #         pass
   #     found = []
   #     for entity in pick :
   #         found.append(Data.search_database({u'name' : entity[0]}))                        commenting out as seems broken implement later 4/15/2020
   #     to_throw = []
   #     for entity in found :
   #         if u'cost' in entity[0].keys() :
   #             if entity[0][u'cost'] <= self.throwThresh :
   #                 pass
   #             else : # on throw la carte
   #                 for u in pick :
   #                     if entity[0][u'name'] == u[0] :
   #                         print ("THROW",u[0])
   #                         for pos in u[1] : #liste de positions
   #                             click_one(pos)
   #     tps2 = time.process_time()
   #     print ("Temps de choix de cartes") , tps2 - tps1
   #     return 1

    def wait_turn(self) : # durée d'un tour 70 s
        print ("Bot wait my turn")
        time.sleep(5)
        sec = 0
        template = cv2.imread('src/ingame/enemy_turn.PNG',0)
        result=findone(template)
        print(result)
        while (tuple_test(result)!=0):
            if(sec > 70) :
                print ("FAIL",sec)
                break
                return 0
            img_template = cv2.imread('src/ingame/enemy_turn.PNG',0)
            result=findone(img_template)
            time.sleep(0.5) #on attend 1 sec
            sec = sec + 0.5
        self.bot_turn = 1 #passe a notre tour
        self.turnNb = self.turnNb+1 #on incrémente le nombre de tour
        print("its the bots turn now")
        return 1

    def scan_hand(self) : #identifie le status de la game
        print ("Bot scan la main ...")
        tps1 = time.process_time()
        x=180
        y=620
        self.hand = [] #on recommence tout
        tps1 = time.process_time()
        while x < 600 :
            autopy.mouse.move(x,y)
            interest= Data.search_database({u'indeck' : 1})# liste de dictionnaire des cartes interessantes
            result =card_identification(interest,3,u'pic_hand',1,1)
            if result != [] :
                if self.hand == [] : #premier passage
                    for entity in result :
                        self.hand.append(entity) # ajout de la carte

                elif (self.hand[-1][0] == result[0][0]) and (abs(self.hand[-1][1][0][0]-x)> 50) : #Detection de doublons
                    pass
                else :
                    for entity in result :
                        self.hand.append(entity) # ajout de la carte
            x=x+50
        tps2 = time.process_time()
        print ("Time", tps2-tps1)

        #self.fight.update_hand(self.hand)# card_list = [[name,[pos]],[...],...]
        print (self.hand)
        return 0


    #def scan_board(self):
    #    print ("Scan board ...")
    #    tps1 = time.process_time()
    #    monster=([],[])
    #    self.board = []
    #    self.board_ennemy=[]
    #    self.board_priority = []
#
    #    #######################SCAN DES MONSTRES DU BOARD######################
    #    print ("Bot scan ses cartes sur le board ...")
    #    img_template = cv2.imread('src/circle_colored.png')
    #    img_template  = cv2.Canny(img_template , 50, 200)
    #    w, h = img_template.shape[:2]#offset du template
    #    monster=findone_cannyfilter(img_template,0,5800000)#initially 60000000 but detection failed
    #    if tuple_test(monster)!=0 :
    #        cpt = 0
    #        thresh = 50
    #        doublon = []
    #        for pt in zip(*monster[::-1]):
    #            doublon.append((pt[0]+w/2,pt[1]+h/2)) # creation d'un liste de tuples
    #        pos = doublon_manager(doublon)
    #        print (pos)
#
    #        for m in pos :
    #            if m[1] < 405 :
    #                self.board_ennemy.append(m)
    #            else :
    #                self.board.append(m)
    #    print ("board ennemy",self.board_ennemy)
    #    print ("board",self.board)
    #    time.sleep(2)
        ############### SCAN DE SON COTE DE TERRAIN #####################
       # """
       # print ("Bot identifie les cartes sur son board ..."
       # for i in self.board :
       #     autopy.mouse.move(i[0],i[1])
       #     for t in self.db_deck:#deck
       #         if t[u'type'] == "minion" :
       #             changed = cv2.resize(t[u'img'],(0,0), fx=self.k_board, fy=self.k_board)#changement d'echelle
       #             result=findone(changed,4,0.75)
       #             if tuple_test(result)!=0 :
       #                 print t[u'name']
       #                 break
#
       # ####################### SCAN ENNEMI ############################
       # print ("Bot identifie ses cartes sur le board ennemi ..."
       # for i in self.board_ennemy :
       #     autopy.mouse.move(i[0],i[1])
       #     for t in self.db_all:#parcourt du deck
       #         if t[u'type'] == "minion" :
       #             if t[u'hero'] == self.ennemy or t[u'hero'] == "neutral":
       #                 changed = cv2.resize(t[u'img'],(0,0), fx=k, fy=k)#changement d'echelle
       #                 result=findone(changed,4,0.7)
       #                 if tuple_test(result)!=0 :
       #                     #self.hand.append((t[u'name'],t[u'id'],x,790,t[u'mana']))
       #                     print t[u'name']
       #                     #self.board_ennemy.append(self.ennemy[1])
       #                     #attack(i,self.board_ennemy[0])
       #                     break
       #                     """
        tps2 = time.process_time()
        print("temps ",tps2 - tps1)




    #def engage_cards(self):
        

    def play_turn(self) : #fonction essentielle qui per,et la gestion d'événenemts un tour
        time.sleep(3) #temps de piocher
        self.scan_hand()
       # self.fight.scan_board()
        #self.engage_cards()

#if __name__ == '__main__':
    #bot = Game_manager()
    
    #print (Data.db_all[200].keys())
    #if bot.start() == 1 :
   # 	bot.earlygame()#appeler une fois pour initialiser la game
    #while 1:
    #    if bot.bot_turn == 1 :
    #        bot.play_turn()
    #        bot.end_turn()
    #    else :
    #        bot.wait_turn()
def end_turn() :
    print ("Bot ending the turn")
    whnd = FindWindowEx(None, None, None, 'Hearthstone')
    print(GetWindowRect(whnd))
    winX = GetWindowRect(whnd)
    rect = ((max(1, winX[0]),winX[1]),(winX[2], winX[3])) #co-ordinates of Hearthstone window
    time.sleep(1)
    template = cv2.imread('src/ingame/my_turn.png',0)
    result=findone(template, 0, .71, rect)
    if result is not None:
        click_one(result)

    else:
        template = cv2.imread('src/ingame/green_end.png',0)
        result=findone(template, 0, .71, rect)
        return click_one(result)    


def clickSoloAdventure() :
    whnd = FindWindowEx(None, None, None, 'Hearthstone')
    print(GetWindowRect(whnd))
    winX = GetWindowRect(whnd)
    rect = ((max(1, winX[0]),winX[1]),(winX[2], winX[3])) #co-ordinates of Hearthstone window
    print(rect)

    template = cv2.imread('src/solo_adventures.png',0)
    result=findone(template, 0, .71, rect)
    print("result:")
    print(result)
    click_one(result)



while 1:
    turn = whoseTurnIsIt()
    if turn == 1 :
        print("its my turn")
        useStaticHeroPower()
        playCard(500,750)
        playCard(460,750)
        playCard(420,750)
        attackHeroWithMinion(540, 465)
        attackHeroWithMinion(470, 465)
        attackMinionOneWithMinion(540, 465)
        attackMinionTwoWithMinion(380, 360)
        end_turn()

    if turn == 0 :
        print("its the enemy's turn")    
    time.sleep(2) 

