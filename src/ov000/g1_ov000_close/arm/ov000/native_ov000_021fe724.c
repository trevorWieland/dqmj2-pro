/* ov000 row 0x021fe724: 104 bytes.
 *
 * What it does: 25 instructions; 2 call(s) to 0x02215698, 0x0204b53c; loops (back edge at +0x58); returns through pop {r3, r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x022372bc (image word 0x022372bc)
 *   test +0x18 cmp r1, #0
 *   test +0x1c cmpne r1, #1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fe724; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_0204b53c(void);


asm u32 native_ov000_021fe724 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    mov r4, r0
    bl ov000_display_context_02215698
    ldr r1, =0x022372bc
    ldr r1, [r1]
    cmp r1, #0
    cmpne r1, #1
    addne sp, sp, #4
    ldmneia sp!, {r3, r4, pc}
    mov r2, #16
    mov r1, #40
    strh r1, [sp, #2]
    strh r2, [sp]
    ldrsh r12, [sp, #2]
    ldr r3, [r4]
    ldr r2, [r4, #0x4]
    add r1, sp, #0
    sub r2, r3, r2
    add r2, r12, r2, lsl #4
    add r0, r0, #16
    strh r2, [sp, #2]
    bl native_fn_0204b53c
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
