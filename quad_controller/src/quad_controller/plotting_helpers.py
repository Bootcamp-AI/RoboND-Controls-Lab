"""helper functions for plotting the path of the quad copter,and
comparing the path it took to the path generated by trajectory_manager"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D
import os
import time
import rospkg



def plot_path_2d(quad_path,
                 planned_path=None,
                 waypoints=None,
                 h_axis='x',
                 v_axis='y'):

    """ Generates and saves a 2D plot of the quad's path.

    Use this function to generate individual 2D plots of the quads path, and the planned path
    Use h_axis and v_axis to specify which two dimension to compare.

    Args:
        quad_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z quad positions
        planned_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z target positions
        waypoints (numpy.ndarray): A 2D numpy.ndarray of x,y,z positions
        out_fname (str): string path and file name to save the output to
        h_axis (str): One of 'x', 'y', or 'z. The 3d axis to use as horizontal in the 2d plot.
        v_axis (str): One of 'x', 'y', or 'z. The 3d axis to use as vertical in the 2d plot.

    Returns: None

    """
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(16, 10))
    axes = fig.add_subplot(111)
    fig.suptitle('Quadrotor Path', weight='bold', fontsize=14)

    # generate the plot for this axes
    axes = path_2d(quad_path, axes, planned_path, waypoints,  h_axis, v_axis)

    quad_patch = patches.Patch(color='k')
    handles = [quad_patch]
    labels = ['quadrotor path']

    if planned_path is not None:
        planned_patch = patches.Patch(color='r')
        labels.append('planned_path')
        handles.append(planned_patch)

    if waypoints is not None:
        waypoints_patch = patches.Patch(color='b')
        labels.append('waypoints')
        handles.append(waypoints_patch)

    fig.legend(handles=handles,
               labels=labels,
               loc='upper right',
               fontsize=11,
               frameon=False)

    rospack = rospkg.rospack.RosPack()
    base_path = rospack.get_path('quad_controller')

    out_path = os.path.join(base_path, 'output_data', 'one_plot_' + str(time.time()) + '.png')
    fig.savefig(out_path, dpi='figure')


def plot_path_3d(quad_path,
                 planned_path=None,
                 waypoints=None,
                 out_fname='/home/d/Desktop/tmp_3d.png',
                 azimuth=210.0,
                 elevation=45.0):

    """ Generates, displays, and saves a 3d plot of the quads path,

    Use this function to generate 3d plots of the path the quad took and path it was trying to follow.
    Use the parameters azimuth, and elevation to specify the initial viewing angle if saving plots to .png.

    Args:
        quad_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z quad positions
        planned_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z target positions
        waypoints (numpy.ndarray): A 2D numpy.ndarray of x,y,z positions
        out_fname (str): string path and file name to save the output to
        azimuth (float): The initial azimuth angle of the viewpoint for the matplotlib 3d plot
        elevation (float): the initial elevation of the viewpoint

    Returns: None

    """

    plt.style.use('ggplot')
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Quadrotor Path', weight='bold', fontsize=14)
    ax3d = fig.add_subplot(111, projection='3d')

    ax3d = path_3d(quad_path, ax3d, planned_path, waypoints)
    ax3d.view_init(elevation, azimuth)

    quad_patch = patches.Patch(color='k')
    handles = [quad_patch]
    labels = ['quadrotor path']

    if planned_path is not None:
        planned_patch = patches.Patch(color='r')
        labels.append('planned_path')
        handles.append(planned_patch)

    if waypoints is not None:
        waypoints_patch = patches.Patch(color='b')
        labels.append('waypoints')
        handles.append(waypoints_patch)

    fig.legend(handles=handles,
               labels=labels,
               loc='upper right',
               fontsize=11,
               frameon=False)


    rospack = rospkg.rospack.RosPack()
    base_path = rospack.get_path('quad_controller')

    out_path = os.path.join(base_path, 'output_data', 'isometric_plot_' + str(time.time()) + '.png')
    fig.savefig(out_path, dpi='figure')


def plot_path_grid(quad_path,
                   planned_path=None,
                   waypoints=None,
                   out_fname='/home/d/Desktop/tmp_grid.png',
                   azimuth=210,
                   elevation=45):
    """Generates and saves a two by two grid of plots of the quadrotor's path.

    Creates four plots with different perspectives on the quads path. Two perspectives with z on the horizontal axis, and the x,y plane.
    Additionally it generates a 3d plot with configurable angle. Shows the plot as well as saves it to .png

    Args:
        quad_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z quad positions
        planned_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z target positions
        waypoints (numpy.ndarray): A 2D numpy.ndaray of x,y,z positions
        out_fname (str): path and file name to save the output to
        azimuth (float): The initial azimuth angle of the viewpoint for the matplotlib 3d plot
        elevation (float): the initial elevation of the viewpoint

    Returns: None

    """


    # set up the figure
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(16,10))
    fig.suptitle('Quadrotor Path: multiple perspectives', weight='bold', fontsize=14)

    # create the axes for the plot
    axe00 = fig.add_subplot(2,2,1)
    axe01 = fig.add_subplot(2,2,2, projection='3d')
    axe10 = fig.add_subplot(2,2,3)
    axe11 = fig.add_subplot(2,2,4)

    # generate the path subplots
    axe00 = path_2d(quad_path, axe00, planned_path, waypoints, h_axis='x', v_axis='y')
    axe01 = path_3d(quad_path, axe01, planned_path, waypoints)
    axe10 = path_2d(quad_path, axe10, planned_path, waypoints, h_axis='x', v_axis='z')
    axe11 = path_2d(quad_path, axe11, planned_path, waypoints, h_axis='y', v_axis='z')

    # set viewpoint for 3d
    axe01.view_init(elevation, azimuth)

    # add legend info to the plots
    quad_patch = patches.Patch(color='k')

    handles = [quad_patch]
    labels = ['quadrotor path']

    if planned_path is not None:
        planned_patch = patches.Patch(color='r')
        labels.append('planned path')
        handles.append(planned_patch)

    if waypoints is not None:
        waypoints_patch = patches.Patch(color='b')
        labels.append('waypoints')
        handles.append(waypoints_patch)

    fig.legend(handles=handles,
               labels=labels,
               loc='upper right',
               fontsize=11,
               frameon=False)

    # save and show the plot
    rospack = rospkg.rospack.RosPack()
    base_path = rospack.get_path('quad_controller')

    out_path = os.path.join(base_path, 'output_data', 'grid_plot_' + str(time.time()) + '.png')

    fig.savefig(out_path, dpi='figure')


def path_2d(quad_path,
            axes,
            planned_path=None,
            waypoints=None,
            h_axis='x',
            v_axis='y',
            quad_lw=1.0,
            path_size=3.5,
            wp_size=6.0):

    """ Plots the path of a quad on a matplotlib axes.

    Only use if you want to modify the look of the plots, otherwise use plot_path_2d to generate plots.

    Args:
        quad_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z quad positions
        axes (matplotlib axes): The matplotlib axes object the path's are plotted on.
        planned_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z target positions
        waypoints (numpy.ndarray): A 2D numpy.ndarray of x,y,z positions
        h_axis (str): One of 'x', 'y', or 'z. The 3d axis to use as horizontal in the 2d plot.
        v_axis (str): One of 'x', 'y', or 'z. The 3d axis to use as vertical in the 2d plot.
        quad_lw (float): The float linewidth for the quads path
        path_size (float): The float markersize for the planned path markers
        wp_size (float): The float markersize for the waypoint markers

    Returns:
        axes (matplotlib axes): matplotlib axes with the path's plotted.

    """

    axis_labels = dict()
    axis_labels[0] = 'X'
    axis_labels[1] = 'Y'
    axis_labels[2] = 'Z'

    axis_pos = dict()
    axis_pos['x'] = 0
    axis_pos['y'] = 1
    axis_pos['z'] = 2

    # select the correct column for the horizontal and vertical axis
    h_ax = axis_pos[h_axis]
    v_ax = axis_pos[v_axis]

    if planned_path is not None:
        axes.plot(planned_path[:,h_ax], planned_path[:,v_ax], 'go',
                  color='r',markersize=path_size, markeredgecolor='r')


    axes.plot(quad_path[:,h_ax], quad_path[:,v_ax],
              color='k', linewidth=quad_lw)

    if waypoints is not None:
        axes.plot(waypoints[:,h_ax], waypoints[:,v_ax], 'gH',
                  markersize=wp_size, color='b',  markeredgecolor='b')

    axes.tick_params(labelsize=9)
    axes.set_xlabel(axis_labels[h_ax], weight='bold')
    axes.set_ylabel(axis_labels[v_ax], weight='bold')

    return axes


def path_3d(quad_path,
            ax3d,
            planned_path=None,
            waypoints=None,
            quad_lw=1.0,
            path_size=3.5,
            wp_size=6.0):

    """ Plots the path of a quad on a matplotlib axes.

    Only use if you want to modify the look of the plots, otherwise use plot_path_3d to generate plots.

    Args:
        quad_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z quad positions
        ax3d (mplot3d axes3d): The mplot3d axes3d object the path's are plotted onto.
        planned_path (numpy.ndarray): A 2D numpy.ndarray of x,y,z target positions
        waypoints (numpy.ndarray): A 2D numpy.ndarray of x,y,z positions
        quad_lw (float): The float linewidth for the quads path
        path_size (float): The float markersize for the planned path markers
        wp_size (float): The float markersize for the waypoint markers

    Returns:
        ax3d (mplot3d axes3d): The mplot3d axes3d with path's plotted onto it.

    """

    if planned_path is not None:
        ax3d.plot(planned_path[:,0], planned_path[:,1], planned_path[:,2], 'go',
                  color='r', markersize=path_size, markeredgecolor='r')

    if waypoints is not None:
        ax3d.plot(waypoints[:,0], waypoints[:,1], waypoints[:,2], 'gH',
                  color='b', markersize=wp_size, markeredgecolor='b')


    ax3d.plot(quad_path[:,0], quad_path[:,1], quad_path[:,2],
              color='k', linewidth=quad_lw)

    ax3d.tick_params(labelsize=8)
    ax3d.set_xlabel('X', weight='bold')
    ax3d.set_ylabel('Y', weight='bold')
    ax3d.set_zlabel('Z', weight='bold')
    return ax3d
