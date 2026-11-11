/* Forward an argument to the handler in slot 0x10c.
 *
 * Loads the handler pointer at 0x022383e8 + 0x10c and, when non-null, calls it
 * with the handler as the first argument and the caller's argument second (the
 * image moves the argument to r1 first and returns through `popeq` when the slot
 * is empty).
 * Unknowns: which handler the slot holds.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_022383e8[];
extern void native_fn_0204b61c(u32, u32);

void native_ov000_02208938(u32 value)
{
    u32 handler = *(u32 *)(native_data_ov000_022383e8 + 0x10c);

    if (handler != 0)
        native_fn_0204b61c(handler, value);
}
