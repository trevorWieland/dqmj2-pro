/* Clear the requested bits of a global control word.
   Unknowns: the block role and the bit meanings. */
#include "context.h"
typedef unsigned short int u16;
extern u16 native_data_020f6ae4;
void native_main_020455c8(int timerNum);
void native_main_020455c8 (int timerNum)
{
    native_data_020f6ae4 &= ~(1 << timerNum);
}