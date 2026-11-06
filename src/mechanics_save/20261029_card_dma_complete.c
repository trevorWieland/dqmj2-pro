#pragma always_inline on
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
    void (*callback)(void *);
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
extern Backend native_data_020e5500 __attribute__((aligned(32)));
extern void native_fn_0200877c(u32);
extern void native_fn_02005d50(u32);
extern void native_fn_02005d80(u32);
extern void native_fn_02010fa8(void);
extern void native_fn_02011504(void);
extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32);
extern void native_fn_02006924(Queue *);
extern void native_fn_0200698c(Thread *);
extern void native_fn_02010c08(void);
static inline int progress(void) {
    Backend *p = &native_data_020e5500;
    p->src += 512;
    p->dst += 512;
    p->len -= 512;
    return p->len > 0;
}
void saved_20261029_card_dma_complete(void) {
    native_fn_0200877c(native_data_020e5500.dma);
    if (!progress()) {
        Backend *p;
        void (*callback)(void *);
        void *argument;
        u32 interrupts;
        native_fn_02005d50(0x80000);
        native_fn_02005d80(0x80000);
        p = &native_data_020e5500;
        native_fn_02010fa8();
        native_fn_02011504();
        *(u32 *)p->descriptor = 0;
        callback = p->callback;
        argument = p->callback_arg;
        interrupts = native_fn_02007ff4();
        p->flags &= ~0x4c;
        native_fn_02006924(&p->busy_queue);
        if (p->flags & 0x10) native_fn_0200698c(p->thread);
        native_fn_02008008(interrupts);
        if (callback) callback(argument);
    } else {
        native_fn_02010c08();
    }
}
