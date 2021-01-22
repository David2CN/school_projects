#miniReservoirSimulator
#Matrix solver

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def thomasAlgorithm(n, soe):
    """
    # n is the number of equations
    # soe is the system of equations
    This function takes in a tri-diagonal system of equations, soe and rhe number of the equations, n, as parameters. It employs the thomas algorithm to return the solution of these sytem of equations.
    """
    w = [0]*n
    g = [0]*n
    w[0] = soe[0][1] / soe[0][0]
    g[0] = soe[0][2] / soe[0][0]

    for i in range(1,n-1):
        w[i] = soe[i][2] / (soe[i][1] - (soe[i][0])*w[i-1])
        g[i] = (soe[i][3] - ((soe[i][0])*g[i-1])) / (soe[i][1] - (soe[i][0])*w[i-1])
        
    g[n-1] = (soe[n-1][2] - ((soe[n-1][0])*g[n-2])) / (soe[n-1][1] - (soe[n-1][0])*w[n-2])            
    #back-substitution            
    solution = [0]*n
    solution[n-1] = g[n-1]
    for i in range(n-2, -1, -1):
        solution[i] = g[i] - w[i]*solution[i+1]

    solu = [round(i, 100) for i in solution]
    return solu


#LHS generator
def LHS(n,Ac,Bc):
    """
    This forms the Left Hand Side of the System of Equations, which is mostly constant with Ac and Bc
    """
    lhs = [0]*n
    for i in range(1,n-1):
        lhs[i] = [Ac, -Bc, Ac]
    lhs[0] = [Ac-Bc, Ac]
    lhs[n-1] = [Ac, -Bc+Ac]   
    return lhs


#RHS generator
def RHS(n, Ac, r, solut):
    """
    This forms the Right Hand Side of the System of Equations, which involves using the pressure values from the previous timestep.
    """
    rhs = [0]*n
    for i in range(n):
        Pi = solut[i]
        rhs[i] = -float(r * Pi)
        if i+1 in prod_blocks:
            q = prod_blocks[i+1]
            rhs[i] = -float((r * Pi) + q)
    return rhs

#equation
def LRHS(n, lhs, rhs):
    """
    This joins the LHS and RHS to form the System of Equations
    """
    for i in range(n):
        lhs[i].append(rhs[i])
    soe = lhs
    return soe
    

#INPUT
dt = 15                #time step, days
dx = 1000            #size of block, width, ft
A = 75000            #area if block, ft²
k = 15            #permeability, md
u = 10            #viscosity, cp
B = 1            #oil FVF, bbl/stb
ct = 3.5 * (10 ** -6)  #compressibility, /psi
ph = 0.18            #porosity
Pi = 6000            #initial pressure, psi
time  = 360            #duration of simulation, days
n = 5                #number of equations
prod_blocks = {4 : -150}   #producing blocks;
#blocks :  production/injection, stb/day


#prior calculation
#Vb, r, Ac, Bc are all constants, check procedure of solution for clarity
Vb = float(A * dx)
r = float((Vb * ph * (ct)) / (5.615 * B * dt))
Ac = float((1.127 * A * (k/1000)) / (u * B * dx))
Bc = float((2 * Ac) + r)

#Marching
rt = int(time / dt)
#rt is the number of time steps
pressure_distribution = [0]
#this is the container for the calculated pressures at each time step across the blocks
solut = [Pi]*n
pressure_distribution[0] = solut
#solut is the initial reservoir pressure across the blocks(i.e., time step 0)
a = 0
index_names, tstep = [0], 0
for i in range(rt):
    #for the index names
    tstep += dt
    index_names.append(tstep)
    lis = pressure_distribution[a]
    #lis is the pressure from the previous timestep
    lhs = LHS(n, Ac, Bc)
    #form LHS
    rhs = RHS(n, Ac, r, lis)
    #form RHS
    soe = LRHS(n, lhs, rhs)
    #form soe
    pressure_distribution.append(thomasAlgorithm(n, soe))
    a =  a + 1


#convert results to a DataFrame
pressure_distribution_dict, block_widths, width = {}, [], dx
for k in range(n):
    det = "Block " + str(k + 1)
    _ = [i[k] for i in pressure_distribution]
    pressure_distribution_dict[det] = _
    block_widths.append([width for o in range(rt + 1)])
    width += dx    
    
pressure_dist_df = pd.DataFrame(pressure_distribution_dict,
index = index_names)


pressure_dist_df.to_excel("savedata/Pressure Distribution.xlsx", sheet_name = "Pressure Distribution", index = True)

newp = pressure_dist_df.transpose()


#plotting results
def pressure_time():
    """
    pressure against time plot.
    """
    for col in pressure_dist_df.columns:
        plt.plot(index_names, pressure_dist_df[col], label = col)
    plt.xlabel('Time(days)')
    plt.ylabel('Pressure(psi)')
    plt.title('Pressure distribution with time')
    plt.legend()
    plt.savefig("savedata/pressure_time.png")    
    plt.show()

def pressure_space():
    """
    pressure against space plot.
    """
    ut = 0
    for col in pressure_dist_df.columns:
        plt.plot(block_widths[ut],pressure_dist_df[col], label = col)
        ut += 1
    plt.xlabel('Block widths(ft)')
    plt.ylabel('Pressure(psi)')
    plt.title('Pressure distribution with space')
    plt.legend()
    plt.savefig("savedata/pressure_space.png")    
    plt.show()
    

#3D plot
def final_plot():
    """
    3D plot, pressure, time and space.
    """
    fig = plt.figure(figsize = (8, 8))
    ax = fig.gca(projection = '3d')

    x = np.array([index_names])
    y = np.array(block_widths)
    z = newp.values
    
    ax.plot_surface(x, y, z, cmap = cm.hot)
    plt.xticks(np.arange(0, 370, 30))
    plt.yticks(np.arange(0, 6000, 1000))
    plt.xlabel('Time step(days)')
    plt.ylabel('Blocks(ft)')    
    ax.set_zlabel('Pressure(psi)')
    plt.title('Plot of Pressure against Space and Time.')
    plt.savefig("savedata/pressure_space_time.png", orientation = "portrait", bbox_inches = "tight")
    plt.show()
    
    
#pressure_space()
#pressure_time()
final_plot()
