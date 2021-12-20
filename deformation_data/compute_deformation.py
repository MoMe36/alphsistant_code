import numpy as np 
from scipy.optimize import minimize
import glob 
import os 
import torch 
import torch.optim as optim 
import torch.nn.functional as F 
import torch.nn as nn 

face_list = np.loadtxt('./results/target_faces.txt').astype(int)
print(face_list)

def optimize_mesh(x, S_ready, Ts): 

    # IL FAUT RECALCULER LES V_TILDE POUR LE MAILLAGE CIBLE DÉFORMÉ
    # IL FAUT DONC RECOMPOSER LES FACES (TRIANGLES) POUR CALCULER V4_TILDE 
    # AVEC V4_TILDE, ON CALCULE T = V_TILDE V^-1
    # ON MINIMISE 

    # Pour recomposer les faces
    predicted_target_vertices = x.reshape(-1,3)

    # on reconstruit les vecteurs associés 
    v1_tilde = predicted_target_vertices[face_list[:,0],:]
    v2_tilde = predicted_target_vertices[face_list[:,1],:]
    v3_tilde = predicted_target_vertices[face_list[:,2],:]
    
    # on recalcule v4 
    d = np.cross(v2_tilde - v1_tilde, v3_tilde - v1_tilde) 
    scale_factor = np.sqrt(np.sum(d**2, axis = 1)).reshape(-1,1)
    v4_tilde = v1_tilde + d / scale_factor

    # v4_tilde permet d'obtenir T_tilde pour les transformations entre faces 
    t1_tilde = v2_tilde - v1_tilde
    t2_tilde = v3_tilde - v1_tilde
    t3_tilde = v4_tilde - v1_tilde


    # 1. Compute T transformations based on x guess + initial target mesh data 
    T = np.concatenate([Ti.T.reshape(3,1,-1) for Ti in Ts], axis = 1) 
    T_tilde = np.concatenate([Ti.reshape(3,1,-1) for Ti in [t1_tilde, t2_tilde, t3_tilde]], axis = 1) 


    # On calcule la matrice de transformation

    Tt = np.zeros((3,3,T.shape[-1]))
    for i in range(T.shape[-1]): 
        # print(np.linalg.det(T[:,:,i]))
        it = np.linalg.inv(T[:,:,i])
        T_current = np.matmul(T_tilde[:,:,i], np.linalg.inv(T[:,:,i]))
        Tt[:,:,i]= T_current

    

    # 2. compute distance for each matrix (frobenius norm)


    loss = np.mean(np.linalg.norm(S_ready - Tt, axis = (0,1)))
    print(loss)
    return loss


def torch_optim(initial_val, S_ready, Ts, iters = 0): 

    initial_tensor = nn.Parameter(torch.tensor(initial_val, requires_grad = True).reshape(-1,3))
    print(initial_tensor[:3])
    adam = optim.Adam([initial_tensor], lr = 1e-3)

    for i in range(iters): 
        v1_tilde = torch.index_select(initial_tensor, 0, torch.tensor(face_list[:,0]).long())
        v2_tilde = torch.index_select(initial_tensor, 0, torch.tensor(face_list[:,1]).long())
        v3_tilde = torch.index_select(initial_tensor, 0, torch.tensor(face_list[:,2]).long())

        d = torch.cross(v2_tilde - v1_tilde, v3_tilde - v1_tilde, dim = 1) 
        scale_factor = torch.sqrt(torch.sum(d**2, axis = 1)).reshape(-1,1)
        v4_tilde = v1_tilde + d / scale_factor

        t1_tilde = v2_tilde - v1_tilde
        t2_tilde = v3_tilde - v1_tilde
        t3_tilde = v4_tilde - v1_tilde
        
        T = torch.tensor(np.concatenate([Ti.T.reshape(3,1,-1) for Ti in Ts], axis = 1))
        T_tilde = torch.cat([t1_tilde.reshape(3,1,-1),
                             t2_tilde.reshape(3,1,-1), 
                             t3_tilde.reshape(3,1,-1)], axis = 1)

        Tt = torch.matmul(torch.permute(T_tilde, (2,0,1)), torch.linalg.inv(torch.permute(T, (2,0,1)))) 
        
        loss = F.mse_loss(torch.permute(torch.tensor(S_ready), (2,0,1)), Tt)
        
        adam.zero_grad()
        loss.backward()
        adam.step()

    print(initial_tensor[:3])
    # initial_tensor +=
    return initial_tensor.detach().numpy()


