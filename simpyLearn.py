import simpy
env = simpy.Environment()

class Car(object):
    def __init__(self,env):
        self.env = env
        self.action = env.process(self.run())
    
    def run(self):
        while True:
            print('Start parking at %d' %env.now)
            parking_duration = 5
            charge_duration = 5
            try:
                yield env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                print("Was interrupted, fuck...")
            
            print('Start driving at %d' %env.now)
            trip_duration = 2
            yield env.timeout(trip_duration)
    
    def charge(self, duration):
        yield self.env.timeout(duration)
        

def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()
    

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

def car(env, name, bcs, driving_time, charge_duration):
    yield env.timeout(driving_time)
    
    print("%s arriving at %d" % (name, env.now))
    with bcs.request() as req:
        yield req
        
        print("%s starting to charge at %s" % (name, env.now))
        yield env.timeout(charge_duration)
        print("%s leaving the bcs at %s" % (name, env.now))