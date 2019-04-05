# Replace | with ,
sed -E 's/[|]/,/g'

# Delete any line without # and "
grep '^[#"]' BAD.csv 

# Swich order of col 2 and 3


# Modifed date format
grep '^[#"]' BAD.csv  | sed -E 's/"([0-9]{2})-([0-9]{2})-([0-9]{4})","([a-zA-z])/\3-\2-\1/g' | grep -v Santa > four.csv

# Swich order of first and last name

# Remove Lines with Santa
grep -v Santa BAD.csv 
 