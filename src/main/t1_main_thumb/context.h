#ifndef T1_MAIN_THUMB_CONTEXT_H
#define T1_MAIN_THUMB_CONTEXT_H

/*
 * Shared context for the main-module Thumb batch 1 lane.
 *
 * The measured functions in this lane are NitroSDK-adjacent Thumb leaves and
 * small helpers in the 0x0208b000-0x020b7000 band of the ARM9 image. Each file
 * is one address-named function; the comments state the mechanism the image
 * proves and the parts that remain unresolved.
 */

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

#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) \
    (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)

#endif
