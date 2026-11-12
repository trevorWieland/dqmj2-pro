/* Tail-call thunk: forward the call and return the callee result.
   Unknowns: the callee role and why a distinct thunk exists beside 0x02063fa0. */
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
extern u32 native_fn_02062690();
u32 native_main_02063fac(void) {
    return native_fn_02062690();
}