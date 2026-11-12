/* ov001 row 0x02218524: 140 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x022185a8, 0x0207b004, 0x0221854c, +2 more; loops (back edge at +0x34); returns through pop {r4, r5, r6, pc}
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
 *   test +0x38 cmp r0, #0
 *   test +0x4c cmp r6, r0
 *   test +0x6c cmp r0, #0
 *   test +0x7c cmp r6, #6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02218524; the literal pool and
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

extern void native_fn_0207b004(void);


asm u32 native_ov001_02218524 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldrb r0, [r5, #0x322]
    mov r4, r1
    mov r6, #0
    cmp r0, #1
    beq ov001_02218524_L58
    ldrb r0, [r5, #0x323]
    cmp r0, #0
    ble ov001_02218524_L84
ov001_02218524_L28:
    add r0, r5, r6
    ldrb r0, [r0, #0x35e]
    mov r1, r4
    bl native_fn_0207b004
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x323]
    add r6, r6, #1
    cmp r6, r0
    blt ov001_02218524_L28
    b ov001_02218524_L84
ov001_02218524_L58:
    ldr r0, [r5, #0x1e8]
    mov r1, r4
    add r0, r0, r6
    ldrb r0, [r0, #0x8]
    bl native_fn_0207b004
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, pc}
    add r6, r6, #1
    cmp r6, #6
    blt ov001_02218524_L58
ov001_02218524_L84:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
