import bpy
import mathutils





def resetColors():
    #reset rgb values to 0.5
    i = 0
    for poly in mesh.data.polygons:
        for idx in poly.loop_indices:
            rgb = [0.5 for i in range(3)]
            color_layer.data[i].color = rgb
            i+= 1


def paintVert(particle,vertex,color):
    #paint vertex
    for poly in mesh.data.polygons:
        for i,index in enumerate(poly.vertices):
            if vertex.index == index:
                loop_index = poly.loop_indices[i]
                color_layer.data[loop_index].color = color
                
              


def vertexToPaint(particle):
    #find vertex closest to particle
    loc = particle.hair_keys[0].co
    pDistance = []
    for i,vert in enumerate(mesh.data.vertices):
        pDistance.append((loc - vert.co).length)
    cVertIndex = pDistance.index(min(pDistance))
    cVert = mesh.data.vertices[cVertIndex]
    return cVert
        
        
def particleColor(particle,vertex):
    #determine particle color by the vector between normal and third hair key
  
    hkl = particle.hair_keys[2].co
    
    hkl = hkl - vertex.co
    hkl = mathutils.Vector([i/hkl.magnitude for i in hkl])
    
    
    normal = mathutils.Vector([i/vertex.normal.magnitude for i in vertex.normal])
  
    xyz = hkl - normal

    rgb = [round((i/2 + 0.5),3)for i in xyz] 

    return rgb


#main


mesh = bpy.context.active_object
pSystem = mesh.particle_systems['ParticleSystem']


#Assume vertex color layer exists with name "Col"
color_layer = mesh.data.vertex_colors["Col"]

resetColors()

nParticles = len(pSystem.particles)

for i,part in enumerate(pSystem.particles):
    
    vert= vertexToPaint(part)
    col = particleColor(part,vert)
    paintVert(part,vert,col)
    
    print("{} %".format(round((i/nParticles),3)*100),end='\r')

    
    
bpy.ops.object.mode_set(mode = 'VERTEX_PAINT')
