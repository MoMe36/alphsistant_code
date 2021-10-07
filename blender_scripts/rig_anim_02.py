import bpy
import os 
import glob 
import numpy as np 

bpy.ops.object.select_all(action = "SELECT") 
bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(location = (0,0,0)) 

ob = bpy.data.objects['Cube'] 
ob.data.name = 'Cube' 
bpy.context.view_layer.objects.active = ob 


sk_names = 'basis,sx,sy,sz'.split(',')
sk_dict = {n:i for i,n in enumerate(sk_names)}
ski_dict = {i:n for i,n in enumerate(sk_names)} 

for _ in range(len(sk_names)):  
    ob.shape_key_add(from_mix = False)
    
for n,current in zip(sk_names, ob.data.shape_keys.key_blocks): 
    current.name = n 


bpy.context.object.active_shape_key_index = sk_dict['sx'] 
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.transform.resize(value = (2.,1.,1.))

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.context.object.active_shape_key_index = sk_dict['sy'] 
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.transform.resize(value = (1.,2.,1.))

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.context.object.active_shape_key_index = sk_dict['sz'] 
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.transform.resize(value = (1.,1.,2.))
bpy.ops.object.mode_set(mode = 'OBJECT')


file = [f for f in glob.glob('*.csv') if 'anim' in f][0]
anim_data = np.genfromtxt(file, delimiter = '\n')[1:] +1 

for sk_n in sk_names: 
    ob.data.shape_keys.key_blocks[sk_n].value = 0.
    ob.data.shape_keys.key_blocks[sk_n].keyframe_insert(data_path = 'value', frame = 0)

for i,ski in enumerate(anim_data):
    print('Anim data: {}'.format(ski))
    for j,idx in enumerate(sk_names): 
        v = 1. if j+1 == int(ski) else 0.
        print(v)
        sk_n = ski_dict[ski]
        ob.data.shape_keys.key_blocks[idx].value = v
        ob.data.shape_keys.key_blocks[idx].keyframe_insert("value", frame = (i+1)*3)
         
    