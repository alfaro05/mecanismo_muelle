import math
import numpy
import matplotlib.pyplot as plt 
import os

def angles(input_angle):
    return(input_angle, 0, input_angle)

def position_tuple(link_len, link_angle):
    return(link_len*math.cos(link_angle),link_len*math.sin(link_angle))

class Link:
    speed = (0,0)
    #absolute speed of one of the endpoints of the link 
    ep_rel_speed = (0,0)
    #relative speed of the other endpoint
    def __init__(self, link_len, link_angle):
        self.length = link_len
        self.angle = link_angle
    def print_node_speed(self, in_letter):
        print(f"The speed of node {in_letter} is:")
        print(f"({self.speed[0]+self.ep_rel_speed[0]:.2f},{self.speed[1]+self.ep_rel_speed[1]:.2f})")
    def get_node_speed(self):
        return(self.speed[0]+self.ep_rel_speed[0],self.speed[1]+self.ep_rel_speed[1])

class Mechanism:
    def __init__(self, in_angle, l2, l3, l4, water_height):
        links_angles = angles(in_angle)
        self.link2 = Link(l2, links_angles[0])
        self.link3 = Link(l3, links_angles[1])
        self.link4 = Link(l4, links_angles[0])
        self.set_position()
        self.water_level = water_height
        self.water_intersection = (0,0)
        self.can_be_reached = False

    def update_angle(self,in_angle):
        links_angles = angles(in_angle)
        self.link2.angle = links_angles[0]
        self.link3.angle = links_angles[1]
        self.link4.angle = links_angles[2]
        self.set_position()
    
    def set_speed(self, omega_in):
        self.link2.ep_rel_speed = (-self.link2.length*omega_in*math.sin(self.link2.angle),
                            self.link2.length*omega_in*math.cos(self.link2.angle)) 
        self.link3.speed=self.link2.ep_rel_speed
        self.link4.ep_rel_speed = (0,0)
        self.omega = omega_in

    def print_speeds(self):
        self.link2.print_node_speed('A')
        self.link3.print_node_speed('B')
        self.link4.print_node_speed('C')

    def get_speeds(self):
        link2_speed = self.link2.get_node_speed()
        return(link2_speed, self.link3.get_node_speed(),self.link4.get_node_speed(),
               link2_speed)

    def set_position(self):
        self.posA = position_tuple(self.link2.length,self.link2.angle)
        rel_posB = position_tuple(self.link3.length,self.link3.angle)
        rel_posP = position_tuple(0.5*self.link3.length,self.link3.angle)
        self.posB = (rel_posB[0]+self.posA[0],rel_posB[1]+self.posA[1])
        self.posP = (rel_posP[0]+self.posA[0],rel_posB[1]+self.posA[1])
        self.posC = (self.link3.length,0)
    
    def print_positions(self):
        print("The position of each node is:")
        print("Node A: "+f"({self.posA[0]:.2f},{self.posA[1]:.2f})")
        print("Node B: "+f"({self.posB[0]:.2f},{self.posB[1]:.2f})")
        print("Node C: "+f"({self.posC[0]:.2f},{self.posC[1]:.2f})")
        print("P: "+f"({self.posP[0]:.2f},{self.posP[1]:.2f})")
    
    def get_positions(self):
        nodeA = (self.posA[0],self.posA[1])
        nodeB = (self.posB[0],self.posB[1])
        nodeC = (self.posC[0],self.posC[1])
        P = (self.posP[0],self.posP[1])
        return(nodeA, nodeB, nodeC, P)

    def set_acceleration(self, alpha):
        tan_acceleration = (-self.link2.length*alpha*math.sin(self.link2.angle),
                                self.link2.length*alpha*math.cos(self.link2.angle))
        norm_acceleration = (-(self.omega**2)*self.link2.length*math.cos(self.link2.angle),
                                  -(self.omega**2)*self.link2.length*math.sin(self.link2.angle))
        self.acceleration = (tan_acceleration[0]+norm_acceleration[0],
                             tan_acceleration[1]+norm_acceleration[1])
    def print_acceleration(self):
        print("The acceleration of A, B and P is:")
        print(f"({self.acceleration[0]:.2f},{self.acceleration[1]:.2f})")

    def get_acceleration(self):
        return(self.acceleration[0],self.acceleration[1])

    def generate_array(self, initial_angle, final_angle):
        x_coord = numpy.array([])
        y_coord = numpy.array([])
        theta_array = numpy.arange(initial_angle, final_angle, 0.001)
        for theta in theta_array:
            self.update_angle(theta)
            self.set_position()
            x_coord = numpy.append(x_coord, self.posP[0])
            y_coord = numpy.append(y_coord, self.posP[1])
        #get the coordinates of the intersection with the surface
        count = 0
        stop_flag = True
        while(count<len(y_coord) and stop_flag):
            if(y_coord[count]+self.water_level < 0.01):
                stop_flag = False
            count +=1
        self.can_be_reached = not(stop_flag)
        #if can_be_reached == True, the boat can be lifted from the water 
        self.water_intersection = (float(x_coord[count-1]),float(y_coord[count-1]))
        #Update the coordinates of the intersection of P and the surface,
        #this value is only valid if can_be_reached == True   
        return(x_coord, y_coord)
    
    def create_plot(self, init_ang, final_ang):
        position_tuple = self.generate_array(init_ang, final_ang)
        quay_array = numpy.arange(0,position_tuple[0].max())
        #list comperhension generated numpy array, for y=0:
        zero_array = numpy.array([0 for i in range(len(quay_array))])
        plt.plot(position_tuple[0], position_tuple[1], color = 'tab:blue', label="Curva de acoplador")
        plt.plot(quay_array, zero_array, color = 'tab:red', label="Ubicación del muelle")
        plt.xlabel("x(m)")
        plt.ylabel("y(m)")
        plt.title('Curva de acoplador')
        plt.legend()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if(os.path.exists(dir_path+'/static/img/plot.png')):
            print("borramos el gorro!!!")
            os.remove(dir_path+'/static/img/plot.png')
        plt.savefig('interfaz/static/img/plot.png')
        plt.close()

if(__name__=="__main__"):
    #code for testing
    meca = Mechanism(2.5, 3, 2, 3, 4)
    meca.set_speed(20)
    meca.set_acceleration(5)
    meca.print_positions()
    meca.print_acceleration()
    print(meca.generate_array(0,5)[0])
    meca.create_plot(0,5)