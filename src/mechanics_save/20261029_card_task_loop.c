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
    void (*task)(void *);
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
extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32);
extern void native_fn_020068d4(void *);
void saved_20261029_card_task_loop(void) {
    Backend *const p = &native_data_020e5500;
    for (;;) {
        u32 interrupt_state = native_fn_02007ff4();
        if (!(p->flags & 8)) {
            do {
                native_fn_020068d4(0);
            } while (!(p->flags & 8));
        }
        native_fn_02008008(interrupt_state);
        p->task(p);
    }
}
