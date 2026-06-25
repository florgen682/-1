from ursina import *
from ursina.shaders import lit_with_shadows_shader

# Импортируем продвинутые интерфейсы из префабов
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

import random
import math

app = Ursina(borderless=False, antialiasing=True)
window.title = "Симулятор автомобильного крана 3D - Идеальная Изометрия"
Entity.default_shader = lit_with_shadows_shader

# --- УЛУЧШЕННОЕ ОСВЕЩЕНИЕ И ТЕНИ ---
sun = DirectionalLight(shadow_map_resolution=Vec2(2048, 2048), shadows=True)
sun.y = 80;
sun.x = 50;
sun.z = -50
sun.look_at(Vec3(5, 0, 5))

shadow_bounds_box = Entity(model='wireframe_cube', scale=(200, 40, 200), position=(0, 0, 0), visible=False)
sun.update_bounds(shadow_bounds_box)

AmbientLight(color=color.rgba(140, 145, 160, 255))
sky_box = Sky(texture='sky_sunset')

# Текстовый HUD
info_panel = Text(text='', position=(-0.85, 0.45), scale=1.1, color=color.gold, parent=camera.ui)

# --- ПРОДВИНУТЫЙ ИНТЕРФЕЙС (UI) ---
progress_bar = HealthBar(
    max_value=3,
    value=0,
    bar_color=color.lime,
    back_color=color.dark_gray,
    scale=(0.3, 0.03),
    position=(0.5, 0.43),
    parent=camera.ui
)
progress_text = Text(text='ПРОГРЕСС ДОСТАВКИ', scale=1.0, color=color.white, position=(0.5, 0.47), parent=camera.ui)


def change_weather(value):
    if value == 'Закат':
        sky_box.texture = 'sky_sunset'
        AmbientLight(color=color.rgba(140, 145, 160, 255))
    elif value == 'Ночь':
        sky_box.texture = 'sky_default'
        AmbientLight(color=color.rgba(30, 30, 40, 255))
    elif value == 'День':
        sky_box.texture = 'sky_default'
        AmbientLight(color=color.rgba(255, 255, 255, 255))


# --- МЕНЮ ПАУЗЫ ---
is_paused = False
headlights_on = True

pause_bg = Entity(model='quad', color=color.black, scale=(0, 0), parent=camera.ui, enabled=False, ignore_paused=True)
pause_bg.alpha = 0.75
resume_button = Button(text='ПРОДОЛЖИТЬ', color=color.orange, scale=(0.3, 0.08), position=(0, 0.0), parent=pause_bg,
                       ignore_paused=True)
resume_button.on_click = lambda: toggle_pause()


def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_bg.enabled = True
        pause_bg.animate_scale(Vec3(2, 2, 1), duration=0.2, curve=curve.out_back)
        application.paused = True
    else:
        pause_bg.animate_scale(Vec3(0, 0, 0), duration=0.15)
        invoke(setattr, application, 'paused', False, delay=0.15)
        invoke(setattr, pause_bg, 'enabled', False, delay=0.15)


# --- ЛАНДШАФТ И ОКРУЖЕНИЕ ---
terminal_size = (200, 1, 200)
ground = Entity(model='plane', texture='noise', color=color.dark_gray, scale=terminal_size, texture_scale=(100, 100),
                position=(0, 0, 0), collider='mesh')
sea = Entity(model='plane', color=color.azure, scale=(600, 1, 600), position=(0, -0.4, 0), specular=0.6, roughness=0.4)


def create_wall(pos, scale): Entity(model='cube', color=color.gray, position=pos, scale=scale, collider='box')


create_wall((0, 2.5, 99), (200, 5, 1))
create_wall((0, 2.5, -99), (200, 5, 1))
create_wall((-99, 2.5, 0), (1, 5, 200))
create_wall((99, 2.5, 0), (1, 5, 200))

