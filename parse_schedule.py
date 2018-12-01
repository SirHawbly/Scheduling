#!/usr/bin/python3


# -----
import sys
import os
import csv
import json
from copy import deepcopy


# -----
# # set up globals for specific days,
# # as well as a list of all the days 
daynames = [MON,TUE,WED,THU,FRI,SAT,SUN]=['mon','tue','wed','thu','fri','sat','sun']
days = {MON:'Monday',TUE:'Tuesday',WED:'Wednesday',THU:'Thursday',
        FRI:'Friday',SAT:'Saturday',SUN:'Sunday'}

# for day in days: print(days[day])

# -----
# # set up entries that will be used for
# # sunday should be empty as desk isnt 
# # open on sundays. the headers on the 
# # objects will be the full names, not
# # the shorts.
temp_entry = {"name":"", "line":0}
for day in days: temp_entry[days[day]] = []
# print(temp_entry)


# -----
def parse_hour_range(entry, item):
	"""
		Given an entry and an hour_range:
		
			entry in form:
				{'name':'', day:[], day:[], day:[], ...}
			hour_range in form:
				['day', 'time-time', 'time-time', 'time-time', ...]

		Parse the hour ranges provided and store them into the
		entry in the right day list. The hour ranges should be
		inbetween 08 - 18 (8am to 6pm) and the days should not
		be sunday (though this isnt asserted).

		The hours that are put into the entry are equivalent 
		to, time1 <= hour < time2 these are then multiplied 
		by 100. the time1 is asserted to be less than time2
			
			ie. 8-10 (8am to 10am) -> 8,9 -> 800, 900
			(10 is not included)
	"""
	title = "parse_hour_range - "

	# # we will split the substrings in form
	# # 	item = "day:00-00:00-00".
	# # so that the item can be in the form
	# # 	item = ['day', '00-00', '00-00'].
	# # into a list based on the colons.
	# print(item)
	item = item.split(':')
	# print(item)

	# # skipping the first item (the day)
	# # we can go through the hours of that
	# # day (assuming they exist)
	for hour_range in item[1:]:

		# # hour ranges are going to be in form:
		# # 	hour_ranges = "8-10"
		# # so we need to split them into a list.
		# # 	hour_ranges = ['8', '10']
		# print(hour_range)
		hours = hour_range.split('-')
		# print("hours - {}".format(hours))

		# # if we were passed an that thats bad,
		# #		item = "name,tue:,wed:9-12"
		# #	tue hours will be [''], which is a "nil" 
		# # so we skip it.
		if (hours == ['']): continue

		# # if we were given something like:
		# # 	item = ['mon', '8-10', '12-14', '15-']
		# # we will assert false, on the "15-" part.
		assert(len(hours) == 2)

		# # set the start and end times of the tuple
		[start, end] = [int(hours[0]), int(hours[1])] 

		# # if the numbers are in the wrong order, 
		# # throw an error.
		if (start >= end):
			print(title,"WARNING",entry['name'],"incorrect hour range (",start,"-",end,"),") 
			print("\tstart: {} is greater then end: {}".format(start,end))
			assert(False)

		# # if we are given times out side of 
		# # operating hours, print out a msg.
		if (start < 8 or end > 18):
			print(title,"WARNING",entry['name'],"incorrect hour range (",start,"-",end,"),")
			print("\teither start: {}<8 or end: {}>17".format(start,end))
			# # if you want to assert that the times 
			# # should be 8am - 5pm uncomment below.
			assert(False)

		# # change the times from 9 o'clock to
		# # 0900 o'clock. Uses the full name
                # # days not the short ones.
		for i in range(start, end):
			entry[days[item[0]]] += [i*100]

	return 


# -----
def write_output_as_human(output, log_file):
	"""
		given an object to output, in the form of:
			[['name':'cat1', mon:[], tue:[], ...], 
				[...],
			]

		then, we can write it out in human readable form, 
		line by line, into the log_file after making it
		sort of human readable.

		as well as in json format using json.dump(), this 
		does mean that the json output in the logfile is 
		all on one line.
	"""
	title = "write_output_human - "

	# print(output)

	# # create a string that contains all 
	# # of the information of the output
	# # just in a more friendly format.
	output_string = "[\n"
	for line in output: output_string += "\t{}\n".format(line)
	output_string += "]\n"
	# print(output_string)

	# # print out that we are going to write
	# # out output_string into the provided 
	# # log file, and do a json dump.
	print(title + "writing readable txt and json to {}".format(log_file))
	with open(log_file, 'w') as log_output:

		log_output.write("\n-- human readable --\n")

		for line in output_string:
			log_output.write(line)

		log_output.write("\n-- json by user --\n")

		json.dump(output, log_output)

		log_output.write("\n")

	# # return out, we are done.
	return 


