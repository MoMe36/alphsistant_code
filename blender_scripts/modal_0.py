import bpy
import numpy as np 


def make_topology(): 
    
    vert_data = np.loadtxt("Bureau/Modis/AlphSistant_code/facemesh_tests/face_0.txt")
    edge_data = np.loadtxt("Bureau/Modis/AlphSistant_code/facemesh_tests/edges_t_0.txt").astype(int).tolist()
    faces = []

    face_mesh = bpy.data.meshes.new('face')
    face_mesh.from_pydata(vert_data, edge_data, faces)
    face_mesh.update()
    ob = bpy.data.objects.new('face', face_mesh)
    bpy.context.scene.collection.objects.link(ob)
        
    

class ModalFaceOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "mehdi.modal_timer_operator"
    bl_label = "ModalFaceOperator"

    _timer = None
    
    def __init__(self): 
        make_topology()

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            ob = bpy.data.objects['face']
            try: 
                target = np.loadtxt("Bureau/Modis/AlphSistant_code/facemesh_tests/face_0.txt")
                for i, (vs, vt) in enumerate(zip(ob.data.vertices, target)): 
                    vs.co = vt
            except: 
                print('Abort') 
                pass 


        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(ModalFaceOperator)


def unregister():
    bpy.utils.unregister_class(ModalFaceOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mehdi.modal_timer_operator()
