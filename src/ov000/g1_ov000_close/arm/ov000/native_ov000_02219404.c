/* ov000 row 0x02219404: 124 bytes.
 *
 * What it does: 29 instructions; 3 call(s) to 0x021df3bc, 0x021df3bc, 0x02219480; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x74 -> native_data_0222fa08 (image word 0x0222fa08)
 *   pool +0x78 -> constant 0x02245e54 (image word 0x02245e54)
 *   branch +0x38 -> +0x5c
 *   test +0x2c cmp r1, #0
 *   test +0x34 cmpeq r2, r1
 *   test +0x50 cmp r1, r0, lsr #27
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02219404; the literal pool and
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

extern u8 native_data_0222fa08[];
extern void native_fn_021df3bc(void);
extern void native_fn_02219480(void);


asm u32 native_ov000_02219404 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =native_data_0222fa08
    mov r4, r0
    ldrb r0, [r1, #0x1]
    bl native_fn_021df3bc
    mov r5, r0
    mov r0, r4
    bl native_fn_021df3bc
    ldr r1, =0x02245e54
    ldrb r2, [r0, #0x3]
    ldrb r1, [r1]
    cmp r1, #0
    ldreqb r1, [r5, #0x3]
    cmpeq r2, r1
    bne ov000_02219404_L5c
    ldrh r1, [r0]
    ldrh r0, [r5]
    mov r1, r1, lsl #16
    mov r1, r1, lsr #27
    mov r0, r0, lsl #16
    cmp r1, r0, lsr #27
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
ov000_02219404_L5c:
    ldr r1, =native_data_0222fa08
    mov r0, #0
    strb r4, [r1, #0x4]
    bl native_fn_02219480
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
}
