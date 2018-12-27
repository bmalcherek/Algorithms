from random import randint, choice, uniform
from math import ceil
from copy import deepcopy

# HEURISTIC GLOBAL VARIABLES
TASKS = 50
T_MIN = 5
T_MAX = 30
MAINTENANCE_CHANCE = 0.35
M2_PENALTY = 0.1
MAINTENANCE_TIME_COEFFICIENT = 1.5
PHEROMONE_DECREASE_COEFFICIENT = 1.5
POPULATION = 100
ITERATIONS = 1000
BEST_ANTS = 20
EVAPORATION_RATE = 0.2
ALPHA = 3
BETA = 2
Q = 2

# OTHER GLOBAL VARIABLES
INPUT_FILE = open("input.txt", "w")
OUTPUT_FILE = open("output.txt", "w")
JOBS = list()
ANTS = list()
PHEROMONE_MATRIX_M1 = list()
PHEROMONE_MATRIX_M2 = list()

# GLOBAL VARIABLES TO CALCULATE FROM GENERATED DATA
AVERAGE_M2_TIME = 0
MAINTENANCE_DURATION = 0
MAX_MAINTENANCE = TASKS - 2


class Job:
    def __init__(self, o1, o2, i):
        self.begin_time_m1 = None
        self.begin_time_m2 = None
        self.end_time_m1 = None
        self.end_time_m2 = None
        self.penalty = None
        self.real_length_op2 = None
        self.op1 = o1
        self.op2 = o2
        self.id = i

    def set_begin_time_m1(self, time):
        self.begin_time_m1 = time

    def set_begin_time_m2(self, time):
        self.begin_time_m2 = time

    def set_end_time_m1(self, time):
        self.end_time_m1 = time

    def set_end_time_m2(self, time):
        self.end_time_m2 = time

    def set_penalty(self, p):
        self.penalty = p
        self.real_length_op2 = ceil(p * self.op2)

    def __str__(self):
        # return f"job{self.index}"
        return str(self.id)

    def __repr__(self):
        return str(self)


class Maintenance:
    def __init__(self, time, job):
        self.begin_time = time
        self.length = MAINTENANCE_DURATION
        self.end_time = time + self.length
        self.parent_job = job.id
        self.id = self.parent_job + TASKS

    def set_times(self, time):
        self.begin_time = time
        self.end_time = time + self.length

    def __str__(self):
        return f"mtc{self.parent_job}"

    def __repr__(self):
        return str(self)


class IdleTime:
    def __init__(self, time):
        self.begin_time = time
        self.end_time = None
        self.length = None

    def set_end_time(self, time):
        self.end_time = time
        self.length = self.end_time - self.begin_time

    def __str__(self):
        return f"idle {self.begin_time} - {self.end_time}"

    def __repr__(self):
        return str(self)


class Ant:
    def __init__(self, solution_m1, solution_m2):
        self.solution_m1 = solution_m1
        self.solution_m2 = solution_m2
        self.score = score(self.solution_m1, self.solution_m2)
        self.not_used_jobs_m1 = deepcopy(JOBS)
        self.possible_m2_jobs = list()
        self.best_m1 = None
        self.best_m2 = None
        self.best_score = 9999999999999

    def set_score(self):
        self.score = score(self.solution_m1, self.solution_m2)

    def reset(self):
        self.score = None
        self.not_used_jobs_m1 = deepcopy(JOBS)
        self.possible_m2_jobs = list()

        self.solution_m1 = list()
        self.solution_m2 = list()

    def __str__(self):
        return str(self.score)

    def __repr__(self):
        return str(self)


def generate_jobs():
    print(TASKS, file=INPUT_FILE)
    t2_sum = 0

    for i in range(TASKS):
        t1 = randint(T_MIN, T_MAX)
        t2 = randint(T_MIN, T_MAX)
        t2_sum += t2
        # temp = [t1, t2]
        job = Job(t1, t2, i)
        JOBS.append(job)

        print(f"czas_operacji1_{i};{t1};czas_operacji2_{i};{t2}", file=INPUT_FILE)

    global AVERAGE_M2_TIME
    global MAINTENANCE_DURATION
    AVERAGE_M2_TIME = ceil(t2_sum / TASKS)
    MAINTENANCE_DURATION = ceil(MAINTENANCE_TIME_COEFFICIENT * AVERAGE_M2_TIME)


