for file in raw_indicators/*
do
	cat $file | sed s/\ \*$//g | sed s/\ /_/g | sed s/-/_/g | tr '[:upper:]' '[:lower:]' | sort | uniq > ${file#raw_}
done
