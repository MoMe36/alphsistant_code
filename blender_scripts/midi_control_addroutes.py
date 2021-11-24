import bpy 

target_ob = 'head'
midi_controller_id = "Arturia BeatStep:Arturia BeatStep MIDI 1 24:0"
midi_high = 20
blender_high = 100
controllers = [10,74,71,76,77,93,73,75,114,18,19,16,17,91,79,72]

bpy.data.window_managers['WinMan'].addroutes_midi_in_enum = midi_controller_id
bpy.data.window_managers['WinMan'].addroutes_midi_debug = True


for sk in bpy.data.objects[target_ob].data.shape_keys.key_blocks: 
    sk.value = 0

target_sk = 'mouthFunnel,mouthPucker,mouthSmile_L,mouthSmile_R'.split(',')

# Remove existing routes 
bpy.context.scene.MOM_Items.clear()


for i,sk in enumerate(target_sk):
    bpy.context.scene.MOM_Items.add() 
    route = bpy.context.scene.MOM_Items[i]
    route.id_type = "shape_keys"
    route.id.shape_keys = bpy.data.shape_keys['Key']
    route.data_path = "key_blocks[\"{}\"].value".format(target_sk[i])
    route.cont_type = "cc7"
    route.controller = controllers[i]
    route.mode = 'Receive'
    route.rescale = 'Cut'
    route.rescale_outside_high = midi_high
    route.rescale_blender_high = blender_high
    