# -----
def write_output_as_time(output, json_file):
	"""
		given an object to output, in the form of:
			[['name':'cat1', mon:[], tue:[], ...], 
				[...], ... ]

		parse the data so that the hours available per 
		day house all of the people slotted there.
		
		then output the data to json_file with a dump,
		json.dump(), the output in the json file will 
		be on one line, in the form:
			[[MON, 8:[], 9:[], ...],
				[day, ...] ]
	"""
	title = "write_output_as_time - "

	# # start a dictionary for output
	output_list = {}

	# # populate the dictionary as above, in
	# # form:
	# # {'Monday':{800:[], ...}, 'Tuesday':...,}
	for day in days:
		output_list[days[day]] = {}
		for i in range(8, 18):
			output_list[days[day]][i*100] = []

	# print(output_list)

	# # loop through the possible days, using
	# # all the user's days data to insert 
	# # their name into the dictionary under 
	# # the appropriate day(full name)/time
	for day in days: 
		for user in output:
			for time in user[days[day]]:
				output_list[days[day]][time] += [user['name'],]

	# print(output_list)
	
	# # print out that we are going to write 
	# # out to the provided file, and then
	# # run a json dump.
	print(title + "writing json output to {}".format(json_file))
	with open(json_file, 'w') as json_output:
		json.dump(output_list, json_output)

	# # return out, we are done.
	return 


# -----
def read_csv_file(schedule_file, output_file, output_json):
	"""
		Reads in a csv file, using this format:

			name,day:time-time,day:time-time,day:time-time ...
			*not all days need to be included* 

			ie. name00,mon:13-15,tue:8-10, ...

		It uses this format to populate an array of users
		and days/times they are available and returns it.

	"""
	title = "read_csv_file - "

	# # print that we are starting to read
	# # the schedule file.
	print(title + "reading from '{}'.".format(schedule_file))

	# # linting the csv
	with open(schedule_file) as input_file:

		line = 0
                # # format = (name,day:s-e,day:s-e:s-e,day:,)
		csv_parser = csv.reader(input_file)
		for entry in csv_parser:
			line += 1
			if (line == 1): continue

			# # print(line,entry)
			for section in entry:
				for item in entry:

					# # if we are in a date/time section, parse it,
					# # first, split the string on the colons...
					if ":" in item:

						item = item.split(":")						
						# print(item[0])

						# # if the first item in the set isnt a day name
						if (not item[0] in daynames):
							print(title,"on line ",line,", incorrect day name -", item)
							assert(False)

						# # run through all of the times in the set, checking that they 
						# # are correct
						for times in item[1:]:

							# # split all of the time ranges by the hyphens ie "8-10"
							# print(times)
							times = times.split("-")

							# # if there is nothing in the set of times, just skip it
							if (times == ['']): 
								continue

							# # if there arent two times, or the set is empty
							if (len(times) != 2):
								print(title,"on line",line,", incorrect time range -", item)
								assert(False)

							# # if either of the times are out of the range
							if (int(times[0]) < 8 or 18 < int(times[1])):	
								print(title, "on line",line,"in",times, "either (", times[0], "< 8 ), or (", times[1], "> 18 )" )
								assert(False)
							if (int(times[1]) < int(times[0])):	
								print(title, "on line", line, "in", times, "," ,times[0],">", times[1])
								assert(False)


	# # open the file, and create a csv
	# # parser for it, split it up, since it
	# # is a string, into a list.
	output_data = []
	with open(schedule_file) as input_file:

		csv_parser = csv.reader(input_file)
		current_line = 0

		for entry in csv_parser:

			entry = sum([i.split(',') for i in entry], [])
			# print(entry, end='\n')

			# # pull off the first line, which is just 
			# # the formatting guide.
			if (current_line == 0): 
				current_line += 1
				continue

			# # create a copy of the template entry
			# # set the current line of that copy.
			output_entry = deepcopy(temp_entry)
			output_entry['line'] = current_line

			# # loop through all of the items in the
			# # entry, which includes, the name, the
			# # days, and the hours per day available.
			for item in entry: 

				# # the first entry of the row is the 
				# # name of the person being sched'ed.
				if (entry.index(item) == 0):
					output_entry['name'] = item
					continue
			
				# # all other entries of the row are the
				# # available hour_ranges.
				else:	
					parse_hour_range(output_entry, item)

			# # add the entry to the output list,
			# # and increment the line counter.
			for entry in output_entry:
				if (output_entry[entry] != []):
					print(entry, '-', output_entry[entry], end='. ')
			print()
			output_data += [output_entry]
			current_line += 1

	# # print out the amount of entries
	# # that are processed, and write it
	# # out in the provided files.
	# print(title + "outputting {} user's entries".format(output_data))
	print(title + "outputting {} user's entries".format(len(output_data)))
	write_output_as_human(output_data, output_file)
	write_output_as_time(output_data, output_json)
	
	return
	

