from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise

app = Ursina()

window.fps_counter.enabled = True
window.exit_button.visible = False
window.title = "Minecraft first try"

BLOCK_REGISTRY = {
    1: {'name': 'Grass', 'color': color.green, 'highlight': color.lime},
    2: {'name': 'Dirt',  'color': color.brown, 'highlight': color.light_gray},
    3: {'name': 'Stone', 'color': color.dark_gray, 'highlight': color.white},
    4: {'name': 'Brick', 'color': color.orange, 'highlight': color.yellow}
}

selected_block = 1

class Voxel(Button):
    def __init__(self, position=(0,0,0), block_type=1):
        block_info = BLOCK_REGISTRY[block_type]
        
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='white_cube', 
            color=block_info['color'],
            highlight_color=block_info['highlight']
        )
        self.block_type = block_type

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                hand.mine_animation()
                destroy(self)
                
            elif key == 'right mouse down':
                hand.place_animation()
                new_pos = self.position + mouse.normal
                Voxel(position=new_pos, block_type=selected_block)

class PlayerHand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui, 
            model='cube',
            texture='white_cube',
            color=BLOCK_REGISTRY[selected_block]['color'],
            scale=(0.2, 0.2, 0.4),
            rotation=(30, -30, 0),
            position=(0.6, -0.4, 1)
        )

    def update_block_type(self):
        self.color = BLOCK_REGISTRY[selected_block]['color']

    def mine_animation(self):
        self.position = (0.5, -0.5, 0.9)
        self.rotation = (15, -45, -10)
        invoke(self.reset_position, delay=0.1)

    def place_animation(self):
        self.position = (0.6, -0.3, 1.1)
        invoke(self.reset_position, delay=0.1)

    def reset_position(self):
        self.position = (0.6, -0.4, 1)
        self.rotation = (30, -30, 0)

class InventoryHotbar(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.slots = []
        self.indicators = []
        self.setup_ui()

    def setup_ui(self):
        start_x = -0.3
        spacing = 0.2
        
        for i, b_id in enumerate(BLOCK_REGISTRY):
            slot = Entity(
                parent=self,
                model='quad',
                color=color.black66 if b_id == selected_block else color.black33,
                scale=(0.15, 0.1),
                position=(start_x + (i * spacing), -0.42)
            )
            preview = Entity(
                parent=slot,
                model='quad',
                color=BLOCK_REGISTRY[b_id]['color'],
                scale=(0.6, 0.6),
                position=(0, 0, -0.1)
            )
            self.slots.append(slot)

    def update_selection(self):
        for i, slot in enumerate(self.slots):
            if i + 1 == selected_block:
                slot.color = color.black66
                slot.scale = (0.17, 0.12) 
            else:
                slot.color = color.black33
                slot.scale = (0.15, 0.1)

noise = PerlinNoise(octaves=2, seed=random.randint(1, 1000))
world_size = 24 

for x in range(world_size):
    for z in range(world_size):

        noise_val = noise([x / 20, z / 20])
        y_height = int(noise_val * 6) + 2
        
        Voxel(position=(x, y_height, z), block_type=1)     
        Voxel(position=(x, y_height - 1, z), block_type=2) 
        
        for y in range(y_height - 4, y_height - 1):
            Voxel(position=(x, y, z), block_type=3)        

def update():
    global selected_block
    
    if held_keys['1'] and selected_block != 1: selected_block = 1; hotbar.update_selection(); hand.update_block_type()
    if held_keys['2'] and selected_block != 2: selected_block = 2; hotbar.update_selection(); hand.update_block_type()
    if held_keys['3'] and selected_block != 3: selected_block = 3; hotbar.update_selection(); hand.update_block_type()
    if held_keys['4'] and selected_block != 4: selected_block = 4; hotbar.update_selection(); hand.update_block_type()
    
    if held_keys['escape']:
        application.quit()

player = FirstPersonController()
player.y = 8                     
player.cursor.color = color.red  

hand = PlayerHand()
hotbar = InventoryHotbar()

app.run()