pole_positions = [(-90, -90), (90, -90), (-90, 90), (90, 90)]
for px, pz in pole_positions:
    Entity(model='cube', color=color.gray, scale=(0.6, 20, 0.6), position=(px, 10, pz))
    Entity(model='cube', color=color.light_gray, scale=(2.5, 1.0, 2.5), position=(px, 20, pz))

container_colors = [color.red, color.blue, color.green, color.orange]
random.seed(10)
for z_pos in range(30, 80, 15):
    for x_pos in range(-70, 71, 15):
        if random.choice([True, False]) and abs(x_pos) > 10:
            height = random.randint(1, 4)
            for h in range(height):
                Entity(model='cube', color=random.choice(container_colors), scale=(8, 3.6, 5),
                       position=(x_pos, 1.8 + h * 3.6, z_pos), collider='box')
from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import random
import math

app = Ursina(borderless=False, antialiasing=True)
window.title = "Симулятор автомобильного крана 3D - Идеальная Изометрия"
Entity.default_shader = lit_with_shadows_shader

# --- УЛУЧШЕННОЕ ОСВЕЩЕНИЕ И ТЕНИ ---
sun = DirectionalLight(shadow_map_resolution=Vec2(2048, 2048), shadows=True)
sun.y = 80;
sun.x = 50;
sun.z = -50
sun.look_at(Vec3(5, 0, 5))

shadow_bounds_box = Entity(model='wireframe_cube', scale=(200, 40, 200), position=(0, 0, 0), visible=False)
sun.update_bounds(shadow_bounds_box)

ambient_light = AmbientLight(color=color.rgba(140, 145, 160, 255))
sky_box = Sky(texture='sky_sunset')

# Текстовый HUD
info_panel = Text(text='', position=(-0.85, 0.45), scale=1.1, color=color.gold, parent=camera.ui)

# --- ПРОДВИНУТЫЙ ИНТЕРФЕЙС (UI) ---
progress_bar = HealthBar(max_value=3, value=0, bar_color=color.lime, back_color=color.dark_gray, scale=(0.3, 0.03),
                         position=(0.5, 0.43), parent=camera.ui)
progress_text = Text(text='ПРОГРЕСС ДОСТАВКИ', scale=1.0, color=color.white, position=(0.5, 0.47), parent=camera.ui)


def change_weather(value):
    global ambient_light
    if value == 'Закат':
        sky_box.texture = 'sky_sunset'
        ambient_light.color = color.rgba(140, 145, 160, 255)
    elif value == 'Ночь':
        sky_box.texture = 'sky_default'
        ambient_light.color = color.rgba(30, 30, 40, 255)
    elif value == 'День':
        sky_box.texture = 'sky_default'
        ambient_light.color = color.rgba(255, 255, 255, 255)


# --- МЕНЮ ПАУЗЫ ---
is_paused = False
headlights_on = True

pause_bg = Entity(model='quad', color=color.black, scale=(0, 0), parent=camera.ui, enabled=False, ignore_paused=True)
pause_bg.alpha = 0.75
resume_button = Button(text='ПРОДОЛЖИТЬ', color=color.orange, scale=(0.3, 0.08), position=(0, 0.0), parent=pause_bg,
                       ignore_paused=True)


def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_bg.enabled = True
        pause_bg.animate_scale(Vec3(2, 2, 1), duration=0.2, curve=curve.out_back)
        application.paused = True
    else:
        pause_bg.animate_scale(Vec3(0, 0, 0), duration=0.15)
        invoke(setattr, application, 'paused', False, delay=0.15)
        invoke(setattr, pause_bg, 'enabled', False, delay=0.15)


resume_button.on_click = toggle_pause

# --- ЛАНДШАФТ И ОКРУЖЕНИЕ ---
terminal_size = (200, 1, 200)
ground = Entity(model='plane', texture='noise', color=color.dark_gray, scale=terminal_size, texture_scale=(100, 100), position=(0, 0, 0), collider='mesh')
sea = Entity(model='plane', color=color.azure, scale=(600, 1, 600), position=(0, -0.4, 0), specular=0.6, roughness=0.4)

