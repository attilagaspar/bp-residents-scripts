
* script uses nearmrg from here:
* ssc install reclink

cd "C:\Users\Gáspár Attila\workspace\bp-residents-scripts\scripts"
insheet using "..\out\assoc_csv_using.txt", delimiter(",")
save "..\out\assoc_csv_using.dta"
clear
insheet using "..\out\assoc_csv_master.txt", delimiter(",")
reclink nkey1 nkey2  using "..\out\assoc_csv_using.dta", gen(myscore) idm(id) idu(personid)

save "..\out\assoc_matched.dta"
