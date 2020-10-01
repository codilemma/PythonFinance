# Personal Budget Class
import yaml
import datetime
import pandas as pd
from matplotlib import pyplot as plt
from recurrent import RecurringEvent
from dateutil import rrule


class PersonalBudget:
    '''Functions that will help you create a Personal Finace Budget
       (start_date, yaml_file_path)
       enter start_date as a list ('[YYYY,MM,D]')
       enter yaml_file
    '''


    def __init__(self,start_date,yaml_file):
        '''Initialize the Personal Budget with your cash flow file'''

        # Get Start and End Date
        self.today = pd.Timestamp(start_date[0],
                                  start_date[1],
                                  start_date[2]).normalize()

        self.end   = self.today + datetime.timedelta(days=365)

        # Load Cash flow yaml file.
        # TODO: Add Gui for File Selection & Add Excel Import
        with open(yaml_file) as file:
            self.budget = yaml.load(file)

        #initialize Calender
        self.frequency = 0
        self.amount = 0
        self.dates = 0
        self.calendar = pd.DataFrame(index=pd.date_range
                                    (start=self.today,
                                     end=self.end))

        # Build the Calender
        # self.build_calendar()
        #print(self.calendar.head(35))
        
    def build_calendar(self):
        ''' Will automatically build a budget callender when the class is created'''
        
        for k, v in self.budget.items():
            self.frequency = v.get('frequency')
            self.amount = v.get('amount')
            self.dates = self.get_dates(self.frequency)
            i = pd.DataFrame(
                data={k: self.amount},
                index=pd.DatetimeIndex(pd.Series(self.dates))
            )
            self.calendar = pd.concat([self.calendar, i], axis=1).fillna(0)
        
        #self.calendar['total'] = self.calendar.sum(axis=1)
        #self.calendar['cum_total'] = self.calendar['total'].cumsum()
        #self.calendar['savings_total'] = self.calendar['savings'].cumsum()
        #self.calendar['yuko_total'] = self.calendar['yuko'].cumsum()
        #self.calendar['cody_total'] = self.calendar['cody'].cumsum()

        return self.calendar
      
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
            for date in rr.between(self.today, self.end)
        ]
        #except ValueError as e:
        #    raise ValueError('Invalid Frequency')

    def plot_budget(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.calendar.index, self.calendar.total, label='Daily Total')
        plt.plot(self.calendar.index, self.calendar.cum_total, label='Cumulative Total')
        plt.legend()

    def update_totals(self,df):
        # check to see if those columns ixit in our dataframe
        if df.columns.isin(['total','cum_total']).any():
            # if they do exist set them to o
            df['total'] = 0
            df['cum_total'] = 0
        # Recalculate total and cumulative_total
        df['total'] = df.sum(axis=1)
        df['cum_total'] = df['total'].cumsum()
        return df
