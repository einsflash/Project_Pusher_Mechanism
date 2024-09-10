from four_bar_linkage import FourBarLinkage
import tkinter as tk
import numpy as np
import math
        
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
        self.linkage = FourBarLinkage(3., 1.41, 1., 1.41, 45., 0., 0.5, 0.3, 0.01, 10)
        self.linkage.run()
        self.tk = tk.Tk()
        self.width = round(0.8*self.tk.winfo_screenwidth())
        self.height = round(0.8*self.tk.winfo_screenheight())
        self.tk.geometry(f"{self.width}x{self.height}")
        self.tk.title("Four-bar linkage model")
        # frame for linkage
        self.model_frame = tk.Frame(self.tk, width=round(0.7*self.width),
                                    height=round(0.6*self.height))
        self.model_frame.grid(row=0, column=0)
        self.model_animation = tk.Canvas(self.model_frame, width=round(0.7*self.width),
                                         height=round(0.6*self.height))
        self.model_animation.width = round(0.7*self.width)
        self.model_animation.height = round(0.6*self.height)
        self.model_animation.grid(row=0, column=0)
        self.display_linkage()
        # toolbar
        self.toolbar_frame = tk.Frame(self.tk, width=round(0.3*self.width),
                                      height=round(0.6*self.height))
        self.toolbar_frame.width = round(0.3*self.width)
        self.toolbar_frame.height = round(0.6*self.height)
        self.toolbar_frame.grid(row=0, column=1, columnspan=4)
        # classification values
        #self.classification_frame = tk.Frame(self.tk, width=round(0.7*self.width),
        #                                     height=round(0.3*self.height))
        #self.classification_frame.width = round(0.7*self.width)
        #self.classification_frame.height = round(0.3*self.height)
        #self.classification_frame.grid(row=8, column=0, padx=5, pady=5)
        # generate picture
        self.display_toolbar()
        self.display_classification_values()
        self.display_linkage()
    
    # configure toolbar
    def display_toolbar(self):
        # all sliders
        slider_width = round(0.85*self.toolbar_frame.width)
        self.slider_a = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="a",
                                 command=self.update_parameter_a, variable=tk.DoubleVar())
        self.slider_a.grid(row=0, column=1, columnspan=4)
        self.slider_g = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="g",
                                 command=self.update_parameter_g, variable=tk.DoubleVar())
        self.slider_g.grid(row=1, column=1, columnspan=4)
        self.slider_b = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="b",
                                 command=self.update_parameter_b, variable=tk.DoubleVar())
        self.slider_b.grid(row=2, column=1, columnspan=4)
    
        self.slider_h = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="h",
                                 command=self.update_parameter_h, variable=tk.DoubleVar())
        self.slider_h.grid(row=3, column=1, columnspan=4)
        self.slider_p_pos = tk.Scale(self.toolbar_frame, from_=-200., to=200., orient=tk.HORIZONTAL,
                                     length=slider_width, label="P_pos % in CD",
                                     command=self.update_parameter_p_pos, variable=tk.DoubleVar())
        self.slider_p_pos.grid(row=4, column=1, columnspan=4)
        self.slider_p_off = tk.Scale(self.toolbar_frame, from_=-200., to=200., orient=tk.HORIZONTAL,
                                     length=slider_width, label="P_offset % in CD",
                                     command=self.update_parameter_p_off, variable=tk.DoubleVar())
        self.slider_p_off.grid(row=5, column=1, columnspan=4)
        self.slider_alpha = tk.Scale(self.toolbar_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                                     length=slider_width, label="α, °",
                                     command=self.update_parameter_alpha, variable=tk.DoubleVar())
        self.slider_alpha.grid(row=6, column=1, columnspan=4)
        self.update_alpha_slider() # instantly update alpha limits
        self.slider_theta = tk.Scale(self.toolbar_frame, from_=-180., to=180., orient=tk.HORIZONTAL,
                                     length=slider_width, label="θ, °",
                                     command=self.update_parameter_theta, variable=tk.DoubleVar())
        self.slider_theta.grid(row=7, column=1, columnspan=4)
        self.reset_all_sliders()
        # classification values
        self.display_classification_values()
        # all buttons
        self.reset_button = tk.Button(self.toolbar_frame, text="reset", command=self.reset)
        self.reset_button.grid(sticky="W", row=9, column=1)
        # all checkbuttons
        self.animation_button = tk.Checkbutton(self.toolbar_frame, text="animation", variable=tk.IntVar(),
                                               onvalue=1, offvalue=0, command=self.animation)
        self.animation_button.grid(row=9, column=2)
        self.trace_text = tk.Text(self.toolbar_frame, height=1, width=6, bd=0, bg="grey94")
        self.trace_text.insert(tk.END, "Trace:")
        self.trace_text.grid(sticky="W", row=10, column=1)
        self.trace_C_button = tk.Checkbutton(self.toolbar_frame, text="C", variable=tk.IntVar(),
                                             onvalue=1, offvalue=0, command=self.trace_C)
        self.trace_C_button.grid(row=10, column=2)
        self.trace_D_button = tk.Checkbutton(self.toolbar_frame, text="D", variable=tk.IntVar(),
                                             onvalue=1, offvalue=0, command=self.trace_D)
        self.trace_D_button.grid(row=10, column=3)
        self.trace_P_button = tk.Checkbutton(self.toolbar_frame, text="P", variable=tk.IntVar(),
                                             onvalue=1, offvalue=0, command=self.trace_P)
        self.trace_P_button.grid(row=10, column=4)
        
    # update limits for alpha slider
    def update_alpha_slider(self):
        # round alpha limits to prevent errors
        left_limit = np.ceil(self.linkage.alpha_lims[0])
        right_limit = np.floor(self.linkage.alpha_lims[1])
        self.slider_alpha.configure(from_=left_limit, to=right_limit)
        # alpha should be always in alpha_lims
        self.linkage.calculate_alpha_lims()
        if self.linkage.alpha < self.linkage.alpha_lims[0] or self.linkage.alpha > self.linkage.alpha_lims[1]:
            self.linkage.alpha = (self.linkage.alpha_lims[0] + self.linkage.alpha_lims[1])/2
            self.linkage.alpha_rad = math.radians(self.linkage.alpha)
        self.slider_alpha.set(self.linkage.alpha)
        
    # disply classification values T1, T2, T3, L
    def display_classification_values(self):
        # text params in symbols
        text_height=4
        text_width=30
        self.text_classification_values = tk.Text(self.toolbar_frame, height=text_height, width=text_width, bd=0, bg="grey94")
        self.text_classification_values.insert(tk.END, f'T1 = g + h - b - a: {round(self.linkage.T1,3)}')
        self.text_classification_values.insert(tk.END, f'\nT2 = b + g - h - a: {round(self.linkage.T2,3)}')
        self.text_classification_values.insert(tk.END, f'\nT3 = h + b - g - a: {round(self.linkage.T3,3)}')
        self.text_classification_values.insert(tk.END, f'\nL  = g + b + h + a: {round(self.linkage.L,3)}')
        self.text_classification_values.grid(row=8, column=1, columnspan=4, sticky = tk.W+tk.E)
        
    def display_linkage(self):
        # delete already generated linkage picture
        self.model_animation.delete('all')
        # scaling factor to transfrom spatial coordinates to pixels
        scale = self.scaling_factor()
        # Mid point in AB should be always placed in center for symmetry
        AB_mid = (self.linkage.A + self.linkage.B)/2
        AB_mid_x = round(self.model_animation.width/2)
        AB_mid_y = round(self.model_animation.height/2)
        # Point A is a bias and positioned relative to AB_mid
        A_x = round(AB_mid_x - AB_mid[0]*scale)
        A_y = round(AB_mid_y + AB_mid[1]*scale)
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

    # this function is used to make sure that the four bar linkage model fit in GUI frame
    def scaling_factor(self):
        # max length in x direction
        max_x = np.abs(np.cos(self.linkage.theta))*self.linkage.AB
        max_x += 2*max(self.linkage.DA, self.linkage.BC)
        max_x += 2*max(1, np.sqrt(self.linkage.coupler_offset**2+(np.abs(self.linkage.coupler_position)+ 0.5)**2))*self.linkage.CD
        # max length in y direction
        max_y = np.abs(np.sin(self.linkage.theta))*self.linkage.AB
        max_y += 2*max(self.linkage.DA, self.linkage.BC)
        max_y += 2*max(1, np.sqrt(self.linkage.coupler_offset**2+(np.abs(self.linkage.coupler_position)+ 0.5)**2))*self.linkage.CD
        # scaling factor for point coordinates
        scale = min(float(self.model_animation.width)/max_x,
                    float(self.model_animation.height)/max_y)
        return scale
    

    # functions for scales to update parameters
    def update_parameter_a(self, val):
        self.linkage.DA = float(val)
        self.refresh()
    def update_parameter_g(self, val):
        self.linkage.AB = float(val)
        self.refresh()
    def update_parameter_b(self, val):
        self.linkage.BC = float(val)
        self.refresh()
    def update_parameter_h(self, val):
        self.linkage.CD = float(val)
        self.refresh()
    def update_parameter_p_pos(self, val):
        self.linkage.coupler_position = float(val)*self.linkage.CD/100
        self.refresh()
    def update_parameter_p_off(self, val):
        self.linkage.coupler_offset = float(val)*self.linkage.CD/100
        self.refresh()
    def update_parameter_alpha(self, val):
        self.linkage.alpha = float(val)
        self.linkage.alpha_rad = math.radians(self.linkage.alpha)
        self.refresh()
    def update_parameter_theta(self, val):
        self.linkage.theta = float(val)
        self.linkage.theta_rad = math.radians(self.linkage.theta)
        self.refresh()
     
    # refresh the GUI
    def refresh(self):
        self.update_alpha_slider()
        self.linkage.run()
        self.display_classification_values()
        self.display_linkage()
    
    # generate default linkage
    def reset(self):
        self.linkage = FourBarLinkage(3., 1.41, 1., 1.41, 45., 0., 0.5, 0.3, 0.01, 10)
        self.update_alpha_slider()
        self.linkage.run()
        self.reset_all_sliders()
        
    def reset_all_sliders(self):
        self.slider_a.set(self.linkage.DA)
        self.slider_g.set(self.linkage.AB)
        self.slider_b.set(self.linkage.BC)
        self.slider_h.set(self.linkage.CD)
        self.slider_p_pos.set(self.linkage.coupler_position*100/self.linkage.CD)
        self.slider_p_off.set(self.linkage.coupler_offset*100/self.linkage.CD)
        self.slider_alpha.set(self.linkage.alpha)
        self.slider_theta.set(self.linkage.theta)
    
    def animation(self):
        pass
    
    def trace_C(self):
        pass
    def trace_D(self):
        pass
    def trace_P(self):
        pass
  
if __name__ == "__main__":
    GUI().tk.mainloop() 
    pass

