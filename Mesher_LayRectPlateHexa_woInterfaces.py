import gmsh
import numpy as np


#·# INPUTS ----------------------------------------------------------------------------- #

# In-Plane Parameters:
XELEM = 32 #Must be even (to get a point at the central line)
YELEM = 32 #Must be even (to get a point at the central line)
LX = 1000#1000
LY = 1000

# Through-the-thickness Parameters:

#EpL  = np.array([ 2, 2, 2, 2, 2 ]) #Number of elements
#thickness = np.array([ 10.0, 5.0, 5.0, 5.0, 10.0 ])

EpL  = np.array([ 6,6,6,6 ])#np.array([ 10, 10, 10 ]) #Number of elements
thickness = np.array([ 10 , 50 , 30 , 10 ])

#·# ------------------------------------------------------------------------------------ #



#·# 1st COMPUTATIONS    
NLay = np.shape(EpL)[0]  #Number of layers
nelemZ = np.sum( EpL )   #Through-the-thickness discretization 
TH = np.sum(thickness)   #Total thickness
nelements = XELEM*YELEM*nelemZ  #Number of elements 



#·# IN-PLANE GEOMETRY DEFINITION 
v1 = np.array([0,0])     #Vertex1 
v2 = np.array([LX,0])    #Vertex2 
v3 = np.array([LX,LY])	 #Vertex3 
v4 = np.array([0,LY])    #Vertex4 

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add('ClampedRect{0}x{1}_{2}el'.format(LX,LY,nelements))

#Points defining the in-plane rectangle
p1 = gmsh.model.geo.addPoint(v1[0],v1[1],0)
p2 = gmsh.model.geo.addPoint(v2[0],v2[1],0)
p3 = gmsh.model.geo.addPoint(v3[0],v3[1],0)
p4 = gmsh.model.geo.addPoint(v4[0],v4[1],0)

#Lines defining the in-plane rectangle
l1 = gmsh.model.geo.addLine(p1,p2) #Horizontal
l2 = gmsh.model.geo.addLine(p2,p3) #Vertical
l3 = gmsh.model.geo.addLine(p3,p4) #H
l4 = gmsh.model.geo.addLine(p4,p1) #V
gmsh.model.geo.mesh.setTransfiniteCurve(l1,(XELEM+1)) #Horizontal
gmsh.model.geo.mesh.setTransfiniteCurve(l3,(XELEM+1)) #Horizontal
gmsh.model.geo.mesh.setTransfiniteCurve(l2,(YELEM+1)) #Vertical  
gmsh.model.geo.mesh.setTransfiniteCurve(l4,(YELEM+1)) #Vertical  

#In-Plane Curve Loop and First Surface:
cl = gmsh.model.geo.addCurveLoop([l1,l2,l3,l4])
sf = gmsh.model.geo.addPlaneSurface([cl])

gmsh.model.geo.synchronize()

#Set original In-Plane Surface as transfinite:
gmsh.model.geo.mesh.setTransfiniteSurface(sf)
gmsh.model.geo.mesh.setRecombine(2, sf)



#·# EXTRUSION 

SFCount = np.arange(NLay+2) #Initialize surface counter (1st surface has tag = 0)

#Create 3D model from the sequential extrusion of plane surfaces:
for i in range(0,NLay):
    
    #Extrude from last surface:
    ext = gmsh.model.geo.extrude([(2, SFCount[i+1])], 0, 0, thickness[i] , numElements=[EpL[i]] , recombine=True)

    #Overwrite Surface Counter (Top surface recently created will be used as bottom sf for
    #the next extrusion):
    SFCount[i+2] = ext[0][1]

    #Assign a New Physical Group for the created Volume(Layer)
    gmsh.model.addPhysicalGroup(3 , [ext[1][1]], i)



#·# MESH

gmsh.model.geo.synchronize()

gmsh.option.setNumber('Mesh.RecombineAll',1)
gmsh.model.mesh.generate(3)
gmsh.option.setNumber('Mesh.SurfaceFaces',1)
gmsh.option.setNumber('Mesh.Points',1)
gmsh.write('RectLayeredBeam3D{0}x{1}x{2}_{3}el.msh'.format(round(LX),round(LY),round(TH),nelements))
gmsh.fltk.run()
gmsh.finalize()





