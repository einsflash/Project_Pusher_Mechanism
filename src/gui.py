from four_bar_linkage import FourBarLinkage
import tkinter as tk
import numpy as np
        
class ResizableCanvas(tk.Canvas):
  def __init__(self, parent, **kwargs):
    tk.Canvas.__init__(self, **kwargs)
    self.bind("<Configure>", self.resize)
    self.height = self.winfo_reqheight()
    self.width = self.winfo_reqwidth()
    self.scale = [self.width/self.winfo_screenwidth(), self.height/self.winfo_screenheight()]

  def resize(self,event):
    # determine scale factors
    wscale = float(event.width)/(self.width*self.scale[0])
    hscale = float(event.height)/(self.height*self.scale[1])
    self.width = round(event.width*self.scale[0])
    self.height = round(event.height*self.scale[1])
    # resize the canvas 
    self.config(width=self.width, height=self.height)
    # rescale all the objects
    self.scale("all", 0, 0, wscale, hscale)

class GUI:
  def __init__(self):
    # default parameters
    self.linkage = FourBarLinkage(1.41, 1.41, 3., 1., 45., 0., 0.5, 0.3, 0.01, 10)
    self.tk = tk.Tk()
    self.width = round(0.8*self.tk.winfo_screenwidth())
    self.height = round(0.8*self.tk.winfo_screenheight())
    self.tk.geometry(f"{self.width}x{self.height}")
    self.tk.title("Four-bar linkage model")
    self.tk.configure(background="antiquewhite")
    # frame for linkage
    self.model_frame = tk.Frame(self.tk, width=round(0.7*self.width),
                                height=round(0.6*self.height))
    self.model_frame.grid(row=0, column=0, padx=5, pady=5)
    self.model_animation = tk.Canvas(self.model_frame, width=round(0.7*self.width),
                                     height=round(0.6*self.height))
    self.model_animation.width = round(0.7*self.width)
    self.model_animation.height = round(0.6*self.height)
    self.model_animation.grid(row=0, column=0, padx=5, pady=5)
    self.display_linkage()
    # toolbar
    self.toolbar_frame = tk.Frame(self.tk, width=round(0.3*self.width),
                                  height=round(0.6*self.height))
    self.toolbar_frame.width = round(0.3*self.width)
    self.toolbar_frame.height = round(0.3*self.height)
    self.toolbar_frame.grid(row=0, column=1, padx=5, pady=5)
    slider_width = round(0.85*self.toolbar_frame.width)
    self.slider_a = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                             orient=tk.HORIZONTAL, length=slider_width, label="a",
                             command=self.update_parameter_a, variable=tk.DoubleVar())
    self.slider_a.set(self.linkage.a)
    self.slider_a.grid(row=0, column=1, padx=5, pady=5)
    self.slider_g = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                             orient=tk.HORIZONTAL, length=slider_width, label="g",
                             command=self.update_parameter_g, variable=tk.DoubleVar())
    self.slider_g.set(self.linkage.g)
    self.slider_g.grid(row=1, column=1, padx=5, pady=5)
    self.slider_b = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                             orient=tk.HORIZONTAL, length=slider_width, label="b",
                             command=self.update_parameter_b, variable=tk.DoubleVar())
    self.slider_b.set(self.linkage.b)
    self.slider_b.grid(row=2, column=1, padx=5, pady=5)

    self.slider_h = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                             orient=tk.HORIZONTAL, length=slider_width, label="h",
                             command=self.update_parameter_h, variable=tk.DoubleVar())
    self.slider_h.set(self.linkage.h)
    self.slider_h.grid(row=3, column=1, padx=5, pady=5)
    self.slider_p_pos = tk.Scale(self.toolbar_frame, from_=-200., to=200., orient=tk.HORIZONTAL,
                                 length=slider_width, label="P_pos % in CD",
                                 command=self.update_parameter_p_pos, variable=tk.DoubleVar())
    self.slider_p_pos.set(self.linkage.coupler_position*100/self.linkage.h)
    self.slider_p_pos.grid(row=4, column=1, padx=5, pady=5)
    self.slider_p_off = tk.Scale(self.toolbar_frame, from_=-200., to=200., orient=tk.HORIZONTAL,
                                 length=slider_width, label="P_offset % in CD",
                                 command=self.update_parameter_p_off, variable=tk.DoubleVar())
    self.slider_p_off.set(self.linkage.coupler_offset*100/self.linkage.h)
    self.slider_p_off.grid(row=5, column=1, padx=5, pady=5)
    self.display_linkage()
    
  def display_linkage(self):
    # delete later
    self.linkage.B=(3., 0.)
    self.linkage.C=(2., 1.)
    self.linkage.D=(1., 1.)
    self.linkage.P=(1.5, 1.3)
    # max space needed to animate model in x and y directions, it should be improved!!!
    max_x = np.abs(np.cos(self.linkage.theta))*self.linkage.g + self.linkage.a + self.linkage.b
    max_y = np.abs(np.sin(self.linkage.theta))*self.linkage.g + self.linkage.a + self.linkage.b
    # scaling factor for point coordinates
    scale = 0.9*min(float(self.model_animation.width)/max_x,
                    float(self.model_animation.height)/max_y)
    # Point A is a bias
    A_x = round(self.linkage.A[0]*scale + self.linkage.a*scale/0.9)
    A_y = self.model_animation.height - round(self.linkage.A[1]*scale + self.linkage.a*scale/0.9)
    # Point B relative to A
    B_x = round(A_x + (self.linkage.B[0]-self.linkage.A[0])*scale)
    B_y = round(A_y - (self.linkage.B[1]-self.linkage.A[1])*scale)
    # Point C relative to A
    C_x = round(A_x + (self.linkage.C[0]-self.linkage.A[0])*scale)
    C_y = round(A_y - (self.linkage.C[1]-self.linkage.A[1])*scale)
    # Point D relative to A
    D_x = round(A_x + (self.linkage.D[0]-self.linkage.A[0])*scale)
    D_y = round(A_y - (self.linkage.D[1]-self.linkage.A[1])*scale)
    # Point P relative to A
    P_x = round(A_x + (self.linkage.P[0]-self.linkage.A[0])*scale)
    P_y = round(A_y - (self.linkage.P[1]-self.linkage.A[1])*scale)
    # lines
    self.model_animation.create_line(A_x, A_y, B_x, B_y, fill="green", width=3)
    self.model_animation.create_line(B_x, B_y, C_x, C_y, fill="green", width=3)
    self.model_animation.create_line(C_x, C_y, D_x, D_y, fill="green", width=3)
    self.model_animation.create_line(D_x, D_y, A_x, A_y, fill="green", width=3)
    self.model_animation.create_line(C_x, C_y, P_x, P_y, fill="green", width=3)
    self.model_animation.create_line(P_x, P_y, D_x, D_y, fill="green", width=3)
    
    # display point names
    delta_x = round(0.012*self.model_animation.width)
    delta_y = round(0.012*self.model_animation.height)
    self.model_animation.create_text(A_x-delta_x, A_y+delta_y, text="A", fill="black",
                                     font=('Helvetica 11 bold'))
    self.model_animation.create_text(B_x+delta_x, B_y+delta_y, text="B", fill="black",
                                     font=('Helvetica 11 bold'))
    self.model_animation.create_text(C_x+delta_x, C_y-delta_y, text="C", fill="black",
                                     font=('Helvetica 11 bold'))
    self.model_animation.create_text(D_x-delta_x, D_y-delta_y, text="D", fill="black",
                                     font=('Helvetica 11 bold'))
    self.model_animation.create_text(P_x, P_y-np.sqrt(delta_y*delta_y+delta_x*delta_x),
                                     text="P", fill="black", font=('Helvetica 11 bold'))
    
    # display bar names
    delta_x = round(0.012*self.model_animation.width)
    delta_y = round(0.012*self.model_animation.height)
    self.model_animation.create_text((D_x+A_x)/2, (D_y+A_y)/2, text="a", fill="black",
                                     font=('Helvetica 11 bold'))
    self.model_animation.create_text((B_x+A_x)/2, (B_y+A_y)/2, text="g", fill="black",
                                     font=('Helvetica 11 bold'))
    self.model_animation.create_text((B_x+C_x)/2, (B_y+C_y)/2, text="b", fill="black",
                                     font=('Helvetica 11 bold'))
    self.model_animation.create_text((D_x+C_x)/2, (D_y+C_y)/2, text="h", fill="black",
                                     font=('Helvetica 11 bold'))

  # functions for scales to update parameters
  def update_parameter_a(self, val):
    self.linkage.a = float(val)
    self.linkage.run()
    self.model_animation.delete('all')
    self.display_linkage()
  def update_parameter_g(self, val):
    self.linkage.g = float(val)
    self.linkage.run()
    self.model_animation.delete('all')
    self.display_linkage()
  def update_parameter_b(self, val):
    self.linkage.b = float(val)
    self.linkage.run()
    self.model_animation.delete('all')
    self.display_linkage()
  def update_parameter_h(self, val):
    self.linkage.h = float(val)
    self.linkage.run()
    self.model_animation.delete('all')
    self.display_linkage()
  def update_parameter_p_pos(self, val):
    self.linkage.coupler_position = float(val)*self.linkage.h/100
    self.linkage.run()
    self.model_animation.delete('all')
    self.display_linkage()
  def update_parameter_p_off(self, val):
    self.linkage.coupler_offset = float(val)*self.linkage.h/100
    self.linkage.run()
    self.model_animation.delete('all')
    self.display_linkage()
      
  def refresh(self):
    pass
  
if __name__ == "__main__":
    GUI().tk.mainloop() 
    pass

