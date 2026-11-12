/* main row 0x020956a4: 56 bytes.
 *
 * What it does: 4 loads, 0 stores; 2 local pool words (0x00000d12, 0x00000447); 4 branches, 1 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x30 -> constant 0x00000d12 (image word 0x00000d12)
 *   pool +0x34 -> constant 0x00000447 (image word 0x00000447)
 *   branch +0x0c -> +0x2a
 *   branch +0x1a -> +0x20
 *   branch +0x1e -> +0x2a
 *   back edge +0x28 -> +0x10
 *   test +0x0a cmp r3, #0
 *   test +0x26 cmp r1, r3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020956a4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_main_020956a4 (register u32 a0)
{
    push {r4, r5}
    ldr r3, =0x00000d12
    mov r2, #0
    ldrb r3, [r0, r3]
    add r1, r2, #0
    cmp r3, #0
    bls main_020956a4_L2a
    ldr r4, =0x00000447
main_020956a4_L10:
    lsl r5, r1, #2
    add r5, r0, r5
    ldrb r5, [r5, r4]
    lsl r5, r5, #0x18
    lsr r5, r5, #0x1f
    bne main_020956a4_L20
    add r2, r1, #0
    b main_020956a4_L2a
main_020956a4_L20:
    add r1, r1, #1
    lsl r1, r1, #0x18
    lsr r1, r1, #0x18
    cmp r1, r3
    blo main_020956a4_L10
main_020956a4_L2a:
    add r0, r2, #0
    pop {r4, r5}
    bx lr
}
