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
@bp.route('/intro', methods=('GET', 'POST'))
def intro():
    if not Gothic_Flask.Characters.player.name:
        Gothic_Flask.Characters.player.name = "Player"
    name = Gothic_Flask.Characters.player.name
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
    Gothic_Flask.Map.enterance_graveyard.looted = False
    Gothic_Flask.Map.graves_graveyard.looted = False
    if request.method == 'POST':
        Gothic_Flask.Characters.player.name = request.form['name']
        if not name:
            Gothic_Flask.Characters.player.name = "Player"
        return redirect(url_for('game.intro'))
    return render_template('Intro.html', area=intro, name=name)

#Death Screen
@bp.route('/death')
def death():
    Gothic_Flask.Characters.player.name = "Player"
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
    Gothic_Flask.Map.enterance_graveyard.looted = False
    Gothic_Flask.Map.graves_graveyard.looted = False
    return render_template('Game.html', area=death)

#Inventory Screen
@bp.route('<return_area>/Inventory')
def inventory(return_area):
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
    name = Gothic_Flask.Characters.player.name
    return_link = f'game.{return_area}'
    return render_template('Inventory.html', area=inventory, return_area=return_area, return_link=return_link, health=health, gold=gold, copper_shield=copper_shield, copper_shield_durability=copper_shield_durability , silver_shield=silver_shield, silver_shield_durability=silver_shield_durability , small_sword=small_sword, club=club, war_hammer=war_hammer, crypt_key=crypt_key, graveyard_key=graveyard_key, skull_key=skull_key, life_bottle_amount=life_bottle_amount, energy_vile_amount=energy_vile_amount, name=name)

#Combat System
@bp.route('<return_area>/combat')
def combat(return_area):
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health
    enemy_attack = randint(1,2)
    if enemy_attack > 1 and Gothic_Flask.Map.combat.enemy_health > 0:
        if Gothic_Flask.Items.silver_shield.inInventory == True and Gothic_Flask.Items.silver_shield.durability > 0:
            Gothic_Flask.Items.silver_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Silver Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.silver_shield.durability < 0:
                Gothic_Flask.Items.silver_shield.durability = 0
        elif Gothic_Flask.Items.copper_shield.inInventory == True and Gothic_Flask.Items.copper_shield.durability > 0:
            Gothic_Flask.Items.copper_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Copper Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.copper_shield.durability < 0:
                Gothic_Flask.Items.copper_shield.durability = 0
        else:
            Gothic_Flask.Characters.player.health -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            You took {Gothic_Flask.Map.combat.enemy_attack} damage."""
    else:
        enemy_message = f"The {Gothic_Flask.Map.combat.enemy} misses."

    if Gothic_Flask.Characters.player.health <= 0:
        message = f"You have been slain by the {enemy}"
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=combat, message=message, name=name)

    message = "What will you do?"
    return_link = f'game.{return_area}'
    return render_template('Combat/Combat.html', area=combat, return_area=return_area, return_link=return_link, message=message, enemy_message=enemy_message, enemy=enemy, enemy_health=enemy_health, health=health)

#Attack Option
@bp.route('<return_area>/combat_attack')
def combat_attack(return_area):
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health

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

    message = "Attack with what?"
    return render_template('Combat/Combat_Attack.html', area=combat, return_area=return_area, message=message, enemy=enemy, enemy_health=enemy_health, health=health, small_sword=small_sword, club=club, war_hammer=war_hammer)

#Using Arm as weapon
@bp.route('<return_area>/combat_attack_arm')
def combat_attack_arm(return_area):
    Gothic_Flask.Map.combat.enemy_health -= 5
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health
    enemy_attack = randint(1,2)
    if enemy_attack > 1 and Gothic_Flask.Map.combat.enemy_health > 0:
        if Gothic_Flask.Items.silver_shield.inInventory == True and Gothic_Flask.Items.silver_shield.durability > 0:
            Gothic_Flask.Items.silver_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Silver Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.silver_shield.durability < 0:
                Gothic_Flask.Items.silver_shield.durability = 0
        elif Gothic_Flask.Items.copper_shield.inInventory == True and Gothic_Flask.Items.copper_shield.durability > 0:
            Gothic_Flask.Items.copper_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Copper Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.copper_shield.durability < 0:
                Gothic_Flask.Items.copper_shield.durability = 0
        else:
            Gothic_Flask.Characters.player.health -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            You took {Gothic_Flask.Map.combat.enemy_attack} damage."""
    else:
        enemy_message = f"The {Gothic_Flask.Map.combat.enemy} misses."

    if Gothic_Flask.Characters.player.health <= 0:
        message = f"You have been slain by the {enemy}"
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=combat, message=message, name=name)

    message = "You ripped of your own arm and smacked the enemy which dealt 5 damage"
    return_link = f'game.{return_area}'
    return render_template('Combat/Combat.html', area=combat, return_area=return_area, return_link=return_link, message=message, enemy_message=enemy_message, enemy=enemy, enemy_health=enemy_health, health=health)

