import random

from character import *
from level_setup import Level
from character_setup import *
from bag import *

#game variables
level = Level()
level.setup_level(1)
knights = knights_setup(["robin", "galahad", "lancelot", "bedevere", "king_arthur"])
enemies = enemies_setup(level.enemies)
bag = Bag(3, 5, 1)

action_cooldown = 0
action_wait_time = 12
ability_selected = None
target = None
is_clicked = False
is_new_action = False
has_taken_action = False

#works like queue to track order
turn_order = knights + enemies
random.shuffle(turn_order)
curr_character = None

is_running = True
is_win = False

while is_running:

    clock.tick(fps)

    level.draw_bg()
    draw_panel()

    for knight in knights:
        knight.draw()
        
    for enemy in enemies:
        enemy.draw()

    if not curr_character:
        curr_character = turn_order.pop(0)

    pos = pygame.mouse.get_pos()

    if isinstance(curr_character, Knight):
        if not bag.is_opened():
            curr_character.draw_abilities()
        bag.draw()

        if bag.is_opened() and back_button.is_clicked() and is_new_action:
            is_new_action = False
            bag.close()
        elif not bag.is_opened() and bag_button.is_clicked() and is_new_action:
            is_new_action = False
            bag.open()

        for ability in curr_character.abilities:
            if ability.is_activated():
                ability_selected = ability

        if ability_selected:
            for enemy in enemies:
                if enemy.rect.collidepoint(pos) and is_clicked:
                    target = enemy

    #attack action
    # action_cooldown += 1
    if 12 >= action_wait_time:
        if curr_character in knights:
            if ability_selected and target:
                if curr_character.attack(target):
                    turn_order.remove(target)
                    enemies.remove(target)
                has_taken_action = True
            # if is_potion_selected:
            #     curr_character.hp = min(curr_character.hp + potion_effect, curr_character.max_hp)
            #     has_taken_action = True
        else:
            enemy_target =  random.choice(knights)
            if curr_character.attack(enemy_target):
                turn_order.remove(enemy_target)
                knights.remove(enemy_target)
            has_taken_action = True
        action_cooldown = 0
        

    if has_taken_action:
        turn_order.append(curr_character)
        curr_character = None
        ability_selected = None
        target = None
        is_clicked = False
        has_taken_action = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_clicked = True
        else:
            is_clicked = False
        if event.type == pygame.MOUSEBUTTONUP:  
            is_new_action = True
    
    if not knights:
        is_running = False
        
    if not enemies:
        if level.curr_level == 5:
            is_win = True
            is_running = False
        else:
            level.curr_level += 1
            level.setup_level(level.curr_level)
            enemies = enemies_setup(level.enemies)
            turn_order = turn_order + enemies
            random.shuffle(turn_order)

    pygame.display.update()

pygame.quit()