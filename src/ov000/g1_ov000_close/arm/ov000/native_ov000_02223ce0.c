/* ov000 row 0x02223ce0: 96 bytes.
 *
 * What it does: 23 instructions; 3 call(s) to 0x02223dd8, 0x02044cdc, 0x02223dd8; loops (back edge at +0x40); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5c -> constant 0x0224665c (image word 0x0224665c)
 *   branch +0x28 -> +0x40
 *   test +0x1c cmp r2, #0
 *   test +0x24 cmpne r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02223ce0; the literal pool and
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

extern void native_fn_02223dd8(void);
extern void native_fn_02044cdc(void);


asm u32 native_ov000_02223ce0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r3, =0x0224665c
    mov r5, r0
    mov r0, #12
    mla r0, r5, r0, r3
    mov r4, r1
    str r2, [r0, r4, lsl #2]
    cmp r2, #0
    ldrnesh r0, [r2, #24]
    cmpne r0, #0
    bne ov000_02223ce0_L40
    mov r0, r5
    mov r1, r4
    mov r2, #0
    bl native_fn_02223dd8
    ldmia sp!, {r3, r4, r5, pc}
ov000_02223ce0_L40:
    bl native_fn_02044cdc
    mov r2, r0, lsl #24
    mov r0, r5
    mov r1, r4
    mov r2, r2, asr #24
    bl native_fn_02223dd8
    ldmia sp!, {r3, r4, r5, pc}
}
