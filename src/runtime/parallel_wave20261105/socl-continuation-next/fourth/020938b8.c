#include "context.h"
void native_main_020938b8(u16 *output,u16 *left,u16 *right,s32 digits)
{
    u32 value;
    s32 index,carry,left_digits,right_digits;
    left_digits=native_fn_02093874(left,digits);
    right_digits=native_fn_02093874(right,digits);
    if(left_digits<right_digits)left_digits=right_digits;
    if(left_digits!=digits)left_digits++;
    carry=0;
    for(index=0;index<left_digits;index++){
        value=carry+((u32)left[index]+right[index]);
        output[index]=(u16)value;
        carry=(s32)(value>>16);
    }
    if(output!=left && output!=right)native_fn_02008d78(output+index,0,(digits-index)*2);
}
