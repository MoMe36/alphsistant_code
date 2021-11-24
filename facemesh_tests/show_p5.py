from p5 import * 
import numpy as np 



data = np.loadtxt('./face_0.txt')
min_data = np.min(data, axis = 0)
max_data = np.max(data, axis = 0)
data_scaled = (((data - min_data) / (max_data - min_data))-0.5)*200.
print(data_scaled.min(), data_scaled.max())

def setup(): 
    size(640,360)
    no_loop()

def draw(): 
    
    background(0)

    stroke(255)
    # rotate_x(PI*3/2)
    # rotate_z(PI/6)
    fill(255)
    begin_shape()

    for d in data_scaled : 
        with push_matrix(): 
            translate(*d)
            sphere(1)
        break 
    # vertex(-100, -100, -100)
    # vertex( 100, -100, -100)
    # vertex(   0,    0,  100)

    # vertex( 100, -100, -100)
    # vertex( 100,  100, -100)
    # vertex(   0,    0,  100)

    # vertex( 100, 100, -100)
    # vertex(-100, 100, -100)
    # vertex(   0,   0,  100)

    # vertex(-100,  100, -100)
    # vertex(-100, -100, -100)
    # vertex(   0,    0,  100)
    # end_shape()

if __name__ =='__main__':   
    run(mode = 'P3D')