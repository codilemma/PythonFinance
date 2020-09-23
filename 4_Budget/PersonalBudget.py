# Personal Budget Class
import yaml
import datetime
import pandas as pd
from matplotlib import pyplot as plt
from recurrent import RecurringEvent
from dateutil import rrule

TODAY = pd.Timestamp(2020,9,23).normalize()
END = TODAY + datetime.timedelta(days=365)

class PersonalBudget:
    '''Functions that will help you create a Personal Finace Budget
       (start_date, yaml_file_path)
       enter start_date as ('year,month,day')
       enter yaml_file
    '''

    def __init__(self,yaml_file):
        '''Initialize the Personal Budget with your cash flow file'''
        # Load Cash flow yaml file.
        with open(yaml_file) as file:
            self.budget = yaml.load(file)

        #initialize Calender
        self.calendar = pd.DataFrame(index=pd.date_range(start=TODAY, end=END))

        # Build the Calender
        self.build_calendar()

    def build_calendar(self):
        ''' Will automatically build a budget callender when the class is created'''
        
        for k, v in self.budget.items():
            frequency = v.get('frequency')
            amount = v.get('amount')
            dates = self.get_dates(frequency)
            i = pd.DataFrame(
                data={k: amount},
                index=pd.DatetimeIndex(pd.Series(dates))
            )
            self.calendar = pd.concat([self.calendar, i], axis=1).fillna(0)
        
        self.calendar['total'] = self.calendar.sum(axis=1)
        self.calendar['cum_total'] = self.calendar['total'].cumsum()
      
    def get_dates(self, frequency):
        ''' Will create irregular cash flow frequency aliases'''

        # let pandas try and handle single dates
        try:
            return [pd.Timestamp(frequency).normalize()]
        except ValueError:
            pass
        # parse frequency with recurrent
        #try:
        r = RecurringEvent()
        r.parse(frequency)
        rr = rrule.rrulestr(r.get_RFC_rrule())
        return [
            pd.to_datetime(date).normalize()
            for date in rr.between(TODAY, END)
        ]
        #except ValueError as e:
        #    raise ValueError('Invalid Frequency')

    def plot_budget(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.calendar.index, self.calendar.total, label='Daily Total')
        plt.plot(self.calendar.index, self.calendar.cum_total, label='Cumulative Total')
        plt.legend()