# -----
def main():
	"""
		runs the parsing program, depending on the args  
		provided. creates a file with a provided name (or 
		schedule by default) in the directory provided 
		(current directory is default, max 1 lvl deep).
	
		if one arg is provided, or if --help was provided 
		print out the way to correctly call the program

		if two arguments are provided, the last arg is 
		the input file. we run the default method with it 
		and 'schedule.txt' and 'schedule.json'

		if three arguments are provided then the second
		one is the input file, and the third is the path
		to store the output. They are put into either:

			if path provided
			'path/schedule.txt' and 
			'path/schedule.json'

			- or -

			if name provided
			'name.txt' and 
			'name.json'
	"""

	if (len(sys.argv) == 1 or sys.argv[1] == '--help'):
		
		name = sys.argv[0]
		print("\n-- Help Information -- \n".format(name) +
	
					"  -- Command Structure --\n"
					"  {} in_file\n".format(name) +
					"  - or -\n" +
					"  {} in_file out_path/\n".format(name) +
					"  - or -\n" +
					"  {} in_file out_file\n\n".format(name) +

					"  Note: \n" +
					"  -- default name for output will be\n" +
					"    'schedule.txt' and 'schedule.json.'\n" +
					"  -- default path is the current directory.\n\n" +

					"  -- Input Structure --\n" +
					"  provide an input file in the form of:\n" + 
					"    'name,day:s-f:s-f:s-f,day:s-f:s-f'\n" +
					"    'name01,mon:8-10:12-14,tue:8-10,...'\n" +
					"    '...'\n" +
					"  Note: \n" +
					"  -- not all days need to be provided.\n" +
					"  -- times need to be tuples (ss-ee).\n")
		return	

	# # we are provided a input file and no
	# # output files, so we set those to the 	
	# # defaults.
	elif (len(sys.argv) == 2):
		out_file = "schedule.txt"
		out_json = "schedule.json"

	elif (len(sys.argv) == 3):

		# # if we are provided a path, throw the 
		# # file into that path. ie char[-1:] = '/'.
		# print(sys.argv[2][-1:])
		if (sys.argv[2][-1:] == "/"):

			path = sys.argv[2]

			# # if we are given a directory, we try
			# # to create it, in case its not there.
			try: os.mkdir(path)
			except OSError:  
				print ("Creation of the directory {} failed".format(path))

			# # we were not given a name, so just 
			# # append the default name on it.
			out_file = sys.argv[2]+"schedule.txt"
			out_json = sys.argv[2]+"schedule.json"

		# # else if we are provided a file
		# # append the correct extentions and
		# # contine on.
		else :
			out_file = sys.argv[2]+".txt"
			out_json = sys.argv[2]+".json"

	# # call the read_csv function to parse
	# # the input file, mod it, and write it
	# # out to the given (or not given) files.
	read_csv_file(sys.argv[1], out_file, out_json)

	# # return out, we are done.
	return


# -----
# # call the main function it pulls
# # command line args so nothing needs
# # to be passed to it.
main()


# -----

