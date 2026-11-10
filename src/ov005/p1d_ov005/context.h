#ifndef OV005_P1D_CONTEXT_H
#define OV005_P1D_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Per-object interface reached through the object's +0x20 word.  The interface
   exposes a callback table at +0x0c; individual wrappers call fixed slots. */
typedef struct {
    u8 pad[0x0c];
    void *table;   /* +0x0c */
} Ov005Interface;

#endif
