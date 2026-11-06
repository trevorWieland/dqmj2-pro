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
    volatile u32 src;
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
    u8 prefix[8];
    u32 base;
    u8 fields0c[20];
    u8 data[512];
} Cache;
extern Backend native_data_020e5500 __attribute__((aligned(32)));
extern void native_fn_02008e0c(const void *,void *,u32);
int saved_20261029_card_cache_copy(Cache *cache) {
    Backend *const p = &native_data_020e5500;
    u32 base = p->src & ~511;
    if (base == cache->base) {
        u32 offset = p->src - base;
        u32 count = 512 - offset;
        if (count > p->len) count = p->len;
        native_fn_02008e0c(cache->data + offset,(void *)p->dst,count);
        p->src += count;
        p->dst += count;
        p->len -= count;
    }
    return p->len != 0;
}
