import Gothic_Flask.Engine
import Gothic_Flask.Map
import Gothic_Flask.Items
import Gothic_Flask.Characters
from random import randint

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('game', __name__, url_prefix='/game')

#area = Gothic_Flask.Map.Map('intro')
#Gothic = Gothic_Flask.Engine.Engine(area)
#Gothic.play()

#Intro Area
@bp.route('/intro')
def intro():
    return render_template('Intro.html', area=intro)

#Death Screen
@bp.route('/death')
def death():
    Gothic_Flask.Characters.player.health = 100
    Gothic_Flask.Characters.player.gold = 0
    Gothic_Flask.Items.copper_shield.inInventory = False
    Gothic_Flask.Items.copper_shield.durability = 50
    Gothic_Flask.Items.silver_shield.inInventory = False
    Gothic_Flask.Items.silver_shield.durability = 100
    Gothic_Flask.Items.small_sword.inInventory = False
    Gothic_Flask.Items.club.inInventory = False
    Gothic_Flask.Items.war_hammer.inInventory = False
    Gothic_Flask.Items.life_bottle.amount = 0
    Gothic_Flask.Items.energy_vile.amount = 0
    Gothic_Flask.Items.crypt_key.inInventory = False
    Gothic_Flask.Items.graveyard_key.inInventory = False
    Gothic_Flask.Items.skull_key.inInventory = False
    return render_template('Game.html', area=death)

#Inventory Screen
@bp.route('/Inventory')
def inventory():
    health = Gothic_Flask.Characters.player.health
    gold = Gothic_Flask.Characters.player.gold
    copper_shield_durability = Gothic_Flask.Items.copper_shield.durability
    if Gothic_Flask.Items.copper_shield.inInventory:
        copper_shield = True
    else:
        copper_shield = False
    silver_shield_durability = Gothic_Flask.Items.silver_shield.durability
    if Gothic_Flask.Items.silver_shield.inInventory:
        silver_shield = True
    else:
        silver_shield = False
    if Gothic_Flask.Items.small_sword.inInventory:
        small_sword = True
    else:
        small_sword = False
    if Gothic_Flask.Items.club.inInventory:
        club = True
    else:
        club = False
    if Gothic_Flask.Items.war_hammer.inInventory:
        war_hammer = True
    else:
        war_hammer = False
    if Gothic_Flask.Items.crypt_key.inInventory:
        crypt_key = True
    else:
        crypt_key = False
    if Gothic_Flask.Items.graveyard_key.inInventory:
        graveyard_key = True
    else:
        graveyard_key = False
    if Gothic_Flask.Items.skull_key.inInventory:
        skull_key = True
    else:
        skull_key = False
    if Gothic_Flask.Items.life_bottle.amount > 0:
        life_bottle_amount = Gothic_Flask.Items.life_bottle.amount
    else:
        life_bottle_amount = 0
    if Gothic_Flask.Items.energy_vile.amount > 0:
        energy_vile_amount = Gothic_Flask.Items.energy_vile.amount
    else:
        energy_vile_amount = 0
    return render_template('Inventory.html', area=inventory, health=health, gold=gold, copper_shield=copper_shield, silver_shield=silver_shield, small_sword=small_sword, club=club, war_hammer=war_hammer, crypt_key=crypt_key, graveyard_key=graveyard_key, skull_key=skull_key, life_bottle_amount=life_bottle_amount, energy_vile_amount=energy_vile_amount)

#Main Crypt Area
@bp.route('/main_crypt')
def main_crypt():
    if Gothic_Flask.Items.copper_shield.inInventory:
        copper_shield = True
    else:
        copper_shield = False
    message = "What will you do?"
    return render_template('Main_Crypt.html', area=main_crypt, copper_shield=copper_shield, message=message)

#Taking copper shield action
@bp.route('/main_crypt/take_copper_shield')
def main_crypt_take_copper_shield():
    Gothic_Flask.Items.copper_shield.inInventory = True
    if Gothic_Flask.Items.copper_shield.inInventory:
        copper_shield = True
    else:
        copper_shield = False
    message = "You took the copper shield"
    return render_template('Main_Crypt.html', area=main_crypt, copper_shield=copper_shield, message=message)

#Statue Crypt Area
@bp.route('/statue_crypt')
def statue_crypt():
    if Gothic_Flask.Items.small_sword.inInventory:
        small_sword = True
    else:
        small_sword = False
    message = "What will you do?"
    return render_template('Statue_Crypt.html', area=statue_crypt, small_sword=small_sword, message=message)

