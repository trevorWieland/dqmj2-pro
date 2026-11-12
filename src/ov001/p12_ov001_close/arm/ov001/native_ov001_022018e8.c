/* ov001 row 0x022018e8: 428 bytes.
 *
 * What it does: 105 instructions; 31 call(s) to 0x02089868, 0x02045680, 0x021fd84c, +28 more; loops (back edge at +0x04); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 31 calls (105 instructions, 31 calls, 10 branches, 20 back edges, 2 literal slots).
 *
 *   pool +0x1a4 -> native_data_0222ed34 (image word 0x0222ed34)
 *   pool +0x1a8 -> constant 0x04001048 (image word 0x04001048)
 *   branch +0x0c -> +0xb4
 *   branch +0x5c -> +0x70
 *   branch +0x6c -> +0x8c
 *   branch +0x10c -> +0x120
 *   branch +0x11c -> +0x13c
 *   branch +0x154 -> +0x188
 *   test +0x08 cmp r0, #1
 *   test +0x58 cmp r0, #2
 *   test +0x68 cmp r0, #2
 *   test +0xb8 cmp r0, #0
 *   test +0x108 cmp r0, #2
 *   test +0x118 cmp r0, #2
 *   test +0x150 cmp r0, #1
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022018e8; the literal pool and
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

extern void native_fn_02089868(void);
extern void native_fn_02045680(void);
extern void native_fn_021fd84c(void);
extern u8 native_data_0222ed34[];
extern void native_fn_02206888(void);
extern void native_fn_02203320(void);
extern void native_fn_021e13a8(void);
extern void native_fn_021ff238(void);
extern void native_fn_021fea54(void);
extern void native_fn_02203308(void);
extern void native_fn_022030b8(void);
extern void native_fn_022033a4(void);
extern void native_fn_02201760(void);
extern void native_fn_02041538(void);
extern void native_fn_02041908(void);


asm u32 native_ov001_022018e8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02089868
    cmp r0, #1
    bne ov001_022018e8_Lb4
    mov r0, #0
    bl native_fn_02045680
    bl native_fn_021fd84c
    ldr r0, =native_data_0222ed34
    mov r1, #0
    ldrsb r0, [r0, #3]
    bl native_fn_02206888
    ldr r3, =0x04001048
    mov r0, #0
    ldrh r1, [r3]
    sub r2, r3, #72
    bic r1, r1, #63
    orr r1, r1, #63
    strh r1, [r3]
    ldr r1, [r2]
    bic r1, r1, #57344
    str r1, [r2]
    bl native_fn_02203320
    cmp r0, #2
    beq ov001_022018e8_L70
    mov r0, #1
    bl native_fn_02203320
    cmp r0, #2
    bne ov001_022018e8_L8c
ov001_022018e8_L70:
    mov r0, #4
    bl native_fn_021e13a8
    mov r0, #1
    bl native_fn_021ff238
    bl native_fn_021fea54
    mov r0, #1
    ldmia sp!, {r3, pc}
ov001_022018e8_L8c:
    mov r0, #0
    mov r1, #127
    bl native_fn_02203308
    bl native_fn_021fea54
    mov r0, #2
    bl native_fn_021e13a8
    mov r0, #1
    bl native_fn_021ff238
    mov r0, #1
    ldmia sp!, {r3, pc}
ov001_022018e8_Lb4:
    bl native_fn_022030b8
    cmp r0, #0
    mov r0, #0
    ldmeqia sp!, {r3, pc}
    bl native_fn_02045680
    bl native_fn_021fd84c
    ldr r0, =native_data_0222ed34
    mov r1, #0
    ldrsb r0, [r0, #3]
    bl native_fn_02206888
    ldr r3, =0x04001048
    mov r0, #0
    ldrh r1, [r3]
    sub r2, r3, #72
    bic r1, r1, #63
    orr r1, r1, #63
    strh r1, [r3]
    ldr r1, [r2]
    bic r1, r1, #57344
    str r1, [r2]
    bl native_fn_02203320
    cmp r0, #2
    beq ov001_022018e8_L120
    mov r0, #1
    bl native_fn_02203320
    cmp r0, #2
    bne ov001_022018e8_L13c
ov001_022018e8_L120:
    mov r0, #4
    bl native_fn_021e13a8
    mov r0, #1
    bl native_fn_021ff238
    bl native_fn_021fea54
    mov r0, #1
    ldmia sp!, {r3, pc}
ov001_022018e8_L13c:
    mov r0, #0
    mov r1, #127
    bl native_fn_02203308
    mov r0, #1
    bl native_fn_02203320
    cmp r0, #1
    bne ov001_022018e8_L188
    mov r0, #1
    bl native_fn_022033a4
    bl native_fn_02201760
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #10
    mov r1, #12
    bl native_fn_02041908
    mov r0, #1
    ldmia sp!, {r3, pc}
ov001_022018e8_L188:
    bl native_fn_021fea54
    mov r0, #2
    bl native_fn_021e13a8
    mov r0, #1
    bl native_fn_021ff238
    mov r0, #1
    ldmia sp!, {r3, pc}
}
