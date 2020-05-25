#!/usr/bin/env python2.7
#-*-coding:Latin-1 -*

import time
import numpy as np
import os
from pprint import pprint
import json
from threading import *
from low_lvl import *
from gauge import *
from PIL import Image
import urllib
import cv2

#Classe de gestion des combats
#Fonctionne avec la classe cards
#All the strategy should be here
#class Fight_manager :
#    def ___init__():
        

#########Card Rejecting###########

        ###FirstTurnStart###
      

    #def __init__(self,opponent,database):#construct
    #    self.cardsOnBoard = [] # list of cards class object
    #    self.oldcardsOnBoard = [] # list of cards class object
    #    self.nopponent=opponent[0]#class of opponent
    #    self.popponent=opponent[1][0]#position of opponent -> depacking tuple Oo
    #    print ("Bot fight against",self.nopponent,self.popponent)
    #    self.cardsInHand = []#update in
    #    self.redList = []#opponent minion to attack
    #    self.blackList = []#opponent minion to ignore
    #    self.data = database

def turn(self): #gere les actions d'un tour
    return 0
##########SCAN###########################################
def scan_board(self):
    print ("Bot scan the board")
    tps1 = time.process_time()
    found = []
    interest= self.data.search_database({u'type' : u'Minion',u'pic_mboard': 0})
    #interest= self.data.search_database({u'indeck' : 1})# liste de dictionnaire des cartes interessantes

    result =card_identification(interest,4,u'pic_mboard',6,4)
    if result != [] :
        for entity in result :
            found.append(entity) # ajout de la carte
    tps2 = time.process_time()
    print (found)
    print ("time",tps2-tps1)

##########UPDATE############################################
def update_board(self): #check cards object on the board
    return 0

def update_hand(card_list): # card_list = [[name,[pos]],[...],...]
    for u in card_list :
        print (u[0])
    return 0

def update_mana(self): # number of mana
    return 0
##########STRATEGY###########################################
def highStrategy(self):
    return 0

def lowStragegy(self):
    return 0
##########LOW_LVL_FUNCTION##################################
def attack(self,friendminion,opponentminion):
    return 0

def target_opponent(self,opponentcard):
    return 0

turnButtonX = 930
turnButtonY = 390 
startButtonX = 0
startButtonY = 0
confirmButtonX = 0
confirmButtonY = 0
heroPowerButtonX = 630
heroPowerButtonY = 630 
##for mulliganing
cardOneX = 165
cardOneY = 245
cardTwoX = 360
cardTwoY = 245
cardThreeX = 555
cardThreeY = 245     

enemyHeroX = 510
enemyHeroY = 180

enemyMinionX = 545
enemyMinionY = 330

enemyMinionXX = 470
enemyMinionYY = 330


def useStaticHeroPower() :  #for hunter, warrior etc where there is nothing to do afterwards
    autopy.mouse.smooth_move(heroPowerButtonX, heroPowerButtonY)
    time.sleep(1)   
    autopy.mouse.click()

def endTurn() :
    autopy.mouse.smooth_move(turnButtonX, turnButtonY)
    time.sleep(1)   
    autopy.mouse.click(RIGHT_BUTTON)    
    autopy.mouse.click()

def playCard(x, y):
    autopy.mouse.move(x,y)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)
    autopy.mouse.move(500,300)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)      

def attackHeroWithMinion(x, y):
    autopy.mouse.move(x,y)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)
    autopy.mouse.move(enemyHeroX,enemyHeroY)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)     

def attackMinionOneWithMinion(x, y):
    autopy.mouse.move(x,y)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)
    autopy.mouse.move(enemyMinionX,enemyMinionY)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)   

def attackMinionTwoWithMinion(x, y):
    autopy.mouse.move(x,y)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)
    autopy.mouse.move(enemyMinionXX,enemyMinionYY)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)         

         


