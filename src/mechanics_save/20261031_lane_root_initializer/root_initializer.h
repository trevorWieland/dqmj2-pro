#ifndef ROOT_INITIALIZER_H
#define ROOT_INITIALIZER_H
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value,type,offset) (*(type)((u8 *)(value)+(offset)))
#endif
