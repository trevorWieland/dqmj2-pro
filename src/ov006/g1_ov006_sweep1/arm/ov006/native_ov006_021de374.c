/* ov006 row 0x021de374: 676 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x28c -> native_data_02207940 (image word 0x02207940)
 *   pool +0x290 -> constant 0x0220f738 (image word 0x0220f738)
 *   pool +0x294 -> native_data3_0220f72c (image word 0x0220f72c)
 *   pool +0x298 -> native_data3_0220f654 (image word 0x0220f654)
 *   pool +0x29c -> constant 0x0220f69c (image word 0x0220f69c)
 *   pool +0x2a0 -> constant 0x0220f594 (image word 0x0220f594)
 *   back edge +0x7c -> +0x60
 *   branch +0x184 -> +0x190
 *   back edge +0x248 -> +0x200
 *   test +0x78 cmp r5, #4
 *   test +0x180 cmp r1, #0
 *   test +0x23c cmp r8, #2
 *   0 block transfer(s), 33 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021de374; the literal pool and
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

extern u8 native_data_02207940[];
extern void native_fn_021dfd70(void);
extern void native_fn_02048fcc(void);
extern u8 native_data3_0220f72c[];
extern void native_fn_021df134(void);
extern void native_fn_021ddf08(void);
extern void native_fn_02048f1c(void);
extern void native_fn_02048f2c(void);
extern void native_fn_02048f3c(void);
extern void native_fn_021df234(void);
extern void native_fn_021df140(void);
extern void native_fn_0204b4f4(void);
extern void native_fn_0204b61c(void);
extern void native_fn_02049794(void);
extern void native_fn_02048f6c(void);
extern void native_fn_021ddf18(void);
extern void native_fn_02049ae4(void);
extern void native_fn_020853c8(void);
extern u8 native_data3_0220f654[];
extern void native_fn_0204b85c(void);
extern void native_fn_0205f98c(void);
extern void native_fn_02048a60(void);
extern void native_fn_0205fa4c(void);
extern void native_fn_021de964(void);
extern void native_fn_021dfe48(void);


asm u32 native_ov006_021de374 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    ldr r1, =native_data_02207940
    mov r0, #0
    ldrh r2, [r1, #2]
    ldrh r1, [r1]
    strh r2, [sp, #26]
    strh r1, [sp, #24]
    bl native_fn_021dfd70
    ldr r0, =0x0220f738
    bl native_fn_02048fcc
    ldr r0, =native_data3_0220f72c
    mov r1, #1
    mov r2, #0
    strh r1, [r0, #2]
    strb r2, [r0]
    strh r2, [r0, #6]
    sub r1, r2, #1
    strh r1, [r0, #4]
    strb r2, [r0, #0x8]
    bl native_fn_021df134
    bl native_fn_02048fcc
    mov r5, #0
    mov r4, #32
ov006_021de374_L60:
    mov r0, r5
    mov r1, r4
    bl native_fn_021ddf08
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #4
    blt ov006_021de374_L60
    mov r0, #3
    mov r1, #1
    bl native_fn_02048f1c
    mov r0, #2
    mov r1, #1
    bl native_fn_02048f2c
    mov r0, #0
    mov r1, #1
    bl native_fn_02048f3c
    bl native_fn_021df234
    bl native_fn_021df140
    mov r3, #2
    str r3, [sp]
    mov r1, #36
    str r1, [sp, #0x4]
    add r1, sp, #24
    mov r2, #192
    bl native_fn_0204b4f4
    bl native_fn_021df140
    mov r1, #0
    bl native_fn_0204b61c
    mov r0, #22
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r1, #10
    str r1, [sp, #0x8]
    mov r1, #2
    str r1, [sp, #0xc]
    str r0, [sp, #0x10]
    ldr r2, =native_data3_0220f72c
    str r0, [sp, #0x14]
    ldrsb r2, [r2, #28]
    mov r1, #31
    mov r3, #3
    bl native_fn_02049794
    mov r0, #1
    str r0, [sp]
    str r0, [sp, #0x4]
    mov r1, #20
    str r1, [sp, #0x8]
    mov r1, #2
    str r1, [sp, #0xc]
    str r0, [sp, #0x10]
    ldr r2, =native_data3_0220f72c
    str r0, [sp, #0x14]
    ldrsb r2, [r2, #28]
    mov r1, #0
    mov r3, #127
    bl native_fn_02049794
    mov r0, #1
    bl native_fn_02048f6c
    mov r4, r0
    mov r0, #1
    bl native_fn_02048f6c
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021ddf18
    mov r2, r4, lsl #24
    mov r1, r0
    mov r0, r2, asr #24
    bl native_fn_021ddf08
    bl native_fn_02049ae4
    ldr r1, [r0]
    cmp r1, #0
    beq ov006_021de374_L190
    ldr r0, [r0, #0x4]
    bl native_fn_020853c8
ov006_021de374_L190:
    mov r4, #0
    str r4, [sp]
    mov r0, #51
    str r0, [sp, #0x4]
    ldr r0, =native_data3_0220f654
    add r1, sp, #24
    mov r2, #8
    mov r3, #1
    str r4, [sp, #0x8]
    bl native_fn_0204b85c
    ldr r0, =native_data3_0220f654
    mov r1, r4
    ldr r0, [r0, #0x1c]
    bl native_fn_0205f98c
    mov r1, #224
    mov r2, #96
    bl native_fn_02048a60
    ldr r0, =native_data3_0220f654
    mov r1, r4
    bl native_fn_0205fa4c
    ldr r9, =0x0220f69c
    mov r8, r4
    mov r7, r4
    mov r10, #56
    add r6, sp, #24
    mov r5, #8
    mov r4, #1
    mov r11, #208
ov006_021de374_L200:
    add r0, r8, #21
    str r7, [sp]
    and r0, r0, #255
    str r0, [sp, #0x4]
    mov r0, r9
    mov r1, r6
    mov r2, r5
    mov r3, r4
    str r7, [sp, #0x8]
    bl native_fn_0204b85c
    ldr r0, [r9, #0x1c]
    mov r1, r11
    mov r2, r10
    bl native_fn_02048a60
    add r8, r8, #1
    cmp r8, #2
    add r9, r9, #72
    add r10, r10, #104
    blt ov006_021de374_L200
    mov r0, #0
    mov r1, r0
    mov r2, r0
    mov r3, r0
    bl native_fn_021de964
    ldr r0, =0x0220f594
    mov r1, #0
    str r1, [r0, #0x50]
    strb r1, [r0]
    str r1, [r0, #0x1c]
    str r1, [r0, #0x4c]
    str r1, [r0, #0x40]
    str r1, [r0, #0x2c]
    bl native_fn_021dfe48
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
