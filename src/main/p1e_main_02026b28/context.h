#ifndef P1E_CONTEXT_H
#define P1E_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Runtime block at 0x020ec9b8 used by the boot/init path. */
typedef struct {
    u8 pad00[0x08];
    u32 field08;   /* +0x08 frame/state counter */
    u8 pad0c[0x04];
    u32 field10;   /* +0x10 */
} MainRuntimeState;

extern MainRuntimeState native_data_020ec9b8;

#endif
