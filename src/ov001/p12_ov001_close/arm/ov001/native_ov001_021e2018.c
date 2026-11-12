/* ov001 row 0x021e2018: 96 bytes.
 *
 * What it does: 22 instructions; 2 call(s) to 0x021e2068, 0x021e204c; loops (back edge at +0x4c); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (22 instructions, 2 calls, 0 branches, 1 back edge, 2 literal slots).
 *
 *   pool +0x58 -> constant 0x022388ec (image word 0x022388ec)
 *   pool +0x5c -> constant 0x0223893c (image word 0x0223893c)
 *   branch +0x24 -> +0x50
 *   back edge +0x4c -> +0x34
 *   test +0x0c cmp r12, #0
 *   test +0x20 cmp lr, #0
 *   test +0x38 cmp r3, r0
 *   test +0x48 cmp r2, lr
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e2018; the literal pool and
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



asm u32 native_ov001_021e2018 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldrb r12, [r0, #0x31e]
    mov r2, #0
    cmp r12, #0
    ldreq r1, =0x022388ec
    ldreqb lr, [r1, #0x18]
    ldrne r1, =0x022388ec
    ldrneb lr, [r1, #0x19]
    cmp lr, #0
    ble ov001_021e2018_L50
    ldr r1, =0x0223893c
    ldrb r3, [r0, #0x31f]
    add r1, r1, r12
ov001_021e2018_L34:
    ldrb r0, [r1, r2, lsl #1]
    cmp r3, r0
    moveq r0, #1
    ldmeqia sp!, {r3, pc}
    add r2, r2, #1
    cmp r2, lr
    blt ov001_021e2018_L34
ov001_021e2018_L50:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
