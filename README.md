# Controls_Algo
 Simple 2D PD Control Loop
 
 This code runs a simple PD control loop. The user can click on the game display to select the target position. The two default objects will then try to approach that target.
 
 The fundamental basic equation for the PD control loop is the following, which aims to accelerate an object towards a target position:
 acceleration_x = [ K_p * (x_target - x_object)] + [ K_d * (velocity_final - velocity_object)]
 
 K_p and K_d are gains, which are typically determined from they physical parameters of a system.
 
 (x_target - x_object) is the positional error, which is how far away the object is from the target.
 
 (velocity_final - velocity_object) is the velocity error, which is the delta-velocity between the desired final velocity and the object's current velocity.
 This program currently has velocity_final set to zero, meaning it wants the object to be at rest on the target.
 
 # Running the program
 To run the code, the user will need pygame and numpy installed on their machine/virtual environment.
 
 main.py is the game-loop file, and should run as-is. This file imports the second file. PhysObjects.py
 
 # Modifying the program
 In PhysObjects.py, the class Object2D contains the control methods: control_IfElse() and control_PD()
 In the control_PD method, there are hard-coded values for k_p and k_d. These can be adjusted to modify the behavior of the red circle.
