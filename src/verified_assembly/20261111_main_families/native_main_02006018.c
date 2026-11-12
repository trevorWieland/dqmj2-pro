/* Tail call through a literal function pointer (0x02006018, 12 bytes).
 *
 * Loads the address 0x02005ff8 from the literal pool and branches to it without
 * touching the argument registers.
 *
 * Unknowns: the callee's role and why this indirection exists beside a direct branch.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; a C tail call through a function pointer puts the pointer in ip, not r1.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;
extern void native_fn_02005ff8(void);


asm void native_main_02006018 (void)
{
    ldr r1, =native_fn_02005ff8
    bx r1
}
