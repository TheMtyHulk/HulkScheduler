import numpy as np
class Task_Assignment_Calc:
    def __init__(self,num_tasks, estimated_task_times, num_vms,) -> None:
        self.num_tasks = num_tasks
        self.estimated_task_times = estimated_task_times
        self.num_vms = num_vms
        
  
    def estimate_task_times(self,num_tasks):
        return np.random.rand(num_tasks) * 10  # Random estimates between 0 and 10

    def initialize_particles(self,num_particles, num_tasks, num_vms):
        particles = np.zeros((num_particles, num_tasks, num_vms))
        for i in range(num_particles):
            for task_id in range(num_tasks):
                vm_id = np.random.randint(0, num_vms)
                particles[i, task_id, vm_id] = 1
        return particles

    def calculate_completion_time(self,particle, task_times):
        completion_times = np.sum(particle * task_times[:, None], axis=0)
        return np.max(completion_times)

    def update_particles(self,particles, velocities, global_best, personal_bests, task_times, w=0.5, c1=1.0, c2=1.5):
        num_particles = particles.shape[0]
        for i in range(num_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = w * velocities[i] + c1 * r1 * (personal_bests[i] - particles[i]) + c2 * r2 * (global_best - particles[i])
            particles[i] += velocities[i]
            particles[i] = np.clip(particles[i], 0, 1)
            # Ensure each task is assigned to exactly one VM
            for task_id in range(particles.shape[1]):
                assigned_vm = np.argmax(particles[i, task_id])
                particles[i, task_id] = 0
                particles[i, task_id, assigned_vm] = 1
        return particles, velocities

    def pso_task_scheduling(self,num_tasks, task_times, num_vms, num_particles=30, num_iterations=100):
        particles = self.initialize_particles(num_particles, num_tasks, num_vms)
        velocities = np.zeros_like(particles)
        personal_bests = np.copy(particles)
        personal_best_times = np.array([self.calculate_completion_time(p, task_times) for p in personal_bests])
        global_best = personal_bests[np.argmin(personal_best_times)]
        global_best_time = np.min(personal_best_times)

        for _ in range(num_iterations):
            for i, particle in enumerate(particles):
                completion_time = self.calculate_completion_time(particle, task_times)
                if completion_time < personal_best_times[i]:
                    personal_bests[i] = particle
                    personal_best_times[i] = completion_time
                    if completion_time < global_best_time:
                        global_best = particle
                        global_best_time = completion_time

            particles, velocities =self.update_particles(particles, velocities, global_best, personal_bests, task_times)

        # Convert global_best to the desired output format
        task_distribution = np.argmax(global_best, axis=1)
        adjusted_distribution = np.zeros((num_tasks, num_vms), dtype=int)
        for task_id, vm_id in enumerate(task_distribution):
            adjusted_distribution[task_id, vm_id] = 1

        return adjusted_distribution, global_best_time

    def adjust_scheduling(self,best_distribution, actual_task_times, num_vms):
        num_tasks = len(actual_task_times)
        adjusted_distribution, adjusted_time = self.pso_task_scheduling(num_tasks, actual_task_times, num_vms)
        return adjusted_distribution, adjusted_time

    # Main execution flow
    # num_tasks = 15

num_vms = 5

# estimated_task_times = estimate_task_times(num_tasks)

with open('flength.txt','r') as f:
     estimated_task_times = np.array([float(line.strip()) for line in f])

num_tasks = len(estimated_task_times)

T=Task_Assignment_Calc()

initial_distribution, initial_time = T.pso_task_scheduling(num_tasks, estimated_task_times, num_vms)

actual_task_times = np.random.rand(num_tasks) * 8  # Actual times, for example

adjusted_distribution, adjusted_time = T.adjust_scheduling(initial_distribution, actual_task_times, num_vms)

    # Print the adjusted task distribution in the desired format
T=Task_Assignment_Calc()
for task_assignment in adjusted_distribution:
    print(task_assignment)
print("Adjusted Completion Time:", adjusted_time)