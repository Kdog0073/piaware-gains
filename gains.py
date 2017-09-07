#!/usr/bin/python2
import time, socket, subprocess, fileinput, os, random, sys, shutil

def gain_test(g):
    for line in fileinput.input('/boot/piaware-config.txt', inplace=1):
        if line.startswith('rtlsdr-gain'):
            print 'rtlsdr-gain '+g
        else:
            print line,
    fileinput.close()
    os.system("sudo systemctl restart dump1090-fa")
    time.sleep(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost',30003))
    t = time.time()
    d = ''
    while 1:
        d += s.recv(32)
        if time.time() - t > measure_duration:
            break
    s.close()
    messages = 0
    positions = 0
    planes = {}
    for l in d.split('\n'):
        a = l.split(',')
        messages += 1
        if len(a) > 4:
            if a[1] == '3':
                positions += 1
            planes[a[4]] = 1
    print "g=",g, "msg=", messages, "pos=", positions, "pln=", len(planes.keys())
    return (g, messages, positions, len(planes.keys()))
      

measure_duration = 62 #seconds
ntests = 5

gains = "20.7 22.9 25.4 28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0 49.6".split()
base_gain = "max"
results = {}
has_gain = False

shutil.copyfile('/boot/piaware-config.txt', '/boot/orig-piaware-config.txt') #backup original file

try:
    for line in fileinput.input('/boot/piaware-config.txt'):
        if line.startswith('rtlsdr-gain'):
            has_gain = True
            break
    fileinput.close()
    
    if has_gain == False:
        sys.exit("rtlsdr-gain is not initialized in /boot/piaware-config.txt")
    print "Setup success! Beginning gain tests"
    base_results = gain_test(base_gain) 

    for i in range(ntests):
        print "test", i+1, "of", ntests
        random.shuffle(gains)
        for g in gains:
            if g not in results:
                results[g] = [0.0,0.0,0.0] #msgs, positions, aircraft
    
            (g0, messages0, positions0, planes0) = base_results #results before at base level
            (g, messages, positions, planes) = gain_test(g)
            (g1, messages1, positions1, planes1) = gain_test(base_gain) #results after at base level

            #average before and after to determine rough base performance at the time of the test
            base_messages_avg = ((messages0 + messages1 + 0.0)/2)
            base_positions_avg = ((positions0 + positions1 + 0.0)/2)
            base_planes_avg = ((planes0 + planes1 + 0.0)/2)
    
            messagespct = messages / base_messages_avg * 100
            positionspct = positions / base_positions_avg * 100
            planespct = planes / base_planes_avg * 100
    
            print "*****  gain=", g, "messages%=", messagespct, "positions%=", positionspct, "planes%=", planespct, "  *****"
    
            results[g][0] += messagespct
            results[g][1] += positionspct
            results[g][2] += planespct

            base_results = (g1, messages1, positions1, planes1)

    print "\n===Totals==="
    print "Gain, Messages %, Positions %, Aircraft %"
    gains.sort()
    for g in gains:
        (messages,positions,planes) = results[g]
        print g, messages/ntests, positions/ntests, planes/ntests

finally:
    # restore original file
    shutil.copyfile('/boot/orig-piaware-config.txt', '/boot/piaware-config.txt')
    os.system("sudo systemctl restart dump1090-fa")