obstacles = []


def create_wall(pos, scale):
    w = Entity(model='cube', color=color.gray, position=pos, scale=scale, collider='box')
    obstacles.append(w)


create_wall((0, 2.5, 99), (200, 5, 1))
create_wall((0, 2.5, -99), (200, 5, 1))
create_wall((-99, 2.5, 0), (1, 5, 200))
create_wall((99, 2.5, 0), (1, 5, 200))

pole_positions = [(-90, -90), (90, -90), (-90, 90), (90, 90)]
for px, pz in pole_positions:
    create_wall((px, 10, pz), (0.6, 20, 0.6))
    Entity(model='cube', color=color.light_gray, scale=(2.5, 1.0, 2.5), position=(px, 20, pz))

# Декоративные контейнеры
container_colors = [color.red, color.blue, color.green, color.orange]
random.seed(10)
for z_pos in range(30, 80, 15):
    for x_pos in range(-70, 71, 15):
        if random.choice([True, False]) and abs(x_pos) > 10:
            height = random.randint(1, 4)
            for h in range(height):
                create_wall((x_pos, 1.8 + h * 3.6, z_pos), (8, 3.6, 5))

# --- АВТОКРАН ---
truck = Entity(model='cube', color=color.gray, scale=(2.4, 0.7, 5.0), position=(0, 0.5, -50), collider='box')
bumper = Entity(model='cube', color=color.black, scale=(2.5, 0.35, 0.35), position=(0, -0.15, 2.6))
bumper.world_parent = truck

cabin_base = Entity(model='cube', color=color.red, scale=(2.3, 1.0, 1.6), position=(0, 0.7, 1.5), parent=truck,
                    collider='box')
cabin_top = Entity(model='cube', color=color.red, scale=(2.2, 0.7, 1.3), position=(0, 1.4, 1.35), parent=truck)
windshield = Entity(model='cube', color=color.cyan, scale=(2.0, 0.5, 0.1), position=(0, 1.4, 2.01), parent=truck)
windshield.alpha = 0.6

headlight_l = Entity(model='cube', color=color.white, scale=(0.3, 0.15, 0.1), position=(-0.9, 0.4, 2.51), parent=truck,
                     emissive=True)
headlight_r = Entity(model='cube', color=color.white, scale=(0.3, 0.15, 0.1), position=(0.9, 0.4, 2.51), parent=truck,
                     emissive=True)


def click_truck_lights():
    global headlights_on
    headlights_on = not headlights_on
    headlight_l.enabled = headlights_on
    headlight_r.enabled = headlights_on


cabin_base.on_click = click_truck_lights

back_wheels, front_wheels = [], []


def create_wheel(pos, is_front=False):
    w_pivot = Entity(position=pos, parent=truck)
    Entity(model='cube', color=color.hex('#15181c'), scale=(0.45, 0.45, 0.65), parent=w_pivot, roughness=0.9)
    Entity(model='cube', color=color.light_gray, scale=(0.25, 0.25, 0.7), parent=w_pivot)
    if is_front:
        front_wheels.append(w_pivot)
    else:
        back_wheels.append(w_pivot)


for p in [(-1.25, 0.1, -1.7), (1.25, 0.1, -1.7), (-1.25, 0.1, -0.5), (1.25, 0.1, -0.5)]: create_wheel(p, is_front=False)
for p in [(-1.25, 0.1, 1.4), (1.25, 0.1, 1.4)]: create_wheel(p, is_front=True)

platform = Entity(model='cube', color=color.gray, scale=(1.8, 0.3, 1.8), position=(0, 0.7, -1.3), parent=truck)
boom = Entity(model='cube', color=color.orange, scale=(0.5, 0.5, 7.0), origin_z=-0.5, specular=0.5)

