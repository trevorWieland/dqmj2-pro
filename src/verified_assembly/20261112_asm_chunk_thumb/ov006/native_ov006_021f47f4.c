/* ov006 row 0x021f47f4: 52 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x30 -> native_data3_0221c060 (image word 0x0221c060)
 *   branch +0x0e -> +0x2c
 *   test +0x0c cmp r4, r1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f47f4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 52 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data3_0221c060[];
extern void native_fn_021f4ac4(void);


asm u32 native_ov006_021f47f4 (register u32 a0)
{
    push {r4, lr}
    ldr r1, =native_data3_0221c060
    add r4, r0, #0x0
    ldr r2, [r1, #0]
    mov r1, #0x62
    ldrsb r1, [r2, r1]
    cmp r4, r1
    beq ov006_021f47f4_L2c
    mov r1, #0x1
    bl native_fn_021f4ac4
    ldr r0, =native_data3_0221c060
    ldr r1, [r0, #0]
    mov r0, #0x62
    ldrsb r0, [r1, r0]
    mov r1, #0x0
    bl native_fn_021f4ac4
    ldr r0, =native_data3_0221c060
    ldr r0, [r0, #0]
    add r0, #0x62
    strb r4, [r0, #0]
ov006_021f47f4_L2c:
    pop {r4, pc}
    mov r8, r8
}
