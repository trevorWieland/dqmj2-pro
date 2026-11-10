#include "context.h"

extern void native_fn_02008e0c(const void *src, void *dest, u32 size);
extern void (*native_data_020dcd34)(Sha1Context *context, const void *block, u32 size);

/* Append `size` bytes to the hash stream.  The 64-bit bit counter advances by
   eight bits per byte; a partial staging block is completed and flushed first,
   aligned whole blocks go straight to the callback, unaligned ones are staged
   64 bytes at a time. */
void native_main_0200d094(Sha1Context *context, const u8 *src, u32 size)
{
    u8 *block = context->block;
    s32 bulk;
    u32 low;
    u32 sum;
    u32 space;

    if (size == 0)
        return;
    low = context->bits_lo;
    sum = low + (size << 3);
    if (sum < low)
        context->bits_hi += 1;
    context->bits_hi += size >> 29;
    context->bits_lo = sum;
    if (context->pending != 0) {
        if (context->pending + size >= 0x40) {
            space = 0x40 - context->pending;
            native_fn_02008e0c(src, &block[context->pending], space);
            size -= space;
            src += space;
            native_data_020dcd34(context, block, 0x40);
            context->pending = 0;
        } else {
            native_fn_02008e0c(src, &block[context->pending], size);
            context->pending += size;
            return;
        }
    }
    if (size >= 0x40) {
        bulk = size & ~0x3f;
        size -= bulk;
        if (((u32)src & 3) == 0) {
            native_data_020dcd34(context, src, bulk);
            src += bulk;
        } else {
            do {
                native_fn_02008e0c(src, block, 0x40);
                src += 0x40;
                native_data_020dcd34(context, block, 0x40);
                bulk -= 0x40;
            } while (bulk > 0);
        }
    }
    context->pending = size;
    if (size != 0)
        native_fn_02008e0c(src, block, size);
}
