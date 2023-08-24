# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import LoadComposableNodes
from launch_ros.actions import Node
from launch_ros.descriptions import ComposableNode
from nav2_common.launch import RewrittenYaml
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetLaunchConfiguration


def generate_launch_description():
    # Get the launch directory
    this_pgk_dir = get_package_share_directory('tuw_nav2')

    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    log_level = LaunchConfiguration('log_level')

    bt_navigator_yaml          = os.path.join(this_pgk_dir, 'config', 'nav2', 'pioneer3dx', 'v1', 'bt_navigator.yaml')
     

    lifecycle_nodes = ['controller_server',
                       'smoother_server',
                       'planner_server',
                       'behavior_server',
                       'bt_navigator',
                       'waypoint_follower',
                       'velocity_smoother']

    remappings = [('/tf', 'tf'),
                  ('/tf_static', 'tf_static')]

    # Create our own temporary YAML files that include substitutions
    param_substitutions = {
        'use_sim_time': use_sim_time,
        'autostart': autostart}

    bt_navigator_yaml_rewritten = RewrittenYaml(
            source_file=bt_navigator_yaml,
            root_key=namespace,
            param_rewrites=param_substitutions,
            convert_types=True)


    declare_controller_server_yaml = DeclareLaunchArgument(
        'controller_server_yaml',
        default_value='controller_server_purepursuite.yaml',
        description='controller server file name')


    declare_smoother_server_yaml = DeclareLaunchArgument(
        'smoother_server_yaml',
        default_value='smoother_server.yaml',
        description='smoother server file name')

    declare_behavior_server_yaml = DeclareLaunchArgument(
        'behavior_server_yaml',
        default_value='behavior_server.yaml',
        description='behavior server file name')
    
    declare_waypoint_follower_yaml = DeclareLaunchArgument(
        'waypoint_follower_yaml',
        default_value='waypoint_follower.yaml',
        description='waypoint follower file name')

    declare_planner_server_yaml = DeclareLaunchArgument(
        'planner_server_yaml',
        default_value='planner_server.yaml',
        description='planner server file name')
    
    declare_velocity_smoother_yaml = DeclareLaunchArgument(
        'velocity_smoother_yaml',
        default_value='velocity_smoother.yaml',
        description='velocity smoother file name')
    
    declare_use_robot = DeclareLaunchArgument(
        'use_robot',
        default_value='pioneer3dx',
        description='Robot used and configuration folder used: ./nav2/$use_robot/$use_version/..')

    declare_use_version = DeclareLaunchArgument(
        'use_version',
        default_value='v1',
        description='Robot used and configuration folder used: ./nav2/$use_robot/$use_version/..')

    stdout_linebuf_envvar = SetEnvironmentVariable(
        'RCUTILS_LOGGING_BUFFERED_STREAM', '1')

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', default_value='true',
        description='Automatically startup the nav2 stack')

    declare_log_level_cmd = DeclareLaunchArgument(
        'log_level', default_value='info',
        description='log level')

    def create_full_path_configurations(context):
        controller_server_param_file_path = os.path.join(
            this_pgk_dir,
            'config', 'nav2',
            context.launch_configurations['use_robot'],
            context.launch_configurations['use_version'],
            context.launch_configurations['controller_server_yaml'])
        print(controller_server_param_file_path)
        behavior_server_param_file_path = os.path.join(
            this_pgk_dir,
            'config', 'nav2',
            context.launch_configurations['use_robot'],
            context.launch_configurations['use_version'],
            context.launch_configurations['behavior_server_yaml'])
        print(behavior_server_param_file_path)
        smoother_server_param_file_path = os.path.join(
            this_pgk_dir,
            'config', 'nav2',
            context.launch_configurations['use_robot'],
            context.launch_configurations['use_version'],
            context.launch_configurations['smoother_server_yaml'])
        print(smoother_server_param_file_path)
        waypoint_follower_param_file_path = os.path.join(
            this_pgk_dir,
            'config', 'nav2',
            context.launch_configurations['use_robot'],
            context.launch_configurations['use_version'],
            context.launch_configurations['waypoint_follower_yaml'])
        print(waypoint_follower_param_file_path)
        planner_server_param_file_path = os.path.join(
            this_pgk_dir,
            'config', 'nav2',
            context.launch_configurations['use_robot'],
            context.launch_configurations['use_version'],
            context.launch_configurations['planner_server_yaml'])
        print(planner_server_param_file_path)
        velocity_smoother_param_file_path = os.path.join(
            this_pgk_dir,
            'config', 'nav2',
            context.launch_configurations['use_robot'],
            context.launch_configurations['use_version'],
            context.launch_configurations['velocity_smoother_yaml'])
        print(velocity_smoother_param_file_path)
        return [SetLaunchConfiguration('controller_server_param_file_path', controller_server_param_file_path),
                SetLaunchConfiguration('behavior_server_param_file_path', behavior_server_param_file_path),
                SetLaunchConfiguration('smoother_server_param_file_path', smoother_server_param_file_path),
                SetLaunchConfiguration('waypoint_follower_param_file_path', waypoint_follower_param_file_path),
                SetLaunchConfiguration('planner_server_param_file_path', planner_server_param_file_path),
                SetLaunchConfiguration('velocity_smoother_param_file_path', velocity_smoother_param_file_path)]

    create_full_path_configurations_arg = OpaqueFunction(function=create_full_path_configurations)


    load_nodes = GroupAction(
        actions=[
            Node(
                package='nav2_controller',
                executable='controller_server',
                output='screen',
                respawn_delay=2.0,
                parameters=[LaunchConfiguration('controller_server_param_file_path')],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings + [('cmd_vel', 'cmd_vel_nav')]),
            Node(
                package='nav2_smoother',
                executable='smoother_server',
                name='smoother_server',
                output='screen',
                respawn_delay=2.0,
                parameters=[LaunchConfiguration('smoother_server_param_file_path')],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
            Node(
                package='nav2_planner',
                executable='planner_server',
                name='planner_server',
                output='screen',
                respawn_delay=2.0,
                parameters=[LaunchConfiguration('planner_server_param_file_path')],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
            Node(
                package='nav2_behaviors',
                executable='behavior_server',
                name='behavior_server',
                output='screen',
                respawn_delay=2.0,
                parameters=[LaunchConfiguration('behavior_server_param_file_path')],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
            Node(
                package='nav2_bt_navigator',
                executable='bt_navigator',
                name='bt_navigator',
                output='screen',
                respawn_delay=2.0,
                parameters=[bt_navigator_yaml_rewritten],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
            Node(
                package='nav2_waypoint_follower',
                executable='waypoint_follower',
                name='waypoint_follower',
                output='screen',
                respawn_delay=2.0,
                parameters=[LaunchConfiguration('waypoint_follower_param_file_path')],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
            Node(
                package='nav2_velocity_smoother',
                executable='velocity_smoother',
                name='velocity_smoother',
                output='screen',
                respawn_delay=2.0,
                parameters=[LaunchConfiguration('velocity_smoother_param_file_path')],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings +
                        [('cmd_vel', 'cmd_vel_nav'), ('cmd_vel_smoothed', 'cmd_vel')]),
            Node(
                package='nav2_lifecycle_manager',
                executable='lifecycle_manager',
                name='lifecycle_manager_navigation',
                output='screen',
                arguments=['--ros-args', '--log-level', log_level],
                parameters=[{'use_sim_time': use_sim_time},
                            {'autostart': autostart},
                            {'node_names': lifecycle_nodes}]),
        ]
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Set environment variables
    ld.add_action(stdout_linebuf_envvar)

    # Declare the launch options
    ld.add_action(declare_use_robot)
    ld.add_action(declare_use_version)
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_controller_server_yaml)
    ld.add_action(declare_behavior_server_yaml)
    ld.add_action(declare_smoother_server_yaml)
    ld.add_action(declare_waypoint_follower_yaml)
    ld.add_action(declare_planner_server_yaml)
    ld.add_action(declare_velocity_smoother_yaml)
    ld.add_action(declare_autostart_cmd)
    ld.add_action(declare_log_level_cmd)
    ld.add_action(declare_log_level_cmd)
    
    #Opaque function call
    ld.add_action(create_full_path_configurations_arg)

    # Add the actions to launch all of the navigation nodes
    ld.add_action(load_nodes)

    return ld
