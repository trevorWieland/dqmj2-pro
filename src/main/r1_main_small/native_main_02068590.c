/* No-op entry point: an empty body that returns to the caller.
   Unknowns: why the address is called and whether callers rely on the no-op. */
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
u32 native_main_02068590(u32 arg0) {
    return arg0;
}