import matplotlib.pyplot as plt 
import numpy as np 


data = np.loadtxt('./face_0.txt')
edge_data = np.loadtxt('./edges_t_0.txt').astype(int)

def randrange(n, vmin, vmax):
    """
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    """
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(data[:,0], data[:,1], data[:,2])
for i,edge in enumerate(edge_data): 
    p0 = data[edge[0]]
    p1 = data[edge[1]]
    p =  np.vstack([p0.reshape(1,-1), p1.reshape(1,-1)])

    ax.plot(xs = p[:,0], ys = p[:,1], zs= p[:,2], color = 'blue')
    if i > 20: 
        break 

# n = 100
print(edge_data.shape)

# # For each set of style and range settings, plot n random points in the box
# # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
#     xs = randrange(n, 23, 32)
#     ys = randrange(n, 0, 100)
#     zs = randrange(n, zlow, zhigh)
#     ax.scatter(xs, ys, zs, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
