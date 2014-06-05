import simpy

class SimpleEMS:

    def __init__(self, env):
        self.env = env
        self.calls = simpy.FilterStore(env)
        self.env.process(self.producerA())
        self.env.process(self.consumerA())

    def producerA(self):
        # Produces an 'A' for the store every 1 time unit
        while True:
            yield self.env.timeout(1.0)
            self.calls.put('A')
            print self.env.now, ": Producer A fired event."


    def consumerA(self):
        while True:
            # Wait for A's
            yield self.store.get(filter = lambda x : x == 'A')
            print self.calls.now, ": Consumer A got an 'A'"


def main():
    env = simpy.Environment()
    bd = SimpleEMS(env)
    env.run(until=2)

if __name__ == "__main__":
    main()