#Using Small Sword as weapon
@bp.route('<return_area>/combat_attack_small_sword')
def combat_attack_small_sword(return_area):
    Gothic_Flask.Map.combat.enemy_health -= 10
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health
    enemy_attack = randint(1,2)
    if enemy_attack > 1 and Gothic_Flask.Map.combat.enemy_health > 0:
        if Gothic_Flask.Items.silver_shield.inInventory == True and Gothic_Flask.Items.silver_shield.durability > 0:
            Gothic_Flask.Items.silver_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Silver Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.silver_shield.durability < 0:
                Gothic_Flask.Items.silver_shield.durability = 0
        elif Gothic_Flask.Items.copper_shield.inInventory == True and Gothic_Flask.Items.copper_shield.durability > 0:
            Gothic_Flask.Items.copper_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Copper Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.copper_shield.durability < 0:
                Gothic_Flask.Items.copper_shield.durability = 0
        else:
            Gothic_Flask.Characters.player.health -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            You took {Gothic_Flask.Map.combat.enemy_attack} damage."""
    else:
        enemy_message = f"The {Gothic_Flask.Map.combat.enemy} misses."

    if Gothic_Flask.Characters.player.health <= 0:
        message = f"You have been slain by the {enemy}"
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=combat, message=message, name=name)

    message = "You attacked with your small sword and dealt 10 damage"
    return_link = f'game.{return_area}'
    return render_template('Combat/Combat.html', area=combat, return_area=return_area, return_link=return_link, message=message, enemy_message=enemy_message, enemy=enemy, enemy_health=enemy_health, health=health)

#Using Club as weapon
@bp.route('<return_area>/combat_attack_club')
def combat_attack_club(return_area):
    Gothic_Flask.Map.combat.enemy_health -= 15
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health
    enemy_attack = randint(1,2)
    if enemy_attack > 1 and Gothic_Flask.Map.combat.enemy_health > 0:
        if Gothic_Flask.Items.silver_shield.inInventory == True and Gothic_Flask.Items.silver_shield.durability > 0:
            Gothic_Flask.Items.silver_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Silver Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.silver_shield.durability < 0:
                Gothic_Flask.Items.silver_shield.durability = 0
        elif Gothic_Flask.Items.copper_shield.inInventory == True and Gothic_Flask.Items.copper_shield.durability > 0:
            Gothic_Flask.Items.copper_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message: f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Copper Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.copper_shield.durability < 0:
                Gothic_Flask.Items.copper_shield.durability = 0
        else:
            Gothic_Flask.Characters.player.health -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            You took {Gothic_Flask.Map.combat.enemy_attack} damage."""
    else:
        enemy_message = f"The {Gothic_Flask.Map.combat.enemy} misses."

    if Gothic_Flask.Characters.player.health <= 0:
        message = f"You have been slain by the {enemy}"
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=combat, message=message, name=name)

    message = "You attacked with your club and dealt 15 damage"
    return_link = f'game.{return_area}'
    return render_template('Combat/Combat.html', area=combat, return_area=return_area, return_link=return_link, message=message, enemy_message=enemy_message, enemy=enemy, enemy_health=enemy_health, health=health)

