



import deepSI
from deepSI.systems.system import System, System_deriv, System_data
import numpy as np
from gym.spaces import Box


class Ball_in_box(System_deriv): #discrate system single system
    """docstring for double_well_system

    dvxdt = (1/x**2-1/(1-x)**2)/200+ux-self.gamma*vx
    dvydt = (1/y**2-1/(1-y)**2)/200+uy-self.gamma*vy
    """
    def __init__(self, Fmax=0.25, Nresist=0.7):
        '''Noise, system setting and x0 settings'''
        self.Fmax = Fmax
        dt = 2*np.pi/20 #20 points in the sin
        self.gamma = Fmax*dt/0.1 # ux*dt/gamma = X=0.1
        super(Ball_in_box, self).__init__(dt=dt,nx=2)
        self.action_space = Box(float(-1),float(1),shape=(2,))

    def reset_state(self):
        self.x = [0.5,0.5,0,0] #[x,y,vx,vy]

    def deriv(self,x,u): #will be converted by 
        ux,uy = np.clip(u,-1,1)*self.Fmax
        x,y,vx,vy = x
        dvxdt = (1/x**2-1/(1-x)**2)/200+ux-self.gamma*vx
        dvydt = (1/y**2-1/(1-y)**2)/200+uy-self.gamma*vy
        return [vx,vy,dvxdt,dvydt]

    def h(self,x,u):
        return x[0],x[1] #return position

class Ball_in_box_video(Ball_in_box): #discrate system single system
    """docstring for double_well_system

    V(x) = 1/2*min((x-a)**2,(x+a)**2)
    v' = -(x-a) if x>0 else (x+a) + u #+ resistance 
    x' = v
    Fmax < a
    Fmin > -a
    """
    def __init__(self, Fmax=0.25, image_height=25, image_width=25):
        self.image_height, self.image_width = image_height, image_width
        super(Ball_in_box_video, self).__init__(Fmax=Fmax)
        self.observation_space = Box(0.,1.,shape=(self.image_height,self.image_width))

    def h(self,x,u):
        # A = np.zeros((self.image_width,self.image_height))
        Y = np.linspace(0,1,num=self.image_height)
        X = np.linspace(0,1,num=self.image_width)
        X,Y = np.meshgrid(X,Y)
        # self.X = X[y,x]
        r = 0.22
        A = np.clip((r**2-(X-x[0])**2-(Y-x[1])**2)/r**2,0,1)
        return A #return position

if __name__ == '__main__':
    sys = Ball_in_box_video() 
    exp = System_data(u=[sys.action_space.sample() for i in range(1000)])
    print(sys.action_space.low)
    sys_data = sys.apply_experiment(exp)

    sys_data.to_video(file_name='test')
