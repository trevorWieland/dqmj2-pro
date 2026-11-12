/* ov001 row 0x021fe0a4: 532 bytes.
 *
 * What it does: 129 instructions; 16 call(s) to 0x02049ad0, 0x02202360, 0x021db438, +13 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill (129 instructions, 16 calls, 2 branches, 13 back edges, 4 literal slots).
 *
 *   pool +0x204 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x208 -> native_data_0222ef58 (image word 0x0222ef58)
 *   pool +0x20c -> native_data_0222ef5c (image word 0x0222ef5c)
 *   pool +0x210 -> native_data_0222ef60 (image word 0x0222ef60)
 *   branch +0x70 -> +0x84
 *   branch +0x78 -> +0x184
 *   branch +0x11c -> +0x154
 *   test +0x34 cmp r6, #0
 *   test +0x6c cmp r0, #1
 *   test +0x74 cmp r0, #4
 *   test +0xc0 cmp r0, #0
 *   test +0x10c cmp r6, #0
 *   1 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fe0a4; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_02202360(void);
extern void native_fn_021db438(void);
extern void native_fn_02049f4c(void);
extern void native_fn_0207b244(void);
extern void native_fn_021fcb64(void);
extern void native_fn_0204a574(void);
extern u8 native_data_0222ef58[];
extern void native_fn_0204a104(void);
extern void native_fn_0204a154(void);
extern u8 native_data_0222ef5c[];
extern void native_fn_02213b4c(void);
extern void native_fn_02063144(void);
extern void native_fn_02049ffc(void);
extern u8 native_data_0222ef60[];


asm u32 native_ov001_021fe0a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #16
    mov r0, #27
    bl native_fn_02049ad0
    ldr r1, =0x02239c10
    mov r6, r0
    ldrsb r0, [r1, #12]
    bl native_fn_02202360
    mov r5, r0
    ldrsb r1, [r5, #8]
    mov r0, #0
    mov r7, #1
    bl native_fn_021db438
    cmp r6, #0
    mov r4, r0
    addeq sp, sp, #16
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    ldr r1, [r6]
    mov r0, r6
    ldr r6, [r1, #0x4]
    bl native_fn_02049f4c
    ldr r0, =0x02239c10
    mov r2, #0
    ldrsb r0, [r0, #12]
    mov r1, #16
    strh r2, [sp, #14]
    strh r1, [sp, #12]
    cmp r0, #1
    beq ov001_021fe0a4_L84
    cmp r0, #4
    beq ov001_021fe0a4_L184
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_021fe0a4_L84:
    ldr r0, [r5]
    add r1, r4, #256
    add r0, r4, r0
    ldr r2, [r4, #0x1e8]
    ldrb r0, [r0, #0x35e]
    ldrsh r1, [r1, #242]
    add r2, r2, #70
    bl native_fn_0207b244
    mov r6, r0
    ldr r1, [r5]
    mov r0, r4
    add r1, r4, r1
    ldrb r1, [r1, #0x35e]
    mov r2, r6
    bl native_fn_021fcb64
    cmp r0, #0
    moveq r7, #3
    mov r0, #3
    stmia sp, {r0, r7}
    mov r3, #1
    add r1, sp, #12
    str r3, [sp, #0x8]
    mov r0, #27
    mov r2, #5
    bl native_fn_0204a574
    ldrsh r2, [sp, #12]
    ldr r3, =native_data_0222ef58
    add r1, sp, #12
    add r0, r2, r0
    strh r0, [sp, #12]
    mov r2, r7
    mov r0, #27
    bl native_fn_0204a104
    ldrsh r1, [sp, #12]
    cmp r6, #0
    add r0, r1, r0
    strh r0, [sp, #12]
    add r1, sp, #12
    ble ov001_021fe0a4_L154
    mov r0, #4
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r2, r7
    mov r3, r6
    mov r0, #27
    bl native_fn_0204a154
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_021fe0a4_L154:
    ldrsh r0, [sp, #12]
    ldr r3, =native_data_0222ef5c
    mov r2, r7
    add r0, r0, #24
    strh r0, [sp, #12]
    mov r0, #27
    bl native_fn_0204a104
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_021fe0a4_L184:
    ldr r0, [r5]
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    bl native_fn_02213b4c
    bl native_fn_02063144
    mov r4, r0
    mov r0, r6
    bl native_fn_02049ffc
    mov r0, #16
    strh r0, [sp, #12]
    ldr r3, =native_data_0222ef60
    add r1, sp, #12
    mov r0, #27
    mov r2, r7
    bl native_fn_0204a104
    ldrsh r2, [sp, #12]
    mov r1, #2
    mov r0, #0
    add r2, r2, #16
    strh r2, [sp, #12]
    str r1, [sp]
    str r0, [sp, #0x4]
    mov r3, r4
    mov r0, #27
    add r1, sp, #12
    mov r2, r7
    bl native_fn_0204a154
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
