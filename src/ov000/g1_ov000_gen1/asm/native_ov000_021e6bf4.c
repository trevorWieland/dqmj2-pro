/* ov000 row 0x021e6bf4: 72 bytes.
 *
 * What it does: 18 instructions, 2 call(s), 3 load(s), 0 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021e6bf4; every literal pool
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

extern void native_fn_021e6bac(void);
extern void native_fn_021e78ac(void);


asm u32 native_ov000_021e6bf4 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #0xc
    mov r4, r0
    mov r0, r1
    add r1, sp, #0
    bl native_fn_021e78ac
    cmp r0, #0
    addeq sp, sp, #0xc
    moveq r0, #0
    ldmeqia sp!, {r3, r4, pc}
    ldr r1, [sp]
    ldr r2, [sp, #4]
    ldr r3, [sp, #8]
    mov r0, r4
    bl native_fn_021e6bac
    mov r0, #1
    add sp, sp, #0xc
    ldmia sp!, {r3, r4, pc}
}
