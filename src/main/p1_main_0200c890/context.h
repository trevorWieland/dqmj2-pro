#ifndef P1_CONTEXT_H
#define P1_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;

/* Main-module transfer control block, measured field offsets.  The block holds
   one queued callback plus the completion bookkeeping polled by the wait
   helpers below. */
typedef struct {
    u16 active;                  /* +0x00 non-zero while a transfer is open */
    u16 pad02;
    u32 value04;                 /* +0x04 snapshot of the tick source */
    u32 value08;                 /* +0x08 second tick snapshot */
    u32 state0c;                 /* +0x0c completion flag polled by callers */
    u32 value10;                 /* +0x10 channel slot */
    u32 value14;                 /* +0x14 second channel slot */
    u32 value18;                 /* +0x18 block handed to the sync helper */
    u32 pending;                 /* +0x1c outstanding transfer count */
    void (*callback)(u32, u32);  /* +0x20 queued completion callback */
    u32 callback_arg;            /* +0x24 argument handed to the callback */
    u16 *halfword_out;           /* +0x28 destination for streamed values */
} TransferBlock;

/* The pending word is also addressed as its own object by the wait loops. */
typedef struct {
    u32 pending;
} PendingWord;

extern TransferBlock native_data_020e540c;
extern PendingWord native_data_020e5428;

/* Currently installed wait routine; the wrappers park here before retrying. */
extern void (*native_data_020dce4c)(void);

#endif
