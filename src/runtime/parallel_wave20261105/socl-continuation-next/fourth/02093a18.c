#include "context.h"
void native_main_02093a18(u16 *output,u16 *input,u16 scalar,s32 digits)
{
    u32 value;
    s32 index;
    u32 borrow=scalar;
    for(index=0;index<digits;index++){
        value=input[index]-borrow;
        output[index]=(u16)value;
        borrow=(value>>16)&1;
        if(!borrow)break;
    }
    if(output!=input)for(index++;index<digits;index++)output[index]=input[index];
}
