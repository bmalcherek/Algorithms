from random import randint, choice, uniform
from math import ceil
import msvcrt as m


# HEURISTIC GLOBAL VAIRABLES
TASKS = 10   
T_MIN = 5
T_MAX = 20
MAINTENANCE_CHANCE = 0.3
M2_PENALTY = 0.1
MAINTENANCE_TIME_COEFFICIENT = 1.5
POPULATION = 100

# OTHER GLOBAL VARIABLES
INPUT_FILE = open("input.txt", "w")
OUTPUT_FILE = open("output.txt", "w")
JOBS = list()

# GLOBAL VARIABLES TO CALCULATE FROM GENERATED DATA
AVERAGE_M2_TIME = 0
MAINENANE_DURATION = 0


class Job:
	def __init__(self, o1, o2, i):
		self.op1 = o1
		self.op2 = o2
		self.index = i

	def set_begin_time(self, time):
		self.begin_time = time

	def set_end_time(self, time):
		self.end_time = time

	def __str__(self):
		# return f"job{self.index}"
		return str(self.index)

	def __repr__(self):
		return str(self)


class Maintenance:
	def __init__(self, time):
		self.begin_time = time
		self.length = MAINENANE_DURATION
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

	def __str__(self):
		return f"idle {self.begin_time} - {self.end_time}"

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
	global MAINENANE_DURATION
	AVERAGE_M2_TIME = ceil(t2_sum / TASKS)
	MAINENANE_DURATION = ceil(MAINTENANCE_TIME_COEFFICIENT * AVERAGE_M2_TIME)

 
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
			print("----M1 END----")

		if (m2_time_busy < 1) and (len(possible_m2_jobs) > 0 or current_m2_penalty > 1):
			# random choice between normal job or maintenance. X is float between 0 and 1 and if its lower than MAINTENANCE_CHANCE algorithm is choosing maintenance
			# program cannot do more than 1 maintenance in a row, so it will ignore random choice if current_m2_penalty == 1
			x = uniform(0, 1)
			print(x)

			if x < MAINTENANCE_CHANCE and current_m2_penalty > 1:
				if is_idle:
					idle.set_end_time(time)
					solution_m2_with_maintenance.append(idle)
					is_idle= False

				current_m2_penalty = 1
				m2_time_busy = MAINENANE_DURATION
				maintenance_count += 1
				maintenance = Maintenance(time)
				solution_m2_with_maintenance.append(maintenance)

			elif len(possible_m2_jobs) > 0:
				if is_idle:
					idle.set_end_time(time)
					solution_m2_with_maintenance.append(idle)
					is_idle= False

				job2 = choice(possible_m2_jobs)
				solution_m2.append(job2)
				solution_m2_with_maintenance.append(job2)
				possible_m2_jobs.remove(job2)
				m2_time_busy = ceil(job2.op2 * current_m2_penalty)
				current_m2_penalty += M2_PENALTY

			elif len(possible_m2_jobs) == 0 and x >= MAINTENANCE_CHANCE and not(is_idle):
				idle = IdleTime(time)
				is_idle = True

		elif m2_time_busy < 1 and len(possible_m2_jobs) == 0 and current_m2_penalty == 1 and not(is_idle):
			idle = IdleTime(time)
			is_idle = True


		print(time, solution_m1, solution_m2, solution_m2_with_maintenance, m2_time_busy)

		time += 1
		m1_time_busy -= 1
		m2_time_busy -= 1


generate_jobs()
# print(AVERAGE_M2_TIME)
print(JOBS)
generate_random_solution()