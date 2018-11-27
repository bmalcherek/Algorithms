from random import randint, choice, uniform
from math import ceil
import msvcrt as m


TASKS = 5
T_MIN = 5
T_MAX = 20
IDLE_TIME_COEFFICIENT = 1.5
INPUT_FILE = open("input.txt", "w")
OUTPUT_FILE = open("output.txt", "w")
JOBS = list()
MAINTENANCE_CHANCE = 0.5
M2_PENALTY = 0.1

average_m2_time = 0

def generate_jobs():
	t2_sum = 0

	for i in range(TASKS):		
		t1 = randint(T_MIN, T_MAX)
		t2 = randint(T_MIN, T_MAX)
		t2_sum += t2
		temp = [t1, t2]
		JOBS.append(temp)

		print(f"czas_operacji1_{i};{t1};czas_operacji2_{i};{t2}", file=INPUT_FILE)

	# jobs = np.array(jobs)
	average_m2_time = ceil(t2_sum / TASKS)
	print(ceil(t2_sum / TASKS), average_m2_time)

print(average_m2_time)


def generate_random_solution():
	time = 0
	not_used_jobs = [i for i  in range(TASKS)]
	possible_m2_jobs = list()
	solution_m1 = list()
	solution_m2 = list()
	solution_m2_with_maintenance = list()
	m1_time_busy = 0
	m2_time_busy = 0
	first_done = False
	last_done = False
	current_m2_penalty = 1
	maintenance_count = 0

	while len(solution_m2) != len(JOBS) or m2_time_busy > 0:

		if m1_time_busy < 1 and len(not_used_jobs) > 0:
			if first_done:
				possible_m2_jobs.append(job1)
			first_done = True
			job1 = choice(not_used_jobs)
			not_used_jobs.remove(job1)
			solution_m1.append(job1)
			m1_time_busy = JOBS[job1][0]
			# if first_done:
			# 	possible_m2_jobs.append(job1)

		if len(not_used_jobs) == 0 and not(last_done):
			last_done = True
			possible_m2_jobs.append(job1)

		print(time, average_m2_time, not_used_jobs, possible_m2_jobs, solution_m2, solution_m2_with_maintenance, current_m2_penalty)

		if (m2_time_busy < 1) and (len(possible_m2_jobs) > 0 or current_m2_penalty > 1):

			# random choice between normal job or maintenance. X is float between 0 and 1 and if its bigger than MAINTENANCE_CHANCE algorithm is choosing maintenance
			# program cannot do more than 1 maintenance in a row, so it will ignore random choice if current_m2_penalty == 1
			x = uniform(0, 1)

			if x > MAINTENANCE_CHANCE and current_m2_penalty > 1:
				current_m2_penalty = 1
				m2_time_busy = average_m2_time * IDLE_TIME_COEFFICIENT
				maintenance_count += 1
				solution_m2_with_maintenance.append(f"m{maintenance_count}")

			else:
				if len(possible_m2_jobs) > 0:
					job2 = choice(possible_m2_jobs)
					solution_m2.append(job2)
					solution_m2_with_maintenance.append(job2)
					possible_m2_jobs.remove(job2)
					m2_time_busy = ceil(JOBS[job2][1] * current_m2_penalty)
					current_m2_penalty += M2_PENALTY

		m1_time_busy -= 1
		m2_time_busy -= 1
		time += 1
		# if(time%100 == 0):
		# 	m.getch()


print(TASKS, file=INPUT_FILE)
generate_jobs()
generate_random_solution()