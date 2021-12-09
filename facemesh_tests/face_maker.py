import numpy as np 


polygons = np.loadtxt('./polygons_0.txt').astype(int)
edges = np.loadtxt('./edges_t_0.txt').astype(int)


polygons = polygons[:5]
print(polygons)

vertices = []
for polygon in polygons: 
    p_verts = []
    for p_edge in polygon: 
        verts = edges[p_edge]
        print('Edge {} - Verts: {}'.format(p_edge,verts))
        p_verts.append(verts)
    input()
    print(p_verts)
    p_verts = list(set(np.array(p_verts).flatten().astype(int).tolist()))
    print(p_verts)
    print(list(set(p_verts)))
    vertices.append(p_verts)
    print(vertices)
    input()
print(vertices)