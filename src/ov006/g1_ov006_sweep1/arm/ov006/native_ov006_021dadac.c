/* ov006 row 0x021dadac: 508 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1f4 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x1f8 -> native_data_0220cc24 (image word 0x0220cc24)
 *   branch +0x13c -> +0x164
 *   branch +0x160 -> +0x180
 *   back edge +0x18c -> +0xbc
 *   back edge +0x1e8 -> +0x1b0
 *   test +0x138 cmp r0, #0
 *   test +0x188 cmp r9, #5
 *   test +0x198 cmp r0, #0
 *   test +0x1e4 cmp r7, r0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dadac; the literal pool and
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

extern void native_fn_02063eec(void);
extern void native_fn_021d7860(void);
extern void native_fn_021d77f8(void);
extern u8 native_data_0220cc24[];
extern void native_fn_021d7d28(void);
extern void native_fn_02067b58(void);
extern void native_fn_02048094(void);
extern void native_fn_02067748(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02048034(void);
extern void native_fn_021d79e4(void);
extern void native_fn_021d7e34(void);
extern void native_fn_02067bd4(void);
extern void native_fn_020643fc(void);
extern void native_fn_021d7ebc(void);
extern void native_fn_02046af4(void);
extern void native_fn_021d7ad0(void);
extern void native_fn_021d8414(void);
extern void native_fn_021d79f8(void);


asm u32 native_ov006_021dadac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    bl native_fn_02063eec
    mov r8, r0
    ldr r11, =0x021c9698
    bl native_fn_021d7860
    mov r0, #3
    bl native_fn_021d77f8
    ldr r0, =native_data_0220cc24
    mov r1, #23
    bl native_fn_021d7d28
    bl native_fn_02067b58
    ldr r0, [r0, #0x24]
    mov r1, #0
    add r0, r0, #1
    bl native_fn_02048094
    bl native_fn_02067748
    ldr r1, [r0, #0x4]
    mov r0, #15
    add r1, r1, #59
    mov r1, r1, lsl #16
    mov r2, r1, lsr #16
    mov r1, #2
    bl native_fn_0205dc70
    mov r1, #32
    bl native_fn_02048034
    mov r0, #0
    mov r1, #15
    mov r2, #2
    mov r3, #140
    bl native_fn_021d79e4
    mov r0, #1
    mov r1, #15
    mov r2, #2
    mov r3, #16
    bl native_fn_021d79e4
    mov r0, #2
    mov r1, #15
    mov r2, r0
    mov r3, #129
    bl native_fn_021d79e4
    bl native_fn_021d7e34
    mov r9, #0
    mov r10, #10
    mov r4, #40
    add r6, sp, #8
    mov r5, #255
ov006_021dadac_Lbc:
    mov r0, r9
    bl native_fn_02067bd4
    mov r7, r0
    add r0, r9, #1
    mov r1, #0
    bl native_fn_02048094
    add r0, r9, #3
    and r0, r0, #255
    mov r1, #15
    mov r2, #2
    mov r3, #141
    bl native_fn_021d79e4
    ldr r0, [r7, #0x8]
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_020643fc
    mov r1, #16
    mov r2, r10
    bl native_fn_021d7ebc
    str r6, [sp]
    mov r0, r11
    add r1, r7, #20
    mov r2, #31
    mov r3, #0
    str r5, [sp, #0x4]
    bl native_fn_02046af4
    add r0, r9, #8
    and r0, r0, #255
    mov r1, r6
    bl native_fn_021d7ad0
    ldr r0, [r7, #0xc]
    cmp r0, #0
    beq ov006_021dadac_L164
    mov r1, r6
    mov r2, #16
    mov r3, #6
    bl native_fn_021d8414
    add r0, r9, #13
    and r0, r0, #255
    mov r1, r6
    bl native_fn_021d7ad0
    b ov006_021dadac_L180
ov006_021dadac_L164:
    add r0, r9, #13
    and r0, r0, #255
    mov r1, #15
    mov r2, #2
    mov r3, #122
    str r4, [sp]
    bl native_fn_021d79f8
ov006_021dadac_L180:
    add r10, r10, #2
    add r9, r9, #1
    cmp r9, #5
    blt ov006_021dadac_Lbc
    ldrb r0, [r8]
    mov r7, #0
    cmp r0, #0
    addle sp, sp, #72
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r6, r8
    mov r5, #2
    mov r4, #15
ov006_021dadac_L1b0:
    str r5, [sp]
    ldr r0, [r6, #0x34]
    add r9, r7, #18
    add r0, r0, #147
    mov r3, r0, lsl #16
    mov r1, r4
    mov r2, r5
    and r0, r9, #255
    mov r3, r3, lsr #16
    bl native_fn_021d79f8
    ldrb r0, [r8]
    add r7, r7, #1
    add r6, r6, #48
    cmp r7, r0
    blt ov006_021dadac_L1b0
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
