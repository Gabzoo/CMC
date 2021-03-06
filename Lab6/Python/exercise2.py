""" Lab 6 Exercise 2

This file implements the pendulum system with two muscles attached

"""

from math import sqrt

import farms_pylog as pylog
import numpy as np
from matplotlib import pyplot as plt

from cmcpack import DEFAULT
from cmcpack.plot import save_figure
from muscle import Muscle
from muscle_system import MuscleSystem
from neural_system import NeuralSystem
from pendulum_system import PendulumSystem
from system import System
from system_animation import SystemAnimation
from system_parameters import (MuscleParameters, NetworkParameters,
                               PendulumParameters)
from system_simulation import SystemSimulation

plt.close('all')

# Global settings for plotting
# You may change as per your requirement
plt.rc('lines', linewidth=2.0)
plt.rc('font', size=12.0)
plt.rc('axes', titlesize=14.0)     # fontsize of the axes title
plt.rc('axes', labelsize=14.0)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=14.0)    # fontsize of the tick labels
plt.rc('ytick', labelsize=14.0)    # fontsize of the tick labels

DEFAULT["save_figures"] = True


def system_init():
    """Initialize default system."""
    ########## PENDULUM ##########
    # Define and Setup your pendulum model here
    # Check Pendulum.py for more details on Pendulum class
    P_params = PendulumParameters()  # Instantiate pendulum parameters
    P_params.L = 1.0  # To change the default length of the pendulum
    P_params.m = 0.25  # To change the default mass of the pendulum
    pendulum = PendulumSystem(P_params)  # Instantiate Pendulum object
    #### CHECK OUT Pendulum.py to ADD PERTURBATIONS TO THE MODEL #####
    pylog.info('Pendulum model initialized \n {}'.format(
        pendulum.parameters.showParameters()))

    ########## MUSCLES ##########
    # Define and Setup your muscle model here
    # Check MuscleSystem.py for more details on MuscleSystem class
    m1_param = MuscleParameters()  # Instantiate Muscle 1 parameters
    m1_param.f_max = 200.  # To change Muscle 1 max force
    m1_param.l_opt = 0.4
    m1_param.l_slack = 0.45
    m2_param = MuscleParameters()  # Instantiate Muscle 2 parameters
    m2_param.f_max = 200.  # To change Muscle 2 max force
    m2_param.l_opt = 0.4
    m2_param.l_slack = 0.45
    m1 = Muscle('m1', m1_param)  # Instantiate Muscle 1 object
    m2 = Muscle('m2', m2_param)  # Instantiate Muscle 2 object
    # Use the MuscleSystem Class to define your muscles in the system
    # Instantiate Muscle System with two muscles
    muscles = MuscleSystem(m1, m2)
    pylog.info('Muscle system initialized \n {} \n {}'.format(
        m1.parameters.showParameters(),
        m2.parameters.showParameters()))
    # Define Muscle Attachment points
    m1_origin = np.asarray([0.0, 0.9])  # Origin of Muscle 1
    m1_insertion = np.asarray([0.0, 0.15])  # Insertion of Muscle 1

    m2_origin = np.asarray([0.0, 0.8])  # Origin of Muscle 2
    m2_insertion = np.asarray([0.0, -0.3])  # Insertion of Muscle 2
    # Attach the muscles
    muscles.attach(np.asarray([m1_origin, m1_insertion]),
                   np.asarray([m2_origin, m2_insertion]))

    ########## ADD SYSTEMS ##########
    # Create a system with Pendulum and Muscles using the System Class
    # Check System.py for more details on System class
    sys = System()  # Instantiate a new system
    sys.add_pendulum_system(pendulum)  # Add the pendulum model to the system
    sys.add_muscle_system(muscles)  # Add the muscle model to the system

    ########## INITIALIZATION ##########
    t_max = 4  # Maximum simulation time
    time = np.arange(0., t_max, 0.001)  # Time vector
    ##### Model Initial Conditions #####
    x0_P = np.asarray([np.pi/2, 0.0])  # Pendulum initial condition
    # Muscle Model initial condition
    l_ce_0 = sys.muscle_sys.initialize_muscle_length(np.pi/2)
    x0_M = np.asarray([0.05, l_ce_0[0], 0.05, l_ce_0[1]])
    x0 = np.concatenate((x0_P, x0_M))  # System initial conditions

    ########## System Simulation ##########
    sim = SystemSimulation(sys)  # Instantiate Simulation object
    # Simulate the system for given time
    sim.initalize_system(x0, time)  # Initialize the system state
    return sim


