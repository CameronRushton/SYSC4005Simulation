# SYSC 4005 Simulation
Group members: Madelyn Krasnay, Eric Bedard, Cameron Rushton

The simulation models two inspectors taking three different components (inspector one takes infinite component ones and inspector two takes
random, infinite components two or three) and adding them to their respective buffers that are accessed by three workstations. 
Once the buffers in the workstation are not empty, a product can be made. Priority is given to workstation one with three having lowest priority.

Current implementation is iterative and not multithreaded. It also doesn't use the given files yet.
Seeds for random choosing of component 2 and 3 can be given.
