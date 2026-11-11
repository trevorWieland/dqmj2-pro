#ifndef P1K_CONTEXT_H
#define P1K_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Mechanism indices for this ov006 batch:
   - dispatch tables: 0x0221a920 / 0x0221a92c hold one function pointer each;
     0x0221aad0 is a vtable-style table (entry +0x04 = allocate, +0x0c = flush,
     +0x7c = submit);
   - scene record: 0x0221c008 holds the active record; record +0x0c payload,
     +0x18/+0x19 mode bytes;
   - lookup descriptors: word 0 = base pointer, word 1 = addend;
   - 0x0221c094 = shared three-word buffer, 0x0221c0bc = frame counter. */

#endif
