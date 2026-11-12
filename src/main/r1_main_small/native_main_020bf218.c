/* Return the address of the 0x021d424c block.
   Unknowns: the block contents and why the address is exposed. */
#include "context.h"
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
extern u8 native_data_021d424c[];
u32 native_main_020bf218(void) {
    return (u32) native_data_021d424c;
}