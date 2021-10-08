import bpy 
import numpy as np 
import os 
import glob 
import mathutils as m 

# SET UP SCENE
bpy.ops.object.mode_set(mode = "OBJECT")
bpy.ops.object.select_all(action = 'SELECT') 
bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(location = (0,0,0))
ob = bpy.data.objects['Cube']
bpy.context.view_layer.objects.active = ob 

# PREPARE SKS
sk_names = 'basis,mx,my,mz'.split(',') 
sk_dict = {n:i for i,n in enumerate(sk_names)}
ski_dict = {i:n for i,n in enumerate(sk_names)}

# ADD DISPLACEMENT VECTORS
vecs = [(0.,0.,0.), 
        (2.,0.,0.), 
        (0.,2.,0.), 
        (0.,0.,2.)]

# CREATE SHAPE KEYS 
for n in range(len(sk_names)): 
    ob.shape_key_add(from_mix = False)

# SHAPE KEYS RENAME 
for i,(n,sk,v) in enumerate(zip(sk_names, ob.data.shape_keys.key_blocks, vecs)): 
    sk.name = n 
    ob.active_shape_key_index = i
    bpy.ops.object.mode_set(mode = "EDIT")
    bpy.ops.transform.translate(value = v)
    bpy.ops.object.mode_set(mode = 'OBJECT')

# READ ANIM DATA (ARRAY 50X3)
anim_data = np.genfromtxt('anim_data_multiples.csv', delimiter =',') 


# INITIALIZE ANIM 
for sk in sk_names: 
    ob.data.shape_keys.key_blocks[sk].value = 0.
    ob.data.shape_keys.key_blocks[sk].keyframe_insert(data_path = 'value', frame = 0)

# CREATE ANIM WITH WEIGHTING VARIOUS SHAPE KEYS
for i, frame in enumerate(anim_data): 
    for val_idx, val in enumerate(frame): 
        current_sk = ski_dict[val_idx+1]
        ob.data.shape_keys.key_blocks[current_sk].value = val
        ob.data.shape_keys.key_blocks[current_sk].keyframe_insert(data_path = 'value', frame =(i+1)*3)
    