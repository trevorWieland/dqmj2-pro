#include "context.h"

extern void native_fn_02008c14(u32 value, void *dest, u32 size);
extern void (*native_data_020dcd34)(Sha1Context *context, const void *block, u32 size);

#define STORE_BE32(dst, value)                 \
    do {                                       \
        (dst)[0] = (u8)((value) >> 24);        \
        (dst)[1] = (u8)((value) >> 16);        \
        (dst)[2] = (u8)((value) >> 8);         \
        (dst)[3] = (u8)(value);                \
    } while (0)

/* Pad the message, append the 64-bit bit count, flush the final block and emit
   the 20-byte big-endian digest.  The context pointer is scrubbed afterwards.
   `words` and `block` are the same 64-byte block: words view it for zeroing,
   block for byte-wise padding and length stores. */
void native_main_0200d1e8(Sha1Context *context, u8 *digest)
{
    u32 *words = (u32 *)context->block;
    u8 *block;
    u8 *out = digest;
    s32 index = context->pending >> 2;
    s32 position = context->pending;
    u32 lo;
    u32 hi;

    if ((position & 3) == 0)
        words[index] = 0;
    block = context->block;
    block[position] = 0x80;
    position++;
    if ((position & 3) != 0) {
        do {
            block[position] = 0;
            position++;
        } while ((position & 3) != 0);
    }
    index++;
    if (context->pending >= 0x38) {
        if (index < 0x10) {
            do {
                words[index] = 0;
                index++;
            } while (index < 0x10);
        }
        native_data_020dcd34(context, words, 0x40);
        index = 0;
    }
    if (index < 0xe) {
        do {
            words[index] = 0;
            index++;
        } while (index < 0xe);
    }
    lo = context->bits_lo;
    block[0x3f] = (u8)lo;
    block[0x3e] = (u8)(lo >> 8);
    block[0x3d] = (u8)(lo >> 16);
    block[0x3c] = (u8)(lo >> 24);
    hi = context->bits_hi;
    block[0x3b] = (u8)hi;
    block[0x3a] = (u8)(hi >> 8);
    block[0x39] = (u8)(hi >> 16);
    block[0x38] = (u8)(hi >> 24);
    native_data_020dcd34(context, words, 0x40);
    lo = context->state[0];
    STORE_BE32(out + 0x00, lo);
    lo = context->state[1];
    STORE_BE32(out + 0x04, lo);
    lo = context->state[2];
    STORE_BE32(out + 0x08, lo);
    lo = context->state[3];
    STORE_BE32(out + 0x0c, lo);
    lo = context->state[4];
    STORE_BE32(out + 0x10, lo);
    context->pending = 0;
    native_fn_02008c14(0, &context, 4);
}
