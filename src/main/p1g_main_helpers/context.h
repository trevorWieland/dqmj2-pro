#ifndef P1G_CONTEXT_H
#define P1G_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Three-word source / four-word destination pair used by the RTC and clock
   structure initialisers. */
typedef struct {
    u32 a;
    u32 b;
    u32 c;
} Trio;

typedef struct {
    u32 a;
    u32 b;
    u32 c;
    u32 d;
} Quad;

#endif
