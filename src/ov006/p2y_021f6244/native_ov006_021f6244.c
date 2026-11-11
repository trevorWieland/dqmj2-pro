#include "context.h"

/* Display family, 80-byte body: hand the table and the callback to the helper,
   then force the low two bits of both display control pairs. The control pairs are
   raw address literals; writing them through an array symbol swaps the base and
   value registers and costs a one-halfword mismatch. */
void native_ov006_021f6244(void)
{
    native_fn_ov006_021f27d4(&native_data_0220dc04, native_fn_02004cd8);
    *(u16 *)0x04001008 = (*(u16 *)0x04001008 & ~3) | 3;
    *(u16 *)0x0400100A = (*(u16 *)0x0400100A & ~3) | 3;
    *(u16 *)0x04000008 = (*(u16 *)0x04000008 & ~3) | 3;
    *(u16 *)0x0400000A = (*(u16 *)0x0400000A & ~3) | 3;
    *(u16 *)0x0400000C = (*(u16 *)0x0400000C & ~3) | 3;
}
