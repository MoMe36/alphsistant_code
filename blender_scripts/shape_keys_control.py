import bpy 
import numpy as np 
import os 
import glob 
import csv

# GET OBJECT
ob = bpy.data.objects['Head'] 
bpy.context.view_layer.objects.active = ob 


# GET SHAPE KEYS
sk_names = []
for sk in ob.data.shape_keys.key_blocks: 
    sk_names.append(sk.name) 
sk_dict = {s[0].lower():s for s in sk_names}

# INITIALIZE ANIMATION 
for sk in sk_names: 
    ob.data.shape_keys.key_blocks[sk].value= 0
    ob.data.shape_keys.key_blocks[sk].keyframe_insert(data_path = 'value', frame = 0) 

# FIND ANIMATION DATA WITHIN CSV
base_folder = '/home/mehdi/Bureau/Modis/AlphSistant_code/sounds_tests/res/aeiou'
data = glob.glob(os.path.join(base_folder, "*.csv"))
sound = data[0].replace('.csv', '.wav') 


# ADDING SOUND TO SCENE
bpy.context.scene.sequence_editor_clear()
bpy.context.scene.sequence_editor_create()
bpy.contexte.scene.sequence_editor.sequences.new_sound("speaker", sound, channel = 1, frame = 0)

    


# GET HEADER 
with open(data[0], newline = '') as csvfile: 
    reader = csv.reader(csvfile, delimiter = ',') 
    cols = None 
    for row in reader: 
        cols = row
        break 
print(cols)
# GET PREDICTED CLASSES
preds = np.genfromtxt(data[0], delimiter = ',', skip_header = 1)
print(preds)

for p in preds: 
    best_answer = np.argmax(p.flatten()[:-2]) 
    selected_keyframe = sk_dict[cols[best_answer]]

    start = int(p[-2])
    end = int(p[-1])
    print(selected_keyframe, start, end)
    ob.data.shape_keys.key_blocks[selected_keyframe].value = 1

    ob.data.shape_keys.key_blocks[selected_keyframe].keyframe_insert(data_path='value', frame = start)
    ob.data.shape_keys.key_blocks[selected_keyframe].keyframe_insert(data_path='value', frame = end)
    ob.data.shape_keys.key_blocks[selected_keyframe].value = 0
    ob.data.shape_keys.key_blocks[selected_keyframe].keyframe_insert(data_path='value', frame = start-1)
    ob.data.shape_keys.key_blocks[selected_keyframe].keyframe_insert(data_path='value', frame = end+1)
    
    



"""
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
"""   