cable = Entity(model='cube', color=color.black, scale=(0.03, 1, 0.03), origin_y=0.5)
hook = Entity(model='cube', color=color.dark_gray, scale=(0.6, 0.15, 0.6))
pointer = Entity(model='arrow', color=color.lime, scale=(0.4, 0.4, 1.2), enabled=False)

# --- ГРУЗЫ И ЦЕЛИ ---
cargo_list = []
current_cargo = None

target_zone = Entity(model='plane', color=color.blue, scale=(10, 1, 7), position=(-40, 0.03, -35), collider='box')
target_zone.alpha = 0.4
zone_beam = Entity(model='cube', color=color.cyan, scale=(9, 25, 6), position=(-40, 12.5, -35), unlit=True)
zone_beam.alpha = 0.1

# Сцена Финала / Смены уровней
victory_screen = Entity(model='quad', color=color.rgba(0, 0, 0, 216), scale=(2, 2), parent=camera.ui, enabled=False,
                        z=-1)
victory_text = Text(text='', origin=(0, 0), scale=2, color=color.gold, parent=victory_screen, y=0.1)

speed_levels = {1: 8.0, 2: 15.0, 3: 25.0}
target_fovs = {1: 55, 2: 60, 3: 72}
current_speed_level = 2
score = 0

# --- СИСТЕМА УРОВНЕЙ И СЛОЖНОСТИ ---
current_level = 1
max_levels = 3
level_obstacles = []  # Динамические препятствия для уровней


def load_level(level_num):
    global score, current_cargo, cargo_list, level_obstacles
    score = 0
    current_cargo = None
    progress_bar.value = 0

    # Полная очистка старых объектов уровня
    for c in cargo_list: destroy(c)
    for o in level_obstacles: destroy(o)
    cargo_list.clear()
    level_obstacles.clear()

    # Сброс позиции машины
    truck.position = (0, 0.5, -50)
    truck.rotation = (0, 0, 0)
    boom.rotation = (0, 0, 0)
    boom.scale_z = 7.0

    # Настройка параметров под текущий уровень сложности
    if level_num == 1:
        # Уровень 1: Легко. 2 груза, широкая зона, нет лишних преград рядом.
        progress_bar.max_value = 2
        target_zone.scale = (12, 1, 9)
        zone_beam.scale = (11, 25, 8)

        cargo_list.append(
            Entity(model='cube', color=color.red, scale=(6, 3, 3.6), position=(20, 1.5, -20), collider='box'))
        cargo_list.append(
            Entity(model='cube', color=color.green, scale=(6, 3, 3.6), position=(-20, 1.5, -10), collider='box'))

    elif level_num == 2:
        # Уровень 2: Средне. 3 груза, стандартная зона, добавляются бетонные блоки-преграды.
        progress_bar.max_value = 3
        target_zone.scale = (10, 1, 7)
        zone_beam.scale = (9, 25, 6)

        cargo_list.append(
            Entity(model='cube', color=color.red, scale=(6, 3, 3.6), position=(25, 1.5, -20), collider='box'))
        cargo_list.append(
            Entity(model='cube', color=color.blue, scale=(6, 3, 3.6), position=(45, 1.5, -30), collider='box'))
        cargo_list.append(
            Entity(model='cube', color=color.green, scale=(6, 3, 3.6), position=(35, 1.5, -10), collider='box'))

        # Ставим блоки вокруг целевой зоны, мешая заезду машины
        level_obstacles.append(
            Entity(model='cube', color=color.brown, scale=(3, 4, 15), position=(-25, 2, -35), collider='box'))
        level_obstacles.append(
            Entity(model='cube', color=color.brown, scale=(15, 4, 3), position=(-40, 2, -25), collider='box'))

    elif level_num == 3:
        # Уровень 3: Сложно. 4 груза, очень узкая зона разгрузки, куча лабиринтов и узких проездов.
        progress_bar.max_value = 4
        target_zone.scale = (7, 1, 5)
        zone_beam.scale = (6, 25, 4.2)

        cargo_list.append(
            Entity(model='cube', color=color.red, scale=(6, 3, 3.6), position=(15, 1.5, -15), collider='box'))
        cargo_list.append(
            Entity(model='cube', color=color.blue, scale=(6, 3, 3.6), position=(55, 1.5, -35), collider='box'))
        cargo_list.append(
            Entity(model='cube', color=color.green, scale=(6, 3, 3.6), position=(25, 1.5, 5), collider='box'))
        cargo_list.append(
            Entity(model='cube', color=color.orange, scale=(6, 3, 3.6), position=(-15, 1.5, 15), collider='box'))

        # Лабиринт из защитных блоков
        level_obstacles.append(
            Entity(model='cube', color=color.dark_gray, scale=(2, 6, 30), position=(-30, 3, -35), collider='box'))
        level_obstacles.append(
            Entity(model='cube', color=color.dark_gray, scale=(30, 6, 2), position=(-40, 3, -15), collider='box'))
        level_obstacles.append(
            Entity(model='cube', color=color.dark_gray, scale=(20, 5, 4), position=(0, 2.5, -25), collider='box'))
        level_obstacles.append(
            Entity(model='cube', color=color.dark_gray, scale=(4, 5, 20), position=(20, 2.5, -40), collider='box'))

    for c in cargo_list:
        c.alpha = 0
        c.fade_in(duration=0.6)


