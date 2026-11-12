/* ov006 row 0x021dbba4: 488 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1e0 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x1e4 -> native_data_0220ce5c (image word 0x0220ce5c)
 *   back edge +0x38 -> +0x20
 *   branch +0x164 -> +0x174
 *   branch +0x170 -> +0x17c
 *   back edge +0x18c -> +0xfc
 *   test +0x28 cmp r0, #0
 *   test +0x30 cmp r1, #5
 *   test +0x154 cmp r0, #0
 *   test +0x188 cmp r10, #5
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dbba4; the literal pool and
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
extern u8 native_data_0220ce5c[];
extern void native_fn_021d7d28(void);
extern void native_fn_021d79e4(void);
extern void native_fn_02048094(void);
extern void native_fn_02046af4(void);
extern void native_fn_021d7ad0(void);
extern void native_fn_021dc08c(void);


asm u32 native_ov006_021dbba4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    ldr r6, =0x021c9698
    bl native_fn_02063eec
    mov r7, r0
    mov r4, #0
    mov r1, r4
    mov r2, r7
ov006_021dbba4_L20:
    ldr r0, [r2, #0x34]
    add r1, r1, #1
    cmp r0, #0
    addne r4, r4, #1
    cmp r1, #5
    add r2, r2, #48
    blt ov006_021dbba4_L20
    bl native_fn_021d7860
    mov r0, #4
    bl native_fn_021d77f8
    ldr r0, =native_data_0220ce5c
    mov r1, #25
    bl native_fn_021d7d28
    mov r0, #0
    mov r1, #15
    mov r2, #2
    mov r3, #129
    bl native_fn_021d79e4
    mov r0, #1
    mov r1, #15
    mov r2, #2
    mov r3, #143
    bl native_fn_021d79e4
    mov r0, r4
    mov r1, #0
    bl native_fn_02048094
    rsb r0, r4, #5
    mov r1, #32
    bl native_fn_02048094
    mov r0, #17
    mov r1, #15
    mov r2, #2
    mov r3, #162
    bl native_fn_021d79e4
    mov r0, #19
    mov r1, #15
    mov r2, #2
    mov r3, #150
    bl native_fn_021d79e4
    mov r0, #21
    mov r1, #15
    mov r2, #2
    mov r3, #151
    bl native_fn_021d79e4
    mov r0, #23
    mov r1, #15
    mov r2, #2
    mov r3, #152
    bl native_fn_021d79e4
    mov r10, #0
    add r8, r7, #16
    mov r9, r7
    mov r11, r10
    add r5, sp, #8
    mov r4, #255
ov006_021dbba4_Lfc:
    add r0, r10, #1
    mov r1, r11
    bl native_fn_02048094
    add r0, r10, #2
    and r0, r0, #255
    mov r1, #15
    mov r2, #2
    mov r3, #141
    bl native_fn_021d79e4
    str r5, [sp]
    mov r0, r6
    mov r1, r8
    mov r2, #31
    mov r3, #0
    str r4, [sp, #0x4]
    bl native_fn_02046af4
    add r0, r10, #7
    and r0, r0, #255
    mov r1, r5
    bl native_fn_021d7ad0
    ldr r0, [r9, #0x34]
    mov r1, #15
    cmp r0, #0
    add r0, r10, #12
    and r0, r0, #255
    mov r2, #2
    bne ov006_021dbba4_L174
    mov r3, #159
    bl native_fn_021d79e4
    b ov006_021dbba4_L17c
ov006_021dbba4_L174:
    mov r3, #158
    bl native_fn_021d79e4
ov006_021dbba4_L17c:
    add r8, r8, #48
    add r9, r9, #48
    add r10, r10, #1
    cmp r10, #5
    blt ov006_021dbba4_Lfc
    ldr r1, [r7, #0x8]
    mov r0, #18
    mov r2, #4
    bl native_fn_021dc08c
    ldrh r1, [r7, #4]
    mov r0, #20
    mov r2, #4
    bl native_fn_021dc08c
    ldrh r1, [r7, #6]
    mov r0, #22
    mov r2, #4
    bl native_fn_021dc08c
    ldrb r1, [r7, #0x3]
    ldr r2, [r7, #0xc]
    mov r0, #24
    sub r1, r2, r1
    mov r2, #4
    bl native_fn_021dc08c
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
