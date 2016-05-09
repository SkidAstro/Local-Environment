from collections import namedtuple
from operator import attrgetter
import re
import math
import sys

H0 = 67.80
C = 299792.458
PI = 3.1415927

gal = namedtuple("galaxy", "ThingID RA DEC Z")


gals = []


cat_fn = sys.argv[1]

out_fn = sys.argv[2]

out_file = open(out_fn, "w")
out_file.write("# 	ThingID    RA      DEC      Z        3rd_Density       Avg_N_Density\n")

def third_density(lis,target):
    "This function calculates the distance to the third nearest neighber from a target galaxy"
    nei_dist =[]
    density =0 
    for g in lis:        
        if abs((g.Z*(3*10e5))-(target.Z*(3*10e5))) <= 500 :
            dist = abs(calc_dist(target,g))
            nei_dist.append(dist)
  
    nei_dist.sort()

    if len(nei_dist) >= 4:
	density = density_calc(3,nei_dist[3])

    return density

def density_calc(i,R):
    "This function calculates the density based on the distance to the ith nearest galaxy"
    if R != 0:
        NND = i/(PI*(R**2))
    else:
        NND = 0
    return NND

def avg_density(lis,target,i,j):
    "This function calculates the average density of the ith to jth nearest neighbors from a target galaxy"
    nei_dist = []
    density = 0
    avg_density = 0
    for g in lis:
        if abs((g.Z*(3*10e5))-(target.Z*(3*10e5))) <= 500 :
            dist = abs(calc_dist(target,g))
            nei_dist.append(dist)
  
    nei_dist.sort()
    if len(nei_dist) >= j+2:
        for x in range(i+1,j+1):
	    density += density_calc(x,nei_dist[x])
	    
        avg_density = density/9
		
    return avg_density

def distances(lis,target):
    dx_diff =[]
    for g in lis:        
        if abs((g.Z*(3*10e5))-(target.Z*(3*10e5))) <= 500 :
            ax = (target.RA)*PI/180
	    bx = (g.RA)*PI/180
            dx = abs(ax-bx)	
            dx_diff.append(dx)
    dx_diff.sort()	
    print str("shortest: ") + str(dx_diff[1])+ str(",  longest: ") + str(dx_diff[len(dx_diff)-1])

    return 0		
 

def calc_dist(a,b):
    "This function calculates the haversine distance between two galaxies."
    ax = (a.RA)*PI/180
    ay = (a.DEC)*PI/180
    bx = (b.RA)*PI/180
    by = (b.DEC)*PI/180   
    dx = abs(ax-bx)
    
    dy = abs(ay-by)
        
    p1 = math.sin(dy/2)*math.sin(dy/2)
    p2 = math.cos(ay)*math.cos(by)*(math.sin(dx/2)*math.sin(dx/2))
    theta = 2*math.asin(math.sqrt(p1+p2))
    
    V = a.Z*(3*10e5)

    dist = 2*math.sin(theta/2)*V/H0
    
    return dist


def main():    
        
    with open(cat_fn) as cat_file:
        lines = cat_file.readlines()
    
    for line in lines:
        line = line.rstrip(' \t\r\n\0')
        line = line.lstrip(' \t\r\n\0')
       
        entries = re.split(",| +\t*", line)

        gals.append(gal(float(entries[0]), float(entries[1]), float(entries[2]), 
                    float(entries[3])))
    
    for g in gals:
       Avg_NND = avg_density(gals,g,2,10)       		
       third_NND = third_density(gals,g)
          
       out_file.write(str(g.ThingID)+ "      " + str(g.RA) + "      " + str(g.DEC)+ "        " + str(g.Z) +"         "+ str(third_NND)+ "       "+ str(Avg_NND)+"\n")
    out_file.close()

if __name__ == "__main__":
    main()

    
            
