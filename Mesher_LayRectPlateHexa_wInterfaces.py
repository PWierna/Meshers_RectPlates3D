import gmsh
import numpy as np

#·# Inputs ------------------------------------------------------------

LX = 1000      #Beam's Length (X axis)
LY = 1000      #Beam's Length (Y axis)
nelemX = 32  #Number of elements in the X direction
nelemY = 32  #Number of elements in the Y direction

#Vector with thickness of each layer:
#thick_n0 = np.array([10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30,10/30])
#thick_n0 = np.array([0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8 ])
thick_n0 = np.array([ 10 , 50 , 30 , 10 ])

#Vector with number of elements for each layer (Y-Direction):
#nelem_n0 = np.array([3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
#nelem_n0 = np.array([2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2])
nelem_n0 = np.array([ 6,6,6,6 ])

#Interface-to-Laminate thickness ratio:
interf_ratio = 1/1000

#Number of elements through-the-thickness for interfaces:
npi = 1

#·# -------------------------------------------------------------------


#·# 1st parameters computation
tthick0 = np.sum( thick_n0 )        #Original Total thickness
n_lay0  = np.shape(thick_n0)[0]     #Original Nº of layers (w/o interf)
tthick  = tthick0*(1+interf_ratio*(n_lay0-1)) #Total thickness (w/interf)
n_lay   = 2*np.shape(thick_n0)[0]-1 #Total Number of layers (w/interf)
thick_i = tthick0 * interf_ratio    #Thickness of the interfaces

#Vector with thicknesses
thick_n = np.zeros(n_lay)
thick_n[0:n_lay:2] = thick_n0
thick_n[1:n_lay:2] = thick_i
nelem_n = np.zeros(n_lay,dtype=int)
nelem_n[0:n_lay:2] = nelem_n0
nelem_n[1:n_lay:2] = npi

ind_int = np.arange(1,n_lay,2) #Interfaces index

nelem  = np.sum( nelem_n ) * nelemX * nelemY    #Total number of elements 
z0     = tthick / 2                             #Middle coordinate

PCount  = np.arange( 2*n_lay + 2 )+1    #Counter layer vertices
TLCount = np.arange( 2*n_lay )+1        #Counter Transversal Lines
LLCount = np.arange(n_lay+1)+2*n_lay+1  #Counter Longitudinal Lines
CLCount = np.arange( n_lay )+1          #Counter Curve Loops 
SCount  = np.arange( n_lay )+1          #Counter Surfaces 

#·# Initialize Geometric Model and Mesh Algorithm
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add('LayeredBeam2DQuad_{0}elem'.format(nelem))

#Create vertex points for the In-Plane rectangle 
p1 = gmsh.model.geo.addPoint( +LX/2 , -LY/2 , -z0 , 1 )
p2 = gmsh.model.geo.addPoint( +LX/2 , +LY/2 , -z0 , 1 )
p3 = gmsh.model.geo.addPoint( -LX/2 , +LY/2 , -z0 , 1 )
p4 = gmsh.model.geo.addPoint( -LX/2 , -LY/2 , -z0 , 1 )

#Create In-Plane Lines for the rectangle
l1 = gmsh.model.geo.addLine( p1 , p2 ) 
l2 = gmsh.model.geo.addLine( p2 , p3 ) 
l3 = gmsh.model.geo.addLine( p3 , p4 ) 
l4 = gmsh.model.geo.addLine( p4 , p1 ) 

#Set In-Plane lines as transfinite
gmsh.model.geo.mesh.setTransfiniteCurve( l1 , nelemY+1 )
gmsh.model.geo.mesh.setTransfiniteCurve( l3 , nelemY+1 )
gmsh.model.geo.mesh.setTransfiniteCurve( l2 , nelemX+1 )
gmsh.model.geo.mesh.setTransfiniteCurve( l4 , nelemX+1 )

#Create In-Plane Curve-Loop and Surface
cl1 = gmsh.model.geo.addCurveLoop( [l1,l2,l3,l4] )
s1  = gmsh.model.geo.addPlaneSurface( [cl1] )


#Synchronize model and recombine surfaces
gmsh.model.geo.synchronize()

gmsh.model.geo.mesh.setTransfiniteSurface( s1 )
gmsh.model.geo.mesh.setRecombine( 2, s1 )


#Create 3D model from the sequential extrusion of plane surfaces:
SFCount = np.arange(n_lay+2) #Initialize surface counter (1st surface has tag = 0
for i in range(0,n_lay):
    #Extrude from last surface:
    ext = gmsh.model.geo.extrude([(2, SFCount[i+1])], 0, 0, thick_n[i] , numElements=[nelem_n[i]] , recombine=True)
    #Update surface counter
    SFCount[i+2] = ext[0][1]
    #Assign a New Physical Group for the created Volume(Layer)
    gmsh.model.addPhysicalGroup(3 , [ext[1][1]], i)

#Add last Physical Gruop with all Interfaces:
gmsh.model.addPhysicalGroup(3 , ind_int+1 , n_lay )

#Synchronize model 
gmsh.model.geo.synchronize()


gmsh.option.setNumber('Mesh.RecombineAll',1)
gmsh.model.mesh.generate(3)
gmsh.option.setNumber('Mesh.SurfaceFaces',1)
gmsh.option.setNumber('Mesh.Points',1)
gmsh.write('RectLayPlate3D_{0}elem.msh'.format(nelem))
gmsh.fltk.run()
gmsh.finalize()

#Show interfaces conectivity:
print("")
print("INTERFACES:")
print(ind_int + 1)




