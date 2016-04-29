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
out_file.write("# ThingID    RA      DEC      Z        Density\n")

def third_dist(lis,target):
    "This function calculates the distance to the third nearest neighber from a target galaxy"
    nei_dist =[]
    for g in lis:        
        if abs((g.Z*(3*10e5))-(target.Z*(3*10e5))) <= 500 :
            dist = abs(calc_dist(target,g))
            nei_dist.append(dist)
  
    nei_dist.sort()

    if len(nei_dist) >= 4:
	dist_3 = nei_dist[3]
    else:
	dist_3 = 0
    
    return dist_3

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
    
    #print dist

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
       #+f = distances(gals,g)
       		
       d = third_dist(gals,g)
       if(d!= 0):
	NN_density = 3/(PI*(d**2))
       else:
	NN_density = 0	
       
       out_file.write(str(g.ThingID)+ " " + str(g.RA) + " " + str(g.DEC)+ " " + str(g.Z) +" "+ str(NN_density)+ "\n")
    out_file.close()

if __name__ == "__main__":
    main()

    
            
