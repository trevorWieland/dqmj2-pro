/* ov001 row 0x02218498: 140 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x0221851c, 0x022180e0, 0x022184c0, +2 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 5 calls (35 instructions, 5 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x58
 *   branch +0x24 -> +0x84
 *   back edge +0x50 -> +0x28
 *   branch +0x54 -> +0x84
 *   back edge +0x80 -> +0x58
 *   test +0x14 cmp r0, #1
 *   test +0x20 cmp r0, #0
 *   test +0x38 tst r4, r0
 *   test +0x4c cmp r6, r0
 *   test +0x6c tst r4, r0
 *   test +0x7c cmp r6, #6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02218498; the literal pool and
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

extern void native_fn_022180e0(void);


asm u32 native_ov001_02218498 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldrb r0, [r5, #0x322]
    mov r4, r1
    mov r6, #0
    cmp r0, #1
    beq ov001_02218498_L58
    ldrb r0, [r5, #0x323]
    cmp r0, #0
    ble ov001_02218498_L84
ov001_02218498_L28:
    add r0, r5, r6
    ldrb r0, [r0, #0x35e]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r4, r0
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x323]
    add r6, r6, #1
    cmp r6, r0
    blt ov001_02218498_L28
    b ov001_02218498_L84
ov001_02218498_L58:
    ldr r0, [r5, #0x1e8]
    add r0, r0, r6
    ldrb r0, [r0, #0x8]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r4, r0
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, pc}
    add r6, r6, #1
    cmp r6, #6
    blt ov001_02218498_L58
ov001_02218498_L84:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
