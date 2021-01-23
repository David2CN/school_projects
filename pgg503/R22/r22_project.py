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
    

#Preparation of property table
properties = pd.read_csv("R22_properties.csv")
indes = properties["Temperature"].values
properties = properties.drop("Temperature", axis = 1)
cols = properties.columns
properties = pd.DataFrame(properties.values, index = indes, columns = cols)


avail_temp = properties.index #temperature data available
diffs = [20, 22, 24, 26, 28, 30, 36, 38, 40, 46, 48, 50, 60] #various Tco-Tev

fig = plt.figure(figsize = (7, 11))
ax = fig.add_subplot(111)

#Tco-Tev Plots
Rdata = pd.DataFrame()
for tcotev in diffs:
    tev = [i for i in avail_temp if i + tcotev in avail_temp]

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

    temp = data[data["dx"] > 0]
    x = temp["Tev"]
    y = temp["COP"]
    
    #Table of Tev, COP, CR and Tco-Tev
    Rdata = pd.concat([Rdata, temp[["Tev", "COP", "CR", "Tco-Tev"]]], axis = 0, ignore_index = True) 

    #To get smooth lines.
    from scipy import interpolate
    xn = np.linspace(-70, 30, 20)
    splines = interpolate.make_interp_spline(x, y)
    yn = splines(xn)
    ax.text(30, yn[-1], str(tcotev) + "°C")
    ax.plot(xn, yn, color = "black")    
    

#CR Plots
points = [2.04, 2.11, 2.29, 2.57, 2.76, 2.98, 3.37, 4.37]
for point in points:
    #rounding off CR values to 1 d.p.
    mask = Rdata["CR"].apply(lambda x : round(x, 2)) == point
    pdata = Rdata[mask]
    x = pdata["Tev"].values
    y = pdata["COP"].values

    #interpolation to get smooth lines
    xn = np.linspace(-70, 30, 150)
    splines = interpolate.make_interp_spline(x, y)
    yn = splines(xn)
    
    #for labelling the lines; not very efficient.
    yx = abs(yn[0] - yn[-1])
    ang = (math.atan(10 / yx) * (180 / math.pi)) - 90
    ax.text(-20, yn[90], "[CR] = " + str(round(point, 1)), rotation = ang, size = 14)
    ax.plot(xn, yn, color = "black")


ax.text(31, 13.5,  "Temperature\nLift")
Rdata.to_csv("savedata/R22data.csv", index = False)
ax.set_facecolor("xkcd:light peach")
plt.xticks(np.arange(-70, 35, 10))
plt.yticks(np.arange(2, 13.7, 1))        
plt.xlim(-70, 30)
plt.ylim(2.5, 13.7)
plt.xlabel("Evaporating Temperature, Tev, °C")
plt.ylabel("Theoretical Rankine Coefficient of Performance, COP, Dimensionless")
plt.title("THEORETICAL RANKINE COEFFICIENT OF PERFORMANCE\nAGAINST EVAPORATING TEMPERATURE FOR R22\nFOR A RANGE OF -70°C TO 30°C")
plt.savefig("savedata/R22_plot.png", orientation = "portrait", bbox_inches = "tight")
plt.show()
