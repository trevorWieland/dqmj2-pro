/* ov001 row 0x022047ec: 172 bytes.
 *
 * What it does: 42 instructions; 5 call(s) to 0x02204854, 0x022048fc, 0x0220482c, +2 more; loops (back edge at +0x64); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (42 instructions, 5 calls, 3 branches, 2 back edges, 1 literal slot).
 *
 *   pool +0xa8 -> constant 0x0223d904 (image word 0x0223d904)
 *   branch +0x30 -> +0x68
 *   branch +0x38 -> +0x68
 *   branch +0x44 -> +0x5c
 *   back edge +0x64 -> +0x40
 *   branch +0x80 -> +0x98
 *   back edge +0xa0 -> +0x7c
 *   test +0x2c cmp r4, #7
 *   test +0x34 cmp r4, #14
 *   test +0x40 cmp r4, r7
 *   test +0x60 cmp r7, #14
 *   test +0x68 cmp r4, #15
 *   test +0x70 cmp r4, #18
 *   test +0x7c cmp r4, r7
 *   test +0x9c cmp r7, #18
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022047ec; the literal pool and
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

extern void native_fn_022048fc(void);


asm u32 native_ov001_022047ec (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r3, =0x0223d904
    mov r6, r0
    mov r0, #12
    mla r3, r6, r0, r3
    mov r5, r1
    mov r4, r2
    ldr r1, [r3, r5, lsl #2]
    mov r0, #1
    orr r0, r1, r0, lsl r4
    str r0, [r3, r5, lsl #2]
    cmp r4, #7
    blt ov001_022047ec_L68
    cmp r4, #14
    bgt ov001_022047ec_L68
    mov r7, #7
ov001_022047ec_L40:
    cmp r4, r7
    beq ov001_022047ec_L5c
    mov r2, r7, lsl #24
    mov r0, r6
    mov r1, r5
    mov r2, r2, asr #24
    bl native_fn_022048fc
ov001_022047ec_L5c:
    add r7, r7, #1
    cmp r7, #14
    ble ov001_022047ec_L40
ov001_022047ec_L68:
    cmp r4, #15
    ldmltia sp!, {r3, r4, r5, r6, r7, pc}
    cmp r4, #18
    ldmgtia sp!, {r3, r4, r5, r6, r7, pc}
    mov r7, #15
ov001_022047ec_L7c:
    cmp r4, r7
    beq ov001_022047ec_L98
    mov r2, r7, lsl #24
    mov r0, r6
    mov r1, r5
    mov r2, r2, asr #24
    bl native_fn_022048fc
ov001_022047ec_L98:
    add r7, r7, #1
    cmp r7, #18
    ble ov001_022047ec_L7c
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
