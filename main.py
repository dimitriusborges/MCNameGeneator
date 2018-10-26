import random
import unicodedata


class NameGenerator:

    def __init__(self, data, st_size=2):
        """
        
        :param data: data feeding the Markov Chain 
        :param st_size: number of letters in each state
        """
        self.data = data
        self.state_list = []
        self.partial_prob = []
        self.initial_prob = []
        self.state_occur = []
        self.prob_matrix = {}
        self.st_size = st_size

    def set_states(self):

        # read the entire database, pick each state once and doesn't consider frequency
        for reg in self.data:
            for i in range(0, len(reg), self.st_size):
                char = reg[i:i+self.st_size]

                if char not in self.state_list:
                    self.state_list.append(char)

        self.partial_prob = [0] * len(self.state_list)

        # create a initial probability, based on the occurrence of each state as the first combination of a name
        # it is only used to determine the first state, i.e., beginning, of a name
        for state in self.state_list:
            index = self.state_list.index(state)
            for reg in self.data:
                if reg[0: 0+self.st_size] == state: # is the beginning
                    self.partial_prob[index] = self.partial_prob[index] + 1

        # partial_prob = [1/len(estados)]*len(estados)

    def set_states_prob(self):
        """"""

        self.initial_prob = [0] * len(self.state_list)

        # pass the occurrence to probability
        for occur in range(0, len(self.partial_prob)):
            try:
               self.initial_prob[occur] = self.partial_prob[occur] / sum(self.partial_prob)
            except ZeroDivisionError:
                self.initial_prob[occur] = 0

        self.state_occur = [0] * len(self.state_list)

    def build_mc(self):
        """
        :return: 
        """
        # now, building the chain
        for state in self.state_list:

            self.state_occur.clear()
            self.state_occur = [0] * len(self.state_list)

            if len(state)/self.st_size == 1: # ignores (keeps occurrence = 0) states smaller than st_size

                # verify, in each register in the db, what is the next state from the current one
                for reg in self.data:

                    pos = reg.find(state)

                    # and save the number of occurrences
                    if 0 <= pos < len(reg) - self.st_size:

                        try:
                            index = self.state_list.index(reg[pos + self.st_size: pos + 2 * self.st_size])
                            self.state_occur[index] = self.state_occur[index] + 1
                        except ValueError:
                            continue

            # after each state is analysed, pass the occurrences to probabilities
            state_prob = [0] * len(self.state_occur)

            for occur in range(0, len(self.state_occur)):
                try:
                    state_prob[occur] = self.state_occur[occur]/sum(self.state_occur)
                except ZeroDivisionError:
                    state_prob[occur] = 0

            # and add to the prob matrix
            self.prob_matrix[state] = state_prob.copy()

    def print_mc(self):
        """
        
        :return: 
        """
        print(" ", self.state_list)
        for reg in self.prob_matrix:
            print(reg, self.prob_matrix[reg])


class Main:
    def __init__(self):
        """"""
        self.max_size = 8
        self.total_gen = 5
        self.st_size = 2
        self.path_db = "D:/Dropbox/Estudos/Mestrado/Codigos/Python/MarkovNameGenerator/database"

    def name_gen(self):

        # get the database
        with open(self.path_db) as db:
            data = db.readlines()
        data = [unicodedata.normalize('NFD', (reg.strip()).lower()) for reg in data]
        data = [(reg.encode("ascii", "ignore")).decode("utf-8") for reg in data]

        ng = NameGenerator(data, st_size=self.st_size)
        ng.set_states()
        ng.set_states_prob()
        ng.build_mc()

        print(ng.initial_prob)
        ng.print_mc()

        for _ in range(0, self.total_gen):
            # the random walk starts form a state drawn from the initial prob.
            random_name = ""

            estado = random.choices(population=ng.state_list, weights=ng.initial_prob)[0]

            random_name = random_name + estado
            random_name = random_name[0].upper() + random_name[1:]

            # then, n states are determined from the prob matrix
            while len(random_name) < self.max_size:
                prob_estado = ng.prob_matrix[estado] # probabilities associated to the last state visited

                if sum(prob_estado) > 0: # if the state isn't an absorbing one
                    estado = random.choices(population=ng.state_list, weights=prob_estado)[0]# random.choices return a state, respecting the associated probs
                else:
                    break

                random_name = random_name + estado

            print("\n", random_name)

start = Main()
start.name_gen()
