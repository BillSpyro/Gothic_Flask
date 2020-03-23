import Gothic_Flask.Engine
import Gothic_Flask.Map
import Gothic_Flask.Items

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

#Main Crypt Area
@bp.route('/main_crypt')
def main_crypt():
    if Gothic_Flask.Items.copper_shield.inInventory:
        copper_shield = True
    else:
        copper_shield = False
    return render_template('Main_Crypt.html', area=main_crypt, copper_shield=copper_shield)

#Taking copper shield action
@bp.route('/take_copper_shield')
def take_copper_shield():
    Gothic_Flask.Items.copper_shield.inInventory = True
    if Gothic_Flask.Items.copper_shield.inInventory:
        copper_shield = True
    else:
        copper_shield = False
    return render_template('Main_Crypt.html', area=main_crypt, copper_shield=copper_shield)

@bp.route('/<area>')
def area(area=None):
    return render_template('Wrong.html', area=area)
