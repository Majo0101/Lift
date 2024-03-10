import random
import pandas as pd
import matplotlib.pyplot as plt

class Floor:
      def __init__(self, maxEvents, maxTime, elevatorCapacity, simTime, persons, event, consolePrint):
            self.maxEvents = maxEvents
            self.maxTime = maxTime
            self.elevatorCapacity = elevatorCapacity
            self.simTime = simTime
            self.persons = persons
            self.event = event
            self.calendar = None
            self.consolePrint = consolePrint

      def Calendar(self, mode, time, event):
            if mode == 'CAL_INIT':
                  self.calendar = [[-1, -1] for _ in range(self.maxEvents)]
                  return 1
            
            if mode == 'CAL_PRINT':
                  print('\nCalendar:')
                  for index in range(self.maxEvents):
                        if self.calendar[index][1] == -1:
                              print('time:' + str(self.calendar[index - 2][0]) + '  event: ' + str(self.calendar[index - 2][1]))
                              print('time:' + str(self.calendar[index - 1][0]) + '  event: ' + str(self.calendar[index - 1][1]))
                              break
                  print('==')
                  return 1
        
            if mode == 'CAL_SCHEDULE':
                  for index in range(self.maxEvents):
                        if index == self.maxEvents:
                              print('Calendar overflow')
                              return
                        if self.calendar[index][0] == -1:
                              self.calendar[index][0] = time
                              self.calendar[index][1] = event
                              break
                  self.calendar.sort(key = lambda x: (x[0] == -1, x[0]))
                  return 1
        
            if mode == 'CAL_TIME':
                  for index in range(self.maxEvents):
                        if self.calendar[index][0] == -1:
                              return self.calendar[index -2][0]
                  
            if mode == 'CAL_EVENT':
                  for index in range(self.maxEvents):
                        if self.calendar[index][1] == -1:
                              return self.calendar[index -2][1]
                  
            return -1
      
      def Event_1(self, minPeopleCome, maxPeopleCome):
            came = random.randint(minPeopleCome, maxPeopleCome)
            self.persons = self.persons + came
            if self.consolePrint: print('Persons came: ' + str(came) + ', waiting persons: ' + str(self.persons))
            self.Calendar('CAL_SCHEDULE', self.simTime + random.randint(1,5), 1)
            return
    
      def Event_2(self, capacity):
            if self.persons == 0:
                  if self.consolePrint: print('Lift is waiting')
                  pass
            else:
                  self.persons = self.persons - capacity
                  if self.persons < 0: self.persons = 0
                  if self.consolePrint: print('Lift is left, waiting persons: ' + str(self.persons))
            self.Calendar('CAL_SCHEDULE', self.simTime + random.randint(1,5), 2)
            return
    
      def PrintCalendar(self):
            for i, pair in enumerate(self.calendar):
                  print(f"Index {i}: Value at [0] = {pair[0]}, Value at [1] = {pair[1]}")
    

if __name__ == "__main__":
      data = pd.DataFrame(columns=['Capacity', 'Time', 'Persons'])

      # TODO easy settings
      maxValue = 999
      printing = False
      liftFloor1Cap = [2,4,5,7]
      # TODO end

      floor1 = Floor(maxEvents=maxValue, maxTime=maxValue, elevatorCapacity=liftFloor1Cap, simTime=0, persons=0, event=0, consolePrint=printing)

      for capacity in floor1.elevatorCapacity:
            print(f'Simulation start for capacity: {capacity} \n')

            floor1.Calendar('CAL_INIT', 0,0)
            floor1.Calendar('CAL_SCHEDULE', 1, 1)
            floor1.Calendar('CAL_SCHEDULE', 2, 2)

            while floor1.simTime < floor1.maxTime:

                  if floor1.consolePrint: floor1.Calendar('CAL_PRINT', 0, 0)
                  floor1.event = floor1.Calendar('CAL_EVENT', 0, 0)
                  floor1.simTime = floor1.Calendar('CAL_TIME', 0, 0)

                  if floor1.consolePrint: print('                 Time: ' + str(floor1.simTime) + '  Event: ' + str(floor1.event) + '  ', end='')

                  if floor1.event == 1: floor1.Event_1(minPeopleCome=1,maxPeopleCome=10)
                  if floor1.event == 2: floor1.Event_2(capacity=capacity)

                  data.loc[len(data)] = [capacity, floor1.simTime, floor1.persons]

            floor1.simTime = 0
            floor1.persons = 0

            if floor1.consolePrint: 
                  print(f'\nCalendar for the floor 1')
                  floor1.PrintCalendar()

      print('Simulation finished')

      for capacity, group in data.groupby('Capacity'):
            plt.plot(group['Time'], group['Persons'], label=f'Capacity {capacity}')

      plt.xlabel('Time')
      plt.ylabel('Persons')
      plt.title('Waiting Persons over Time by Lift Capacity')
      plt.legend()
      plt.show()