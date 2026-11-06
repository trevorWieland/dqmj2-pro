#include "context000.h"

int native_main_0207b974(int index,int input,int pair,int percentage,int selection){
    const RangeRow *row=native_fn_0207afec(index);
    int lower,upper;
    short begin,end;
    if(pair==0){lower=native_fn_0207afec(index)->lower0;upper=native_fn_0207afec(index)->upper0;}
    else{lower=native_fn_0207afec(index)->lower1;upper=native_fn_0207afec(index)->upper1;}
    begin=row->threshold0;end=row->threshold1;
    if(begin==0 && end==0){lower+=native_fn_0207b94c(upper-lower+1,selection);percentage=1;}
    else if(input>begin){
        if(input>=end)lower=upper;
        else if(begin!=end)lower+=native_fn_02026144((upper-lower)*(input-begin),end-begin);
    }
    if(percentage!=1){int factor=native_fn_0207b94c(11,selection)+95;lower=lower*factor/100;}
    return lower;
}
