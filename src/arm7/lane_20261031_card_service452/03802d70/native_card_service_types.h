#ifndef NATIVE_CARD_SERVICE_TYPES_H
#define NATIVE_CARD_SERVICE_TYPES_H
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct CardArgument {
    u32 result, type, id, src, dst, length, unknown18, sectorSize, unknown20, pageSize, addressWidth;
    u32 programDelay, writeDelay, writeTotal, unknown38, unknown3c, eraseDelay, eraseTotal;
} CardArgument;
typedef struct CardCommon {
    CardArgument *argument;
    u32 unknown04,command;
    s32 owner, references;
    u32 lockQueue[2], target, src, dst, length, dma, request, retry, mode;
    void (*callback)(void *);
    void *callbackArgument;
    void (*task)(void *);
    u8 thread[164];
    void *currentThread;
    u32 priority, busyQueue[2];
} CardCommon;
typedef struct CardTransfer {
    u32 count;
    const u8 *source;
    u8 *destination;
} CardTransfer;
typedef struct CardCommand { u32 unknown, count; } CardCommand;
extern CardCommon native_host_arm7_data_038090c0;
extern CardTransfer native_host_arm7_data_038096c4;
extern CardCommand native_host_arm7_data_038096c0;
extern u32 native_host_arm7_data_038090a0;
extern u8 native_host_arm7_data_038096c0_stack[];
extern void native_host_arm7_fn_037fc054(void *,void (*)(void *),void *,void *,u32,u32);
extern void native_host_arm7_fn_037fc36c(void *);
extern void native_host_arm7_fn_037fe39c(u32,void (*)(u32,u32,s32));
extern void native_host_arm7_fn_038032b8(void *);
extern void native_host_arm7_fn_038031d4(u32,u32,s32);
extern void native_host_arm7_fn_037fc468(s32);
extern u32 native_host_arm7_fn_038027d0(void);
extern s32 native_host_arm7_fn_03802824(void);
extern void native_host_arm7_fn_038029d8(void);
extern void native_host_arm7_fn_03802a0c(u32,u32);
extern void native_host_arm7_fn_03802924(CardTransfer *);
extern void native_host_arm7_fn_03802860(const void *,void *,u32,void (*)(CardTransfer *));
extern void native_host_arm7_fn_0380272c(u32,u32);
#define CARD_COMMON native_host_arm7_data_038090c0
#define CARD_TRANSFER native_host_arm7_data_038096c4
#define CARD_COMMAND native_host_arm7_data_038096c0
#define CARD_SPI_CONTROL (*(volatile u16 *)0x040001a0)
static inline s32 CardStatusReady(void) { return (native_host_arm7_fn_038027d0()&1)==0; }
static inline s32 CardIsChild(void) { return (*(volatile u16 *)0x027ffc40)==2; }
#endif
