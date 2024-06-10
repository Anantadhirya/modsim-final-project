time_step = 1
person_size = 0.45

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

lift_size = 4.0

hall_width = 5
hall_height = 5
floor_width = lift_hall_width + hall_width

stairs_width = 2
stairs_length = 6

# class_hall_width = 3
# class_hall_height = 0.3

classes_position = [pos for floor in range(3, floor_count) for pos in [(floor, "u"), (floor, "d"), (floor, "d")]]