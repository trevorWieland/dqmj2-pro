/* Spin until a status word leaves the value one (0x0200fb48, 24 bytes).
 *
 * Loads the status word at 0x020e5444 and re-reads it while it equals one; the
 * block base is held in ip, leaving r0 for the value.
 *
 * Unknowns: which producer clears the word and why one means busy.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; mwcc puts the block base in r1 (or spills a volatile pointer local), a
 * two-byte difference at the first load and the loop body.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;
extern u8 native_data_020e5444[];


asm void native_main_0200fb48 (void)
{
    ldr r12, =native_data_020e5444
native_main_0200fb48_loop:
    ldr r0, [r12]
    cmp r0, #1
    beq native_main_0200fb48_loop
    bx lr
}