#Using War Hammer as weapon
@bp.route('<return_area>/combat_attack_war_hammer')
def combat_attack_war_hammer(return_area):
    Gothic_Flask.Map.combat.enemy_health -= 20
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health
    enemy_attack = randint(1,2)
    if enemy_attack > 1 and Gothic_Flask.Map.combat.enemy_health > 0:
        if Gothic_Flask.Items.silver_shield.inInventory == True and Gothic_Flask.Items.silver_shield.durability > 0:
            Gothic_Flask.Items.silver_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Silver Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.silver_shield.durability < 0:
                Gothic_Flask.Items.silver_shield.durability = 0
        elif Gothic_Flask.Items.copper_shield.inInventory == True and Gothic_Flask.Items.copper_shield.durability > 0:
            Gothic_Flask.Items.copper_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Copper Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.copper_shield.durability < 0:
                Gothic_Flask.Items.copper_shield.durability = 0
        else:
            Gothic_Flask.Characters.player.health -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            You took {Gothic_Flask.Map.combat.enemy_attack} damage."""
    else:
        enemy_message = f"The {Gothic_Flask.Map.combat.enemy} misses."

    if Gothic_Flask.Characters.player.health <= 0:
        message = f"You have been slain by the {enemy}"
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=combat, message=message, name=name)

    message = "You attacked with your war hammer and dealt 20 damage"
    return_link = f'game.{return_area}'
    return render_template('Combat/Combat.html', area=combat, return_area=return_area, return_link=return_link, message=message, enemy_message=enemy_message, enemy=enemy, enemy_health=enemy_health, health=health)

#Use Item Option
@bp.route('<return_area>/combat_use_item')
def combat_use_item(return_area):
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health

    if Gothic_Flask.Items.life_bottle.amount > 0:
        life_bottle_amount = Gothic_Flask.Items.life_bottle.amount
    else:
        life_bottle_amount = 0
    if Gothic_Flask.Items.energy_vile.amount > 0:
        energy_vile_amount = Gothic_Flask.Items.energy_vile.amount
    else:
        energy_vile_amount = 0

    message = "Use what?"
    return render_template('Combat/Combat_Use_Item.html', area=combat, return_area=return_area, message=message, enemy=enemy, enemy_health=enemy_health, health=health, life_bottle_amount=life_bottle_amount, energy_vile_amount=energy_vile_amount)

#Using Life Bottle as item
@bp.route('<return_area>/combat_use_item_life_bottle')
def combat_use_item_life_bottle(return_area):
    Gothic_Flask.Characters.player.health += 100
    if Gothic_Flask.Characters.player.health > 100:
        Gothic_Flask.Characters.player.health = 100
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health
    enemy_attack = randint(1,2)
    if enemy_attack > 1 and Gothic_Flask.Map.combat.enemy_health > 0:
        if Gothic_Flask.Items.silver_shield.inInventory == True and Gothic_Flask.Items.silver_shield.durability > 0:
            Gothic_Flask.Items.silver_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Silver Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.silver_shield.durability < 0:
                Gothic_Flask.Items.silver_shield.durability = 0
        elif Gothic_Flask.Items.copper_shield.inInventory == True and Gothic_Flask.Items.copper_shield.durability > 0:
            Gothic_Flask.Items.copper_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Copper Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.copper_shield.durability < 0:
                Gothic_Flask.Items.copper_shield.durability = 0
        else:
            Gothic_Flask.Characters.player.health -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            You took {Gothic_Flask.Map.combat.enemy_attack} damage."""
    else:
        enemy_message = f"The {Gothic_Flask.Map.combat.enemy} misses."

    if Gothic_Flask.Characters.player.health <= 0:
        message = f"You have been slain by the {enemy}"
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=combat, message=message, name=name)

    message = "You used a Life Bottle"
    return_link = f'game.{return_area}'
    return render_template('Combat/Combat.html', area=combat, return_area=return_area, return_link=return_link, message=message, enemy_message=enemy_message, enemy=enemy, enemy_health=enemy_health, health=health)

