import simpy

class SimpleDefect:

    def __init__(self, env):
        self.env = env
        self.store = simpy.FilterStore(env)
        self.env.process(self.producerA())
        self.env.process(self.producerB())
        self.env.process(self.consumerA())
        self.env.process(self.consumerB())

    def producerA(self):
        # Produces an 'A' for the store every 1 time unit
        while True:
            yield self.env.timeout(1.0)
            self.store.put('A')
            print self.env.now, ": Producer A fired event."

    def producerB(self):
        # Produces a 'B' for the store every 0.1 time units
        while True:
            yield self.env.timeout(0.1)
            self.store.put('B')
            print self.env.now, ": Producer B fired event."

    def consumerA(self):
        while True:
            # Wait for A's
            yield self.store.get(filter = lambda x : x == 'A')
            print self.env.now, ": Consumer A got an 'A'"

    def consumerB(self):
        while True:
            # Wait for B's
            yield self.store.get(filter = lambda x : x == 'B')
            print self.env.now, ": Consumer B got a 'B'"

def main():
    env = simpy.Environment()
    bd = SimpleDefect(env)
    env.run(until=2)

if __name__ == "__main__":
    main()