/* ov000 row 0x021f3d2c: 72 bytes.
 *
 * What it does: 18 instructions, 2 call(s), 3 load(s), 0 store(s), 1 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021f3d2c; every literal pool
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

extern void native_fn_021e77f8(void);
extern void native_fn_021f3d04(void);


asm u32 native_ov000_021f3d2c (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #0xc
    mov r5, r0
    mov r0, r1
    add r1, sp, #0
    mov r4, #0
    bl native_fn_021e77f8
    cmp r0, #0
    beq ov000_021f3d2c_L03c
    ldr r1, [sp]
    ldr r2, [sp, #4]
    ldr r3, [sp, #8]
    mov r0, r5
    bl native_fn_021f3d04
    mov r4, #1
ov000_021f3d2c_L03c:
    mov r0, r4
    add sp, sp, #0xc
    ldmia sp!, {r4, r5, pc}
}
