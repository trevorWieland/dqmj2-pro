#include "context.h"
u32 native_main_020602ec(TextOwner *owner, u32 item, u32 style, s16 x, s16 y, s32 mode)
{
    u16 buffer[32];
    ItemMetadata *metadata = native_fn_020449d4(item);
    TextContext *context = owner->context04;
    native_fn_02008be0(0, buffer, sizeof(buffer));
    buffer[0] = native_data_020dbc18[(u16)(metadata->flags4.nibble4 + 13) + 0x17b];
    native_fn_02087a48(context, 0, x, y, 1, buffer);
    native_fn_020852b0(context->state3c, style);
    native_fn_02046af4(native_data_021c9698, context->field68, context->format5e, 0, buffer, 255);
    return (u16)(native_fn_02087a48(context, 0, (s16)(x + 8), y, mode, buffer) + 8);
}
