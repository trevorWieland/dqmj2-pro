/* ov000 row 0x02227e80: 60 bytes.
 *
 * What it does: 15 instructions, 2 call(s), 1 load(s), 1 store(s), 1 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02227e80; every literal pool
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

extern void native_fn_0206485c(void);
extern void native_fn_020cf7dc(void);


asm u32 native_ov000_02227e80 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, #0
ov000_02227e80_L00c:
    add r0, r5, r4, lsl #1
    ldrb r0, [r0, #0x7a]
    bl native_fn_020cf7dc
    add r1, r5, r4, lsl #1
    add r4, r4, #1
    strb r0, [r1, #0x7a]
    cmp r4, #5
    blt ov000_02227e80_L00c
    add r0, r5, #0x7a
    mov r1, #5
    bl native_fn_0206485c
    ldmia sp!, {r3, r4, r5, pc}
}
