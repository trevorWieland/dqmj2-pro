/* ov006 row 0x021eda50: 52 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x18 -> +0x32
 *   branch +0x28 -> +0x2c
 *   back edge +0x30 -> +0x1a
 *   test +0x16 cmp r4, #0x0
 *   test +0x26 cmp r1, r6
 *   test +0x2e cmp r0, r4
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eda50; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02026144(void);


asm u32 native_ov006_021eda50 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r5, r1, #0x0
    lsr r1, r2, #0x1f
    add r1, r2, r1
    ldr r6, [sp, #0x18]
    asr r4, r1, #0x1
    add r1, r6, #0x0
    add r7, r3, #0x0
    blx native_fn_02026144
    mov r0, #0x0
    cmp r4, #0x0
    ble ov006_021eda50_L32
ov006_021eda50_L1a:
    strb r0, [r5, r0]
    ldrsb r2, [r7, r1]
    ldrsb r3, [r5, r0]
    add r1, r1, #0x1
    eor r2, r3
    strb r2, [r5, r0]
    cmp r1, r6
    blt ov006_021eda50_L2c
    mov r1, #0x0
ov006_021eda50_L2c:
    add r0, r0, #0x1
    cmp r0, r4
    blt ov006_021eda50_L1a
ov006_021eda50_L32:
    pop {r3, r4, r5, r6, r7, pc}
}
