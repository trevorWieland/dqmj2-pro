/* ov000 row 0x021f27fc: 196 bytes.
 *
 * What it does: 44 instructions; 7 call(s) to 0x0204b1a0, 0x020c1c20, 0x020c1de0, +4 more; loops (back edge at +0x24); returns through pop {r3, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb0 -> constant 0x02236da4 (image word 0x02236da4)
 *   pool +0xb4 -> constant 0x02236da8 (image word 0x02236da8)
 *   pool +0xb8 -> constant 0x02236db4 (image word 0x02236db4)
 *   pool +0xbc -> constant 0x02236db8 (image word 0x02236db8)
 *   pool +0xc0 -> constant 0x02101ae8 (image word 0x02101ae8)
 *   test +0x10 cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f27fc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0204b1a0(void);
extern void native_fn_020c1c20(void);
extern void native_fn_020c1de0(void);
extern void native_fn_020c1c30(void);
extern void native_fn_02048a60(void);
extern void native_fn_020c1cf4(void);
extern void native_fn_02048308(void);


asm u32 native_ov000_021f27fc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #8
    ldr r0, [r0, #0x4]
    ldr r1, =0x02236da4
    cmp r0, #0
    str r0, [r1, #0x8]
    addeq sp, sp, #8
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    bl native_fn_0204b1a0
    ldr r0, =0x02236da4
    ldr r0, [r0, #0x8]
    bl native_fn_020c1c20
    mov r2, #0
    ldr r1, =0x02236da8
    str r2, [sp]
    mov r12, #32
    mov r0, #2
    mov r3, #36
    str r12, [sp, #0x4]
    bl native_fn_020c1de0
    mov r0, #2
    ldr r1, =0x02236db4
    mov r2, #30
    mov r3, #1
    str r0, [sp]
    bl native_fn_020c1c30
    ldr r0, =0x02236da4
    mov r1, #160
    ldr r0, [r0, #0x10]
    mov r2, #24
    bl native_fn_02048a60
    mov r2, #0
    ldr r1, =0x02236db8
    mov r0, #2
    sub r3, r2, #4
    bl native_fn_020c1cf4
    ldr r0, =0x02101ae8
    mov r1, #1
    str r1, [r0, #0xc84]
    bl native_fn_02048308
    mov r0, #1
    add sp, sp, #8
    ldmia sp!, {r3, pc}
}