# Загружаем самый первый уровень при старте
load_level(current_level)


def update():
    global current_cargo, current_speed_level, is_paused
    if victory_screen.enabled or is_paused: return

    hovered_name = "Ничего"
    if mouse.hovered_entity and mouse.hovered_entity in cargo_list:
        hovered_name = "Контейнер найден! Нажмите Пробел для захвата"
    elif mouse.hovered_entity == cabin_base:
        hovered_name = "Кабина машины (Кликни, чтобы переключить фары!)"

    info_panel.text = (
        f'УРОВЕНЬ: {current_level} / {max_levels}\n'
        f'СКОРОСТЬ: {speed_levels[current_speed_level] * 2.5:.0f} км/ч  [Передачи: 1, 2, 3]\n'
        f'СТРЕЛА: {boom.scale_z:.1f}м  [Выдвижение: R / F]\n'
        f'БАШНЯ: Q / E  |  НАКЛОН: T / G\n'
        f'ПОД КУРСОРOM: {hovered_name}\n'
        f'ЗАХВАТ ГРУЗА: [ Пробел ]  |  МЕНЮ ПАУЗЫ: [ Esc ]'
    )

    move_speed = speed_levels[current_speed_level] * time.dt
    turn_speed = 65 * time.dt
    camera.fov = lerp(camera.fov, target_fovs[current_speed_level] if (held_keys['w'] or held_keys['s']) else 60,
                      time.dt * 4)

    target_steer_angle = 0
    if held_keys['a']: target_steer_angle = -28
    if held_keys['d']: target_steer_angle = 30
    for pivot in front_wheels: pivot.rotation_y = lerp(pivot.rotation_y, target_steer_angle, time.dt * 12)

    # Проверка столкновений (включая новые динамические объекты уровней)
    all_ignored = (truck, *back_wheels, *front_wheels)

    if held_keys['w']:
        hit_info = raycast(truck.world_position + Vec3(0, 0.3, 0), truck.forward, distance=2.7, ignore=all_ignored)
        if hit_info.hit:
            camera.shake(duration=0.2, magnitude=0.5, speed=0.03)
            cabin_base.blink(color=color.white, duration=0.15)
        else:
            truck.position += truck.forward * move_speed

    if held_keys['s']:
        hit_info = raycast(truck.world_position + Vec3(0, 0.3, 0), -truck.forward, distance=2.7, ignore=all_ignored)
        if hit_info.hit:
            camera.shake(duration=0.2, magnitude=0.5, speed=0.03)
            cabin_base.blink(color=color.white, duration=0.15)
        else:
            truck.position -= truck.forward * move_speed

    if held_keys['a']: truck.rotation_y -= turn_speed
    if held_keys['d']: truck.rotation_y += turn_speed

    camera.position = truck.position + Vec3(0, 70, -70)
    camera.rotation = Vec3(45, 0, 0)

    # Управление краном
    if held_keys['q']: boom.rotation_y -= 45 * time.dt
    if held_keys['e']: boom.rotation_y += 45 * time.dt
    if held_keys['t'] and boom.rotation_x > -55: boom.rotation_x -= 25 * time.dt
    if held_keys['g'] and boom.rotation_x < 12:  boom.rotation_x += 25 * time.dt
    if held_keys['r'] and boom.scale_z < 25.0: boom.scale_z += 6.0 * time.dt
    if held_keys['f'] and boom.scale_z > 5.0:  boom.scale_z -= 6.0 * time.dt

    boom.position = platform.world_position + Vec3(0, 0.15, 0)
    boom_tip = boom.world_position + boom.forward * boom.scale_z
    hook.position = Vec3(boom_tip.x, max(0.4, boom_tip.y - 6.5), boom_tip.z)
    cable.position = boom_tip
    cable.scale_y = max(0.1, boom_tip.y - hook.y)

    if not current_cargo and len(cargo_list) > 0:
        pointer.enabled = True
        pointer.position = hook.position + Vec3(0, 2.5, 0)
        closest_cargo = min(cargo_list, key=lambda c: distance(hook.position, c.position))
        pointer.look_at_xz(closest_cargo.position)
    else:
        pointer.enabled = False

    if current_cargo:
        current_cargo.position = hook.position + Vec3(0, -1.5, 0)
        current_cargo.rotation = boom.rotation