def generate_random_solution():
    # SOLUTION VARIABLES
    solution_m1 = list()
    solution_m2 = list()
    solution_m2_with_maintenance = list()
    maintenance_count = 0

    # OTHER VARIABLES
    not_used_jobs = deepcopy(JOBS)
    possible_m2_jobs = list()
    m1_time_busy = 0
    m2_time_busy = 0
    first_done = False
    last_done = False
    current_m2_penalty = 1
    time = 0
    is_idle = False
    job1 = None
    job2 = None
    idle = None

    while len(solution_m2) != len(JOBS) or m2_time_busy > 0:
        if m1_time_busy < 1 and len(not_used_jobs) > 0:
            if first_done:
                solution_m1.append(job1)
                job1.end_time_m1 = time
                possible_m2_jobs.append(job1)

            first_done = True
            job1 = choice(not_used_jobs)
            not_used_jobs.remove(job1)
            m1_time_busy = job1.op1
            job1.begin_time_m1 = time

        if len(not_used_jobs) == 0 and m1_time_busy < 1 and not last_done:
            last_done = True
            solution_m1.append(job1)
            job1.end_time_m1 = time
            possible_m2_jobs.append(job1)
        # print("----M1 END----")

        if (m2_time_busy < 1) and (len(possible_m2_jobs) > 0 or current_m2_penalty > 1):
            # random choice between normal job or maintenance. X is float between 0 and 1 and if its lower than
            # MAINTENANCE_CHANCE algorithm is choosing maintenance program cannot do more than 1 maintenance in a row,
            # so it will ignore random choice if current_m2_penalty == 1
            x = uniform(0, 1)
            # print(x)

            if x < MAINTENANCE_CHANCE and current_m2_penalty > 1:
                if is_idle:
                    idle.end_time = time
                    solution_m2_with_maintenance.append(idle)
                    is_idle = False

                current_m2_penalty = 1
                m2_time_busy = MAINTENANCE_DURATION
                maintenance_count += 1
                maintenance = Maintenance(time, job2)
                solution_m2_with_maintenance.append(maintenance)

            elif len(possible_m2_jobs) > 0:
                if is_idle:
                    idle.end_time = time
                    solution_m2_with_maintenance.append(idle)
                    is_idle = False

                job2 = choice(possible_m2_jobs)
                job2.begin_time_m2 = time
                job2.end_time_m2 = time + ceil(job2.op2 * current_m2_penalty)
                solution_m2.append(job2)
                solution_m2_with_maintenance.append(job2)
                possible_m2_jobs.remove(job2)
                m2_time_busy = ceil(job2.op2 * current_m2_penalty)
                job2.set_penalty(current_m2_penalty)
                current_m2_penalty += M2_PENALTY

            elif len(possible_m2_jobs) == 0 and not is_idle:
                idle = IdleTime(time)
                is_idle = True

        elif m2_time_busy < 1 and len(possible_m2_jobs) == 0 and current_m2_penalty == 1 and not is_idle:
            idle = IdleTime(time)
            is_idle = True

        time += 1
        m1_time_busy -= 1
        m2_time_busy -= 1

    return solution_m1, solution_m2_with_maintenance


def score(solution_m1, solution_m2):
    temp = 0
    for job in solution_m1:
        temp += job.end_time_m1 + job.end_time_m2
    # m1_score = solution_m1[-1].end_time_m1
    # m2_score = solution_m2[-1].end_time_m2

    return temp


def generate_output_file(solution_m1, solution_m2):
    maintenance_count = 0
    maintenance_time = 0
    idle_count = 0
    idle_time = 0

    score_b4 = score(solution_m1, solution_m2)
    print(str(score_b4), file=OUTPUT_FILE)

    print("M1: ", end="", file=OUTPUT_FILE)
    first = False
    for job in solution_m1:
        if not first:
            first = True
            print(f"op1_{job.id}, {job.begin_time_m1}, {job.op1}, {job.op1}", end="", file=OUTPUT_FILE)
        else:
            print(f"; op1_{job.id}, {job.begin_time_m1}, {job.op1}, {job.op1}", end="", file=OUTPUT_FILE)

    print("", file=OUTPUT_FILE)
    first = False
    print("M2: ", end="", file=OUTPUT_FILE)

    for element in solution_m2:
        if type(element) is Job:
            print(f"; op1_{element.id}, {element.begin_time_m2}, {element.op1}, {element.op1}", end="",
                  file=OUTPUT_FILE)

        elif type(element) is Maintenance:
            print(f"; maint{maintenance_count}_M2, {element.begin_time}, {element.length}", end="", file=OUTPUT_FILE)
            maintenance_count += 1
            maintenance_time += element.length

        elif type(element) is IdleTime:
            if not first:
                first = True
                print(f"idle{idle_count}_M2, {element.begin_time}, {element.length}", end="", file=OUTPUT_FILE)

            else:
                print(f"; idle{idle_count}_M2, {element.begin_time}, {element.length}", end="", file=OUTPUT_FILE)
            idle_count += 1
            idle_time += element.length

    print("\n0", file=OUTPUT_FILE)
    print(str(maintenance_time), file=OUTPUT_FILE)
    print("0", file=OUTPUT_FILE)
    print(str(idle_time), end="", file=OUTPUT_FILE)


