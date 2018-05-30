catkin_install_python(PROGRAMS robosub_state_machine_node.py
                               dive_state.py
                               sensor_checker_state.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
