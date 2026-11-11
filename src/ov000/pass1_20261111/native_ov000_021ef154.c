/* Field-driven argument mapping and tail call.
 *
 * Loads the word field at 0x02236bd0 + 0x14 (the measured literal is the table
 * base, and the 0x14 is the folded load offset), maps a zero argument to 38 and
 * a non-zero one to 36, truncates that to a byte and tail-calls
 * native_fn_0204b5d4(base_field, byte). mwcc lowers the returned call into
 * `ldr r12, =callee` plus `bx r12`.
 * Unknowns: what the callee does with the pair.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_02236bd0;
extern u32 native_fn_0204b5d4(u32, u8);

u32 native_ov000_021ef154(u32 selector)
{
    return native_fn_0204b5d4(*(u32 *)(&native_data_ov000_02236bd0 + 0x14),
                              (u8)(selector ? 36 : 38));
}
