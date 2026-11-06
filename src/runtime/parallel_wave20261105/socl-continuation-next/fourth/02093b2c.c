#include "context.h"
void native_main_02093b2c(u16 *output,u16 *input,u16 scalar,s32 digits)
{
    s32 index,input_digits;
    u32 carry,value;
    input_digits=native_fn_02093874(input,digits);
    carry=0;
    for(index=0;index<input_digits;index++){
        value=carry+(u32)input[index]*scalar;
        output[index]=(u16)value;
        carry=value>>16;
    }
    if(index<digits)output[index++]=(u16)carry;
    native_fn_02008d78(output+index,0,(digits-index)*2);
}