def exercise2():
    """ Main function to run for Exercise 2.

    Parameters
    ----------
        None

    Returns
    -------
        None
    """
    sim = system_init()

    # Add muscle activations to the simulation
    # Here you can define your muscle activation vectors
    # that are time dependent

   # act1 = np.ones((len(sim.time), 1)) * 0.05
   # act2 = np.ones((len(sim.time), 1)) * 0.05
    A= 0.95

    act1 = 0.05+ np.absolute(np.expand_dims((np.sin(2.*np.pi*sim.time)),axis=1))*A
    act2 = 0.05+ np.absolute(np.expand_dims((np.cos(2.*np.pi*sim.time)),axis=1))*A
    #Frequency Variation
    
    act11 = 0.05 + np.absolute(np.expand_dims((np.sin(2.*np.pi*sim.time*0.25)),axis=1))*A
    act21 = 0.05 + np.absolute(np.expand_dims((np.cos(2.*np.pi*sim.time*0.25)),axis=1))*A
    act12 = 0.05 + np.absolute(np.expand_dims((np.sin(2.*np.pi*sim.time*0.5)),axis=1))*A
    act22 = 0.05 + np.absolute(np.expand_dims((np.cos(2.*np.pi*sim.time*0.5)),axis=1))*A
    act13 = 0.05 + np.absolute(np.expand_dims((np.sin(2.*np.pi*sim.time*2)),axis=1))*A
    act23 = 0.05 + np.absolute(np.expand_dims((np.cos(2.*np.pi*sim.time*2)),axis=1))*A
    act14 = 0.05 + np.absolute(np.expand_dims((np.sin(2.*np.pi*sim.time*4)),axis=1))*A
    act24 = 0.05 + np.absolute(np.expand_dims((np.cos(2.*np.pi*sim.time*4)),axis=1))*A
    
    activations = np.hstack((act1, act2))
    
    activations1 = np.hstack((act11, act21))
    activations2 = np.hstack((act12, act22))
    activations3 = np.hstack((act13, act23))
    activations4 = np.hstack((act14, act24))
    
    plt.figure('Activations forms')
    plt.plot(sim.time, act1, label = "Activation 1 - Sinus")
    plt.plot(sim.time, act2, label = "Activation 2 - Cosinus")
    plt.legend(loc="best")
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    # Method to add the muscle activations to the simulation

    sim.add_muscle_stimulations(activations)

    #: If you would like to perturb the pedulum model then you could do
    # so by
    sim.sys.pendulum_sys.parameters.PERTURBATION = True
    # The above line sets the state of the pendulum model to zeros between
    # time interval 1.2 < t < 1.25. You can change this and the type of
    # perturbation in
    # pendulum_system.py::pendulum_system function

    # Integrate the system for the above initialized state and time
    sim.simulate()

    # Obtain the states of the system after integration
    # res is np.asarray [time, states]
    # states vector is in the same order as x0
    res = sim.results()

    # In order to obtain internal states of the muscle
    # you can access the results attribute in the muscle class
    muscle_1_results = sim.sys.muscle_sys.muscle_1.results
    muscle_2_results = sim.sys.muscle_sys.muscle_2.results
