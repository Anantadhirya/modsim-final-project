#
# General Settings
#
time_step = 1
person_size = 0.45

#
# Simulation Settings
#
time_before_display_close = 60 # in simulation time seconds
time_verbose_print = 3 # in real time seconds
display_fps = 60

#
# Model Behaviour Settings
#
enter_lift_wrong_direction = True

#
# Model Environment Settings
#
floor_count = 11
lift_count = 4

gap = 1
margin = 2.0

lift_hall_width = 10
lift_door_width = 2
lift_door_height = 0.4
lift_door_gap = 2

first_floor_hall_height = 3

hall_width = 5
hall_height = 7
floor_width = lift_hall_width + hall_width

stairs_width = 2
stairs_length = 6

lift_size = 4
lift_gap_x = 0.4
lift_door_inside_gap = 1

lift_max_person = 14
lift_door_transition_duration = 1 # door open and close duration
lift_stay_open_duration = 1 # how long a lift stays open from the last time a person entered or exit the lift

classes_position = [pos for floor in range(3, floor_count) for pos in [(floor, "d"), (floor, "d"), (floor, "d")]]