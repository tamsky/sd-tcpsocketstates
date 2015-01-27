# sd-snmpstats - SNMP Statistics collection for Server Density
# ------------------------------------------------------------------
# (c) 2015 Marc Tamsky <mtamsky@bottlenose.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import csv
import re

class SNMPStats:
    def __init__(self, agentConfig, checksLogger):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger

        # shamelessly stolen from 
        # https://pypi.python.org/pypi/EDDIE-Tool
        # http://pydoc.net/Python/EDDIE-Tool/1.0.0/eddietool.arch.Linux.netstat/
	def run(self):
        """
        Collect network statistics.
        """

        self.data.datahash = {}                        # hash of statistics
                    
        # Get the network statistics from /proc/net/snmp on Linux 2.x/3.x
        fp = open('/proc/net/snmp', 'r')
                    
        line1 = fp.readline()                # read pairs
        line2 = fp.readline()                # of lines
        while len(line2) > 0:
            # Split into (protocol-name, rest-of-line...)
            (proto1, stats_names) = string.split(line1, ':')
            (proto2, stats_values) = string.split(line2, ':')

            # Both lines should have matching protocol value
            if proto1 != proto2:
                checksLogger( "<snmpstat>stats_ctrs.__init__(): error, protocol mis-match reading /proc/net/snmp for stats", 3 )
                raise "snmpstat Error", "Error, protocol mis-match reading /proc/net/snmp for stats."

            # Convert lines to lists:
            stats_names = string.split(stats_names)
            stats_values = string.split(stats_values)

            # Make sure lists lengths are equal
            if len(stats_names) != len(stats_values):
                checksLogger( "<netstat>stats_ctrs.__init__(): warning, list lengths differ, reading /proc/net/snmp for stats, stats_names=%s, stats_values=%s" % (stats_names,stats_values), 4 )
                raise "snmpstat Error", "Error, lists lengths unequal (names vs values)."

            # Build hash "<proto><stat_name>"
            for i in range(0, len(stats_names)):
                self.data.datahash[proto1+stats_names[i]] = int(stats_values[i])
                        
            # Read next pair of lines:
            line1 = fp.readline()
            line2 = fp.readline()
                        
        fp.close()
                                    
        checksLogger( "<snmpstat>stats_ctrs.collectData(): Collected %d network counters" %(len(self.data.datahash)), 6 )
                                    
        fp.close()
        return data
