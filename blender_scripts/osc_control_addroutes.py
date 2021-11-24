import bpy 

target_ob = 'Cube'

bpy.data.window_managers['WinMan'].addroutes_osc_debug = True


#for sk in bpy.data.objects[target_ob].data.shape_keys.key_blocks: 
#    sk.value = 0

target_sk = 'O,A'.split(',')
nb_targets = 2
target_sk = ['Key {}'.format(i+1) for i in range(nb_targets)]

# Remove existing routes 
bpy.context.scene.MOM_Items.clear()


for i,sk in enumerate(target_sk):
    bpy.context.scene.MOM_Items.add() 
    route = bpy.context.scene.MOM_Items[i]

    route.id_type = "shape_keys"
    route.id.shape_keys = bpy.data.shape_keys['Key']
    route.cont_type = "cc7" # not used in the OSC process but yields an error otherwise 
    route.data_path = "key_blocks[\"{}\"].value".format(target_sk[i])
    route.engine = "OSC" 
    route.osc_address = "/bespoke/slider{}".format(i)
    route.mode = 'Receive'
    
    