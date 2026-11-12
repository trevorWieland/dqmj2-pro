/* ov006 row 0x021ed480: 220 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd0 -> native_data3_02219b4c (image word 0x02219b4c)
 *   pool +0xd4 -> constant 0x000005dc (image word 0x000005dc)
 *   pool +0xd8 -> native_data_0220d448 (image word 0x0220d448)
 *   branch +0x82 -> +0x92
 *   test +0x80 cmp r0, #0x0
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed480; the literal pool and
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

extern u8 native_data3_02219b4c[];
extern void native_fn_021edbac(void);
extern void native_fn_021edc78(void);
extern void native_fn_021edc50(void);
extern void native_fn_021ed654(void);
extern void native_fn_021edb9c(void);
extern u8 native_data_0220d448[];
extern void native_fn_021ed9d4(void);
extern void native_fn_021ec6e0(void);
extern void native_fn_021ed6a8(void);
extern void native_fn_021ed700(void);


asm u32 native_ov006_021ed480 (register u32 a0)
{
    push {r3, r4, r5, r6, lr}
    sub sp, #0x24
    add r5, r1, #0x0
    mov r1, #0x0
    add r0, sp, #0xc
    strb r1, [r0, #0]
    strh r1, [r0, #0x4]
    strh r1, [r0, #0x2]
    ldr r0, =native_data3_02219b4c
    add r6, r2, #0x0
    ldr r4, [r0, #0x14]
    add r0, sp, #0x14
    mov r2, #0x8
    bl native_fn_021edbac
    ldr r2, =0x000005dc
    add r0, r4, #0x0
    mov r1, #0x0
    bl native_fn_021edbac
    mov r1, #0x2
    add r0, sp, #0xc
    strb r1, [r0, #0x8]
    mov r1, #0x0
    strb r1, [r0, #0x9]
    mov r0, #0x4
    bl native_fn_021edc78
    add r1, sp, #0xc
    strh r0, [r1, #0xa]
    ldr r0, =native_data3_02219b4c
    ldr r0, [r0, #0x2c]
    str r0, [sp, #0x18]
    bl native_fn_021edc50
    str r0, [sp, #0x18]
    mov r1, #0x8
    add r0, sp, #0xc
    strh r1, [r0, #0x4]
    add r0, sp, #0xc
    add r0, #0x2
    str r0, [sp]
    add r0, sp, #0xc
    str r0, [sp, #0x4]
    ldr r0, =native_data3_02219b4c
    add r1, r4, #0x0
    ldr r0, [r0, #0]
    add r1, #0x18
    add r2, sp, #0x14
    add r3, sp, #0x10
    bl native_fn_021ed654
    add r5, #0x8
    add r0, sp, #0x1c
    add r1, r5, #0x0
    mov r2, #0x8
    bl native_fn_021edb9c
    ldr r2, =native_data_0220d448
    add r0, sp, #0x1c
    mov r1, #0x8
    mov r3, #0x6
    bl native_fn_021ed9d4
    cmp r0, #0x0
    beq ov006_021ed480_L92
    mov r0, #0x2
    bl native_fn_021ec6e0
    mov r0, #0x0
    add sp, #0x24
    mvn r0, r0
    pop {r3, r4, r5, r6, pc}
ov006_021ed480_L92:
    add r3, sp, #0xc
    mov r0, #0x0
    ldrsb r0, [r3, r0]
    mov r1, #0x2
    mov r2, #0x4
    str r0, [sp]
    mov r0, #0x11
    str r0, [sp, #0x4]
    add r0, sp, #0x1c
    str r0, [sp, #0x8]
    mov r5, #0x2
    ldrsh r2, [r3, r2]
    ldrsh r3, [r3, r5]
    add r0, r4, #0x0
    lsl r1, r1, #0xc
    bl native_fn_021ed6a8
    add r2, sp, #0xc
    mov r1, #0x4
    ldrsh r0, [r2, r1]
    add r3, r6, #0x0
    add r0, #0x18
    strh r0, [r2, #0x4]
    ldrsh r1, [r2, r1]
    add r0, r4, #0x0
    mov r2, #0x0
    bl native_fn_021ed700
    mov r0, #0x0
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
}
