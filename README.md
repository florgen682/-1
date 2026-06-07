from ursina import *
from ursina.shaders import lit_with_shadows_shader

app = Ursina(borderless=False)
window.title = "Симулятор автомобильного крана 3D"
Entity.default_shader = lit_with_shadows_shader

# освеение И ОКРУЖЕНИЕ ---
sun = DirectionalLight(y=40, x=20, z=-20, shadows=True)
sun.look_at(Vec3(10, 0, 10))
AmbientLight(color=color.rgba(120, 120, 130, 255))
Sky(texture='sky_sunset')

# Текстовый интерфейс в стиле мобильной игры
info_panel = Text(
    text='УПРАВЛЕНИЕ ТЯЖЕЛЫМ КРАНОМ:\nСтрелки / WASD - Езда машины | Q/E - Поворот стрелы\nT/G - Наклон стрелы | F - Захват контейнера',
    position=(-0.75, 0.45), scale=1.2, color=color.hex('#FBBF24')
)

# --- ЛОКАЦИЯ ПОРТА (Как на картинке) ---
# Огромная асфальтированная площадка терминала
ground = Entity(model='plane', texture='noise', color=color.hex('#4B5563'), scale=(100, 1, 100), position=(0, 0, 0), texture_scale=(50, 50))
# Море на заднем плане
sea = Entity(model='plane', texture='water', color=color.hex('#1D4ED8'), scale=(200, 1, 100), position=(0, -0.1, -60))

# Склады разноцветных контейнеров на заднем плане
container_colors = [color.red, color.blue, color.green, color.orange, color.yellow]
import random
random.seed(42) # Чтобы контейнеры стояли всегда одинаково
for z_pos in range(20, 50, 6):
    for x_pos in range(-30, 30, 4):
        if random.choice([True, False]):
            height = random.randint(1, 3)
            for h in range(height):
                Entity(model='cube', texture='box', color=random.choice(container_colors), 
                       scale=(3, 1.5, 2), position=(x_pos, 0.75 + h*1.5, z_pos))

# --- АВТОМОБИЛЬНЫЙ КРАН (Составная модель спецтехники) ---
# Главная колесная платформа (Шасси грузовика)
truck_body = Entity(model='cube', color=color.hex('#1E3A8A'), scale=(3, 1, 6), position=(0, 0.7, 0))
truck_cabin = Entity(model='cube', color=color.hex('#1E3A8A'), scale=(2.8, 1.4, 1.8), position=(0, 1.4, 2))
cabin_glass = Entity(model='cube', color=color.cyan, scale=(2.6, 0.8, 0.1), position=(0, 1.6, 2.86))

# Колеса грузовика
wheels = []
for x_side in [-1.55, 1.55]:
    for z_side in [-2, -0.5, 1.8]:
        w = Entity(model='cylinder', color=color.black, scale=(0.5, 0.8, 0.8), rotation_z=90, position=(x_side, 0.4, z_side))
        wheels.append(w)

# Поворотная платформа крана (находится сзади грузовика)
crane_platform = Entity(model='cylinder', color=color.hex('#374151'), scale=(2, 0.4, 2), position=(0, 1.3, -1.5))

# Большая телескопическая стрела крана
crane_boom = Entity(model='cube', color=color.hex('#D97706'), scale=(0.6, 0.6, 8), origin_z=-0.5, position=(0, 1.7, -1.5))

# Лебедка, трос и крюк
cable = Entity(model='cylinder', color=color.black, scale=(0.04, 1, 0.04), origin_y=0.5)
hook = Entity(model='cube', color=color.hex('#111827'), scale=(0.8, 0.2, 0.8))

# --- ЦЕЛЕВОЙ ГРУЗ ---
cargo = Entity(model='cube', texture='box', color=color.hex('#DC2626'), scale=(4, 2, 2), position=(8, 1, -2))
# Подсветка зоны, куда нужно привезти груз (Синий маркер, как на твоем скриншоте)
target_zone = Entity(model='plane', color=color.rgba(0, 0, 255, 100), scale=(5, 1, 3), position=(-10, 0.02, -2))
target_marker = Entity(model='cube', color=color.green, scale=(0.2, 2, 0.2), position=(-10, 1, -2))

