#! /bin/bash
  
rm results.log &> /dev/null
rm -rf temp_log &> /dev/null
mkdir temp_log

step=0
total=`wc -l fuck.list | awk '{print $1}'`

while read line; do
  if [[ -z $line ]]; then
    continue
  fi

  while [[ `ps | wc -l` -gt `nproc` ]]; do
    echo "Pending..."
    sleep 2.0
  done

  step=$((step + 1))

  echo "fuck [$step/$total]: ${line}"
  echo "======= fuck: ${line} =======" &> "temp_log/${line}.log"
  ping $line -c 4 &>> "temp_log/${line}.log" &
done < fuck.list

wait
echo "All Done"

for filename in temp_log/*.log; do
  if [[ -z $filename ]]; then
    continue
  fi
  cat $filename >> results.log
done

rm -rf temp_log &> /dev/null
