import bpy 
import mathutils as m 
import random 
#import numpy as np 
#import pandas as pd

bpy.ops.object.mode_set(mode= 'OBJECT') 
bpy.ops.object.select_all(action = 'SELECT') 
bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(size = 2, location = (0,0,0))
bpy.ops.object.armature_add(location = (0,0,0)) 


cube = bpy.data.objects['Cube']
arm = bpy.data.objects['Armature']

for obj in bpy.data.objects: 
    obj.select_set(False)

bpy.context.view_layer.objects.active = cube
bpy.ops.object.modifier_add(type = 'ARMATURE')
cube.modifiers['Armature'].object = arm  


bpy.context.object.vertex_groups.new(name= 'Bone') 
for v in bpy.data.objects['Cube'].data.vertices: 
    bpy.context.object.vertex_groups[0].add([v.index], 1., type = 'REPLACE')



bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
bpy.ops.object.mode_set(mode = 'POSE')
selected_bone = bpy.data.objects['Armature'].pose.bones['Bone'] 

for i in range(3): 
    selected_bone.location = m.Vector((random.uniform(-3,3.),
                                       random.uniform(-3,3.),
                                       random.uniform(-3,3.)))
    selected_bone.keyframe_insert(data_path = 'location',frame = i *20)

selected_bone.location = m.Vector()
selected_bone.keyframe_insert(data_path = 'location', frame = (1+i)*20)


bpy.ops.object.mode_set(mode= 'OBJECT') 