/* Forward an argument to the handler in slot 0x110.
 *
 * Sibling of 0x02208938 over the same block at 0x022383e8 with the next handler
 * slot; the callee is native_fn_0205fa4c.
 * Unknowns: which handler the slot holds.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_022383e8[];
extern void native_fn_0205fa4c(u32, u32);

void native_ov000_0220895c(u32 value)
{
    u32 handler = *(u32 *)(native_data_ov000_022383e8 + 0x110);

    if (handler != 0)
        native_fn_0205fa4c(handler, value);
}
