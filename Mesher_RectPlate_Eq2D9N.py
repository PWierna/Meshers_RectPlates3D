import gmsh
import numpy as np

#·# Inputs ------------------------------------------------------------

LX = 100       #Beam's Length (X axis)
LY = 100       #Beam's Length (Y axis)
nelemX = 20  #Number of elements in the X direction
nelemY = 20  #Number of elements in the Y direction


#·# -------------------------------------------------------------------

nelem = nelemX * nelemY

#·# Initialize Geometric Model and Mesh Algorithm
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add('LayeredBeam2DQuad_{0}elem'.format(nelem))

#Create vertex points for the In-Plane rectangle 
p1 = gmsh.model.geo.addPoint( +LX/2 , -LY/2 , 0 , 1 )
p2 = gmsh.model.geo.addPoint( +LX/2 , +LY/2 , 0 , 1 )
p3 = gmsh.model.geo.addPoint( -LX/2 , +LY/2 , 0 , 1 )
p4 = gmsh.model.geo.addPoint( -LX/2 , -LY/2 , 0 , 1 )

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


#Synchronize model 
gmsh.model.geo.synchronize()


gmsh.option.setNumber('Mesh.RecombineAll',1)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(2)
gmsh.option.setNumber('Mesh.SurfaceFaces',1)
gmsh.option.setNumber('Mesh.Points',1)
gmsh.write('EqRectPlate2D_{0}elem.msh'.format(nelem))
gmsh.fltk.run()
gmsh.finalize()





