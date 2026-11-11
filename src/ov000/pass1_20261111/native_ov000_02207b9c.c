/* Forward an argument to the current handler.
 *
 * Loads the handler pointer at 0x022382c8 + 0x118 and, when it is non-null,
 * calls it with that pointer as the first argument and the caller's argument as
 * the second. The image moves the argument to r1 before loading the pointer and
 * returns through `popeq` when the handler is absent.
 * Unknowns: which handler the slot holds.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_022382c8[];
extern void native_fn_0204b61c(u32, u32);

void native_ov000_02207b9c(u32 value)
{
    u32 handler = *(u32 *)(native_data_ov000_022382c8 + 0x118);

    if (handler != 0)
        native_fn_0204b61c(handler, value);
}
