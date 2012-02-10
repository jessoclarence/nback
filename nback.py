import os
import time
import random
import signal
import sys
import datetime

#http://www.garyrobinson.net/2009/10/non-blocking-raw_input-for-python.html
# The next three functions were taken from the above url
class AlarmException(Exception):
	pass

def alarmHandler(signum, frame):
	raise AlarmException

def nonBlockingRawInput(prompt='', timeout=1):
	signal.signal(signal.SIGALRM, alarmHandler)
	signal.alarm(timeout)
	try:
		text = raw_input(prompt)
		signal.alarm(0)
		return True
	except AlarmException:
		signal.signal(signal.SIGALRM, signal.SIG_IGN)
		return False

n = 2
fp = None

for arg in sys.argv:
	if '-n=' in arg:
		n = int(arg[3:])
		continue

	if '-op=' in arg:
		fp = open(arg[4:],'a')
		continue
	
	if '-h' in arg or '--help' in arg:
		print "A series of numbers will keep flashing."+\
			"If the number that flashed is "+\
			"the same as the n'th number before it,"+\
			"press enter. Give -n=Integer as a command line "+\
			"argument to set n. If you'd like to store stats, "+\
			"give -op=file"
		exit()

print str(n) + " back"
print "Press enter when you find a match"
	
l = []
score = 0
max_score = 0
count_wrong = 0
count_correct = 0
count_missed = 0

for count in range(30):
	is_match = False

	i = int(random.random()*10)
	if i < 3:
		try:
			i = l[count -n]
		except IndexError: pass
	try:
		if i == l[count - n]:
			is_match = True
			max_score = max_score + 3
	except IndexError: pass

	print i

	l.append(i)

	print 

	time.sleep(1)

	m = os.system('clear')

	print 
	print

	inp = nonBlockingRawInput()

	try:
		if inp:
			if is_match:
				count_correct = count_correct + 1
				score = score + 3
				print ':)'
			else: 
				score = score - 2
				count_wrong = count_wrong + 1
				print ':('
		else:
			if is_match:
				score = score - 1
				count_missed = count_missed + 1
	except IndexError: pass
	
	time.sleep(0.5)
	m = os.system('clear')

fscore = float(score)
fmax = float(max_score)
fpercent = (fscore/fmax) * 100

print "Score : " +str(score)
print "Score Percentage : " +str(fpercent) + "%"

print "\nCorrect : " + str(count_correct)
print "Wrong : " + str(count_wrong)
print "Missed : " + str(count_missed)

if fp:
	fp.write(str(datetime.datetime.now())+'\t'+\
		str(n)+'\t'+\
		str(score)+'\t'+\
		str(fpercent)+'%\t'+\
		str(count_correct)+'\t'+\
		str(count_wrong)+'\t'+\
		str(count_missed)+'\n')
	fp.close()
