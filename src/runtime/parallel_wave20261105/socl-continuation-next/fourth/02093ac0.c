#include "context.h"
void native_main_02093ac0(u16 *output,u16 *left,u16 *right,s32 digits)
{
    s32 index,outer,left_digits,right_digits;
    native_fn_02008d78(output,0,digits*2);
    left_digits=native_fn_02093874(left,digits);
    right_digits=native_fn_02093874(right,digits);
    for(outer=0;outer<right_digits;outer++)for(index=0;index<left_digits && index<digits-outer;index++)native_fn_02093aa0(output,(u32)left[index]*right[outer],outer+index,digits);
}
