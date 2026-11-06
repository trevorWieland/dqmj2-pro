#include "context.h"
void native_main_02093930(u16 *output,u16 *input,u16 scalar,s32 digits)
{
    u32 value;
    s32 index;
    u32 carry=scalar;
    for(index=0;index<digits;index++){
        value=input[index]+carry;
        output[index]=(u16)value;
        carry=value>>16;
        if(!carry)break;
    }
    if(output!=input)for(index++;index<digits;index++)output[index]=input[index];
}