#Using Energy Vile as item
@bp.route('<return_area>/combat_use_item_energy_vile')
def combat_use_item_energy_vile(return_area):
    Gothic_Flask.Characters.player.health += 50
    if Gothic_Flask.Characters.player.health > 100:
        Gothic_Flask.Characters.player.health = 100
    enemy = Gothic_Flask.Map.combat.enemy
    enemy_health = Gothic_Flask.Map.combat.enemy_health
    enemy_attack = Gothic_Flask.Map.combat.enemy_attack
    health = Gothic_Flask.Characters.player.health
    enemy_attack = randint(1,2)
    if enemy_attack > 1 and Gothic_Flask.Map.combat.enemy_health > 0:
        if Gothic_Flask.Items.silver_shield.inInventory == True and Gothic_Flask.Items.silver_shield.durability > 0:
            Gothic_Flask.Items.silver_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Silver Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.silver_shield.durability < 0:
                Gothic_Flask.Items.silver_shield.durability = 0
        elif Gothic_Flask.Items.copper_shield.inInventory == True and Gothic_Flask.Items.copper_shield.durability > 0:
            Gothic_Flask.Items.copper_shield.durability -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            Your Copper Shield took {Gothic_Flask.Map.combat.enemy_attack} damage."""
            if Gothic_Flask.Items.copper_shield.durability < 0:
                Gothic_Flask.Items.copper_shield.durability = 0
        else:
            Gothic_Flask.Characters.player.health -= Gothic_Flask.Map.combat.enemy_attack
            enemy_message = f"""The {Gothic_Flask.Map.combat.enemy} hits.
            You took {Gothic_Flask.Map.combat.enemy_attack} damage."""
    else:
        enemy_message = f"The {Gothic_Flask.Map.combat.enemy} misses."

    if Gothic_Flask.Characters.player.health <= 0:
        message = f"You have been slain by the {enemy}"
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=combat, message=message, name=name)

    message = "You used an Energy Vile"
    return_link = f'game.{return_area}'
    return render_template('Combat/Combat.html', area=combat, return_area=return_area, return_link=return_link, message=message, enemy_message=enemy_message, enemy=enemy, enemy_health=enemy_health, health=health)

#Gargoyle Shop
@bp.route('<return_area>/gargoyle_shop')
def gargoyle_shop(return_area):
    gold = Gothic_Flask.Characters.player.gold
    message = "What will you do?"
    return_link = f'game.{return_area}'
    return render_template('Gargoyle/Gargoyle_Shop.html', area=gargoyle_shop, return_area=return_area, return_link=return_link, message=message, gold=gold)

#Gargoyle Shop Health
@bp.route('<return_area>/gargoyle_shop/health')
def gargoyle_shop_health(return_area):
    gold = Gothic_Flask.Characters.player.gold
    message = "What will you do?"
    return render_template('Gargoyle/Gargoyle_Shop_Health.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold)

#Buy Life Bottle action
@bp.route('<return_area>/gargoyle_shop/health_buy_life_bottle')
def gargoyle_shop_health_life(return_area):
    Gothic_Flask.Characters.player.gold -= 100
    Gothic_Flask.Items.life_bottle.amount += 1
    gold = Gothic_Flask.Characters.player.gold
    message = "You bought a Life Bottle"
    return render_template('Gargoyle/Gargoyle_Shop_Health.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold)

#Buy Energy Vile action
@bp.route('<return_area>/gargoyle_shop/health_buy_energy_vile')
def gargoyle_shop_health_energy(return_area):
    Gothic_Flask.Characters.player.gold -= 50
    Gothic_Flask.Items.energy_vile.amount += 1
    gold = Gothic_Flask.Characters.player.gold
    message = "You bought an Energy Vile"
    return render_template('Gargoyle/Gargoyle_Shop_Health.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold)

#Gargoyle Shop Shields
@bp.route('<return_area>/gargoyle_shop/shields')
def gargoyle_shop_shields(return_area):
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
    message = "What will you do?"
    return render_template('Gargoyle/Gargoyle_Shop_Shields.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold, copper_shield=copper_shield, copper_shield_durability=copper_shield_durability, silver_shield=silver_shield, silver_shield_durability=silver_shield_durability)

#Buy Copper Shield Action
@bp.route('<return_area>/gargoyle_shop/shields_buy_copper_shield')
def gargoyle_shop_shields_copper(return_area):
    Gothic_Flask.Characters.player.gold -= 25
    Gothic_Flask.Items.copper_shield.inInventory = True
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
    message = "You bought the copper shield"
    return render_template('Gargoyle/Gargoyle_Shop_Shields.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold, copper_shield=copper_shield, copper_shield_durability=copper_shield_durability, silver_shield=silver_shield, silver_shield_durability=silver_shield_durability)

#Buy Silver Shield Action
@bp.route('<return_area>/gargoyle_shop/shields_buy_silver_shield')
def gargoyle_shop_shields_silver(return_area):
    Gothic_Flask.Characters.player.gold -= 50
    Gothic_Flask.Items.silver_shield.inInventory = True
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
    message = "You bought the silver shield"
    return render_template('Gargoyle/Gargoyle_Shop_Shields.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold, copper_shield=copper_shield, copper_shield_durability=copper_shield_durability, silver_shield=silver_shield, silver_shield_durability=silver_shield_durability)

#Repair Copper Shield Action
@bp.route('<return_area>/gargoyle_shop/shields_repair_copper_shield')
def gargoyle_shop_shields_copper_repair(return_area):
    Gothic_Flask.Characters.player.gold -= 25
    Gothic_Flask.Items.copper_shield.durability = 50
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
    message = "You repaired the copper shield"
    return render_template('Gargoyle/Gargoyle_Shop_Shields.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold, copper_shield=copper_shield, copper_shield_durability=copper_shield_durability, silver_shield=silver_shield, silver_shield_durability=silver_shield_durability)

#Repair Silver Shield Action
@bp.route('<return_area>/gargoyle_shop/shields_repair_copper_shield')
def gargoyle_shop_shields_silver_repair(return_area):
    Gothic_Flask.Characters.player.gold -= 25
    Gothic_Flask.Items.silver_shield.durability = 50
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
    message = "You repaired the silver shield"
    return render_template('Gargoyle/Gargoyle_Shop_Shields.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold, copper_shield=copper_shield, copper_shield_durability=copper_shield_durability, silver_shield=silver_shield, silver_shield_durability=silver_shield_durability)

#Gargoyle Shop Weapons
@bp.route('<return_area>/gargoyle_shop/weapons')
def gargoyle_shop_weapons(return_area):
    gold = Gothic_Flask.Characters.player.gold
    if Gothic_Flask.Items.small_sword.inInventory:
        small_sword = True
    else:
        small_sword = False
    if Gothic_Flask.Items.war_hammer.inInventory:
        war_hammer = True
    else:
        war_hammer = False
    message = "What will you do?"
    return render_template('Gargoyle/Gargoyle_Shop_Weapons.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold, small_sword=small_sword, war_hammer=war_hammer)

#Buy Small Sword action
@bp.route('<return_area>/gargoyle_shop/weapons/buy_small_sword')
def gargoyle_shop_weapons_sword(return_area):
    Gothic_Flask.Characters.player.gold -= 50
    Gothic_Flask.Items.small_sword.inInventory = True
    gold = Gothic_Flask.Characters.player.gold
    if Gothic_Flask.Items.small_sword.inInventory:
        small_sword = True
    else:
        small_sword = False
    if Gothic_Flask.Items.war_hammer.inInventory:
        war_hammer = True
    else:
        war_hammer = False
    message = "You bought the Small Sword"
    return render_template('Gargoyle/Gargoyle_Shop_Weapons.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold, small_sword=small_sword, war_hammer=war_hammer)

#Buy War Hammer action
@bp.route('<return_area>/gargoyle_shop/weapons/buy_war_hammer')
def gargoyle_shop_weapons_hammer(return_area):
    Gothic_Flask.Characters.player.gold -= 200
    Gothic_Flask.Items.war_hammer.inInventory = True
    gold = Gothic_Flask.Characters.player.gold
    if Gothic_Flask.Items.small_sword.inInventory:
        small_sword = True
    else:
        small_sword = False
    if Gothic_Flask.Items.war_hammer.inInventory:
        war_hammer = True
    else:
        war_hammer = False
    message = "You bought the War Hammer"
    return render_template('Gargoyle/Gargoyle_Shop_Weapons.html', area=gargoyle_shop, return_area=return_area, message=message, gold=gold, small_sword=small_sword, war_hammer=war_hammer)

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
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=death, message=message, name=name)
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
    name = Gothic_Flask.Characters.player.name
    return render_template('Death.html', area=waterway_crypt, message=message, name=name)

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
        name = Gothic_Flask.Characters.player.name
        return render_template('Death.html', area=death, message=message, name=name)
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
    name = Gothic_Flask.Characters.player.name
    return render_template('death.html', area=death, message=message, name=name)

#Crypt Graveyard Area
@bp.route('/crypt_graveyard')
def crypt_graveyard():
    message = "What will you do?"
    return render_template('Crypt_Graveyard.html', area=crypt_graveyard, message=message)

#Enterance Graveyard Area
@bp.route('/enterance_graveyard')
def enterance_graveyard():
    if Gothic_Flask.Map.enterance_graveyard.looted:
        looted = True
    else:
        looted = False
    message = "What will you do?"
    return render_template('Enterance_Graveyard.html', area=enterance_graveyard, message=message, looted=looted)

#Looting an open grave action
@bp.route('/enterance_graveyard/loot_an_open_grave')
def enterance_graveyard_loot():
    Gothic_Flask.Map.enterance_graveyard.looted = True
    if Gothic_Flask.Map.enterance_graveyard.looted:
        looted = True
    else:
        looted = False
    gold_yield = randint(20, 100)
    Gothic_Flask.Characters.player.gold += gold_yield
    message = f"""You pillage a nearby open grave.
    The plunder has yielded you {gold_yield} gold"""
    return render_template('Enterance_Graveyard.html', area=enterance_graveyard, message=message, looted=looted)

#Graves Graveyard Area
@bp.route('/graves_graveyard')
def graves_graveyard():
    combat_chance = randint(1,2)
    if combat_chance > 1 and Gothic_Flask.Map.combat.fought == False:
        Gothic_Flask.Map.combat.fought = True
        Gothic_Flask.Map.combat.enemy = Gothic_Flask.Characters.zombie.name
        Gothic_Flask.Map.combat.enemy_health = Gothic_Flask.Characters.zombie.health
        Gothic_Flask.Map.combat.enemy_attack = Gothic_Flask.Characters.zombie.damage
        enemy = Gothic_Flask.Map.combat.enemy
        enemy_health = Gothic_Flask.Map.combat.enemy_health
        enemy_attack = Gothic_Flask.Map.combat.enemy_attack
        health = Gothic_Flask.Characters.player.health
        enemy_message = f"A {enemy} approaches"
        message = "What will you do?"
        return render_template('Combat/Combat.html', area=graves_graveyard, return_area='graves_graveyard', message=message, enemy_message=enemy_message, enemy=enemy, enemy_health=enemy_health)

    if Gothic_Flask.Map.combat.enemy_health >= 0 and Gothic_Flask.Map.combat.fought == True:
        gold_yield = randint(20, 100)
        Gothic_Flask.Characters.player.gold += gold_yield
        message = f"You've gotten {gold_yield} gold for slaying the {Gothic_Flask.Map.combat.enemy}"
    else:
        message = "What will you do?"

    Gothic_Flask.Map.combat.fought = False

    if Gothic_Flask.Map.graves_graveyard.looted:
        looted = True
    else:
        looted = False
    return render_template('Graves_Graveyard.html', area=graves_graveyard, message=message, looted=looted)

#Looting an open grave action
@bp.route('/graves_graveyard/loot_an_open_grave')
def graves_graveyard_loot():
    Gothic_Flask.Map.graves_graveyard.looted = True
    if Gothic_Flask.Map.graves_graveyard.looted:
        looted = True
    else:
        looted = False
    gold_yield = randint(20, 100)
    Gothic_Flask.Characters.player.gold += gold_yield
    message = f"""You pillage a nearby open grave.
    The plunder has yielded you {gold_yield} gold"""
    return render_template('Graves_Graveyard.html', area=graves_graveyard, message=message, looted=looted)

#Graves Graveyard Area
@bp.route('/wooden_gate_graveyard')
def wooden_gate_graveyard():
    if Gothic_Flask.Items.graveyard_key.inInventory:
        graveyard_key = True
    else:
        graveyard_key = False
    message = "What will you do?"
    return render_template('Wooden_Gate_Graveyard.html', area=wooden_gate_graveyard, message=message, graveyard_key=graveyard_key)

#Unknown Area
@bp.route('/<area>')
def area(area=None):
    return render_template('Wrong.html', area=area)
