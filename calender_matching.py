import csv

def check_cycle(c1, c2):
    if c2[0] >= c1[0] and c2[0] <= c1[1]:
        return True
    return False


def adjust_daily_bounds(calender, bound):
    calender_with_bounds = []
    if bound:
        start = ['00:00', bound[0]]
        end = [bound[1], '23:59']
        calender_with_bounds.append(start)
        calender_with_bounds.extend(calender)
        calender_with_bounds.append(end)
    return calender_with_bounds


def calender_to_minutes(calender):
    calender_with_minutes = []
    for s_element in calender:
        start_time = s_element[0].split(':')
        end_time = s_element[1].split(':')
        start_time = int(start_time[0]) * 60 + int(start_time[1])
        end_time = int(end_time[0]) * 60 + int(end_time[1])
        calender_with_minutes.append([start_time, end_time])
    return calender_with_minutes


def remove_cycles_from_calenders(overlapping_calender):
    calender_without_cycles = []
    prev = None
    while overlapping_calender:
        if prev is None:
            prev = overlapping_calender.pop(0)
            continue
        else:
            current = overlapping_calender.pop(0)
        if check_cycle(prev, current):
            # print ('cycle',prev, current)

            # prev = [prev[0], current[1]]
            # print (prev)
            prev = [min(prev[0], current[0]), max(prev[1], current[1])]
            # print ("cycle",prev)
        else:
            calender_without_cycles.append(prev)
            prev = current
    if check_cycle(prev, current):
        prev = [min(prev[0], current[0]), max(prev[1], current[1])]
        # prev = [prev[0], current[1]]

        calender_without_cycles.append(prev)
    else:
        calender_without_cycles.append(prev)
        calender_without_cycles.append(current)
    # print(calender_without_cycles)
    return calender_without_cycles


def calculate_time(s1, s2, meeting):
    available_time = s2[0] - s1[1]
    if available_time >= meeting:
        return True
    return False


def reformat(hour, min):
    if hour < 10:
        hour = '0' + str(hour)
    if min < 10:
        min = '0' + str(min)
    return str(hour) + ':' + str(min)


def extract_free_slots(calender, meeting):
    slots = []
    prev = None
    while calender:
        if prev is None:
            prev = calender.pop(0)
            continue
        else:
            current = calender.pop(0)
        if calculate_time(prev, current, meeting):
            start_hour = prev[1] // 60
            start_min = prev[1] % 60
            end_hour = current[0] // 60
            end_min = current[0] % 60
            start_available_slot = reformat(start_hour, start_min)
            end_available_slot = reformat(end_hour, end_min)
            slots.append([start_available_slot, end_available_slot])
        prev = current
    return slots


def read_csv(file_path):
    # Open the CSV file in read mode
    with open(file_path, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)

        # Convert the reader object to a list
        data = list(reader)

    return data


if __name__ == '__main__':
    path = 'input.csv'

    data = read_csv(path)
    calendar1 = eval(data[1][0])
    calendar2 = eval(data[1][1])
    dailyBounds1 = eval(data[1][2])
    dailyBounds2 = eval(data[1][3])
    meetingDuration = eval(data[1][4])
    calender_with_bounds1 = adjust_daily_bounds(calendar1, dailyBounds1)
    calender_with_bounds2 = adjust_daily_bounds(calendar2, dailyBounds2)
    calender_with_minutes1 = calender_to_minutes(calender_with_bounds1)
    calender_with_minutes2 = calender_to_minutes(calender_with_bounds2)
    overlapping_calender = calender_with_minutes1 + calender_with_minutes2
    overlapping_calender.sort()
    print(extract_free_slots(remove_cycles_from_calenders(overlapping_calender), meetingDuration))

