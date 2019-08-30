#!/usr/bin/env python
# Doc: https://github.com/guettli/wrap_and_log_calls
import os
import sys
import select
import datetime
import subprocess
import psutil
cmd=list(sys.argv)
cmd[0]='dpkg-orig'

def parents(pid=None):
    if pid==1:
        return '\n'
    if pid is None:
        pid = os.getpid()
    process = psutil.Process(pid)
    lines = [parents(process.ppid())]
    lines.append('Parent: %s' % ' '.join(process.cmdline()))
    return '\n'.join(lines)

out_streams = dict()
data = dict()

stdout_read, stdout_write = os.pipe()
out_streams[stdout_read] = sys.stdout
data[stdout_read] = []

stderr_read, stderr_write = os.pipe()
out_streams[stderr_read] = sys.stderr
data[stderr_read] = []

def read_stream(pipe):
    buf = os.read(pipe, 1)
    #print(buf)
    out_streams[pipe].write(buf)
    data[pipe].append(buf)
popen = subprocess.Popen(cmd, stdout=stdout_write, stderr=stderr_write)
while True:
    ret = popen.poll()
    ready_in, ready_out, xlist = select.select([stdout_read, stderr_read], [], [], 0)
    for pipe in ready_in:
        read_stream(pipe)
    if ret is not None and not ready_in:
        break

ret = popen.wait()
with open('/var/tmp/dpkg-calls.log', 'ab') as fd:
    fd.write('----------- %s\n' % (datetime.datetime.now()))
    fd.write('%s\n' % parents())
    fd.write('stdout:\n%s\n\n' % ''.join(data[stdout_read]))
    fd.write('stderr:\n%s\n' % ''.join(data[stderr_read]))
    fd.write('ret: %s\n' % ret)
sys.exit(ret)
