from collections import namedtuple
from enum import Enum
import random
import sys

# all costs in k zeny

class Outcome(Enum):
    SUCCESS = 1
    FAILURE = 2
    BROKEN = 3

class Simulator:
    Result = namedtuple('Result', 'fees oridecons copies cost')

    def __init__(self, start_refine, target_refine, item_cost, copy_cost):
        self.start_refine = start_refine
        self.target_refine = target_refine
        self.item_cost = item_cost
        self.copy_cost = copy_cost
        self.oridecon_cost = 25
        self.outcomes = [Outcome.SUCCESS, Outcome.FAILURE, Outcome.BROKEN]
        self.outcome_weights = {
            0: [1, 0, 0],
            1: [1, 0, 0],
            2: [1, 0, 0],
            3: [1, 0, 0],
            4: [0.5, 0.25, 0.25],
            5: [0.5, 0.25, 0.25],
            6: [0.4, 0.3, 0.3],
            7: [0.4, 0.3, 0.3],
            8: [0.4, 0.3, 0.3],
            9: [0.4, 0.3, 0.3]
        }
        self.safe_refine_copies = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 6, 9: 10 }
        self.safe_refine_oridecons = { 0: 1, 1: 1, 2: 1, 3: 1, 4: 5, 5: 10, 6: 15, 7: 25, 8: 50, 9: 85 }
        self.safe_refine_fees = { 0: 10, 1: 20, 2: 30, 3: 40, 4: 100, 5: 220, 6: 470, 7: 910, 8: 1630, 9: 2740 }
        self.fees = []
        self.oridecons = []
        self.copies = []
    
    def _calc_fee(self, refine_level):
        return min((refine_level + 1), 10) * 10
        
    def safe_refine_results(self):
        fees = 0
        oridecons = 0
        copies = 0
        
        for refine_level in range(self.start_refine, self.target_refine):
            fees += self.safe_refine_fees[refine_level]
            oridecons += self.safe_refine_oridecons[refine_level]            
            copies += self.safe_refine_copies[refine_level]

        cost = fees + oridecons * self.oridecon_cost + copies * self.copy_cost
        return Simulator.Result(fees, oridecons, copies, cost)
        
    def results(self):
        tries = len(self.fees)
        avg_fees = round(sum(self.fees)/tries)
        avg_oridecons = sum(self.oridecons)/tries
        avg_oridecon_cost = round(avg_oridecons * self.oridecon_cost)
        avg_copies = sum(self.copies)/tries
        avg_copies_cost = round(avg_copies * self.copy_cost)        
        avg_cost = avg_fees + avg_oridecon_cost + avg_copies_cost

        return Simulator.Result(avg_fees, avg_oridecons, avg_copies, avg_cost)
        
    def step(self):
        fees = 0
        oridecons = 0
        copies = 0
        refine = self.start_refine
        
        while refine < self.target_refine:
            fees += self._calc_fee(refine)
            oridecons += 1 if refine < 10 else 5
            outcome = random.choices(population=self.outcomes, weights=self.outcome_weights[refine], k=1)[0]
            #print(outcome.name)
            if outcome == Outcome.SUCCESS:
                refine += 1
            elif outcome == Outcome.FAILURE:
                refine -= 1
            elif outcome == Outcome.BROKEN:
                refine -= 1
                copies += 1
                fees += 5
            #print('+{}'.format(refine))

        self.fees.append(fees)
        self.oridecons.append(oridecons)
        self.copies.append(copies)