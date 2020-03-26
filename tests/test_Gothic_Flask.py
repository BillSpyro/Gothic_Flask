from Gothic_Flask import create_app
import Gothic_Flask.Map

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert b'Play' in response.data

def test_death(client):
    response = client.get('/')
    assert b'Play' in response.data

def test_combat(client):
    Gothic_Flask.Map.combat.enemy = "Zombie"
    Gothic_Flask.Map.combat.enemy_health = 20
    response = client.get('/game/graves_graveyard/combat')
    assert b'Attack' in response.data
    assert b'Use Item' in response.data
    assert b'Nothing' in response.data

def test_intro(client):
    response = client.get('/game/intro')
    assert b'Continue' in response.data
    assert b'Save' in response.data
    assert b'Your name is Player' in response.data
    response = client.post('/game/intro', data={'name': 'Gordon'})
    response = client.get('/game/intro')
    assert b'Your name is Gordon' in response.data

def test_main_crypt(client):
    response = client.get('/game/main_crypt')
    assert b'Take copper shield' in response.data
    assert b'Go down the left hallway' in response.data
    assert b'Go down the right hallway' in response.data
    assert b'Go to the gate' in response.data
    assert b'Inventory' in response.data

def test_statue_crypt(client):
    response = client.get('/game/statue_crypt')
    assert b'Take small sword' in response.data
    assert b'Desecrate the statue' in response.data
    assert b'Go back' in response.data
    assert b'Inventory' in response.data

def test_waterway_crypt(client):
    response = client.get('/game/waterway_crypt')
    assert b'Take crypt key' in response.data
    assert b'Go for a swim' in response.data
    assert b'Look for something in the water' in response.data
    assert b'Go back' in response.data
    assert b'Inventory' in response.data

def test_gate_crypt(client):
    response = client.get('/game/gate_crypt')
    assert b'Try the lock' in response.data
    assert b'Use your head' in response.data
    assert b'Go back' in response.data
    assert b'Inventory' in response.data

def test_crypt_graveyard(client):
    response = client.get('/game/crypt_graveyard')
    assert b'Go to the graveyard enterance' in response.data
    assert b'Go deeper into the graveyard' in response.data
    assert b'Go back into the crypt' in response.data
    assert b'Inventory' in response.data

def test_enterance_graveyard(client):
    response = client.get('/game/enterance_graveyard')
    assert b'Loot an open grave' in response.data
    assert b'Talk to the gargoyle' in response.data
    assert b'Go back up the crypt hill' in response.data
    assert b'Inventory' in response.data

def test_gargoyle_shop(client):
    response = client.get('/game/enterance_graveyard/gargoyle_shop')
    assert b'Health' in response.data
    assert b'Shields' in response.data
    assert b'Weapons' in response.data
    assert b'Go back' in response.data

def test_graves_graveyard(client):
    Gothic_Flask.Map.combat.fought = True
    response = client.get('/game/graves_graveyard')
    assert b'Loot an open grave' in response.data
    assert b'Go to the large wooden gate' in response.data
    assert b'Go back up the crypt hill' in response.data
    assert b'Inventory' in response.data