has_cargo = False

# --- СИСТЕМА ДИНАМИЧЕСКОЙ КАМЕРЫ И УПРАВЛЕНИЯ ---
def update():
    global has_cargo
    
    # 1. СЛЕДЯЩАЯ КАМЕРА (Камера плавно летит за грузовиком, создавая вид от 3-го лица)
    camera.position = truck_body.position + Vec3(0, 8, -14)
    camera.look_at(truck_body.position + Vec3(0, 2, 2))
    
    # 2. УПРАВЛЕНИЕ МАШИНОЙ (Езда по порту)
    speed = 5 * time.dt
    if held_keys['w']: truck_body.z += speed
    if held_keys['s']: truck_body.z -= speed
    if held_keys['d']: truck_body.x += speed
    if held_keys['a']: truck_body.x -= speed
    
    # Привязываем колеса и платформу к машине
    for w in wheels:
        w.x = truck_body.x + (1.55 if w.x > truck_body.x else -1.55)
        w.z = truck_body.z + (w.z - truck_body.z) # удерживают смещение
        w.y = truck_body.y - 0.3
    truck_cabin.position = truck_body.position + Vec3(0, 0.7, 2)
    cabin_glass.position = truck_body.position + Vec3(0, 0.9, 2.86)
    crane_platform.position = truck_body.position + Vec3(0, 0.6, -1.5)

    # 3. УПРАВЛЕНИЕ СТРЕЛОЙ КРАНА
    # Поворот башни крана (Q / E)
    if held_keys['q']: crane_boom.rotation_y -= 30 * time.dt
    if held_keys['e']: crane_boom.rotation_y += 30 * time.dt
    
    # Наклон стрелы вверх/вниз (T / G)
    if held_keys['t'] and crane_boom.rotation_x > -45: crane_boom.rotation_x -= 15 * time.dt
    if held_keys['g'] and crane_boom.rotation_x < 10:  crane_boom.rotation_x += 15 * time.dt

    # Привязка основания стрелы к поворотной платформе
    crane_boom.position = crane_platform.position + Vec3(0, 0.4, 0)

    # 4. ФИЗИКА ТРОСА И КРЮКА (Вычисляем конец наклонной стрелы)
    # Находим мировую точку конца стрелы
    boom_tip = crane_boom.position + crane_boom.forward * 4.0
    
    hook.x = boom_tip.x
    hook.z = boom_tip.z
    hook.y = max(0.4, boom_tip.y - 3.5) # Трос зафиксирован по длине
    
    cable.x = boom_tip.x
    cable.z = boom_tip.z
    cable.y = boom_tip.y
    cable.scale_y = boom_tip.y - hook.y

    # Если груз подцеплен — он фиксируется под крюком
    if has_cargo:
        cargo.position = hook.position + Vec3(0, -1, 0)
        cargo.rotation = crane_boom.rotation

def input(key):
    global has_cargo
    if key == 'f':
        if not has_cargo:
            # Проверяем дистанцию от крюка до красного контейнера
            if distance(hook.position, cargo.position + Vec3(0, 1, 0)) < 2.0:
                has_cargo = True
                info_panel.text = "ГРУЗ ЗАХВАЧЕН (LIFT ON)\nПеревезите его на синюю подсвеченную площадку склада!"
        else:
            # Проверяем, привезли ли груз в синюю зону разгрузки
            if distance(cargo.position, target_zone.position) < 3.5:
                has_cargo = False
                cargo.position = target_zone.position + Vec3(0, 1, 0)
                cargo.rotation = (0, 0, 0)
                info_panel.text = "ОТЛИЧНО! Груз доставлен в целевую зону. Задача выполнена!"
            else:
                info_panel.text = "Нельзя сбрасывать груз здесь! Доедьте до синего маркера."

app.run()
