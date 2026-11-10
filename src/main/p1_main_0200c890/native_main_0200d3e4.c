#include "context.h"

/* Stream descriptor filled in by the callers and consumed by the bit-stream
   writer: two opaque words, two scratch buffers, and the open/write/close
   callbacks. */
typedef struct {
    u32 value00;                     /* +0x00 */
    u32 value04;                     /* +0x04 */
    void *buffer08;                  /* +0x08 */
    void *buffer0c;                  /* +0x0c */
    void (*open10)(void *self);      /* +0x10 */
    void (*write14)(void *self, const void *src, u32 size); /* +0x14 */
    void (*close18)(void *self, u32 *result);               /* +0x18 */
} StreamDescriptor;

/* Default descriptor values copied from the measured table object. */
typedef struct {
    u32 value00;
    u32 value04;
    u32 reserved08;
    u32 reserved0c;
    u32 reserved10;
    u32 reserved14;
    u32 reserved18;
} StreamDefaults;

extern StreamDefaults native_data_020d8c8c;
extern u32 native_fn_0200d478(u32 a, u32 b, u32 c, u32 d, u32 e, StreamDescriptor *desc);
extern void native_fn_0200d044(void);
extern void native_fn_0200d094(void);
extern void native_fn_0200d1e8(void);

/* Build the default stream descriptor, bind the bit-stream callbacks and open
   the stream with the caller's parameters. */
u32 native_main_0200d3e4(u32 a, u32 b, u32 c, u32 d, u32 e)
{
    u8 state[0x14];
    u8 output[0x68];
    StreamDescriptor desc;

    *(StreamDefaults *)&desc = native_data_020d8c8c;
    desc.buffer08 = output;
    desc.buffer0c = state;
    desc.open10 = (void (*)(void *))native_fn_0200d044;
    desc.write14 = (void (*)(void *, const void *, u32))native_fn_0200d094;
    desc.close18 = (void (*)(void *, u32 *))native_fn_0200d1e8;
    return native_fn_0200d478(a, b, c, d, e, &desc);
}

