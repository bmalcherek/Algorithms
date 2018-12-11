from random import randint, choice, uniform
from math import ceil
import msvcrt as m


# HEURISTIC GLOBAL VAIRABLES
TASKS = 50
T_MIN = 5
T_MAX = 20
MAINTENANCE_CHANCE = 0.3
M2_PENALTY = 0.1
MAINTENANCE_TIME_COEFFICIENT = 1.5
POPULATION = 100
ITERATIONS = 100
BEST_ANTS = 20
EVAPORATION_RATE = 0.2

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
		self.op1 = o1
		self.op2 = o2
		self.index = i

	def set_begin_time(self, time):
		self.begin_time = time

	def set_end_time(self, time):
		self.end_time = time

	def set_penalty(self, p):
		self.penalty = p
		self.real_length_op2 = ceil(p * self.op2)

	def __str__(self):
		# return f"job{self.index}"
		return str(self.index)

	def __repr__(self):
		re2turn str(self)


class Maintenance:
	def __init__(self, time):
		self.begin_time = time
		self.length = MAINTENANCE_DURATION
		self.end_time = time + self.length

	def __str__(self):
		return "mtc"

	def __repr__(self):
		return str(self)


class IdleTime:
	def __init__(self, time):
		self.begin_time = time

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

	def set_score(self):
		self.score = score(self.solution_m1, self.solution_m2)

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
 	#SOLUTION VARIABLES
	solution_m1 = list()
	solution_m2 = list()
	solution_m2_with_maintenance = list()
	maintenance_count = 0
	idle_count = 0

 	#OTHER VARIABLES
	not_used_jobs = JOBS.copy()
	possible_m2_jobs = list()
	m1_time_busy = 0
	m2_time_busy = 0
	first_done = False
	last_done = False
	current_m2_penalty = 1
	time = 0
	is_idle= False

	while len(solution_m2) != len(JOBS) or m2_time_busy > 0:
		if m1_time_busy < 1 and len(not_used_jobs) > 0:
			if first_done:
				solution_m1.append(job1)
				job1.set_end_time(time)
				possible_m2_jobs.append(job1)

			first_done = True
			job1 = choice(not_used_jobs)
			not_used_jobs.remove(job1)
			m1_time_busy = job1.op1
			job1.set_begin_time(time)

		if len(not_used_jobs) == 0 and m1_time_busy < 1 and not(last_done):
			last_done = True
			solution_m1.append(job1)
			job1.set_end_time(time)
			possible_m2_jobs.append(job1)
			# print("----M1 END----")

		if (m2_time_busy < 1) and (len(possible_m2_jobs) > 0 or current_m2_penalty > 1):
			# random choice between normal job or maintenance. X is float between 0 and 1 and if its lower than MAINTENANCE_CHANCE algorithm is choosing maintenance
			# program cannot do more than 1 maintenance in a row, so it will ignore random choice if current_m2_penalty == 1
			x = uniform(0, 1)
			# print(x)

			if x < MAINTENANCE_CHANCE and current_m2_penalty > 1:
				if is_idle:
					idle.set_end_time(time)
					solution_m2_with_maintenance.append(idle)
					is_idle= False

				current_m2_penalty = 1
				m2_time_busy = MAINTENANCE_DURATION
				maintenance_count += 1
				maintenance = Maintenance(time)
				solution_m2_with_maintenance.append(maintenance)

			elif len(possible_m2_jobs) > 0:
				if is_idle:
					idle.set_end_time(time)
					solution_m2_with_maintenance.append(idle)
					is_idle= False

				job2 = choice(possible_m2_jobs)
				job2.set_begin_time(time)
				job2.set_end_time(time + job2.op2)
				solution_m2.append(job2)
				solution_m2_with_maintenance.append(job2)
				possible_m2_jobs.remove(job2)
				m2_time_busy = ceil(job2.op2 * current_m2_penalty)
				job2.set_penalty(current_m2_penalty)
				current_m2_penalty += M2_PENALTY

			elif len(possible_m2_jobs) == 0 and x >= MAINTENANCE_CHANCE and not(is_idle):
				idle = IdleTime(time)
				is_idle = True

		elif m2_time_busy < 1 and len(possible_m2_jobs) == 0 and current_m2_penalty == 1 and not(is_idle):
			idle = IdleTime(time)
			is_idle = True

		# print(time, solution_m1, solution_m2, solution_m2_with_maintenance, m2_time_busy)

		time += 1
		m1_time_busy -= 1
		m2_time_busy -= 1

	return solution_m1, solution_m2_with_maintenance


def score(solution_m1, solution_m2):
	m1_score = solution_m1[-1].end_time
	m2_score = solution_m2[-1].end_time

	return m1_score + m2_score


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
		if not(first):
			first = True
			print(f"op1_{job.index}, {job.begin_time}, {job.op1}, {job.op1}", end="", file=OUTPUT_FILE)
		else:
			print(f"; op1_{job.index}, {job.begin_time}, {job.op1}, {job.op1}", end="", file=OUTPUT_FILE)

	print("", file=OUTPUT_FILE)
	first = False
	print("M2: ", end="", file=OUTPUT_FILE)

	for element in solution_m2:		
		if type(element) is Job:
			print(f"; op1_{element.index}, {element.begin_time}, {element.op1}, {element.op1}", end="", file=OUTPUT_FILE)

		elif type(element) is Maintenance:
			print(f"; maint{maintenance_count}_M2, {element.begin_time}, {element.length}", end="", file=OUTPUT_FILE)
			maintenance_count += 1
			maintenance_time += element.length

		elif type(element) is IdleTime:
			if not(first):
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
	global PHEROMONE_MATRIX_M1, PHEROMONE_MATRIX_M2

	for i in range(TASKS):
		temp = list()
		for j in range(TASKS):
			temp.append(None)
		PHEROMONE_MATRIX_M1.append(temp)

	for i in range(TASKS + MAX_MAINTENANCE):
		temp = list()
		for j in range(TASKS + MAX_MAINTENANCE):
			temp.append(None)
		PHEROMONE_MATRIX_M2.append(temp)


def update_pheromone_matrix(ants):
	max_weight = BEST_ANTS
	old_pheromone_matrix = PHEROMONE_MATRIX.copy()

	for row in PHEROMONE_MATRIX:
		for cell in row:
			for ant in ants:



generate_jobs()
solution_m1, solution_m2_with_maintenance = generate_random_solution()
generate_output_file(solution_m1, solution_m2_with_maintenance)
start_population()
get_x_best()