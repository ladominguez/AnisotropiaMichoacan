find . -type d -name  "2*"  | awk '{print "convert $(ls -v " $1 "/*.png) " $1 ".pdf"}'
