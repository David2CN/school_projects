#pgg503
#Refrigeration_Liquefaction_Project
#Heat Pump


"""
#subscripts
co = condensing
ev = evaporating

#variables
P = Pressure, MPa
T = Temperature, °C    #Converted to Kelvin in the calculations
H = Enthalpy, kJ/kg
S = Entropy, kJ/kg.K

#
CR = Compression Ratio
COP = Coefficient Of Performance

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

def CR(Pco, Pev):
    """
    To calculate the compression ratio.
                Pco
     CR =  -------
                Pev
    """
    return Pco / Pev
    

def COP(H1, H2, H3):
    """
    To calculate the coefficient of performance.
                    H2 - H1
     COP =    ------------
                    H3 - H2
    """
    return ((H2 - H1) / (H3 - H2))


def H3_(H4, Tco, S2, S4):
    """
    To calculate H3.
    H3 = H4 + Tco * (S2 - S4)
    """
    return H4 + ((Tco + 273) * (S2 - S4))


def interpo(x1, x2, x3, y2, y3):
    """
    Simple straight line interpolation.
    """
    y1 =y3 - (((x3 - x1) / (x3 - x2)) * (y3 - y2))
    return y1        


#Preparation of property table
properties = pd.read_csv("R170_properties.csv")
#To make the temperature values the index, so its easier to access the properties at different temperatures
indes = properties["Temperature"].values
properties = properties.drop("Temperature", axis = 1)
cols = properties.columns
properties = pd.DataFrame(properties.values, index = indes, columns = cols)


#All the necessary calculations
avail_temp = properties.index #temperature data available
#diffs is a list of Tco-Tev that can be gotten from the properties table.
#It is also based on each value having at least four datapoints.
diffs = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60]


fig = plt.figure(figsize = (7, 11))
ax = fig.add_subplot(111)

#Tco-Tev Plots
Rdata = pd.DataFrame()
for tcotev in diffs:
    tev = [i for i in avail_temp if i + tcotev in avail_temp]
    #This is to make sure that all Tev values chosen also have their corresponding Tco value in the properties table.

    data = pd.DataFrame()
    data["Tev"] = tev
    data["Tco-Tev"] = [tcotev for i in range(len(tev))]
    data["Tco"] = data["Tco-Tev"] + data["Tev"]
    data["Pev"] = [properties.loc[x, "Pressure"] for x in data["Tev"]]
    data["Pco"] = [properties.loc[x, "Pressure"] for x in data["Tco"]]
    data["H1"] = [properties.loc[x, "Enthalpy_liquid"] for x in data["Tco"]]
    data["H2"] = [properties.loc[x, "Enthalpy_vapor"] for x in data["Tev"]]
    data["H4"] = [properties.loc[x, "Enthalpy_vapor"] for x in data["Tco"]]
    data["S2"] = [properties.loc[x, "Entropy_vapor"] for x in data["Tev"]]
    data["S4"] = [properties.loc[x, "Entropy_vapor"] for x in data["Tco"]]
    data["H3"] = H3_(data["H4"], data["Tco"], data["S2"], data["S4"])
    data["COP"] = COP(data["H1"], data["H2"], data["H3"])
    data["CR"] = data["Pco"] / data["Pev"]
    data["dx"] = data["S2"] - data["S4"]

    temp = data[data["dx"] > 0] #To remove negative datapoints with negative values of S2-S4
    x = temp["Tev"]
    y = temp["COP"]
    
    #Table of Tev, COP, CR and Tco-Tev
    Rdata = pd.concat([Rdata, temp[["Tev", "COP", "CR", "Tco-Tev"]]], axis = 0, ignore_index = True) 

    #To get smooth lines.
    from scipy import interpolate
    xn = np.linspace(-175, -20, 100)
    splines = interpolate.make_interp_spline(x, y)
    yn = splines(xn)
    plt.plot(xn, yn, color = "black")
    #labelling the lines using the last point on the x-axis(-20) and  the last point on the y-axis
    yt = yn[-1]
    ax.text(-20, yt, str(tcotev) + "°C")
    

#CR Plots
points = [1.5, 1.7, 2.0, 2.3, 2.8, 3.3, 5.0]
for point in points:
    #rounding off CR values to 1 d.p.
    mask = Rdata["CR"].apply(lambda x : round(x, 1)) == point
    pdata = Rdata[mask]
    x = pdata["Tev"].values
    y = pdata["COP"].values
    
    #interpolation
    temp = len(x) // 2
    xn = pd.Series(np.linspace(-150, -20, 10))
    x2, x3, y2, y3 = (x[0]  + x[temp]) / 2, (x[-1] + x[temp]) / 2, (y[0] + y[temp]) / 2, (y[-1] + y[temp]) / 2    
    yn = xn.apply(lambda x : interpo(x, x2, x3, y2, y3))
    xn = xn.values
    yn = yn.values
    
    #angle for rotating text. Based on the triangle formed by the line with the x and y axes. not very efficient though.
    yx = abs(yn[0] - yn[-1])    
    ang = (math.atan(10 / yx) * (180 / math.pi)) - 90
    
    #labelling the CR lines
    plt.text(xn[5], yn[5] - 1.0,  "[CR] = " + str(point), rotation = ang, size = 13)
    plt.plot(xn, yn, label = str(point), color = "black")


ax.text(-18, 23,  "Temperature\nLift")
Rdata.to_csv("savedata/R170data.csv", index = False)
ax.set_facecolor("xkcd:light peach")
plt.xticks(np.arange(-170, -15, 10))
plt.yticks(np.arange(1, 24.5, 1))        
plt.xlim(-150, -20)
plt.ylim(0.5, 24)
plt.xlabel("Evaporating Temperature, Tev, °C")
plt.ylabel("Theoretical Rankine Coefficient of Performance, COP, Dimensionless")
plt.title("THEORETICAL RANKINE COEFFICIENT OF PERFORMANCE\nAGAINST EVAPORATING TEMPERATURE FOR R170\nFOR A RANGE OF -150°C TO -20°C")
plt.savefig("savedata/R170_plot.png", orientation = "portrait", bbox_inches = "tight")
plt.show()

