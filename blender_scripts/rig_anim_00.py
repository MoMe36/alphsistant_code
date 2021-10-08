import bpy 
import mathutils as m 
import random 
import numpy as np 

# SET UP SCENE (DELETE OBJECTS)
bpy.ops.object.mode_set(mode= 'OBJECT') 
bpy.ops.object.select_all(action = 'SELECT') 
bpy.ops.object.delete()


# ADD CUBE AND ARMATURE
bpy.ops.mesh.primitive_cube_add(size = 2, location = (0,0,0))
bpy.ops.object.armature_add(location = (0,0,0)) 

# REFERENCE DATA 
cube = bpy.data.objects['Cube']
arm = bpy.data.objects['Armature']

for obj in bpy.data.objects: 
    obj.select_set(False)

# ASSIGN CUBE DATA TO ARMATURE
bpy.context.view_layer.objects.active = cube
bpy.ops.object.modifier_add(type = 'ARMATURE')
cube.modifiers['Armature'].object = arm  

# CREATE A SINGLE VERTEX GROUP AND ADD VERTICES TO IT 
bpy.context.object.vertex_groups.new(name= 'Bone') 
for v in bpy.data.objects['Cube'].data.vertices: 
    bpy.context.object.vertex_groups[0].add([v.index], 1., type = 'REPLACE')


# CREATE ARMATURE ANIMATION
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