if __name__ == "__main__": 

    files = sorted(glob.glob('*.txt'))
    source_undeformed = [f for f in files if not 'd' in f]
    source_deformed = [f for f in files if 'd' in f]


    # VERTICES
    v1 = np.loadtxt(source_undeformed[0])
    v2 = np.loadtxt(source_undeformed[1])
    v3 = np.loadtxt(source_undeformed[2])
    v4 = np.loadtxt(source_undeformed[3])

    v1t = np.loadtxt(source_deformed[0])
    v2t = np.loadtxt(source_deformed[1])
    v3t = np.loadtxt(source_deformed[2])
    v4t = np.loadtxt(source_deformed[3])

    # NON TRANSLATIONAL VECTORS
    V1 = (v2 - v1).T.reshape(3,1,-1)
    V2 = (v3 - v1).T.reshape(3,1,-1)
    V3 = (v4 - v1).T.reshape(3,1,-1)

    V1t = (v2t - v1t).T.reshape(3,1,-1)
    V2t = (v3t - v1t).T.reshape(3,1,-1)
    V3t = (v4t - v1t).T.reshape(3,1,-1)

    # FOR TRANSFORMATION

    V = np.concatenate([V1,V2,V3], axis = 1)
    Vt = np.concatenate([V1t,V2t,V3t], axis = 1)

    # COMPUTE TRANSFORMATION FOR EACH TRIANGLE

    Qs = np.zeros((3,3,V.shape[-1]))
    for i in range(V.shape[-1]): 
        Q = np.matmul(Vt[:,:,i], np.linalg.inv(V[:,:,i]))
        Qs[:,:,i]= Q

    # LET'S ASSUME TARGET MESH IS SIMILAR TO SOURCE 

    t1 = np.loadtxt(source_undeformed[0])
    t2 = np.loadtxt(source_undeformed[1])
    t3 = np.loadtxt(source_undeformed[2])
    t4 = np.loadtxt(source_undeformed[3])


    T1 = t2 - t1 
    T2 = t3 - t1 
    T3 = t4 - t1 

    # ÇA, CE SONT LES VERTICES DU MAILLAGE
    initial_guess = np.zeros((np.max(face_list) + 1, 3))
    

    for i in range(initial_guess.shape[0]): 
        pos, col = np.where(face_list == i)
        col = col[0]
        pos = pos[0]
        print(pos, col)
        if col == 0: 
            initial_guess[i,:] = t1[pos]
        if col == 1: 
            initial_guess[i,:] = t2[pos]
        else: 
            initial_guess[i,:] = t3[pos]

    # initial_guess += np.random.uniform(-1.,1., size = initial_guess.shape) * 0.01

    # ==========================================
    # ==========================================
    #  TORCH OPTIM

    target_deformed_vertices = torch_optim(initial_guess, Qs, [T1,T2,T3])
    target_deformed_vertices = initial_guess.reshape(-1,3)
    np.savetxt('./results/result_target_mesh.txt', target_deformed_vertices)
    input('Torch done')

    # ==========================================
    # ==========================================
    #  SCIPY OPTIM
    results = minimize(fun = optimize_mesh, 
                                        x0 = initial_guess,
                                        args = (Qs, [T1, T2, T3]), 
                                        options = {'maxiter':1})
    target_deformed_vertices = results.x.reshape(-1,3)                               
    # target_deformed_vertices = np.random.uniform(-1.,1., initial_guess.shape).reshape(-1,3)
    np.savetxt('./results/result_target_mesh.txt', target_deformed_vertices)