def next_level_or_restart():
    global current_level, victory_screen
    victory_screen.enabled = False
    if current_level < max_levels:
        current_level += 1
        load_level(current_level)
    else:
        # Если прошли всё — перезапуск с 1 уровня
        current_level = 1
        load_level(current_level)


def input(key):
    global current_cargo, current_speed_level, score, current_level
    if victory_screen.enabled:
        if key == 'space' or key == 'enter':
            next_level_or_restart()
        return

    if key == 'escape': toggle_pause()
    if key in ['1', '2', '3']: current_speed_level = int(key)

    if key == 'space':
        if not current_cargo:
            for cargo in cargo_list:
                if distance(hook.position, cargo.position + Vec3(0, 1.5, 0)) < 4.5:
                    current_cargo = cargo
                    current_cargo.collider = None
                    camera.shake(duration=0.15, magnitude=0.4)
                    return
        else:
            dist_to_zone = distance_2d(current_cargo.position, target_zone.position)
            if dist_to_zone < (target_zone.scale_x / 2 + 1.5):
                dropped_cargo = current_cargo
                cargo_list.remove(dropped_cargo)
                current_cargo = None
                dropped_cargo.fade_out(duration=0.4)

                def final_drop():
                    global score
                    dropped_cargo.position = target_zone.position + Vec3(0, 1.5 + score * 3.0, 0)
                    dropped_cargo.rotation = Vec3(0, 0, 0)
                    dropped_cargo.alpha = 1.0
                    dropped_cargo.collider = 'box'
                    score += 1
                    progress_bar.value = score
                    if len(cargo_list) == 0:
                        if current_level < max_levels:
                            victory_text.text = f'УРОВЕНЬ {current_level} ПРОЙДЕН!\n\n[ Нажмите Пробел для Уровня {current_level + 1} ]'
                        else:
                            victory_text.text = 'ИГРА ПОЛНОСТЬЮ ПРОЙДЕНА!\n\n[ Нажмите Пробел для перезапуска ]'
                        victory_screen.enabled = True
                        victory_screen.animate_scale(Vec3(2, 2, 1), duration=0.4, curve=curve.out_back)

                invoke(final_drop, delay=0.4)


app.run()
