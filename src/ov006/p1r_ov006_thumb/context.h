#ifndef P1R_CONTEXT_H
#define P1R_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Mechanism index: each row of the 0x21f5e28-0x21f7dd0 display family calls
   0x021f27d4 with its own table word, then rewrites the 3-bit field of three
   u16 registers at 0x04001008 (two) and 0x04000008 (three). */

#endif
