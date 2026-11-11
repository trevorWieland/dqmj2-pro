#ifndef P1F_CONTEXT_H
#define P1F_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Three-word vector used by the scene slot helpers. */
typedef struct {
    u32 x;
    u32 y;
    u32 z;
} Vec3;

#endif
