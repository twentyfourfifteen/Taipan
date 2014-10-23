#!/usr/bin/python -tt
import sys
import math
import random

wares = ['gold','silk','arms','general']
boat = {'gold':0,'silk':0,'arms':0,'general':0,'money':100,'capacity':10,'city':'Hong Kong'}
original_prices = {'gold':800,'silk':200,'arms':50,'general':10}
prices = {'gold':1,'silk':1,'arms':1,'general':1}
actions = ['buy','sell','inventory','run']
cities = ['Hong Kong','Shanghai','Nagasaki','Saigon','Manila','Singapore','Batavia']
turn = 0
player_name = ''

def main():
    global player_name
    if player_name == '':
        player_name = raw_input("What is your name sailor. ")
    print "\n***** Welcome to Hong Kong! *****"
    current_prices('Hong Kong')
    play()

def play():
    global boat
    working = True
    while working:
        print "\nYou have $%s" % (boat['money'])

        for i in wares:
            print "$%s for %s" % (prices[i],proper_name(i))

        toDo = raw_input('What do you want to do? ')
        action = toDo.partition(' ')[0]
        action_item = toDo.partition(' ')[2]

        if action == 'help':
            print "You can:"
            for i in actions:
              print i
        elif action == 'buy':
            buy(action_item)
        elif action == 'sell':
            sell(action_item)
        elif action == 'inventory':
            print "\n---- %s's Master Inventory ----" % (player_name)
            for i in wares:
                print "You have %s of %s." % (boat[i],i)
            print "You have %s dollars on hand." % (boat['money'])
        elif action == 'market':
            for i in wares:
                print "$%s for %s" % (prices[i],proper_name(i))
        elif action == 'sail':
            print 'Ah, the open sea!'
            sail()
        elif action == 'quit' or action =='q':
            print "I knew you weren't fit for sailing %s!\n" % (player_name)
            working = False
        else:
            print "It is not lawful to do that here:"
            print "If you don't know ask for help"


def buy(action_item):
    if action_item.lower() in wares:
        item = action_item
    else:
        item = raw_input('What do you want to buy? ')
        item = item.lower()
    if boat["money"] == 0:
        print 'You have no money!'
        return
    elif item in wares and boat["money"] < prices[item]:
        print "You are too poor!"
        return
    elif item in wares:
        print "\nYou have $%s, %s is $%s per unit" % (boat["money"],item,prices[item])
        max_volume = int(math.floor(boat["money"] / prices[item]))
        print "You have money to buy up to %s %s" % (max_volume,item)
        print "Your ship can hold %s more units." % (boat['capacity']-boat_fill())
        count = get_user_number('buy')
        transaction("buy", item, count)
        return
    elif item == 'help':
        for i in wares:
            print i
        buy(action_item)
    elif item == 'nothing':
        return
    else:
        print "We have no %s" % (item)
        print "If you don't know ask for help"
        buy(action_item)

def sell(action_item):
    if action_item.lower() in wares:
        item = action_item
    else:
        item = raw_input('What do you want to sell? ')
        item = item.lower()
    if item not in wares:
        print "You have no %s" % (item)
        return
    elif boat[item] <= 0:
        print "You don't have any of those to sell"
        return
    elif item in wares:
        print "You have %s units of %s, it is worth $%s per unit" % (boat[item],item,prices[item])
        count = get_user_number('sell')
        if count > boat[item]:
            print "You don't have that many to sell, you only have %s units of %s." % (boat[item], item)
            sell(item)
        else:
            boat[item] -= count
            transaction("sell", item, count)
            return
    elif item == 'help':
        for i in wares:
            print "You have %s units of %s" % (boat[i], i)
        sell()
    elif item == 'nothing':
        return
    else:
        print "If you don't know ask for help"
        sell()

def transaction(direction,item,volume):
    cost = int(prices[item]) * int(volume)
    global turn
    global boat
    if direction == "buy":
        if cost > boat["money"]:
            print "You don't have that much money."
        elif volume == 0:
            print "Buy low, sell high!"
        elif volume > boat['capacity']-boat_fill():
            volume = boat['capacity']-boat_fill()
            print "You only have capacity for more %s units." % (volume)
        else:
            boat[item] += volume
            boat["money"] -= cost
            print "\nSUCCESS"
            print "That costs you %s dollars." % (cost)
            print "We loaded %s units of %s for you." % (volume, item)
            print "You now have %s units of %s in storage and $%s left." % (boat[item], item, boat["money"])
    else:
        boat["money"] += cost
        print "\nSUCCESS"
        print "That earns you %s dollars." % (cost)
        print "We unloaded %s units of %s for you." % (volume, item)
        print "You now have %s units of %s in storage and $%s." % (boat[item], item, boat["money"])

def current_prices(city):
        global original_prices
        global prices
        for i in prices:
                prices[i] = original_prices[i] * random.randrange(1,6)

def proper_name(item):
    first = item[0].upper()
    output = first + item[1:len(item)]
    return output

def get_user_number(transaction):
    i = raw_input("How many do you want to %s.\n" % (transaction))
    #if i == 'all':
    #    return 'all'
    #else:
    try:
        return int(i)
    except:
        print("I didn't recognize {0} as a number".format(i))
        return get_user_number(transaction)

def boat_fill():
    fill = 0
    for i in wares:
        fill += boat[i]
    return fill

def sail():
    global prices
    global turn
    global cities
    global boat
    print " "
    for i in cities:
        print i
    sail_to = raw_input("Where do you want to go? ")
    if sail_to == boat['city']:
        print "You're already there, pick somewhere else"
    else:
        boat['city'] = sail_to
        turn +=1
        print "\n***** Welcome to %s, turn %s *****" % (sail_to,turn)
        current_prices(sail_to)
    # get robbed
    if 1 == random.randrange(1,2):
        print "You got robbed! Your ship was emptied while you were asleep."
        for i in wares:
            boat[i] = 0

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()