/* ov001 row 0x021e28d0: 180 bytes.
 *
 * What it does: 43 instructions; 3 call(s) to 0x021e295c, 0x021e2928, 0x021e2900; loops (back edge at +0x74); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (43 instructions, 3 calls, 2 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0xac -> constant 0x022388ec (image word 0x022388ec)
 *   pool +0xb0 -> constant 0x0223893c (image word 0x0223893c)
 *   branch +0x28 -> +0x8c
 *   branch +0x44 -> +0x80
 *   branch +0x54 -> +0x78
 *   back edge +0x74 -> +0x58
 *   back edge +0x88 -> +0x30
 *   test +0x10 cmp r2, #0
 *   test +0x24 cmp r2, #0
 *   test +0x40 cmp r12, r3
 *   test +0x50 cmp r6, r4
 *   test +0x6c cmp r7, r4
 *   test +0x84 cmp r6, r2
 *   test +0x90 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e28d0; the literal pool and
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



asm u32 native_ov001_021e28d0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldrb r2, [r0, #0x31e]
    mov r1, #0
    mov r6, #0
    cmp r2, #0
    ldreq r2, =0x022388ec
    ldreqb r2, [r2, #0x18]
    ldrne r2, =0x022388ec
    ldrneb r2, [r2, #0x19]
    cmp r2, #0
    ble ov001_021e28d0_L8c
    ldr r5, =0x0223893c
ov001_021e28d0_L30:
    ldrb r4, [r0, #0x31e]
    add r3, r5, r6, lsl #1
    ldrb r12, [r0, #0x31f]
    ldrb r3, [r4, r3]
    cmp r12, r3
    bne ov001_021e28d0_L80
    sub r4, r2, #1
    mov r7, r6
    cmp r6, r4
    bge ov001_021e28d0_L78
ov001_021e28d0_L58:
    ldrb r12, [r0, #0x31e]
    add lr, r5, r7, lsl #1
    add r7, r7, #1
    add r3, lr, r12
    ldrb r3, [r3, #0x2]
    cmp r7, r4
    strb r3, [lr, r12]
    blt ov001_021e28d0_L58
ov001_021e28d0_L78:
    add r1, r1, #1
    sub r2, r2, #1
ov001_021e28d0_L80:
    add r6, r6, #1
    cmp r6, r2
    blt ov001_021e28d0_L30
ov001_021e28d0_L8c:
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    ldreq r0, =0x022388ec
    streqb r2, [r0, #0x18]
    ldrne r0, =0x022388ec
    strneb r2, [r0, #0x19]
    mov r0, r1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