#Taking small sword action
@bp.route('/statue_crypt/take_small_sword')
def statue_crypt_take_small_sword():
    Gothic_Flask.Items.small_sword.inInventory = True
    if Gothic_Flask.Items.small_sword.inInventory:
        small_sword = True
    else:
        small_sword = False
    message = "You took the small sword"
    return render_template('Statue_Crypt.html', area=statue_crypt, small_sword=small_sword, message=message)

#Desecrating the statue action
@bp.route('/statue_crypt/desecrate_the_statue')
def statue_crypt_desecrate_the_statue():
    if Gothic_Flask.Items.small_sword.inInventory:
        small_sword = True
    else:
        small_sword = False
    chance = randint(1,3)
    if chance == 1:
        message = """Your attempt at destorying the statue was to no avail,
        but while trying, a piece of the statue fell off
        and hit you smack in the skull, causing it to
        explode into tiny pieces."""
        return render_template('Death.html', area=death, message=message)
    elif chance == 2:
        message = "Your attempt at destorying the statue was to no avail."
    else:
        message = """Your attempt at destorying the statue was to no avail,
        but while trying, you find a Life Bottle wedged
        in the statue. You then take it for yourself."""
        Gothic_Flask.Items.life_bottle.amount += 1
    return render_template('Statue_Crypt.html', area=statue_crypt, small_sword=small_sword, message=message)

#Waterway Crypt Area
@bp.route('/waterway_crypt')
def waterway_crypt():
    if Gothic_Flask.Items.crypt_key.inInventory:
        crypt_key = True
    else:
        crypt_key = False
    message = "What will you do?"
    return render_template('Waterway_Crypt.html', area=waterway_crypt, crypt_key=crypt_key, message=message)

#Taking crypt key action
@bp.route('/waterway_crypt/take_crypt_key')
def waterway_crypt_take_crypt_key():
    Gothic_Flask.Items.crypt_key.inInventory = True
    if Gothic_Flask.Items.crypt_key.inInventory:
        crypt_key = True
    else:
        crypt_key = False
    message = "You take the crypt key"
    return render_template('Waterway_Crypt.html', area=waterway_crypt, crypt_key=crypt_key, message=message)

#Going for a swim action
@bp.route('/waterway_crypt/swim')
def waterway_crypt_swim():
    message = """You jump right into the water. But have you forgotten?
    You are only just a skeleton and bouyancy is a problem
    for the undead. You then proceed to drown."""
    return render_template('Death.html', area=waterway_crypt, message=message)

#Looking in the water action
@bp.route('/waterway_crypt/look')
def waterway_crypt_look():
    Gothic_Flask.Items.crypt_key.inInventory = True
    if Gothic_Flask.Items.crypt_key.inInventory:
        crypt_key = True
    else:
        crypt_key = False
    chance = randint(1,3)
    if chance == 1:
        message = """While trying to fish something out of the water,
        something grabs your boney hand and drags you in.
        You then proceed to drown."""
        return render_template('Death.html', area=death, message=message)
    elif chance == 2:
        message = "You find nothing."
    else:
        message = """You manage to fish something out of the water. It
        is an energy vile."""
        Gothic_Flask.Items.energy_vile.amount += 1
    return render_template('Waterway_Crypt.html', area=waterway_crypt, crypt_key=crypt_key, message=message)

#Gate Crypt Area
@bp.route('/gate_crypt')
def gate_crypt():
    if Gothic_Flask.Items.crypt_key.inInventory:
        crypt_key = True
    else:
        crypt_key = False
    message = "What will you do?"
    return render_template('Gate_Crypt.html', area=gate_crypt, crypt_key=crypt_key, message=message)

#Trying the lock action
@bp.route('/gate_crypt/try_the_lock')
def gate_crypt_try():
    if Gothic_Flask.Items.crypt_key.inInventory:
        crypt_key = True
    else:
        crypt_key = False
    message = "You try to fiddle with the lock to no avail."
    return render_template('Gate_Crypt.html', area=gate_crypt, crypt_key=crypt_key, message=message)

#Using your head action
@bp.route('/gate_crypt/use_your_head')
def gate_crypt_use():
    message = """You bang your skull on the lock to no avail.
    fustrated and determined you continuosly bang
    your skull on the lock. After banging too many
    times your skull has exploded into a million
    tiny pieces."""
    return render_template('death.html', area=death, message=message)

#Crypt Graveyard Area
@bp.route('/crypt_graveyard')
def crypt_graveyard():
    message = "What will you do?"
    return render_template('Crypt_Graveyard.html', area=crypt_graveyard, message=message)

#Unknown Area
@bp.route('/<area>')
def area(area=None):
    return render_template('Wrong.html', area=area)
