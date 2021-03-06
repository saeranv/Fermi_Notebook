import numpy as np
import pandas as pd
import bash_epw
import math

import matplotlib.pyplot as plt
import matplotlib


#Define graph constants
plt.xlabel('Hr')
plt.ylabel('E (mWh)')
plt.title("Wind Energy (mWh) by Hour")
plt.grid()
plt.axis([0,8760,0,1000])

def main():
    bash_epw.set_uwg()
    uwg = bash_epw.main()
    epw = uwg.weather
    pp = bash_epw.pp

    #doc = epw.__doc__

    # windshare specs
    turbine_ht_array = [25.,45.,65.]#np.arange(25.)#15.,60.,15.)   # m
    turbine_radius_array = [3.,6,21.]#25. # m length of blade

    #turbine_swept_area = 7.5  # m2
    #turbine_dir = 3*math.pi/2. # West in radians
    z0r = 0.25
    von_karman = 0.4
    zero_plane = 0.05#0.75*16.
    air_density = 1.225     #kg/m3
    perf_coef = 0.4 # performance coefficient
    #wind_prof = uwg.RSM.windProf
    x_val = np.array(range(8760))

    #v_z = lambda v_epw: v_epw * math.ln((turbine_ht-zero_plane)/z0)/von_karman

    u_spd = np.array(epw.staUmod) # m/s
    u_dir = np.array(map(lambda d: d*math.pi/180., epw.staUdir)) # deg to radians


    def Pcalc(turbine_diameter, v_z_):
        return (0.125 * air_density * math.pi * math.pow(turbine_diameter,2) * math.pow(v_z_,3) * perf_coef) / 1000.0 # Power (kW) at time step t
    def Ucalc(turbine_ht_, i_):
        # Apparently wind turbines can rotate to the wind....
        v = u_spd[i_] * ((math.log(turbine_ht_/0.5)) / (math.log(10.0/0.5))) # from LB
        if turbine_radius > 3:
            v = abs(v * math.sin(u_dir[t + 1]))   # account for direction of wind
        return v

    h = 1 # infinitisemal timestep
    #print wind_prof
    # Forward Euler method to calculate wind differential
    # https://www.engineeringtoolbox.com/wind-power-d_1214.html
    for i in xrange(len(turbine_ht_array)):

        for j in xrange(len(turbine_radius_array)):

            P = np.zeros(8760)
            E = np.zeros(8760)
            V = np.zeros(8760)

            turbine_ht = turbine_ht_array[i]
            turbine_radius = turbine_radius_array[j]

            V[0] = Ucalc(turbine_ht, 0)
            P[0] = Pcalc(turbine_radius*2,V[0])
            E[0] = P[0]*h


            for t in xrange(0,8760-1):

                # from uwg
                #v_z = (u_spd[t + 1]/von_karman)  * math.log((turbine_ht-zero_plane)/z0r)
                # from lb
                #vMet * ((math.log(height/roughness_length)) / (math.log(refH/metrl)))
                #station_roughness_length = 0.1
                #reference_roughness_length = 0.5?
                V[t+1] = Ucalc(turbine_ht,t+1)

                #P[t+1] = (0.5 * v_z**3 * air_density * turbine_swept_area) * perf_coef / 1000.0 # Power (kW) at time step t
                P[t+1] = Pcalc(turbine_radius*2, V[t+1])
                E[t+1] = E[t] + h * P[t] # kWh
                # Should be approx 650 kWh at 12 m/s
                #if turbine_radius > 15 and turbine_ht > 55:
                    #print 'tblade={} & tht={}'.format(turbine_radius, turbine_ht)
                    #print P[t+1], round(V[t+1],2), abs(math.sin(u_dir[t+1]))

            print "turb_ht={},turb_blade={} | ".format(turbine_ht,turbine_radius),
            print round(E[-1],2), "kWh,", round(E[-1]/5000.0,2)

            #wdf = pd.DataFrame({"E":E,"P":P, "V":V})
            #print wdf.head
            #print wdf.tail

            V = map(lambda v: v*10, V)
            E = map(lambda x: x/1000.0, E)

            label_str = "turb_ht={},turb_blade={}".format(turbine_ht,turbine_radius)
            plt.plot(x_val, E, label = label_str)
            plt.legend()
            #plt.plot(range(8760),P,'r')
    #plt.plot(range(8760),V,'k')
    plt.show() # ctrl w to close

    return epw

if __name__ == "__main__":
    epw = main()
