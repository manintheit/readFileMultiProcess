import sys
import multiprocessing
import time
import linecache
#lck = multiprocessing.Lock()
#########################################################
def readWriteFile(fName, thName, start, end):
    global lck
    #lck.acquire()
    with open('dirs/' + str(thName) + '.txt', 'w') as wf:
        for pos in xrange(start, end +1):
            wf.write(linecache.getline(fName, pos))
    #lck.release()

########################################################
def lineCount(fName):
    counter = 0
    with open(fName) as rf:
        for line in rf:
            counter += 1
        return counter

############################################################

def rangeCalculator(thCount, fName):
    a_list = []
    b_list = []
    division = lineCount(fName) // thCount
    remainder = lineCount(fName) % thCount
    for rng in xrange(thCount):
        a_list.append(rng*division +1)
        if (remainder != 0 ) and (rng+1 == thCount):
            b_list.append(lineCount(fName))
        else:
            b_list.append((rng +1 ) * division)

    print a_list
    print b_list
    return zip(a_list, b_list)

#################################################
start = time.clock()
thCount = int(sys.argv[1])
fName = sys.argv[2]
threads = []
print "Thread Count Set to {}".format(thCount)
print "Processing a file {}".format(fName)


ranges = rangeCalculator(thCount, fName)
print ranges


for i in xrange(thCount):
    p = multiprocessing.Process(target=readWriteFile, args=(fName, i, ranges[i][0],ranges[i][1]))
    threads.append(p)


for i in (threads):
    print i
    i.start()

for i in (threads):
    i.join()
    pass



end = time.clock()
print 'Done...'
print "%.2gs" % (end-start)

