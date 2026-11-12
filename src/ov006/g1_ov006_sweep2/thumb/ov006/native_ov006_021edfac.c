/* ov006 row 0x021edfac: 56 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x34 -> constant 0x0221a940 (image word 0x0221a940)
 *   branch +0x0c -> +0x30
 *   branch +0x22 -> +0x2a
 *   branch +0x28 -> +0x2c
 *   back edge +0x2e -> +0x14
 *   test +0x0a cmp r0, #0x0
 *   test +0x20 cmp r0, #0xe
 *   test +0x2c cmp r0, #0x0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021edfac; the literal pool and
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

extern void native_fn_021ee7d8(void);
extern void native_fn_02006eb8(void);


asm u32 native_ov006_021edfac (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r5, #0x0
    mvn r5, r5
    bl native_fn_021ee7d8
    cmp r0, #0x0
    beq ov006_021edfac_L30
    ldr r4, =0x0221a940
    add r6, sp, #0x0
    mov r7, #0x1
ov006_021edfac_L14:
    add r0, r4, #0x0
    add r1, r6, #0x0
    add r2, r7, #0x0
    blx native_fn_02006eb8
    ldr r0, [sp]
    cmp r0, #0xe
    bne ov006_021edfac_L2a
    mov r0, #0x0
    add r5, r0, #0x0
    b ov006_021edfac_L2c
ov006_021edfac_L2a:
    mov r0, #0x0
ov006_021edfac_L2c:
    cmp r0, #0x0
    bne ov006_021edfac_L14
ov006_021edfac_L30:
    add r0, r5, #0x0
    pop {r3, r4, r5, r6, r7, pc}
}
