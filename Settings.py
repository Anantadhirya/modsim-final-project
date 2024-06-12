time_step = 1
person_size = 0.45

# Behaviour Settings
enter_lift_wrong_direction = True

# SGLC Settings
floor_count = 11
lift_count = 4

gap = 1
margin = 2.0

lift_hall_width = 10
lift_door_width = 2
lift_door_height = 0.4
lift_door_gap = 2
# lift_door_gap = (lift_hall_width - (lift_count // 2) * lift_door_width) / ((lift_count // 2) + 1)

first_floor_hall_height = 3

hall_width = 5
hall_height = 7
floor_width = lift_hall_width + hall_width

stairs_width = 2
stairs_length = 6

lift_size = 4
lift_gap_x = 0.4
lift_door_inside_gap = 1
# lift_door_inside_gap = (lift_size - lift_door_width) / 2

lift_max_person = 14
lift_door_transition_duration = 1 # door open and close duration
lift_stay_open_duration = 1 # how long a lift stays open from the last time a person entered or exit the lift

time_before_display_close = 60

time_verbose_print = 3 # in seconds

# class_hall_width = 3
# class_hall_height = 0.3

classes_position = [pos for floor in range(3, floor_count) for pos in [(floor, "d"), (floor, "d"), (floor, "d")]]