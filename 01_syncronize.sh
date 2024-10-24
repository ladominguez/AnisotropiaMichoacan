find ./2* -type d | awk '{print "sac << END\nread " $1 "/*.sac\nsync\nch lcalda true\nw over\nquit\nEND\n"}'

taup_setsac -ph SKS-0 --evdpkm 20*/*sac
