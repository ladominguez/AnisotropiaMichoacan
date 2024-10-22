find ./2* -type d | awk '{print "sac << END\nread " $1 "/*.sac\nrmean\nrtrend\nch o 0\nw over\nquit\nEND\n"}'
