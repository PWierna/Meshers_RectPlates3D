import sys                                                                
import numpy as np                                                        
import meshio                                     
import sys                                          
                                                    
original_stdout = sys.stdout #Original standard output                    
                                                    
                                   
#·# PARSE INPUT DATA 
inputfile= str(input('\nEnter .msh file name/path (include .msh extension): '))    
inputmsh = meshio.read(inputfile)    
N_COORD  = inputmsh.points                    #Nodal coordinates    
CONECT   = inputmsh.cells_dict["quad9"]  #Conectivities    
NPE = 9   #Nodes per element in hexahedron    


#·# BUILD CONNECTIVITIES AND COORDINATES MATRICES
# Build Connectivities Matrix
element_nodes = 1 + CONECT #pyth indices start in 0 & nªnod must start in 1
print('Element nodes')
print(element_nodes)
num_elements  = np.shape(element_nodes)[0] #Number of elements
print('\n'+18*'-'+' {0} 9-NODED QUAD ELEMENTS DETECTED '.format(num_elements)+18*'-'+'\n')
Elements = np.zeros([num_elements , NPE+1]) #Add aditional column(mat type)
Elements[:,0]  = 1  #1st Column = Layer /Material number
Elements[:,1:] = element_nodes   #Connectivity

print(Elements)

# Build Coordinates Matrix
Nodes = N_COORD 
print(Nodes)


#·# WRITE OUTPUT (.txt file)
with open('Connectivities_and_Coordinates_Eq2D.txt','w') as f:
    sys.stdout = f #Change the standard output to the file created

    print('\nMACRO_MODEL.Conectivity = [\n')
    #np.set_printoptions(threshold=sys.maxsize)
    #print(Elements)
    for row in range(0, np.shape(Elements)[0]):
        print('{0:>6}\t{1:>6}\t{2:>6}\t{3:>6}\t{4:>6}\t{5:>6}\t{6:>6}\t{7:>6}\t{8:>6}\t{9:>6}'.format(int(Elements[row,0]),int    (Elements[row,1]),int(Elements[row,2]),int(Elements[row,3]),int(Elements[row,4]),int(Elements[row,5]),int(Elements[row,6]),int(Elements[row,7]),int(Elements[row,8]),int(Elements[row,9])))

    print('\n];')
    print('\nMACRO_MODEL.Coordinates = [\n')
    for row in range(0, np.shape(Nodes)[0]):
        print('{0:>6}\t{1:>6}'.format(Nodes[row,0],Nodes[row,1]))
    print('\n];')



