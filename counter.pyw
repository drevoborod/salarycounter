#!/usr/bin/env python3

import re
import tkinter as tk


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Salary counter")
        self.resizable(width=0, height=0)
        tk.Frame(self, height=10).grid(row=0)
        mainframe = tk.Frame(self)
        mainframe.grid(row=1, padx=10)
        tk.Label(mainframe, text="Enter spent time \n(HH:MM):").grid(row=0, column=0)
        tk.Label(mainframe, text="Enter price of one hour:").grid(row=0, column=1)
        self.quantity = tk.Entry(mainframe, width=10)
        self.quantity.grid(row=1, column=0, pady=5)
        self.hourly_cost = tk.DoubleVar(mainframe, value=DEFAULT_PRICE)
        hourly_cost_entry = tk.Entry(mainframe, width=10, textvariable=self.hourly_cost)
        hourly_cost_entry.grid(row=1, column=1)
        tk.Frame(mainframe, height=5).grid(row=2)
        tk.Label(mainframe, text="Total hours in decimal:").grid(row=3, column=0)
        tk.Label(mainframe, text="Total price:").grid(row=3, column=1)
        self.total_hours = tk.StringVar(mainframe)
        tk.Label(mainframe, relief="sunken", width=10, textvariable=self.total_hours).grid(row=4, column=0, pady=5)
        self.total_price = tk.StringVar(mainframe)
        tk.Label(mainframe, relief="sunken", width=10, textvariable=self.total_price).grid(row=4, column=1)
        tk.Frame(self, height=20).grid(row=2)
        tk.Button(self, text="Calculate", command=self.calculate).grid(row=3, pady=10)
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<Escape>", lambda e: self.quit())
        self.bind("<Control-c>", lambda e: self.copy())
        hourly_cost_entry.bind("<FocusIn>", lambda e: hourly_cost_entry.delete(0, "end"))
        #self.quantity.bind("<Button-1>", lambda e: hourly_cost_entry.delete(0, "end"))
        self.quantity.focus()
        self.mainloop()

    def calculate(self):
        try:
            hours = self.quantity.get()
            cost = self.hourly_cost.get()
        except tk.TclError:
            pass
        else:
            if re.compile("^[0-9]{1,6}:[0-5][0-9]$").match(hours):
                match = True
            elif re.compile("^[0-9]{1,6}$").match(hours):
                hours += ":00"
                match = True
            else:
                match = False
            if match:
                res = calculate(cost, hours)
                self.total_hours.set(res[0])
                self.total_price.set(res[1])

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.total_price.get())


def calculate(hour_price, total_hours):
    full_time = total_hours.split(":")
    minutes = int(full_time[1])
    time_minutes = (minutes * 100 / 60) / 100
    time_decimal = ".".join((full_time[0], "{}".format(time_minutes).split(".")[1]))
    time_decimal_rounded = ".".join((str(int(full_time[0])), "{:.2f}".format(time_minutes).split(".")[1])).rstrip("0").rstrip(".")
    total = float(time_decimal) * hour_price
    return time_decimal_rounded, "{:.2f}".format(total)


DEFAULT_PRICE = 0.0
if __name__ == "__main__":
    Main()
