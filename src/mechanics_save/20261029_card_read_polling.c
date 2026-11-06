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
typedef struct {
    u32 first;
    u32 control;
    u32 base;
    u8 padding[20];
    u32 data[128];
} Cache;
extern Backend native_data_020e5500 __attribute__((aligned(32)));
extern void native_fn_02010ba8(u32,u32);
extern int native_fn_02010b1c(Cache *);
static inline u32 progress(volatile Backend *direct) {
    direct->src += 512;
    direct->dst += 512;
    return (direct->len -= 512);
}
void saved_20261029_card_read_polling(Cache *cache) {
    Backend *const p = &native_data_020e5500;
    for (;;) {
        u32 base = p->src & ~511;
        u32 destination;
        u32 control;
        u32 position;
        u32 bytes;
        if (base != p->src || p->dst & 3 || p->len < 512) {
            cache->base = base;
            destination = (u32)cache->data;
        } else {
            destination = p->dst;
        }
        native_fn_02010ba8(0xb7000000 | (base >> 8),base << 24);
        position = 0;
        bytes = 0;
        *(volatile u32 *)0x040001a4 = cache->control;
        for (;;) {
            control = *(volatile u32 *)0x040001a4;
            if (control & 0x800000) {
                u32 data = *(volatile u32 *)0x04100010;
                if (bytes < 512) {
                    ((u32 *)destination)[position] = data;
                    bytes += 4;
                    position += 1;
                }
            }
            if (!(control & 0x80000000)) break;
        }
        if (destination == p->dst) {
            if (!progress(&native_data_020e5500)) break;
        } else {
            if (!native_fn_02010b1c(cache)) break;
        }
    }
}
