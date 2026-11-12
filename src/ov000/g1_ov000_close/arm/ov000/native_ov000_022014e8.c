/* ov000 row 0x022014e8: 116 bytes.
 *
 * What it does: 26 instructions; 3 call(s) to 0x02201548, 0x022153bc, 0x0220151c; loops (back edge at +0x5c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x68 -> constant 0x02237d54 (image word 0x02237d54)
 *   pool +0x6c -> constant 0x02237d70 (image word 0x02237d70)
 *   pool +0x70 -> constant 0x02237778 (image word 0x02237778)
 *   branch +0x24 -> +0x60
 *   branch +0x4c -> +0x60
 *   back edge +0x5c -> +0x34
 *   test +0x1c cmp r1, #0
 *   test +0x44 cmp r7, r0
 *   test +0x58 cmp r6, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022014e8; the literal pool and
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

extern void native_fn_022153bc(void);


asm u32 native_ov000_022014e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r1, =0x02237d54
    ldr r2, =0x02237d70
    ldrb r1, [r1, r0]
    ldr r5, [r2, r0, lsl #2]
    mov r8, #0
    mov r6, r8
    cmp r1, #0
    ldrsh r7, [r5, #38]
    ble ov000_022014e8_L60
    ldr r1, =0x02237778
    add r9, r1, r0
    add r4, r1, r0, lsl #7
ov000_022014e8_L34:
    add r0, r4, r6, lsl #2
    ldr r1, [r0, #0x2dc]
    mov r0, r5
    bl native_fn_022153bc
    cmp r7, r0
    movge r8, #1
    bge ov000_022014e8_L60
    ldrb r0, [r9, #0x5dc]
    add r6, r6, #1
    cmp r6, r0
    blt ov000_022014e8_L34
ov000_022014e8_L60:
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
