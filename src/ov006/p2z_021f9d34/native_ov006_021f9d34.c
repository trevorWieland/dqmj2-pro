#include "context.h"

/* Display family, 80-byte body: the same straight-line control-pair program as
   the harvested rows, with its own table. */
void native_ov006_021f9d34(void)
{
    native_fn_ov006_021f27d4(&native_data_0220de60, native_fn_02004cd8);
    *(u16 *)0x04001008 = (*(u16 *)0x04001008 & ~3) | 3;
    *(u16 *)0x0400100A = (*(u16 *)0x0400100A & ~3) | 3;
    *(u16 *)0x04000008 = (*(u16 *)0x04000008 & ~3) | 3;
    *(u16 *)0x0400000A = (*(u16 *)0x0400000A & ~3) | 3;
    *(u16 *)0x0400000C = (*(u16 *)0x0400000C & ~3) | 3;
}