def start_population():
    for i in range(POPULATION):
        temp_m1, temp_m2 = generate_random_solution()
        ant = Ant(temp_m1, temp_m2)
        ANTS.append(ant)


def get_x_best():
    ants = sorted(ANTS, key=lambda x: x.score)
    ants = ants[:BEST_ANTS]
    return ants


def initialize_pheromone_matrix():

    # last row of first pheromone matrix is start node so values on ith will indicate how much ants like to start
    # from that row

    global PHEROMONE_MATRIX_M1, PHEROMONE_MATRIX_M2

    for i in range(TASKS + 1):
        temp = list()
        for j in range(TASKS):
            temp.append(0)
        PHEROMONE_MATRIX_M1.append(temp)

    for i in range(2 * TASKS):
        temp = list()
        for j in range(2 * TASKS):
            temp.append(0)
        PHEROMONE_MATRIX_M2.append(temp)


def evaporation():
    global PHEROMONE_MATRIX_M1, PHEROMONE_MATRIX_M2

    for i in range(len(PHEROMONE_MATRIX_M1)):
        for j in range(len(PHEROMONE_MATRIX_M1[0])):
            PHEROMONE_MATRIX_M1[i][j] *= 1 - EVAPORATION_RATE

    for i in range(len(PHEROMONE_MATRIX_M2)):
        for j in range(len(PHEROMONE_MATRIX_M2[0])):
            PHEROMONE_MATRIX_M2[i][j] *= 1 - EVAPORATION_RATE


def update_pheromone_matrix():
    global PHEROMONE_MATRIX_M1, PHEROMONE_MATRIX_M2
    # ants = get_x_best()

    evaporation()

    for ant in ANTS:

        pheromone = Q / ant.score
        PHEROMONE_MATRIX_M1[-1][ant.solution_m1[0].id] += 1

        for i in range(len(ant.solution_m1) - 1):
            row = ant.solution_m1[i].id
            column = ant.solution_m1[i + 1].id
            PHEROMONE_MATRIX_M1[row][column] += pheromone

        '''
        J = Job, M = Maintenance, I = Idle
        In pheromone matrix for M2 we count maintenances and jobs, but there are 3 types of tasks (maintenance, 
        job and idle). If type(ant.solution_m2[i]) == I algorithm will do nothing. 
        If type(ant.solution_m2[i]) == J there are 3 options for next task, J, M, I. If it's J we get it's id as 
        a column, if it's M we get it's parent_id and add number of tasks to get the column number, if it's I there
        are again 2 options, M or I and algorithm will do the same as above to get the column number
        And if type(ant.solution_m2[i]) == M there are 2 options, J or I, if it's I the only option after it is I, so
        the procedure to get column number is already explained
        '''

        for i in range(len(ant.solution_m2) - 1):
            if type(ant.solution_m2[i]) == Job:
                row = ant.solution_m2[i].id
                column = None

                if type(ant.solution_m2[i + 1]) == Job:
                    column = ant.solution_m2[i + 1].id

                elif type(ant.solution_m2[i + 1]) == Maintenance:
                    column = ant.solution_m2[i + 1].parent_job + TASKS

                else:
                    if type(ant.solution_m2[i + 2]) == Job:
                        column = ant.solution_m2[i + 2].id

                    elif type(ant.solution_m2[i + 2]) == Maintenance:
                        column = ant.solution_m2[i + 2].parent_job + TASKS

                PHEROMONE_MATRIX_M2[row][column] += pheromone

            elif type(ant.solution_m2[i]) == Maintenance:
                row = ant.solution_m2[i].parent_job + TASKS
                column = None

                if type(ant.solution_m2[i + 1]) == Job:
                    column = ant.solution_m2[i + 1].id

                else:
                    column = ant.solution_m2[i + 2].id

                PHEROMONE_MATRIX_M2[row][column] += pheromone


