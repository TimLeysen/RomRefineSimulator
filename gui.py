from collections import namedtuple
from enum import Enum
from tkinter import *
from simulator import Simulator

class RefineType(Enum):
    NORMAL = 1
    SAFE = 2

class Widget:
    def __init__(self):
        self.window = Tk()
        self.window.title('ROM Refine Simulator')
        self.row = 0
        self._init_input()

        self.simulate = Button(self.window, text='Simulate', command=self._simulate_clicked)
        self.simulate.grid(column=0, row=self.row, sticky=N+S+E+W)
        self.progress = StringVar()
        Label(self.window, textvariable=self.progress).grid(column=1, row=self.row)
        self.row += 1

        self._init_output()

    def _init_input(self):
        self.current_refine = StringVar()
        self.target_refine = StringVar()
        self.item_cost = StringVar()
        self.copy_cost = StringVar()
        self.simulations = StringVar()
        self.add_item_cost = IntVar()

        self._add_entry('Current refine', self.current_refine, '8')
        self._add_entry('Target refine', self.target_refine, '10')
        self._add_entry('Item cost [k]', self.item_cost, '1700')
        self._add_entry('Copy cost [k]', self.copy_cost, '1000')
        self._add_entry('Simulations', self.simulations, '10000')
        self._add_checkbutton('Add item cost', self.add_item_cost, False)

    def _init_output(self):
        def add_label(text, column):
            label = Label(self.window, text=text, anchor=W)
            label.grid(column=column, row=self.row)
            return label
        self.normal_label = add_label('Normal', 1)
        self.safe_label = add_label('Safe', 2)
        self.row += 1

        def create_dict():
            return {RefineType.NORMAL: StringVar(), RefineType.SAFE: StringVar()}    
        self.fees = create_dict()
        self.oridecons = create_dict()
        self.copies = create_dict()
        self.total_cost = create_dict()
        
        self._add_result_labels('Fees', self.fees.values())
        self._add_result_labels('Oridecons', self.oridecons.values())
        self._add_result_labels('Copies', self.copies.values())
        self._add_result_labels('Total cost', self.total_cost.values())

    def _reset_output(self):
        self.normal_label.config(bg='lightgrey')
        self.safe_label.config(bg='lightgrey')
    
        def reset(output):
            for k in output.keys():
                output[k].set('')

        reset(self.fees)
        reset(self.oridecons)
        reset(self.copies)
        reset(self.total_cost)

       
    def _set_output(self, normal_results, safe_results):    
        def set_output(results, key):
            fees, oridecons, copies, cost = results
            self.fees[key].set('{}k'.format(fees))
            self.oridecons[key].set('{:.1f}'.format(oridecons))
            self.copies[key].set('{:.1f}'.format(copies))        
            item_cost = int(self.item_cost.get()) if self.add_item_cost.get() == 1 else 0
            self.total_cost[key].set('{}k'.format(cost + item_cost))
        
        set_output(normal_results, RefineType.NORMAL)
        set_output(safe_results, RefineType.SAFE)
        
        if normal_results.cost < safe_results.cost:
            self.normal_label.config(bg='lime')
        elif normal_results.cost > safe_results.cost:
            self.safe_label.config(bg='lime')

    def _simulate_clicked(self):
        self.simulate['state'] = 'disabled'
        self.window.update()
        self._reset_output()

        sim = Simulator(
            int(self.current_refine.get()),
            int(self.target_refine.get()),
            int(self.item_cost.get()),
            int(self.copy_cost.get()))

        def update_progress(fraction):
            self.progress.set('{:.1f}%'.format(100*fraction))
            self.window.update()

        n = int(self.simulations.get())
        update_progress_interval = round(n/100)
        for i in range(n):
            sim.step()
            if (i % update_progress_interval == 0):
                update_progress(i/n)
        update_progress(1)

        self._set_output(sim.results(), sim.safe_refine_results())
        self.simulate['state'] = 'normal'
        self.window.update()

    def _add_entry(self, text, textvariable, default_text='', width=10):
        Label(self.window, text=text, anchor=W).grid(column=0, row=self.row, sticky=E)
        textvariable.set(default_text)
        Entry(self.window, width=width, textvariable=textvariable).grid(column=1, row=self.row)
        self.row += 1

    def _add_checkbutton(self, text, intvariable, default_value=False, width=10):
        Label(self.window, text=text, anchor=W).grid(column=0, row=self.row, sticky=E)
        intvariable.set(1 if default_value else 0)
        Checkbutton(self.window, text='', variable=intvariable).grid(column=1, row=self.row, sticky=W)
        self.row += 1

    def _add_result_labels(self, prefix_text, textvariables):
        Label(self.window, text=prefix_text + ' ', anchor=W).grid(column=0, row=self.row, sticky=E)
        column = 1
        for textvar in textvariables:
            Label(self.window, textvariable=textvar, anchor=W).grid(column=column, row=self.row)
            column += 1
        self.row += 1

if __name__ == '__main__':
    w = Widget()
    w.window.mainloop()