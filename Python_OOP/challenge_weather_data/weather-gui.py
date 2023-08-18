# Import packages
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as pp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import weatherdata

# Main class to create figure and plot weather data
class WeatherApp:

    def __init__(self, master):

        # Configure main window
        master.title("Daily Temperatures App")
        master.resizable("false", "false")
        
        # Create frame for title and logo of application
        self.frame = ttk.Frame(master)
        self.frame.config(padding = (20,10))
        self.frame.pack()

        # Add photo and text to first frame
        image = Image.open("weather.png")
        resized_image = image.resize((200, 100))
        photo_image = ImageTk.PhotoImage(resized_image)
        
        self.app_name_photo = ttk.Label(self.frame, text = "Daily Temperatures App", 
                                        image = photo_image, font = ("Arial", 18, "bold") )
        self.app_name_photo.config(justify = "left")
        self.app_name_photo.grid(row = 0, column = 0, columnspan = 2)
        self.app_name_photo.image = photo_image
        self.app_name_photo.config(compound ='left')

        # Add second frame for the dropdown menu, year entry and button to plot data
        self.frame_select = ttk.Frame(master)
        self.frame_select.pack()

        # Add labels to select city and to enter year 
        self.select_city_frame = ttk.Label(self.frame_select, text = "Select city:",
                                            justify = "left")
        self.select_city_frame.grid(row = 0, column = 0)

        self.select_city_frame = ttk.Label(self.frame_select, text = "Enter year:",
                                            justify = "left")
        self.select_city_frame.grid(row = 0, column = 1)
        
        # Add dropdown menu for selecting city
        city = tk.StringVar()
        self.menu = ttk.Combobox(self.frame_select, textvariable = city, 
                              values = ["PASADENA", "PORTLAND", "HILO", "FORREST", "DARWIN"])
        self.menu.grid(row = 1, column = 0, padx=10, pady=10)

        # Add button to plot data
        self.button = ttk.Button(self.frame_select, text = "Show", 
                                 command = self.show_plot)
        self.button.grid(row = 1, column = 2)

        # Add entry box to write year for plotting
        self.entry_year = ttk.Entry(self.frame_select, text = "Year")
        self.entry_year.grid(row = 1, column = 1, padx=10)

        # Add third frame to display results (plot)
        self.frame_plot = ttk.LabelFrame(master, text = "Temperatures Plot")
        self.frame_plot.pack()
        self.frame_plot.config(padding=(2,10))

        # Figure
        f, ax = pp.subplots(figsize=(8,4))
        ax.axis('off')
        self.a = ax
        self.canvas = FigureCanvasTkAgg(f, self.frame_plot)
        self.canvas.draw()
        self.canvas._tkcanvas.pack()

    # Method for preparing data for plotting
    def _process_data(self):

        days, tminn, tmaxn, tminr, tmaxr, thisyear, avg = weatherdata.data_to_plot(
            self.city, self.year)
        self.days = days
        self.tmin_normal = tminn
        self.tmax_normal = tmaxn
        self.tmin_record = tminr
        self.tmax_record = tmaxr 
        self.avg = avg
        self.thisyear = thisyear

    # Method for showing data plot
    def show_plot(self):

        self.city = self.menu.get()
        self.year = int(self.entry_year.get())

        # Check if city is not empty
        if self.city !='':
            # Check if year is in range acceptable
            if (self.year <= 2022) & (self.year > 1900):
                # Get data
                self._process_data()
                # Plot data
                self.a.clear()
                self.a.fill_between(self.days, self.tmin_record, self.tmax_record, color=(0.92,0.92,0.89), step='mid')
                self.a.fill_between(self.days, self.tmin_normal, self.tmax_normal, color=(0.78,0.72,0.72))
                self.a.fill_between(self.days, self.thisyear['TMIN'], self.thisyear['TMAX'],color=(0.73,0.21,0.41), alpha=0.6, step='mid')
                self.a.axis(xmin=1, xmax=365, ymin=-15, ymax=50)
                self.a.set(xlabel = "Day of the year", ylabel = "Temperature (Celcius)",
                           title = f"{self.city}, {self.year}: average temperature = {self.avg:.2f} C")
                self.a.legend(["Record temperatures", "Average temperatures", "Year temperatures"])
                self.canvas.draw()
            else:
                messagebox.showerror(title = "Invalid year",
                                     message = "Please enter valid year (integer between 1900 and 2022).")
        else:
            messagebox.showerror(title = "Invalid city",
                                 message = "Please select city name from menu.")

# Main function 
def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":main()