def use_pheromone_matrix(ant):
    solution_m2 = list()  # Solution for M2 without maintenances used to stop condition of while loop
    time = 0
    m1_busy_time = 0
    m2_busy_time = 0
    last_done_m1 = False
    first_done_m2 = False
    job1 = None
    current_penalty = 1
    is_idle = False
    idle = None
    job2 = None

    while len(solution_m2) != TASKS or m2_busy_time > 0:
        if m1_busy_time < 1:
            if len(ant.solution_m1) == 0:
                # sum_of_last_row = sum(PHEROMONE_MATRIX_M1[-1])
                # x = uniform(0, sum_of_last_row)
                sum_of_all_m1 = 0
                for job in ant.not_used_jobs_m1:
                    sum_of_all_m1 += (PHEROMONE_MATRIX_M1[-1][job.id] ** ALPHA) * ((1 / job.op1) ** BETA)

                temp_sum = 0
                x = uniform(0, sum_of_all_m1)
                # index = 0

                # for i in range(len(PHEROMONE_MATRIX_M1[-1])):
                #     if temp_sum >= x:
                #         break
                #     temp_sum += PHEROMONE_MATRIX_M1[-1][i]
                #     index = i
                for job in ant.not_used_jobs_m1:
                    temp_sum += (PHEROMONE_MATRIX_M1[-1][job.id] ** ALPHA) * ((1 / job.op1) ** BETA)
                    if temp_sum >= x:
                        job1 = job
                        break

                # job1 = ant.not_used_jobs_m1[index]
                ant.not_used_jobs_m1.remove(job1)
                ant.solution_m1.append(job1)
                m1_busy_time = job1.op1

            elif len(ant.not_used_jobs_m1) >= 0 and not last_done_m1:

                if len(ant.not_used_jobs_m1) == 0:
                    last_done_m1 = True

                ant.possible_m2_jobs.append(job1)
                job1.end_time_m1 = time
                last_job_id_m1 = ant.solution_m1[-1].id
                sum_of_all_m1 = 0
                temp_sum = 0

                # sum_of_available_jobs_m1 = 0
                #
                # for job in ant.not_used_jobs_m1:
                #     sum_of_available_jobs_m1 += PHEROMONE_MATRIX_M1[last_job_id_m1][job.id]

                # x = uniform(0, sum_of_available_jobs_m1)
                # temp_sum = 0

                # for job in ant.not_used_jobs_m1:
                #     temp_sum += PHEROMONE_MATRIX_M1[last_job_id_m1][job.id]
                #     if temp_sum > x:
                #         job1 = job
                #         break

                for job in ant.not_used_jobs_m1:
                    sum_of_all_m1 += (PHEROMONE_MATRIX_M1[last_job_id_m1][job.id] ** ALPHA) * ((1 / job.op1) ** BETA)

                x = uniform(0, sum_of_all_m1)

                for job in ant.not_used_jobs_m1:
                    temp_sum += (PHEROMONE_MATRIX_M1[last_job_id_m1][job.id] ** ALPHA) * ((1 / job.op1) ** BETA)
                    if temp_sum >= x:
                        job1 = job
                        break

                if temp_sum == 0 and len(ant.not_used_jobs_m1) > 0:
                    job1 = choice(ant.not_used_jobs_m1)

                if not last_done_m1:
                    ant.solution_m1.append(job1)
                    job1.begin_time_m1 = time
                    ant.not_used_jobs_m1.remove(job1)
                    m1_busy_time = job1.op1

        if m2_busy_time < 1 and len(ant.possible_m2_jobs) > 0:

            if is_idle:
                is_idle = False
                idle.set_end_time(time)

            if not first_done_m2 and len(ant.possible_m2_jobs) > 0:
                job2 = ant.possible_m2_jobs[0]
                mtc = Maintenance(time, job2)
                ant.possible_m2_jobs.append(mtc)
                ant.possible_m2_jobs.remove(job2)
                job2.begin_time_m2 = time
                job2.end_time_m2 = time + job2.op2
                job2.set_penalty(current_penalty)
                m2_busy_time = job2.op2
                ant.solution_m2.append(job2)
                solution_m2.append(job2)
                first_done_m2 = True
                current_penalty += 0.1

            elif len(ant.possible_m2_jobs) > 0:
                if type(ant.solution_m2[-1]) == IdleTime:
                    last_job_id_m2 = ant.solution_m2[-2].id
                else:
                    last_job_id_m2 = ant.solution_m2[-1].id

                # sum_of_available_jobs_m2 = 0
                #
                # for job in ant.possible_m2_jobs:
                #     sum_of_available_jobs_m2 += PHEROMONE_MATRIX_M2[last_job_id_m2][job.id]
                #
                # x = uniform(0, sum_of_available_jobs_m2)
                # temp_sum = 0
                # job = None
                #
                # for j in ant.possible_m2_jobs:
                #     temp_sum += PHEROMONE_MATRIX_M2[last_job_id_m2][j.id]
                #     if temp_sum > x:
                #         job = j
                #         break
                sum_of_all_m2 = 0
                temp_sum = 0
                for job in ant.possible_m2_jobs:
                    if type(job) == Job:
                        sum_of_all_m2 += (PHEROMONE_MATRIX_M2[last_job_id_m2][job.id] ** ALPHA) * (
                                (1 / job.op1) ** BETA)
                    else:
                        sum_of_all_m2 += (PHEROMONE_MATRIX_M2[last_job_id_m2][job.id] ** ALPHA) * (
                                    (1 / job.length) ** BETA)

                x = uniform(0, sum_of_all_m2)

                for job in ant.possible_m2_jobs:
                    if type(job) == Job:
                        temp_sum += (PHEROMONE_MATRIX_M2[last_job_id_m2][job.id] ** ALPHA) * (
                                (1 / job.op1) ** BETA)
                    else:
                        temp_sum += (PHEROMONE_MATRIX_M2[last_job_id_m2][job.id] ** ALPHA) * (
                                    (1 / job.length) ** BETA)
                    if temp_sum >= x:
                        job2 = job
                        break

                if temp_sum == 0:
                    job2 = choice(ant.possible_m2_jobs)

                if job2.id < TASKS:
                    solution_m2.append(job2)
                    ant.possible_m2_jobs.remove(job2)

                    for task in ant.possible_m2_jobs:
                        if type(task) == Maintenance:
                            ant.possible_m2_jobs.remove(task)

                    if current_penalty > 1 and len(solution_m2) != TASKS:
                        mtc = Maintenance(time, job2)
                        ant.possible_m2_jobs.append(mtc)

                    job2.set_penalty(current_penalty)
                    current_penalty += 0.1
                    job2.begin_time_m2 = time
                    job2.end_time_m2 = time + ceil(job2.op2 * current_penalty)
                    m2_busy_time = ceil(job2.op2 * current_penalty)
                    ant.solution_m2.append(job2)

                else:
                    mtc = job2
                    mtc.set_times(time)
                    ant.solution_m2.append(mtc)
                    ant.possible_m2_jobs.remove(mtc)
                    m2_busy_time = mtc.length
                    current_penalty = 1
                    # TODO implement case if chosen job is maintenance

        elif not is_idle and m2_busy_time < 1:
            is_idle = True
            idle = IdleTime(time)
            ant.solution_m2.append(idle)

        time += 1
        m1_busy_time -= 1
        m2_busy_time -= 1


# if __name__ == 'main':
generate_jobs()
start_population()
initialize_pheromone_matrix()
update_pheromone_matrix()
for _ in range(ITERATIONS):
    for ant in ANTS:
        ant.reset()
        x = uniform(0, 1)
        if x < 0.2:
            t1, t2 = generate_random_solution()
            ant.solution_m1, ant.solution_m2 = t1, t2
        else:
            use_pheromone_matrix(ant)
        scr = score(ant.solution_m1, ant.solution_m2)
        if scr < ant.best_score:
            ant.best_score = scr
            ant.best_m1, ant.best_m2 = ant.solution_m1, ant.solution_m2
        ant.score, ant.solution_m1, ant.solution_m2 = ant.best_score, ant.best_m1, ant.best_m2

    update_pheromone_matrix()
    best = get_x_best()
    print(best[0].score)

print("xd")
