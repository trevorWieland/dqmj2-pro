#ifndef MASKED_CALLERS_H
#define MASKED_CALLERS_H
typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value,type,offset) (*(type)((u8 *)(value)+(offset)))
#endif
