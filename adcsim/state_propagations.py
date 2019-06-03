"""
Functions in this file output the result of the differential equations that are used to propagate attitude given the
state passed to them (state includes attitude information and angular velocity information).

Includes the 'differential attitude equation" and the 'differential angular velocity equation' (Euler's rotational
equation of motion).

The angular velocity equation is always the same, but the attitude equation can use any attitude parametrization.
"""
import numpy as np
from adcsim import util as ut


# differential equations for an MRP attitude parametrization
def state_dot_mrp(state, control, inertia, inertia_inv):
    """
    Differential attitude equation for the Modified Rodriguez Parameters (MRP) attitude parametrization, with eulers
    rotational equation of motion.
    :param state: np.ndarray. The current attitude state (first index is attitude, second index is angular velocity)
    :param control: np.ndarray. The current applied torque to the spacecraft in the body frame
    :param inertia: np.ndarray. Moment of inertial tensor of the spacecraft.
    :param inertia_inv: np.ndarray. Inverse of the moment of inertial tensor of the spacecraft.
    :return: np.ndarray. First index is value of attitude differential equation, second is value of angular velocity
    differential equation
    """
    # sigmas
    a = (1 - state[0] @ state[0]) * np.identity(3) + 2 * ut.cross_product_operator(state[0]) + 2 * \
        np.outer(state[0], state[0])
    sigma_propagation = (1/4) * a  @ state[1]

    # omegas
    omega_propagation = inertia_inv @ ((-ut.cross_product_operator(state[1]) @ inertia @ state[1]) + control)

    return np.array([sigma_propagation, omega_propagation])


# old (could be in 'old' folder)
# equations change with reference frame
def state_dot_ref_frame(state, control, omega_r, inertia, inertia_inv):
    # sigmas
    a = (1 - state[0] @ state[0]) * np.identity(3) + 2 * ut.cross_product_operator(state[0]) + 2 * \
        np.outer(state[0], state[0])
    sigma_propagation = (1/4) * a  @ (state[1] - omega_r)

    # omegas
    omega_propagation = inertia_inv @ ((-ut.cross_product_operator(state[1]) @ inertia @ state[1]) + control)

    return np.array([sigma_propagation, omega_propagation])


# old (could be in 'old' folder)
# equations change with reaction wheels
def state_dot_reaction_wheels(state, control, inertia_rw, inertia_inv_rw, hs):
    # sigmas
    a = (1 - state[0] @ state[0]) * np.identity(3) + 2 * ut.cross_product_operator(state[0]) + 2 * \
        np.outer(state[0], state[0])
    sigma_propagation = (1/4) * a  @ state[1]

    # omegas
    cross = ut.cross_product_operator(state[1])
    omega_propagation = inertia_inv_rw @ ((-cross @ inertia_rw @ state[1]) - cross @ hs + control)

    return np.array([sigma_propagation, omega_propagation])
