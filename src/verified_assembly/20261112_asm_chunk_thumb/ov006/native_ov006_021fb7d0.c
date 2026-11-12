/* ov006 row 0x021fb7d0: 48 bytes.
 *
 * What it does: Writes one block of 5 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   branch +0x0e -> +0x22
 *   branch +0x1c -> +0x22
 *   back edge +0x26 -> +0x06
 *   test +0x0c cmp r0, #0x0
 *   test +0x1a cmp r0, #0x0
 *   test +0x24 cmp r4, #0x4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb7d0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 16 of 48 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021fabe4(void);


asm u32 native_ov006_021fb7d0 (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r5, =0x0221c0ec
    mov r4, #0x0
ov006_021fb7d0_L6:
    ldr r0, [r5, #0x8]
    add r1, r0, r4
    ldrb r0, [r1, #0x4]
    cmp r0, #0x0
    beq ov006_021fb7d0_L22
    sub r0, r0, #0x1
    strb r0, [r1, #0x4]
    ldr r0, [r5, #0x8]
    add r0, r0, r4
    ldrb r0, [r0, #0x4]
    cmp r0, #0x0
    bne ov006_021fb7d0_L22
    bl native_fn_021fabe4
ov006_021fb7d0_L22:
    add r4, r4, #0x1
    cmp r4, #0x4
    blt ov006_021fb7d0_L6
    pop {r3, r4, r5, pc}
    mov r8, r8
}
