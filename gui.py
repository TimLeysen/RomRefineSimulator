from tkinter import *
from simulator import Simulator

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
        self.repair_cost = StringVar()
        self.simulations = StringVar()
        self.add_item_cost = IntVar()

        self._add_entry('Current refine', self.current_refine, '8')
        self._add_entry('Target refine', self.target_refine, '10')
        self._add_entry('Item cost [k]', self.item_cost, '1700')
        self._add_entry('Repair cost [k]', self.repair_cost, '1000')
        self._add_entry('Simulations', self.simulations, '10000')
        self._add_checkbutton('Add item cost', self.add_item_cost, False)

    def _init_output(self):
        self.fees = StringVar()
        self.oridecons = StringVar()
        self.repairs = StringVar()
        self.total_cost = StringVar()
        self.safe_refine_cost = StringVar()

        self._add_result_labels('Fees', self.fees)
        self._add_result_labels('Oridecons', self.oridecons)
        self._add_result_labels('Repairs', self.repairs)
        self._add_result_labels('Total cost', self.total_cost)
        self._add_result_labels('Safe refine cost', self.safe_refine_cost)

    def _reset_output(self):
        self.fees.set('')
        self.oridecons.set('')
        self.repairs.set('')
        self.total_cost.set('')
        self.safe_refine_cost.set('')

    def _set_output(self, results, safe_refine_cost):
        avg_fees, avg_oridecons, avg_repairs, avg_cost = results
        self.fees.set('{}k'.format(avg_fees))
        self.oridecons.set('{:.1f}'.format(avg_oridecons))
        self.repairs.set('{:.1f}'.format(avg_repairs))        
        item_cost = int(self.item_cost.get()) if self.add_item_cost.get() == 1 else 0
        self.total_cost.set('{}k'.format(avg_cost + item_cost))
        self.safe_refine_cost.set('{}k'.format(safe_refine_cost + item_cost))

    def _simulate_clicked(self):
        self.simulate['state'] = 'disabled'
        self.window.update()
        self._reset_output()

        sim = Simulator(
            int(self.current_refine.get()),
            int(self.target_refine.get()),
            int(self.item_cost.get()),
            int(self.repair_cost.get()))

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

        self._set_output(sim.results(), sim.safe_refine_cost())
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

    def _add_result_labels(self, prefix_text, textvariable):
        Label(self.window, text=prefix_text + ' ', anchor=W).grid(column=0, row=self.row, sticky=E)
        Label(self.window, textvariable=textvariable, anchor=W).grid(column=1, row=self.row)
        self.row += 1

if __name__ == '__main__':
    w = Widget()
    w.window.mainloop()