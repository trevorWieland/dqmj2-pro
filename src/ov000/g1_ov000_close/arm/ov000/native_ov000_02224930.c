/* ov000 row 0x02224930: 128 bytes.
 *
 * What it does: 31 instructions; 2 call(s) to 0x02223c54, 0x020629e0; loops (back edge at +0x10); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x7c -> constant 0x022468b8 (image word 0x022468b8)
 *   test +0x18 cmp r0, #0
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02224930; the literal pool and
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

extern void ov000_context_02246600_02223c54(void);
extern void native_fn_020629e0(void);


asm u32 native_ov000_02224930 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x022468b8
    mov r1, #0
    str r1, [r0, #0x14]
    bl ov000_context_02246600_02223c54
    ldrsb r0, [r0, #89]
    cmp r0, #0
    ldreq r0, =0x022468b8
    moveq r1, #0
    ldrne r0, =0x022468b8
    movne r1, #1
    strb r1, [r0, #0x18]
    ldr r0, =0x022468b8
    mov r1, #29
    strb r1, [r0, #0x1a]
    strb r1, [r0, #0x19]
    bl native_fn_020629e0
    ldr r1, =0x022468b8
    mov r3, #0
    strb r0, [r1, #0x1d]
    strb r3, [r1, #0x1e]
    strb r3, [r1, #0x1f]
    mov r0, #1
    strb r3, [r1, #0x20]
    mov r2, #127
    strb r2, [r1, #0x21]
    str r3, [r1, #0x24]
    strb r3, [r1, #0x1c]
    add r0, r0, #1
    strb r0, [r1, #0x1]
    ldmia sp!, {r3, pc}
}
