/* ov000 row 0x02220afc: 236 bytes.
 *
 * What it does: 55 instructions; 3 call(s) to 0x02228fdc, 0x02227f94, 0x02220b20; loops (back edge at +0xd0); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xdc -> constant 0x02246420 (image word 0x02246420)
 *   pool +0xe0 -> constant 0x02246424 (image word 0x02246424)
 *   pool +0xe4 -> constant 0x022463dc (image word 0x022463dc)
 *   pool +0xe8 -> constant 0x022463b0 (image word 0x022463b0)
 *   branch +0x3c -> +0xb0
 *   branch +0x7c -> +0x9c
 *   branch +0x98 -> +0xc0
 *   branch +0xac -> +0xc0
 *   back edge +0xd0 -> +0x24
 *   test +0x30 cmp r0, #0
 *   test +0x38 cmpne r0, #0
 *   test +0x78 cmp r0, r4
 *   test +0xc4 cmp r7, #3
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02220afc; the literal pool and
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

extern void native_fn_02228fdc(void);
extern void native_fn_02227f94(void);


asm u32 native_ov000_02220afc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    mov r7, #0
    ldr r8, =0x02246420
    ldr r9, =0x02246424
    ldr r6, =0x022463dc
    mov r11, r7
    mov r5, r7
    mvn r4, #0
ov000_02220afc_L24:
    ldr r0, =0x022463b0
    ldr r10, [r0, #0x1c]
    ldrsh r0, [r10, #24]
    cmp r0, #0
    ldrnesh r0, [r10, #156]
    cmpne r0, #0
    beq ov000_02220afc_Lb0
    ldr r0, =0x022463b0
    ldr r0, [r0, #0x20]
    bl native_fn_02228fdc
    add r1, sp, #12
    str r1, [sp]
    add r1, sp, #13
    str r1, [sp, #0x4]
    add r1, sp, #16
    str r1, [sp, #0x8]
    and r2, r0, #255
    ldr r0, [r10, #0x14]
    ldr r1, [r10, #0x98]
    and r3, r7, #255
    bl native_fn_02227f94
    cmp r0, r4
    beq ov000_02220afc_L9c
    ldrb r2, [sp, #0xd]
    ldr r1, [sp, #0x10]
    mov r3, r7, lsl #1
    strh r0, [r6, r3]
    strb r2, [r8]
    strb r1, [r9]
    b ov000_02220afc_Lc0
ov000_02220afc_L9c:
    mov r0, r7, lsl #1
    strh r5, [r6, r0]
    strb r5, [r8]
    strb r5, [r9]
    b ov000_02220afc_Lc0
ov000_02220afc_Lb0:
    mov r0, r7, lsl #1
    strh r11, [r6, r0]
    strb r11, [r8]
    strb r11, [r9]
ov000_02220afc_Lc0:
    add r7, r7, #1
    cmp r7, #3
    add r8, r8, #1
    add r9, r9, #1
    blt ov000_02220afc_L24
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
