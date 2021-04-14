#!/bin/bash
#cat haproxy.cfg_ha-ald| sed '/^[[:space:]]*#/d' | awk ' BEGIN { ip = "(([a-zA-Z](-?[a-zA-Z0-9])*)\\.)+[a-zA-Z]{2,}" } ;$0 ~ ip {for(i=1;i<=NF;i++){ reg = match($i,ip) ; if (reg != 0 && $i !~ /#/) print substr($i, RSTART, RLENGTH)  } }' | sed '/[(.pem)(.lst)]$/d'| sort | uniq 
#cat haproxy.cfg_ha-ald* | awk ' $1 == "acl" {print $2}'
#cat haproxy.cfg_ha-ald* | awk -v domain="lachanviruscorona.lotus.vn" '{for (i=1;i<=NF;i++) if ($i ~ "^"domain) {print;next}}'

function get_frontend()
	{
#	 cat $1 | sed '/^[[:space:]]*#/d;/^[[:space:]]*$/d' | awk -v domain=$2 ' BEGIN { RS="frontend" }; {for (i=1;i<=NF;i++) if ($i ~ "^"domain) {print $3;next}} ' | sort | uniq
	 awk '/./ && !/^ *#/' $1| awk -v domain=$2 ' BEGIN { RS="frontend" }; {for (i=1;i<=NF;i++) if ($i ~ "^"domain) {print $3;next}} ' | awk '!x[$0]++'
	}
function get_acl()
	{
#	 cat $1 | sed '/^[[:space:]]*#/d;/^[[:space:]]*$/d' | awk -v wan=$3 ' BEGIN { RS="frontend" }; $3 ~ wan' | awk -v domain=$2 ' $1 == "acl" {for (i=1;i<=NF;i++) if ($i ~ "^"domain||$i ~ "m."domain||$i ~ "www."domain) {print $2;next}} '
	 awk '/./ && !/^ *#/' $1|awk -v wan=$3 ' BEGIN { RS="frontend" }; $3 ~ wan' | awk -v domain=$2 ' $1 == "acl" {for (i=1;i<=NF;i++) if ($i ~ "^"domain||$i ~ "m."domain||$i ~ "www."domain) {print $2;next}} '
	}
function print_cfg()
	{
	raw=""
	wan=$(get_frontend "$1" "$2")
	for ip in ${wan};do
	 batch=""
# 	 Bk=""
	 filename=$(grep -lR $ip *)
	 echo "(" $filename ")"
	 echo $ip 
	 acl="$(get_acl "$1" "$2" "$ip")"
	 if ! [[ -z "$acl" ]];then
	#echo $acl | awk ' { printf "-v pat"NR"="$0" \47
	  for pat in ${acl};do
#	   batch+="$(cat $1| sed '/^[[:space:]]*#/d;/^[[:space:]]*$/d' | awk -v wan=$ip ' BEGIN { RS="frontend" }; $3 ~ wan' | awk -v acl=$pat ' {for (i=1;i<=NF;i++) if ($i ~ "^"acl) {print;next}} ')\n"
	   batch+="$(awk '/./ && !/^ *#/' $1|awk -v wan=$ip ' BEGIN { RS="frontend" }; $3 ~ wan'  | awk -v acl=$pat ' {for (i=1;i<=NF;i++) if ($i ~ "^"acl) {print;next}} ')\n"
	  done
	 else 
#	  batch+="$(cat $1 | sed '/^[[:space:]]*#/d;/^[[:space:]]*$/d'| awk -v wan=$ip ' BEGIN { RS="frontend" }; $3 ~ wan' | awk -v domain=$2 ' {for (i=1;i<=NF;i++) if ($i ~ "^"domain||$i ~ "www."domain) {print;next}} ')\n"
	  batch+="$(awk '/./ && !/^ *#/' $1|awk -v wan=$ip ' BEGIN { RS="frontend" }; $3 ~ wan' | awk -v domain=$2 ' {for (i=1;i<=NF;i++) if ($i ~ "^"domain||$i ~ "www."domain) {print;next}} ')\n"
	 fi
	 echo -e "$batch"
	 echo ""
	 raw+="$batch"
	done 

	backend=$(echo -e "$raw" | awk '$1 ~ /use_backend/ {print $2} ' | awk '!x[$0]++')
	for be in ${backend};do
#	 Bk+="$(cat $1 | sed '/^[[:space:]]*#/d;/^[[:space:]]*$/d'| awk -v pat=$be ' BEGIN { RS="\nbackend" }; $1 ~ pat {print $0}')"
#	 cat $1 | sed '/^[[:space:]]*#/d;/^[[:space:]]*$/d'| awk -v pat=$be ' BEGIN { RS="\nbackend" }; ($1 ~ pat) {print $0}'| sed '/server/,${/server/!d}'
#	 awk -v pat=$be ' BEGIN { RS="\nbackend" }; ($1 ~ pat) {print "( "FILENAME" )";print "backend"$0}' $1 | tee >(awk '$1 ~ /server/ {print $3}' >> iplan.txt)
	 awk -v pat=$be ' BEGIN { RS="\nbackend";FS="\n" }; ($1 ~ pat) {print "( "FILENAME" )";printf "backend";{for (i=1;i<=NF;i++) if (i<=4||$i ~ "^[[:space:]]*server") {print $i}}}' $1| tee >(awk '$1 ~ /server/ {print $3}' >> iplan.txt)
#	 Bk+=$(awk -v pat=$be ' BEGIN { RS="\nbackend";print FILENAME;printf "backend" }; $1 ~ pat ' $1)
	done
#	 eho -e "$Bk"
 	 echo ""
	}
echo "" > iplan.txt
list=$(cat list.txt|sed '/^[[:space:]]*#/d;/^[[:space:]]*$/d')
for dm in ${list};do
 echo "$dm"
 print_cfg "$1" "$dm"
 echo ""
done
#awk '$1 ~ /server/ {print $3}' ipbackend.txt | awk '!x[$0]++' >> iplan.txt
