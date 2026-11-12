/* ov000 row 0x02227648: 80 bytes.
 *
 * What it does: 20 instructions, 3 call(s), 0 load(s), 5 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02227648; every literal pool
 * word and branch target is read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02216260(void);
extern void native_fn_0222390c(void);
extern void native_fn_022276ac(void);


asm u32 native_ov000_02227648 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #0x14
    mov r0, #0x13
    str r0, [sp]
    mov r1, #0x20
    mov r0, #0x1d
    str r1, [sp, #4]
    mov r1, #4
    str r1, [sp, #8]
    mov r3, #0
    mov r1, r0
    str r3, [sp, #0xc]
    mov ip, #1
    mov r2, #2
    str ip, [sp, #0x10]
    bl native_fn_02216260
    bl native_fn_0222390c
    bl native_fn_022276ac
    add sp, sp, #0x14
    ldmia sp!, {pc}
}
