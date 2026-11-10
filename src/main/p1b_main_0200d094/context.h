#ifndef P1B_CONTEXT_H
#define P1B_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;

/* Streaming SHA-1 context measured at 0x0200e53d0-adjacent call sites: the five
   running state words, the 64-bit appended-bit counter, the staged byte count
   and the 64-byte block that is flushed through the hash callback. */
typedef struct {
    u32 state[5];     /* +0x00 A..E */
    u32 bits_lo;      /* +0x14 low word of the bit counter */
    u32 bits_hi;      /* +0x18 high word of the bit counter */
    s32 pending;      /* +0x1c bytes staged in block */
    u8 block[0x40];   /* +0x20 64-byte hash block */
} Sha1Context;

#endif
