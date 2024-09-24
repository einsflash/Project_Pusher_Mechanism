from four_bar_linkage import FourBarLinkage
import tkinter as tk
import numpy as np
import math

class GUI:
    
    def __init__(self):
        # default parameters
        self.linkage = FourBarLinkage(3., 1.41, 1., 1.41, 45., 0., 0.25, 0.3, 0.025, 20)
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
        width = round(0.7*self.width)
        height = round(0.9*self.height)
        # canvas to display linkage
        self.model_animation = tk.Canvas(self.model_frame, width=width,
                                         height=height)
        self.model_animation.width = width
        self.model_animation.height = height
        self.model_animation.grid(row=0, column=0)
        # toolbar
        width = round(0.3*self.width)
        self.toolbar_frame = tk.Frame(self.tk, width=width,
                                      height=height)
        self.toolbar_frame.width = width
        self.toolbar_frame.height = height
        self.toolbar_frame.grid(row=0, column=1, columnspan=4)
        # generate picture
        self.display_toolbar()
        self.initiate_linkage_display()
        # trace is disabled
        self.trace_C = False
        self.trace_D = False
        self.trace_P = False
        # positions to trace them
        self.positions_C = []
        self.positions_D = []
        self.positions_P = []
    
    # configure toolbar
    def display_toolbar(self):
        # checkbutton to select input values
        self.input_text = tk.Text(self.toolbar_frame, height=1, width=6, bd=0, bg="grey94")
        self.input_text.insert(tk.END, "Input:")
        self.input_text.grid(sticky="W", row=0, column=1)
        self.input_classification_values = tk.IntVar()
        self.input_classification_values_button = tk.Checkbutton(self.toolbar_frame, text="classification values", 
                                                                 variable=self.input_classification_values,
                                                                 onvalue=1, offvalue=0,
                                                                 command=self.input_classification)
        self.input_classification_values_button.grid(row=0, column=2)
        
        # exit button
        self.reset_button = tk.Button(self.toolbar_frame, text="Exit", command=self.tk.destroy)
        self.reset_button.grid(row=0, column=4)
        
        
        # initiate sliders to set geometrical parameters
        slider_width = round(0.85*self.toolbar_frame.width)
        # input bar's length
        self.slider_a = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="a",
                                 command=self.update_parameter_a, variable=tk.DoubleVar())
        self.slider_a.grid(row=1, column=1, columnspan=4)
        self.slider_g = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="g",
                                 command=self.update_parameter_g, variable=tk.DoubleVar())
        self.slider_g.grid(row=2, column=1, columnspan=4)
        self.slider_b = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="b",
                                 command=self.update_parameter_b, variable=tk.DoubleVar())
        self.slider_b.grid(row=3, column=1, columnspan=4)
        self.slider_h = tk.Scale(self.toolbar_frame, from_=0.1, to=5., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="h",
                                 command=self.update_parameter_h, variable=tk.DoubleVar())
        self.slider_h.grid(row=4, column=1, columnspan=4)
        # input classification values
        self.slider_T1 = tk.Scale(self.toolbar_frame, from_=-5., to=5., resolution=0.01,
                                  orient=tk.HORIZONTAL, length=slider_width, label="T1 = g + h - b - a",
                                  command=self.update_parameter_T1, variable=tk.DoubleVar())
        self.slider_T1.grid(row=1, column=1, columnspan=4)
        self.slider_T2 = tk.Scale(self.toolbar_frame, from_=-5., to=5., resolution=0.01,
                                  orient=tk.HORIZONTAL, length=slider_width, label="T2 = b + g - h - a",
                                  command=self.update_parameter_T2, variable=tk.DoubleVar())
        self.slider_T2.grid(row=2, column=1, columnspan=4)
        self.slider_T3 = tk.Scale(self.toolbar_frame, from_=-5., to=5., resolution=0.01,
                                  orient=tk.HORIZONTAL, length=slider_width, label="T3 = h + b - g - a",
                                  command=self.update_parameter_T3, variable=tk.DoubleVar())
        self.slider_T3.grid(row=3, column=1, columnspan=4)
        self.slider_L = tk.Scale(self.toolbar_frame, from_=0.01, to=10., resolution=0.01,
                                 orient=tk.HORIZONTAL, length=slider_width, label="L  = g + b + h + a",
                                 command=self.update_parameter_L, variable=tk.DoubleVar())
        self.slider_L.grid(row=4, column=1, columnspan=4)
        # hide first classification sliders
        self.hide_classification_sliders()
        
        # input further params
        self.slider_p_pos = tk.Scale(self.toolbar_frame, from_=-200., to=200., orient=tk.HORIZONTAL,
                                     length=slider_width, label="P_pos % in CD",
                                     command=self.update_parameter_p_pos, variable=tk.DoubleVar())
        self.slider_p_pos.grid(row=5, column=1, columnspan=4)
        self.slider_p_off = tk.Scale(self.toolbar_frame, from_=-200., to=200., orient=tk.HORIZONTAL,
                                     length=slider_width, label="P_offset % in CD",
                                     command=self.update_parameter_p_off, variable=tk.DoubleVar())
        self.slider_p_off.grid(row=6, column=1, columnspan=4)
        self.slider_alpha = tk.Scale(self.toolbar_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                                     length=slider_width, label="α, °",
                                     command=self.update_parameter_alpha, variable=tk.DoubleVar())
        self.slider_alpha.grid(row=7, column=1, columnspan=4)
        self.update_alpha_slider() # instantly update alpha limits
        self.slider_theta = tk.Scale(self.toolbar_frame, from_=-180., to=180., orient=tk.HORIZONTAL,
                                     length=slider_width, label="θ, °",
                                     command=self.update_parameter_theta, variable=tk.DoubleVar())
        self.slider_theta.grid(row=8, column=1, columnspan=4)
        # reset all sliders with current values
        self.reset_bars_sliders()
        
        # classification values
        self.init_display_classification_values()
        self.init_display_bars_values()
        self.hide_bars_values()
        
        # initialize reset button
        self.reset_button = tk.Button(self.toolbar_frame, text="reset", command=self.reset)
        self.reset_button.grid(sticky="W", row=10, column=1)
        
        # initialize checkbuttons with necessary text
        self.enable_animation = tk.IntVar()
        self.animation_button = tk.Checkbutton(self.toolbar_frame, text="animation", 
                                               variable=self.enable_animation,
                                               onvalue=1, offvalue=0, command=self.animation)
        self.animation_button.grid(row=10, column=2)
        self.trace_text = tk.Text(self.toolbar_frame, height=1, width=6, bd=0, bg="grey94")
        self.trace_text.insert(tk.END, "Trace:")
        self.trace_text.grid(sticky="W", row=11, column=1)
        self.enable_trace_C = tk.IntVar()
        self.trace_C_button = tk.Checkbutton(self.toolbar_frame, text="C", variable=self.enable_trace_C,
                                             onvalue=1, offvalue=0, command=self.trace_C)
        self.trace_C_button.grid(row=11, column=2)
        self.enable_trace_D = tk.IntVar()
        self.trace_D_button = tk.Checkbutton(self.toolbar_frame, text="D", variable=self.enable_trace_D,
                                             onvalue=1, offvalue=0, command=self.trace_D)
        self.trace_D_button.grid(row=11, column=3)
        self.enable_trace_P = tk.IntVar()
        self.trace_P_button = tk.Checkbutton(self.toolbar_frame, text="P", variable=self.enable_trace_P,
                                             onvalue=1, offvalue=0, command=self.trace_P)
        self.trace_P_button.grid(row=11, column=4)
        
        # display type of linkage
        self.init_display_information()
        
    # update limits for alpha slider
    def update_alpha_slider(self):
        # round alpha limits to prevent errors
        left_limit = np.ceil(self.linkage.alpha_lims[0])
        right_limit = np.floor(self.linkage.alpha_lims[1])
        self.slider_alpha.configure(from_=left_limit, to=right_limit)
        # alpha should be always in alpha_lims
        self.linkage.calculate_alpha_lims()
        if self.linkage.alpha < self.linkage.alpha_lims[0] or \
           self.linkage.alpha > self.linkage.alpha_lims[1]:
            self.linkage.alpha = (self.linkage.alpha_lims[0] + self.linkage.alpha_lims[1])/2
            self.linkage.alpha_rad = math.radians(self.linkage.alpha)
        self.slider_alpha.set(self.linkage.alpha)
     
    # init classification display values
    def init_display_classification_values(self):
        # text params in symbols
        text_height=4
        text_width=30
        # display text
        self.text_classification_values = tk.Text(self.toolbar_frame, height=text_height, 
                                                  width=text_width, bd=0, bg="grey94")
        self.text_classification_values.grid(row=9, column=1, columnspan=4, sticky=tk.W+tk.E)
        
    # display classification values T1, T2, T3, L
    def display_classification_values(self):
        self.text_classification_values.delete('1.0', tk.END)
        self.text_classification_values.insert(tk.END, f'T1 = g + h - b - a: {round(self.linkage.T1,3)}')
        self.text_classification_values.insert(tk.END, f'\nT2 = b + g - h - a: {round(self.linkage.T2,3)}')
        self.text_classification_values.insert(tk.END, f'\nT3 = h + b - g - a: {round(self.linkage.T3,3)}')
        self.text_classification_values.insert(tk.END, f'\nL  = g + b + h + a: {round(self.linkage.L,3)}')
    
    # init bars display values
    def init_display_bars_values(self):
        # text params in symbols
        text_height=4
        text_width=10
        # display text
        self.text_bars_values = tk.Text(self.toolbar_frame, height=text_height, 
                                        width=text_width, bd=0, bg="grey94")
        self.text_bars_values.grid(row=9, column=1, columnspan=4, sticky=tk.W+tk.E)
        
        
    # display bars values a,b,g,h
    def display_bars_values(self):
        self.text_bars_values.delete('1.0', tk.END)
        self.text_bars_values.insert(tk.END, f'a = {round(self.linkage.DA,3)}')
        self.text_bars_values.insert(tk.END, f'\ng = {round(self.linkage.AB,3)}')
        self.text_bars_values.insert(tk.END, f'\nb = {round(self.linkage.BC,3)}')
        self.text_bars_values.insert(tk.END, f'\nh = {round(self.linkage.CD,3)}')
    
    # init classification of linkage
    def init_display_information(self):
        # Set the height and width for the text box
        text_height = 3
        text_width = 30
        self.text_information = tk.Text(self.toolbar_frame, height=text_height,
                                        width=text_width, bd=0, bg="grey94")
        self.text_information.grid(row=12, column=1, columnspan=4, sticky=tk.W+tk.E)
        
    # display Input_Link_Type, Output_Link_Type, Linkage_Type
    def display_information(self):
        self.text_information.delete('1.0', tk.END)
        self.text_information.insert(tk.END, f'Input Link Type: {self.linkage.Input_Link_Type}')
        self.text_information.insert(tk.END, f'\nOutput Link Type: {self.linkage.Output_Link_Type}')
        self.text_information.insert(tk.END, f'\nLinkage Type: {self.linkage.Linkage_Type}')
        
    # initiate all structures for linkage display (all coordinates are set to -1)
    def initiate_linkage_display(self):
        # invalid linkage text
        self.model_animation.invalid_text = self.model_animation.create_text(round(self.model_animation.width/2),
                                                                             round(self.model_animation.height/2),
                                                                             text="Invalid setup, change geometrical values",
                                                                             fill="black", font=('Helvetica 11 bold'))
        # hide the error text
        self.model_animation.itemconfigure(self.model_animation.invalid_text, state='hidden')
        
        # dasplay
        
        # trace
        self.model_animation.trace_C = self.model_animation.create_line([(-1,-1), (-1,-1)], fill="black", width=1)
        self.model_animation.trace_D = self.model_animation.create_line([(-1,-1), (-1,-1)], fill="black", width=1)
        self.model_animation.trace_P = self.model_animation.create_line([(-1,-1), (-1,-1)], fill="black", width=1)
        
        # display angles
        self.model_animation.alpha_arc = self.model_animation.create_arc(-1,-1,-1,-1, start = 0,
                                                                         extent=self.linkage.alpha, outline = "black",
                                                                         dash=(2,2))
        self.model_animation.theta_arc = self.model_animation.create_arc(-1,-1,-1,-1, start = 0,
                                                                         extent=self.linkage.theta, outline = "black",
                                                                         dash=(2,2))
        
        # horizontal line
        self.model_animation.horizont_line = self.model_animation.create_line(-1,-1,-1,-1, fill="black", dash=(2,2))
        
        # bars
        self.model_animation.AB_line = self.model_animation.create_line(-1,-1,-1,-1, fill="green", width=3)
        self.model_animation.BC_line = self.model_animation.create_line(-1,-1,-1,-1, fill="green", width=3)
        self.model_animation.CD_line = self.model_animation.create_line(-1,-1,-1,-1, fill="green", width=3)
        self.model_animation.DA_line = self.model_animation.create_line(-1,-1,-1,-1, fill="green", width=3)
        self.model_animation.CP_line = self.model_animation.create_line(-1,-1,-1,-1, fill="green", width=3)
        self.model_animation.PD_line = self.model_animation.create_line(-1,-1,-1,-1, fill="green", width=3)
    
        # display names
        self.model_animation.A_text = self.model_animation.create_text(-1,-1, text="A", fill="black",
                                                                       font=('Helvetica 11 bold'))
        self.model_animation.B_text = self.model_animation.create_text(-1,-1, text="B", fill="black",
                                                                       font=('Helvetica 11 bold'))
        self.model_animation.C_text = self.model_animation.create_text(-1,-1, text="C", fill="black",
                                                                       font=('Helvetica 11 bold'))
        self.model_animation.D_text = self.model_animation.create_text(-1,-1, text="D", fill="black",
                                                                       font=('Helvetica 11 bold'))
        self.model_animation.P_text = self.model_animation.create_text(-1,-1, text="P", fill="black",
                                                                       font=('Helvetica 11 bold'))
        self.model_animation.alpha_text = self.model_animation.create_text(-1,-1, text="α", fill="black",
                                                                           font=('Helvetica 11 bold'))
        self.model_animation.theta_text = self.model_animation.create_text(-1,-1, text="θ", fill="black",
                                                                           font=('Helvetica 11 bold'))
        self.model_animation.DA_text = self.model_animation.create_text(-1,-1, text="a", fill="black",
                                                                        font=('Helvetica 11 bold'))
        self.model_animation.AB_text = self.model_animation.create_text(-1,-1, text="g", fill="black",
                                                                        font=('Helvetica 11 bold'))
        self.model_animation.BC_text = self.model_animation.create_text(-1,-1, text="b", fill="black",
                                                                        font=('Helvetica 11 bold'))
        self.model_animation.CD_text = self.model_animation.create_text(-1,-1, text="h", fill="black",
                                                                        font=('Helvetica 11 bold'))
        
        # firstly hide all the objects, as they are not configured yet
        self.hide_linkage()

    # this function is used to make sure that the four bar linkage model fit in GUI frame
    def scaling_factor(self):
        # max length in x direction
        # links AB and CD
        max_x = np.abs(np.cos(self.linkage.theta_rad))*max(self.linkage.AB, self.linkage.CD)
        # links DA and BC
        horizontal_value = max(self.linkage.DA, self.linkage.BC)
        max_x += 2*horizontal_value
        # point P
        max_x += 2*max(np.sqrt(self.linkage.coupler_position**2 +\
                               self.linkage.coupler_offset**2)*self.linkage.CD, 0.0)
        # max length in y direction
        # links AB and CD
        max_y = np.abs(np.sin(self.linkage.theta_rad))*max(self.linkage.AB, self.linkage.CD)
        # links DA and BC
        vertical_value = max(self.linkage.DA, self.linkage.BC)
        max_y += 2*vertical_value
        # point P
        max_y += 2*max(np.sqrt(self.linkage.coupler_position**2 +\
                               self.linkage.coupler_offset**2)*self.linkage.CD, 0.0)
        # scaling factor for point coordinates
        scale = min(float(self.model_animation.width)/max_x,
                    float(self.model_animation.height)/max_y)
        return scale
    
    # normalities to 4 linkage bars
    def calculate_normalities(self):
        AB = self.linkage.B - self.linkage.A
        BC = self.linkage.C - self.linkage.B
        CD = self.linkage.D - self.linkage.C
        DA = self.linkage.A - self.linkage.D
        n_AB = [AB[1], -AB[0]]/np.linalg.norm(AB)
        n_BC = [BC[1], -BC[0]]/np.linalg.norm(BC)
        n_CD = [CD[1], -CD[0]]/np.linalg.norm(CD)
        n_DA = [DA[1], -DA[0]]/np.linalg.norm(DA)
        return n_AB, n_BC, n_CD, n_DA

    # functions for sliders to update parameters
    def update_parameter_a(self, val):
        self.linkage.DA = float(val)
        self.delete_tracing()
        self.refresh()
    def update_parameter_g(self, val):
        self.linkage.AB = float(val)
        self.delete_tracing()
        self.refresh()
    def update_parameter_b(self, val):
        self.linkage.BC = float(val)
        self.delete_tracing()
        self.refresh()
    def update_parameter_h(self, val):
        self.linkage.CD = float(val)
        self.delete_tracing()
        self.refresh()
    def update_parameter_p_pos(self, val):
        self.linkage.coupler_position = float(val)/100
        self.delete_tracing()
        self.refresh()
    def update_parameter_p_off(self, val):
        self.linkage.coupler_offset = float(val)/100
        self.delete_tracing()
        self.refresh()
    def update_parameter_alpha(self, val):
        self.linkage.alpha = float(val)
        self.linkage.alpha_rad = math.radians(self.linkage.alpha)
        self.refresh()
    def update_parameter_theta(self, val):
        self.linkage.theta = float(val)
        self.delete_tracing()
        self.linkage.theta_rad = math.radians(self.linkage.theta)
        self.refresh()
    def update_parameter_T1(self, val):
        self.linkage.T1 = float(val)
        self.delete_tracing()
        self.linkage.calculate_Edge_Value()
        self.refresh()
    def update_parameter_T2(self, val):
        self.linkage.T2 = float(val)
        self.delete_tracing()
        self.linkage.calculate_Edge_Value()
        self.refresh()
    def update_parameter_T3(self, val):
        self.linkage.T3 = float(val)
        self.delete_tracing()
        self.linkage.calculate_Edge_Value()
        self.refresh()
    def update_parameter_L(self, val):
        self.linkage.L = float(val)
        self.delete_tracing()
        self.linkage.calculate_Edge_Value()
        self.refresh()
     
    # refresh the GUI
    def refresh(self):
        self.update_alpha_slider()
        self.linkage.run()
        self.display_classification_values()
        self.display_bars_values()
        self.display_information()
        self.update_linkage_display()
    
    # generate default linkage
    def reset(self):
        self.linkage = FourBarLinkage(3., 1.41, 1., 1.41, 45., 0., 0.25, 0.3, 0.05, 10)
        self.update_alpha_slider()
        self.linkage.run()
        self.reset_bars_sliders()
        self.reset_classifications_sliders()
        self.delete_tracing()
    
    # reset bars sliders + angles
    def reset_bars_sliders(self):
        self.slider_a.set(self.linkage.DA)
        self.slider_g.set(self.linkage.AB)
        self.slider_b.set(self.linkage.BC)
        self.slider_h.set(self.linkage.CD)
        self.slider_p_pos.set(self.linkage.coupler_position*100)
        self.slider_p_off.set(self.linkage.coupler_offset*100)
        self.slider_alpha.set(self.linkage.alpha)
        self.slider_theta.set(self.linkage.theta)
    
    # reset classifications sliders + angles
    def reset_classifications_sliders(self):
        self.slider_T1.set(self.linkage.T1)
        self.slider_T2.set(self.linkage.T2)
        self.slider_T3.set(self.linkage.T3)
        self.slider_L.set(self.linkage.L)
        self.slider_p_pos.set(self.linkage.coupler_position*100)
        self.slider_p_off.set(self.linkage.coupler_offset*100)
        self.slider_alpha.set(self.linkage.alpha)
        self.slider_theta.set(self.linkage.theta)
        
    # input classifiaction values instead of bar's length
    def input_classification(self):
        if self.input_classification_values.get():
            self.hide_bars_sliders()
            self.hide_classification_values()
            self.show_classification_sliders()
            self.show_bars_values()
            self.reset_classifications_sliders()
            self.display_bars_values()
        else:
            self.hide_classification_sliders()
            self.hide_bars_values()
            self.show_bars_sliders()
            self.show_classification_values()
            self.reset_bars_sliders()
            self.display_classification_values()
    
    # hide classification sliders
    def hide_classification_sliders(self):
        self.slider_T1.grid_remove()
        self.slider_T2.grid_remove()
        self.slider_T3.grid_remove()
        self.slider_L.grid_remove()
        
    # show classification sliders
    def show_classification_sliders(self):
        self.slider_T1.grid()
        self.slider_T2.grid()
        self.slider_T3.grid()
        self.slider_L.grid()
    
    # hide bars sliders
    def hide_bars_sliders(self):
        self.slider_a.grid_remove()
        self.slider_b.grid_remove()
        self.slider_g.grid_remove()
        self.slider_h.grid_remove()
        
    # show bars sliders
    def show_bars_sliders(self):
        self.slider_a.grid()
        self.slider_b.grid()
        self.slider_g.grid()
        self.slider_h.grid()
        
    # hide values of classification values
    def hide_classification_values(self):
        self.text_classification_values.grid_remove()
        
    # show values of classification values
    def show_classification_values(self):
        self.text_classification_values.grid()
       
    # hide values of bars values
    def hide_bars_values(self):
        self.text_bars_values.grid_remove()
        
    # show values of bars values
    def show_bars_values(self):
        self.text_bars_values.grid()
        
    # function to initialize animation
    def animation(self):
        self.run_animation()
    
    # repeated function to animate movement
    def run_animation(self):
        if self.enable_animation.get():
            self.linkage.animation_alpha()
            self.refresh()
            self.tk.after(25, self.run_animation)
    
    # enable/disable C-point tracing
    def trace_C(self):
        if self.enable_trace_C.get():
            self.trace_C = True
        else:
            self.trace_C = False
            
    # enable/disable D-point tracing
    def trace_D(self):
        if self.enable_trace_D.get():
            self.trace_D = True
        else:
            self.trace_D = False
            
    # enable/disable P-point tracing
    def trace_P(self):
        if self.enable_trace_P.get():
            self.trace_P = True
        else:
            self.trace_P = False
    
    # delete tracing
    def delete_tracing(self):
        self.positions_C = []
        self.positions_D = []
        self.positions_P = []
    
    # hide all linkage widgets
    def hide_linkage(self):
        self.model_animation.itemconfigure(self.model_animation.trace_C, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.trace_P, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.trace_D, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.alpha_arc, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.theta_arc, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.horizont_line, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.AB_line, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.BC_line, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.CD_line, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.DA_line, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.CP_line, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.PD_line, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.A_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.B_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.C_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.D_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.P_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.alpha_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.theta_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.DA_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.AB_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.BC_text, state='hidden')
        self.model_animation.itemconfigure(self.model_animation.CD_text, state='hidden')
        
    # show all linkage widgets
    def show_linkage(self):
        self.model_animation.itemconfigure(self.model_animation.trace_C, state='normal')
        self.model_animation.itemconfigure(self.model_animation.trace_P, state='normal')
        self.model_animation.itemconfigure(self.model_animation.trace_D, state='normal')
        self.model_animation.itemconfigure(self.model_animation.alpha_arc, state='normal')
        self.model_animation.itemconfigure(self.model_animation.theta_arc, state='normal')
        self.model_animation.itemconfigure(self.model_animation.horizont_line, state='normal')
        self.model_animation.itemconfigure(self.model_animation.AB_line, state='normal')
        self.model_animation.itemconfigure(self.model_animation.BC_line, state='normal')
        self.model_animation.itemconfigure(self.model_animation.CD_line, state='normal')
        self.model_animation.itemconfigure(self.model_animation.DA_line, state='normal')
        self.model_animation.itemconfigure(self.model_animation.CP_line, state='normal')
        self.model_animation.itemconfigure(self.model_animation.PD_line, state='normal')
        self.model_animation.itemconfigure(self.model_animation.A_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.B_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.C_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.D_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.P_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.alpha_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.theta_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.DA_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.AB_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.BC_text, state='normal')
        self.model_animation.itemconfigure(self.model_animation.CD_text, state='normal')
        
    def update_linkage_display(self):
        # check if setup is valid
        if self.linkage.geometric_Validity:
            # show linkage
            self.show_linkage()
            # hide error message
            self.model_animation.itemconfigure(self.model_animation.invalid_text, state='hidden')
        else:
            # hide linkage
            self.hide_linkage()
            # show error message
            self.model_animation.itemconfigure(self.model_animation.invalid_text, state='normal')
            return
        
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
        
        # tracing
        # number of points to trace
        N_points = 5*round((self.linkage.alpha_lims[1]-self.linkage.alpha_lims[0])/ \
                   (self.linkage.alpha_velocity * self.linkage.t)) # delete later this factor of 5
        # trace C
        if self.trace_C:
            if len(self.positions_C)<=N_points:
                self.positions_C.append(C_x)
                self.positions_C.append(C_y)
            if len(self.positions_C)>2:
                self.model_animation.coords(self.model_animation.trace_C, self.positions_C)
        else:
            self.model_animation.itemconfigure(self.model_animation.trace_C, state='hidden')
        # trace D
        if self.trace_D:
            if len(self.positions_D)<=N_points:
                self.positions_D.append(D_x)
                self.positions_D.append(D_y)
            if len(self.positions_D)>2:
                self.model_animation.coords(self.model_animation.trace_D, self.positions_D)
        else:
            self.model_animation.itemconfigure(self.model_animation.trace_D, state='hidden')
        # trace P   
        if self.trace_P:
            if len(self.positions_P)<=N_points:
                self.positions_P.append(P_x)
                self.positions_P.append(P_y)
            if len(self.positions_P)>2:
                self.model_animation.coords(self.model_animation.trace_P, self.positions_P)
        else:
            self.model_animation.itemconfigure(self.model_animation.trace_P, state='hidden')

        # update arc alpha
        radius_alpha = round(min(self.width/30, self.linkage.AB*scale, self.linkage.DA*scale))
        self.model_animation.coords(self.model_animation.alpha_arc, [A_x-radius_alpha, A_y-radius_alpha,
                                                                     A_x+radius_alpha, A_y+radius_alpha])
        self.model_animation.itemconfigure(self.model_animation.alpha_arc, extent=self.linkage.alpha)
        
        # update arc theta
        radius_theta = round(min(self.width/20, self.linkage.AB*scale))
        if self.linkage.theta!=0:            
            self.model_animation.coords(self.model_animation.theta_arc, [A_x-radius_theta, A_y-radius_theta,
                                                                         A_x+radius_theta, A_y+radius_theta])
            self.model_animation.itemconfigure(self.model_animation.theta_arc, extent=self.linkage.theta)
        else:
            self.model_animation.itemconfigure(self.model_animation.theta_arc, state='hidden')
            
        # update horizontal line
        self.model_animation.coords(self.model_animation.horizont_line, [A_x, A_y, A_x+3*radius_alpha, A_y])
        
        # update bars
        self.model_animation.coords(self.model_animation.AB_line, [A_x, A_y, B_x, B_y])
        self.model_animation.coords(self.model_animation.BC_line, [B_x, B_y, C_x, C_y])
        self.model_animation.coords(self.model_animation.CD_line, [C_x, C_y, D_x, D_y])
        self.model_animation.coords(self.model_animation.DA_line, [D_x, D_y, A_x, A_y])
        self.model_animation.coords(self.model_animation.CP_line, [C_x, C_y, P_x, P_y])
        self.model_animation.coords(self.model_animation.PD_line, [P_x, P_y, D_x, D_y])
    
        # update point's names
        delta_x = round(0.012*self.model_animation.width)
        delta_y = round(0.012*self.model_animation.height)
        self.model_animation.coords(self.model_animation.A_text, [A_x-delta_x, A_y+delta_y])
        self.model_animation.coords(self.model_animation.B_text, [B_x+delta_x, B_y+delta_y])
        self.model_animation.coords(self.model_animation.C_text, [C_x+delta_x, C_y-delta_y])
        self.model_animation.coords(self.model_animation.D_text, [D_x-delta_x, D_y-delta_y])
        self.model_animation.coords(self.model_animation.P_text, [P_x, P_y-np.sqrt(delta_y*delta_y+delta_x*delta_x)])
        
        # update angle's names
        self.model_animation.coords(self.model_animation.alpha_text,
                                    [A_x + radius_alpha*np.cos(self.linkage.alpha_rad/2)+10,
                                     A_y - radius_alpha*np.sin(self.linkage.alpha_rad/2)])
        if self.linkage.theta!=0.0: 
            self.model_animation.coords(self.model_animation.theta_text,
                                        [A_x + radius_theta*np.cos(self.linkage.theta_rad/2)+10,
                                         A_y - radius_theta*np.sin(self.linkage.theta_rad/2)])
        else:
            self.model_animation.itemconfigure(self.model_animation.theta_text, state='hidden')
        
        # update bar's names
        radius_names = round(scale*min(self.linkage.AB, self.linkage.BC, self.linkage.CD,
                                       self.linkage.DA)/10)        
        g, b, h, a = self.calculate_normalities()
        self.model_animation.coords(self.model_animation.DA_text, [round(radius_names*a[0]+(A_x+D_x)/2),
                                                                   round(-radius_names*a[1]+(A_y+D_y)/2)])
        self.model_animation.coords(self.model_animation.AB_text, [round(radius_names*g[0]+(A_x+B_x)/2),
                                                                   round(-radius_names*g[1]+(A_y+B_y)/2)])
        self.model_animation.coords(self.model_animation.BC_text, [round(radius_names*b[0]+(C_x+B_x)/2),
                                                                   round(-radius_names*b[1]+(C_y+B_y)/2)])
        self.model_animation.coords(self.model_animation.CD_text, [round(radius_names*h[0]+(C_x+D_x)/2),
                                                                   round(-radius_names*h[1]+(C_y+D_y)/2)])
        
  
if __name__ == "__main__":
    GUI().tk.mainloop() 
    pass

