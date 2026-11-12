/* ov006 row 0x022061e8: 320 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x13c -> native_data2_0221c290 (image word 0x0221c290)
 *   branch +0x34 -> +0x128
 *   branch +0x40 -> +0x120
 *   branch +0xe0 -> +0xf8
 *   branch +0xf4 -> +0x120
 *   branch +0x110 -> +0x11c
 *   branch +0x118 -> +0x120
 *   back edge +0x130 -> +0x2c
 *   test +0x30 cmp r0, #100
 *   test +0xdc cmp r0, #0
 *   test +0x100 cmp r0, #0
 *   test +0x12c cmp r7, #12
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022061e8; the literal pool and
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

extern u8 native_data2_0221c290[];
extern void native_fn_02008c58(void);
extern void native_fn_0206d9c8(void);
extern void native_fn_0207cd98(void);
extern void native_fn_02062a10(void);
extern void native_fn_0206c9b4(void);
extern void native_fn_0204b1b0(void);
extern void native_fn_0206ccb4(void);
extern void native_fn_0206cf44(void);
extern void native_fn_02063fa0(void);
extern void native_fn_021e7ed8(void);
extern void native_fn_02063fac(void);
extern void native_fn_021e7f08(void);
extern void native_fn_0206da10(void);


asm u32 native_ov006_022061e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r1, #12
    mul r6, r0, r1
    ldr r1, =native_data2_0221c290
    mov r0, #0
    mov r2, #48
    bl native_fn_02008c58
    bl native_fn_0206d9c8
    mov r7, #0
    mov r5, #1
    mov r11, #18
ov006_022061e8_L2c:
    add r0, r7, r6
    cmp r0, #100
    bge ov006_022061e8_L128
    bl native_fn_0207cd98
    movs r8, r0
    beq ov006_022061e8_L120
    bl native_fn_02062a10
    mov r4, r0
    mov r0, r8
    bl native_fn_02062a10
    str r5, [sp]
    mov r1, r0
    ldrsh r0, [r4, #24]
    ldrb r1, [r1, #0x1a]
    mov r2, r5
    mov r3, #32
    bl native_fn_0206c9b4
    mov r1, r7, lsr #31
    mov r4, r0
    rsb r0, r1, r7, lsl #30
    add r1, r1, r0, ror #30
    mov r0, #40
    mul r0, r1, r0
    add r0, r0, #48
    and r9, r0, #255
    mov r0, r7, asr #1
    add r0, r7, r0, lsr #30
    mov r0, r0, asr #2
    add r1, r0, #1
    mov r0, #40
    mul r0, r1, r0
    and r10, r0, #255
    bl native_fn_0204b1b0
    mov r1, r4
    mov r2, #3
    mov r3, #8
    str r11, [sp]
    bl native_fn_0206ccb4
    mov r0, r4
    mov r1, r9
    mov r2, r10
    bl native_fn_0206cf44
    mov r0, r8
    bl native_fn_02063fa0
    cmp r0, #0
    beq ov006_022061e8_Lf8
    mov r1, r9, lsr #3
    mov r2, r10, lsr #3
    mov r0, #11
    bl native_fn_021e7ed8
    b ov006_022061e8_L120
ov006_022061e8_Lf8:
    mov r0, r8
    bl native_fn_02063fac
    cmp r0, #0
    mov r1, r9, lsr #3
    mov r0, #12
    mov r2, r10, lsr #3
    beq ov006_022061e8_L11c
    bl native_fn_021e7ed8
    b ov006_022061e8_L120
ov006_022061e8_L11c:
    bl native_fn_021e7f08
ov006_022061e8_L120:
    ldr r0, =native_data2_0221c290
    str r8, [r0, r7, lsl #2]
ov006_022061e8_L128:
    add r7, r7, #1
    cmp r7, #12
    blt ov006_022061e8_L2c
    bl native_fn_0206da10
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
