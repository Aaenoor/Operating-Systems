#!/usr/bin/env python
# coding: utf-8

# # Process Class

# In[1]:


import random

class Process:
    def __init__(self, process_id, arrival_time, burst_time, memory_required):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.memory_required = memory_required
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None


# # Simulation Environment

# In[2]:


def generate_processes(num_processes):
    processes = []
    for i in range(num_processes):
        arrival_time = random.randint(0, 10)
        burst_time = random.randint(1, 10)
        memory_required = random.randint(1, 100)
        processes.append(Process(i, arrival_time, burst_time, memory_required))
    return processes

def add_to_queues(processes, current_time):
    ready_queue = []
    waiting_queue = []
    for process in processes:
        if process.arrival_time <= current_time:
            ready_queue.append(process)
        else:
            waiting_queue.append(process)
    return ready_queue, waiting_queue


# # Scheduling Algorithms

# First-Come, First-Served (FCFS)
# 

# In[3]:


def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        process.start_time = current_time
        process.completion_time = current_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        current_time += process.burst_time
    return processes


# Shortest Job First (SJF)

# In[4]:


def sjf_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    current_time = 0
    while processes:
        ready_queue = [p for p in processes if p.arrival_time <= current_time]
        if ready_queue:
            ready_queue.sort(key=lambda x: x.burst_time)
            process = ready_queue.pop(0)
            processes.remove(process)
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            current_time += process.burst_time
    return processes


# Round Robin (RR)

# In[5]:


def rr_scheduling(processes, quantum):
    queue = sorted(processes, key=lambda x: x.arrival_time)
    current_time = 0
    while queue:
        process = queue.pop(0)
        if process.remaining_time <= quantum:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            current_time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
        else:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            current_time += quantum
            process.remaining_time -= quantum
            queue.append(process)
    return processes


# # Memory Management

# First-Fit

# In[6]:


class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.memory_blocks = [total_memory]

    def allocate(self, process):
        for i in range(len(self.memory_blocks)):
            if self.memory_blocks[i] >= process.memory_required:
                self.memory_blocks[i] -= process.memory_required
                if self.memory_blocks[i] == 0:
                    self.memory_blocks.pop(i)
                return True
        return False

    def deallocate(self, process):
        self.memory_blocks.append(process.memory_required)
        self.memory_blocks.sort()


# # Scheduling and Memory Management Simulation

# In[23]:


def sjf_scheduling(ready_queue):
    # Sort the ready queue based on burst time (shortest job first)
    sorted_queue = sorted(ready_queue, key=lambda p: p.burst_time)
    return sorted_queue

def simulate(processes, scheduling_algorithm, memory_manager):
    current_time = 0
    ready_queue, waiting_queue = add_to_queues(processes, current_time)
    
    while ready_queue or waiting_queue:
        print(f"Current Time: {current_time}")
        print(f"Ready Queue: {[p.process_id for p in ready_queue]}")
        print(f"Waiting Queue: {[p.process_id for p in waiting_queue]}")
        
        if not ready_queue:
            current_time += 1
            ready_queue, waiting_queue = add_to_queues(processes, current_time)
            continue
        
        # Ensure there are processes in the ready queue before scheduling
        if ready_queue:
            process = scheduling_algorithm(ready_queue)[0]  # Select first process in SJF order
            print(f"Selected Process: {process.process_id}")
            
            if memory_manager.allocate(process):
                if current_time < process.arrival_time:
                    current_time = process.arrival_time
                process.start_time = current_time
                current_time += process.burst_time
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                memory_manager.deallocate(process)
                print(f"Process {process.process_id}: Scheduled")
            else:
                print(f"Process {process.process_id}: Not enough memory, waiting")
                waiting_queue.append(process)
            
            ready_queue.remove(process)
            ready_queue, waiting_queue = add_to_queues(processes, current_time)
        else:
            current_time += 1
            ready_queue, waiting_queue = add_to_queues(processes, current_time)

    return processes


# # User Interface

# In[24]:


def simulate(processes, scheduling_algorithm, memory_manager):
    current_time = 0
    ready_queue, waiting_queue = add_to_queues(processes, current_time)
    
    while ready_queue or waiting_queue:
        print(f"Current Time: {current_time}")
        print(f"Ready Queue: {[p.process_id for p in ready_queue]}")
        print(f"Waiting Queue: {[p.process_id for p in waiting_queue]}")
        
        if not ready_queue:
            current_time += 1
            ready_queue, waiting_queue = add_to_queues(processes, current_time)
            continue
        
        process = scheduling_algorithm(ready_queue)[0]
        print(f"Selected Process: {process.process_id}")
        
        if memory_manager.allocate(process):
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            memory_manager.deallocate(process)
            print(f"Process {process.process_id}: Scheduled")
        else:
            print(f"Process {process.process_id}: Not enough memory, waiting")
            waiting_queue.append(process)
        
        ready_queue.remove(process)
        ready_queue, waiting_queue = add_to_queues(processes, current_time)
    
    return processes


# In[25]:


def main():
    num_processes = int(input("Enter the number of processes: "))
    processes = []
    
    for i in range(num_processes):
        process_id = i + 1
        arrival_time = int(input(f"Enter arrival time for Process {process_id}: "))
        burst_time = int(input(f"Enter burst time for Process {process_id}: "))
        memory_required = int(input(f"Enter memory required for Process {process_id}: "))
        processes.append(Process(process_id, arrival_time, burst_time, memory_required))
    
    print("Select Scheduling Algorithm: ")
    print("1. FCFS")
    print("2. SJF")
    print("3. RR")
    scheduling_choice = int(input())
    
    print("Select Memory Management Technique: ")
    print("1. First-Fit")
    memory_choice = int(input())
    
    total_memory = int(input("Enter the total memory: "))
    memory_manager = MemoryManager(total_memory)
    
    if scheduling_choice == 1:
        scheduled_processes = simulate(processes, fcfs_scheduling, memory_manager)
    elif scheduling_choice == 2:
        scheduled_processes = simulate(processes, sjf_scheduling, memory_manager)
    elif scheduling_choice == 3:
        quantum = int(input("Enter the time quantum: "))
        scheduled_processes = simulate(processes, lambda p: rr_scheduling(p, quantum), memory_manager)
    
    for process in scheduled_processes:
        print(f"Process {process.process_id}: Waiting Time = {process.waiting_time}, Turnaround Time = {process.turnaround_time}")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




