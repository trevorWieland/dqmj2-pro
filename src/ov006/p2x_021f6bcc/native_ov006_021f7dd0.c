#include "context.h"

/* Program the display control pairs after handing the two tables to the helper. */
void native_ov006_021f7dd0(void)
{
    native_fn_ov006_021f27d4(&native_data_0220dd4c, &native_data_02004cd8);
    *(u16 *)0x04001008 = (*(u16 *)0x04001008 & ~3) | 3;
    *(u16 *)0x0400100A = (*(u16 *)0x0400100A & ~3) | 3;
    *(u16 *)0x0400000A = (*(u16 *)0x0400000A & ~3) | 3;
    *(u16 *)0x0400000C = (*(u16 *)0x0400000C & ~3) | 3;
}
