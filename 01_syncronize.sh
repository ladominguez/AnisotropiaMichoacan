find ./2* -type d | awk '{print "sac << END\nread " $1 "/*.sac\nsync\nw over\nquit\nEND\n"}'
