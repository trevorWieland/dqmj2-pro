/* ov006 row 0x021dd4f0: 140 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x1c -> +0x78
 *   branch +0x34 -> +0x78
 *   back edge +0x74 -> +0x38
 *   test +0x28 cmp r8, #0
 *   test +0x5c cmp r5, r8
 *   test +0x7c cmp r7, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dd4f0; the literal pool and
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

extern void native_fn_02044cdc(void);


asm u32 native_ov006_021dd4f0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    movs r10, r0
    mov r9, r1
    mov r11, r2
    mov r8, r3
    ldr r7, [sp, #0x28]
    ldr r6, [sp, #0x30]
    beq ov006_021dd4f0_L78
    mov r0, r9
    bl native_fn_02044cdc
    cmp r8, #0
    add r4, r0, #1
    mov r5, #0
    ble ov006_021dd4f0_L78
ov006_021dd4f0_L38:
    mov r0, r9
    mov r1, r11
    add r2, r5, #1
    blx r6
    mov r1, #100
    add r2, r10, r5
    mul r1, r0, r1
    ldrb r0, [r1, r2]
    add r5, r5, #1
    cmp r5, r8
    mul r0, r4, r0
    mov r0, r0, lsl #16
    add r0, r7, r0, asr #16
    mov r0, r0, lsl #16
    mov r7, r0, asr #16
    blt ov006_021dd4f0_L38
ov006_021dd4f0_L78:
    ldrsh r0, [sp, #44]
    cmp r7, r0
    movge r7, r0
    mov r0, r7
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
