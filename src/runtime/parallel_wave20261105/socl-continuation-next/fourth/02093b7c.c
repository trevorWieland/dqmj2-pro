#include "context.h"
void native_main_02093b7c(u16 *output,u16 *input,s32 digits)
{
    u32 value;
    s32 input_digits,inner,outer;
    input_digits=native_fn_02093874(input,digits);
    if(input_digits*2<digits)native_fn_02008d78(output+input_digits*2,0,(digits-input_digits*2)*2);
    for(outer=0;outer<input_digits;outer++){
        inner=outer*2;
        if(inner>=digits)break;
        value=(u32)input[outer]*input[outer];
        output[inner]=(u16)value;
        if(inner==digits-1)break;
        output[inner+1]=(u16)(value>>16);
    }
    for(outer=0;outer<input_digits;outer++)for(inner=outer+1;inner<input_digits && outer+inner<digits;inner++){
        value=(u32)input[inner]*input[outer];
        if(value<=0x7fff8000)native_fn_02093aa0(output,value*2,outer+inner,digits);
        else {
            native_fn_02093aa0(output,value,outer+inner,digits);
            native_fn_02093aa0(output,value,outer+inner,digits);
        }
    }
}
