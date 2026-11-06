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
extern Backend native_data_020e5500 __attribute__((aligned(32)));
extern u8 native_data_020e54a0[];
extern u8 native_data_020e5b20[];
extern void native_fn_02008c58(u32,void *,u32);
extern void native_fn_02007308(void *,u32);
extern void native_fn_02008e0c(const void *,void *,u32);
extern void native_fn_020065f0(Thread *,void (*)(void),void *,void *,u32,u32);
extern void native_fn_0200698c(Thread *);
extern void native_fn_0200a3d0(u32,void (*)(u32,u32,u32));
extern void native_fn_02011244(void);
extern void native_fn_02011210(u32,u32,u32);
extern void native_fn_0201021c(u32);
static inline void fill_fast(void *destination, u32 value, u32 length) {
    native_fn_02008c58(value, destination, length);
}
static inline const volatile BootParameters *parameters(void) {
    return (const volatile BootParameters *)0x027ffc40;
}
static inline int child(void) {
    return parameters()->type == 2;
}
static inline void queue_init(Queue *q) {
    q->head = q->tail = 0;
}
void saved_20261029_card_common_initialize(void) {
    Backend *p = &native_data_020e5500;
    p->lock = -3;
    p->ref = 0;
    p->target = 0;
    p->descriptor = native_data_020e54a0;
    fill_fast(native_data_020e54a0,0,96);
    native_fn_02007308(native_data_020e54a0,96);
    p->flush_i = 0xffffffff;
    p->flush_d = 0xffffffff;
    if (!child()) native_fn_02008e0c((void *)0x027ffe00,(void *)0x027ffa80,352);
    queue_init(&p->lock_queue);
    queue_init(&p->busy_queue);
    p->priority = 4;
    native_fn_020065f0(p->thread,native_fn_02011244,0,native_data_020e5b20,1024,p->priority);
    native_fn_0200698c(p->thread);
    native_fn_0200a3d0(11,native_fn_02011210);
    if (!child()) native_fn_0201021c(1);
}
