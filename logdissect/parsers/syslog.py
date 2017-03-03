# MIT License
# 
# Copyright (c) 2017 Dan Persons <dpersonsdev@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import datetime
from logdissect.parsers.type import ParseModule as OurModule
from logdissect.data.data import LogEntry
from logdissect.data.data import LogData
# import logdissect.data.data

# Take this out later:
import sys

class ParseModule(OurModule):
    def __init__(self, options):
        self.name = 'syslog'
        self.desc = 'Syslog parsing module'
        self.data = LogData()
        self.newdata = LogData()
        self.date_format = \
                re.compile(r"^([A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2})")
        # self.date_format = \
        #         re.compile(r"^([A-Z][a-z]{2} \d{1,2} \d{2} \d{2}:\d{2}:\d{2})")


    def parse_log(self):
        # This shouldn't be needed, but:
        self.newdata = LogData()
	current_entry = LogEntry()
        self.data.source_file_mtime = \
                os.path.getmtime(self.data.source_full_path)
        timestamp = \
                datetime.datetime.fromtimestamp(self.data.source_file_mtime)
        timelist = str(self.data.source_file_mtime).split('-')
        self.data.source_file_year = timelist[0]
        entry_year = self.data.source_file_year
        recent_date_stamp = 9999999999
        
        # To Do: add some detection to fill in LogData class vars
        
        # self.data.source_file_mtime = \
        #         os.path.getmtime(self.data.source_full_path)
        self.data.source_file = self.data.source_full_path.split('/')[-1]
	with open(str(self.data.source_full_path), 'r') as logfile:
	# with reversed(open(self.data.source_full_path, 'r').readlines()) as loglines:
        # logfile = open(str(self.data.source_full_path), 'r')
            # self.data.lines = logfile.readlines()
            loglines = reversed(logfile.readlines())
            
        for line in loglines:
            ourline = line.rstrip()
            if len(current_entry.raw_text) >0:
                current_entry.raw_text = ourline + '\n' + \
                        current_entry.raw_text
            else: current_entry.raw_text = ourline
            match = re.findall(self.date_format, ourline)
            # match = re.match(self.date_format, ourline)
            if match:
                date_list = str(match[0]).split(' ')
                # date_list = str(match.split(' '))
                months = {'Jan':'01', 'Feb':'02', 'Mar':'03', \
                        'Apr':'04', 'May':'05', 'Jun':'06', \
                        'Jul':'07', 'Aug':'08', 'Sep':'09', \
                        'Oce':'10', 'Nov':'11', 'Dec':'12'}
                # if date_list[0] in months:
                int_month = months[date_list[0]]
                daydate = str(date_list[1]).strip().zfill(2)
                # time_list = str(date_list[2].split(':'))
                # time_list = str(str(date_list[2]).split(':'))
                timelist = str(str(date_list[2]).replace(':',''))
                date_stamp = str(int_month) + str(daydate) + str(timelist)
                # date_stamp = str(int_month) + str(daydate) + \
                #         str(time_list[0]) + str(time_list[1]) + \
                #         str(time_list[2])
                # Check for Dec-Jan
                if int(date_stamp) > recent_date_stamp:
                    entry_year = entry_year - 1
                recent_date_stamp = int(date_stamp)
                # Date_stamp should be called as an integer
                current_entry.date_stamp = int(date_stamp)
                # current_entry.date_stamp_year = int(str(entry_year) \
                #         + str(current_entry.date_stamp))
                current_entry.date_stamp_year = str(entry_year) \
                        + str(current_entry.date_stamp)
                self.newdata.entries.append(current_entry)
                current_entry = LogEntry()
            
            # for line in loglines:
            #     ourline = line.rstrip()
            #     current_entry.raw_text = ourline + '\n' + current_entry.raw_text
            #     match = re.match(self.date_format, ourline)
            #     if match:
            #         date_list = str(match.split(' '))
            #         months = {'Jan':'01', 'Feb':'02', 'Mar':'03', \
            #                 'Apr':'04', 'May':'05', 'Jun':'06', \
            #                 'Jul':'07', 'Aug':'08', 'Sep':'09', \
            #                 'Oce':'10', 'Nov':'11', 'Dec':'12'}
            #         if date_list[0] in months:
            #             int_month = months[date]
            #         daydate = str(date_list[1]).strip().zfill(2)
            #         time_list = str(date_list[2].split(':'))
            #         date_stamp = str(int_month) + str(daydate) + \
            #                 str(time_list[0]) + str(time_list[1]) + \
            #                 str(time_list[2])
            #         # Check for Dec-Jan
            #         if int(date_stamp) > recent_date_stamp:
            #             entry_year = entry_year - 1
            #         recent_date_stamp = int(date_stamp)
            #         # Date_stamp should be called as an integer
            #         current_entry.date_stamp = int(date_stamp)
            #         current_entry.date_stamp_year = int(str(entry_year) \
            #                 + str(current_entry.date_stamp))
            #         self.data.entries.append(current_entry)
        
        # Write the entries to the log object
        self.newdata.entries.reverse()
        # return self.data
        return 0
