/* Indexed word read from the 0x020e2cc0 table.
   Unknowns: the table element meaning and its bounds. */
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
extern u8 native_data_020e2cc0[];
u32 native_main_020bf4ec(s32 arg0) {
    return *(u32 *)(native_data_020e2cc0 + (arg0 * 4));
}