#PARTIE 2A
    theta = np.linspace(np.pi/4, 3*np.pi/4,50)
    # plot muscle 1 length
    plt.figure('Muscle Length')
    L1 = np.sqrt(sim.sys.muscle_sys.a1_m1**2 + sim.sys.muscle_sys.a2_m1**2 - 2*sim.sys.muscle_sys.a1_m1*sim.sys.muscle_sys.a2_m1*np.cos(theta))
    plt.plot(theta, L1, label = 'Muscle 1')
    print(sim.sys.muscle_sys.a1_m1)
    print(sim.sys.muscle_sys.a2_m1)
    print(sim.sys.muscle_sys.a1_m2)
    print(sim.sys.muscle_sys.a2_m2)
     # plot muscle 2 length
    L2 = np.sqrt(sim.sys.muscle_sys.a1_m2**2 + sim.sys.muscle_sys.a2_m2**2 + 2*sim.sys.muscle_sys.a1_m2*sim.sys.muscle_sys.a2_m2*np.cos(theta))
    plt.plot(theta, L2, label = 'Muscle 2')
    plt.xlabel('Theta [rad]')
    plt.ylabel('Muscle Length [m]')
    plt.legend(loc="upper left")
    plt.show()
    plt.figure('Muscle moment arm')
    h1 = sim.sys.muscle_sys.a1_m1*sim.sys.muscle_sys.a2_m1*np.sin(theta)/L1
    plt.plot(theta, h1, label = 'Muscle 1')
    h2 = sim.sys.muscle_sys.a1_m2*sim.sys.muscle_sys.a2_m2*np.sin(theta)/L2
    plt.plot(theta, h2, label = 'Muscle 2')
    plt.xlabel('Theta [rad]')
    plt.ylabel('Moment arm of muscle [m]')
    plt.legend(loc="upper left")
    plt.show()

#PARTIE 2B
    
    plt.figure('Pendulum')
    plt.figure('Pendulum Phase')
    plt.plot(res[:, 1], res[:, 2])
#PARTIE2C
    # Plotting the results
    plt.figure('Pendulum')
    plt.title('Pendulum Phase')
    plt.plot(res[:, 1], res[:, 2], label ="Initial f=1")
    
    sim.add_muscle_stimulations(activations1)
    sim.sys.pendulum_sys.parameters.PERTURBATION = True
    sim.simulate()
    res1 = sim.results()
    plt.plot(res1[:, 1], res1[:, 2], label="f=0.25")
    
    sim.add_muscle_stimulations(activations2)
    sim.sys.pendulum_sys.parameters.PERTURBATION = True
    sim.simulate()
    res2 = sim.results()
    plt.plot(res2[:, 1], res2[:, 2], label="f=0.5")
    
    sim.add_muscle_stimulations(activations3)
    sim.sys.pendulum_sys.parameters.PERTURBATION = True
    sim.simulate()
    res3 = sim.results()
    plt.plot(res3[:, 1], res3[:, 2], label="f=2")
    
    sim.add_muscle_stimulations(activations4)
    sim.sys.pendulum_sys.parameters.PERTURBATION = True
    sim.simulate()
    res4 = sim.results()
    plt.plot(res4[:, 1], res4[:, 2], label="f=4")
    
    
    plt.xlabel('Position [rad]')
    plt.ylabel('Velocity [rad.s]')
    plt.grid()
    plt.legend(loc="best")
    
    
    
    # To animate the model, use the SystemAnimation class
    # Pass the res(states) and systems you wish to animate
    simulation = SystemAnimation(
        res, sim.sys.pendulum_sys, sim.sys.muscle_sys
    )
    if not DEFAULT["save_figures"]:
        # To start the animation
        simulation.animate()
        plt.show()
    else:
        figures = plt.get_figlabels()
        pylog.debug("Saving figures:\n{}".format(figures))
        for fig in figures:
            plt.figure(fig)
            save_figure(fig)
            plt.close(fig)


if __name__ == '__main__':
    from cmcpack import parse_args
    parse_args()
    exercise2()

