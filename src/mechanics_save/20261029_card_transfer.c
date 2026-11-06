typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    void *head;
    void *tail;
} Queue;
typedef struct {
    u8 opaque[0xc0];
} Thread;
typedef struct {
    void *descriptor;
    int command;
    volatile s32 lock;
    volatile int ref;
    Queue lock_queue;
    int target;
    u32 src;
    u32 dst;
    u32 len;
    u32 dma;
    int req;
    int retry;
    int mode;
    void (*callback)(void);
    void *callback_arg;
    void (*task)(void);
    Thread thread[1];
    void *current;
    u32 priority;
    Queue busy_queue;
    volatile u32 flags;
    u32 flush_i;
    u32 flush_d;
} Backend;
typedef struct { u16 type; } BootParameters;
typedef struct { u32 first; u32 control; } CardParameters;
extern Backend native_data_020e5500 __attribute__((aligned(32)));
extern CardParameters native_data_020e5b40;
extern void native_fn_02009034(u32,const void *,void *,u32);
extern void native_fn_02010ba8(u32,u32);
void saved_20261029_card_transfer_prepare(void) {
    Backend *const p = &native_data_020e5500;
    CardParameters *const parameters = &native_data_020e5b40;
    native_fn_02009034(p->dma,(void *)0x04100010,(void *)p->dst,512);
    native_fn_02010ba8((p->src >> 8) | 0xb7000000,p->src << 24);
    *(volatile u32 *)0x040001a4 = parameters->control;
}
