"""
https://behreajj.medium.com/shaping-models-with-bmesh-in-blender-2-9-2f4fcc889bf0
"""        
import bpy 
import random 
import bmesh 

# SET UP SCENE 
bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action = 'SELECT') 
bpy.ops.object.delete()

# PREPARE CUBE
bpy.ops.mesh.primitive_cube_add(location = (0,0,0)) 
ob = bpy.data.objects['Cube'] 
bpy.context.view_layer.objects.active = ob 

# INITIALIZE SHAPE KEYS 
ob.shape_key_add(from_mix = False) 
sk_block = ob.data.shape_keys.name 
ob.shape_key_add(from_mix = False) 

# RENAME SK
last_name = ""
for k in ob.data.shape_keys.key_blocks: 
    last_name = k.name
ob.data.shape_keys.key_blocks[last_name].name = 'mysk_0'

# SET ACTIVE SHAPE KEYS
ob.active_shape_key_index = 1
ob.data.shape_keys.key_blocks['mysk_0'].value = 1. 

# DEFORM CUBE THROUGH RESIZE 
bpy.ops.object.mode_set(mode ='EDIT') 
bpy.ops.transform.resize(value = (1.,1.,0.5))
bpy.ops.object.mode_set(mode ='OBJECT') 

# ADD FRAMES
ob.data.shape_keys.key_blocks['mysk_0'].value = 0
ob.data.shape_keys.key_blocks['mysk_0'].keyframe_insert("value", frame = 0)
ob.data.shape_keys.key_blocks['mysk_0'].value = 1. 
ob.data.shape_keys.key_blocks['mysk_0'].keyframe_insert("value", frame = 10)
ob.data.shape_keys.key_blocks['mysk_0'].value = 0
ob.data.shape_keys.key_blocks['mysk_0'].keyframe_insert("value", frame = 20)
