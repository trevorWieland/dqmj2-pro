/* ov001 row 0x021fde38: 620 bytes.
 *
 * What it does: 154 instructions; 18 call(s) to 0x02202360, 0x021fe08c, 0x02049ad0, +15 more; loops (back edge at +0x44); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 18 calls (154 instructions, 18 calls, 15 branches, 14 back edges, 1 literal slot).
 *
 *   pool +0x268 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x34 -> +0x254
 *   branch +0x6c -> +0x23c
 *   branch +0x78 -> +0x21c
 *   branch +0x7c -> +0x21c
 *   branch +0x80 -> +0x12c
 *   branch +0x84 -> +0x94
 *   branch +0x88 -> +0x21c
 *   branch +0x8c -> +0x1c0
 *   branch +0x90 -> +0xf4
 *   branch +0xf0 -> +0x23c
 *   branch +0x128 -> +0x23c
 *   branch +0x14c -> +0x1b4
 *   branch +0x1b0 -> +0x23c
 *   branch +0x1bc -> +0x23c
 *   branch +0x218 -> +0x23c
 *   back edge +0x250 -> +0x38
 *   test +0x30 cmp r0, #0
 *   test +0x68 cmp r1, r0
 *   test +0x70 cmp r9, #5
 *   test +0x148 cmp r1, r0
 *   test +0x188 cmp r0, #0
 *   test +0x1e4 cmp r0, #0
 *   test +0x24c cmp r1, r0, asr #24
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fde38; the literal pool and
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

extern void ov001_table_f0_entry_02202360(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02048fbc(void);
extern void native_fn_0204a574(void);
extern void native_fn_021fe738(void);
extern void native_fn_02065818(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_0207b244(void);
extern void native_fn_021fcb64(void);
extern void native_fn_0204a3ec(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02213b4c(void);
extern void native_fn_022007f0(void);
extern void native_fn_0204a448(void);
extern void native_fn_0204a04c(void);
extern void native_fn_02049604(void);


asm u32 native_ov001_021fde38 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    ldr r1, =0x02239c10
    mov r9, r0
    ldrsb r0, [r1, #12]
    bl ov001_table_f0_entry_02202360
    add r11, sp, #12
    mov r5, #0
    mov r6, r0
    strh r5, [r11]
    strh r5, [r11, #2]
    ldrh r0, [r6, #12]
    cmp r0, #0
    ble ov001_021fde38_L254
ov001_021fde38_L38:
    add r7, r5, #9
    mov r0, r7, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    mov r4, r0
    ldr r1, [r4]
    mov r0, #0
    ldr r8, [r1, #0x4]
    mov r1, #16
    strh r1, [sp, #12]
    bl native_fn_02048fbc
    ldrsb r1, [r4, #5]
    cmp r1, r0
    beq ov001_021fde38_L23c
    cmp r9, #5
    addls pc, pc, r9, lsl #2
    b ov001_021fde38_L21c
    b ov001_021fde38_L21c
    b ov001_021fde38_L12c
    b ov001_021fde38_L94
    b ov001_021fde38_L21c
    b ov001_021fde38_L1c0
    b ov001_021fde38_Lf4
ov001_021fde38_L94:
    mov r1, #24
    strh r1, [sp, #12]
    ldr r2, [r6, #0x4]
    mov r0, r7, lsl #24
    add r2, r2, r5
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    str r2, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    mov r0, r0, asr #24
    mov r1, r11
    mov r2, #0
    mov r3, #1
    bl native_fn_0204a574
    add r0, r5, #14
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021fe738
    ldrsb r1, [r8, #28]
    ldrsb r2, [r8, #29]
    bl native_fn_02065818
    b ov001_021fde38_L23c
ov001_021fde38_Lf4:
    add r1, r5, #11
    mov r1, r1, lsl #16
    mov r1, r1, lsr #16
    str r1, [sp]
    mov r1, #1
    mov r0, r7, lsl #24
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    mov r0, r0, asr #24
    mov r1, r11
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    b ov001_021fde38_L23c
ov001_021fde38_L12c:
    ldrsb r1, [r6, #8]
    mov r0, #0
    bl ov001_side_slot_record_021db438
    mov r4, r0
    ldr r2, [r6, #0x4]
    ldrh r0, [r6, #14]
    add r1, r2, r5
    cmp r1, r0
    bge ov001_021fde38_L1b4
    add r0, r4, r2
    add r0, r5, r0
    ldrb r8, [r0, #0x35e]
    add r0, r4, #256
    ldrsh r1, [r0, #242]
    ldr r2, [r4, #0x1e8]
    mov r0, r8
    add r2, r2, #70
    mov r10, #1
    bl native_fn_0207b244
    mov r2, r0
    mov r0, r4
    mov r1, r8
    bl native_fn_021fcb64
    cmp r0, #0
    moveq r10, #3
    mov r0, r7, lsl #24
    mov r1, #1
    str r1, [sp]
    mov r0, r0, asr #24
    mov r2, r10
    mov r3, r8
    mov r1, r11
    bl native_fn_0204a3ec
    b ov001_021fde38_L23c
ov001_021fde38_L1b4:
    mov r0, r8
    bl native_fn_02049ffc
    b ov001_021fde38_L23c
ov001_021fde38_L1c0:
    ldr r0, [r6, #0x4]
    add r0, r0, r5
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    bl native_fn_02213b4c
    mov r8, r0
    and r0, r8, #255
    mov r4, #1
    bl native_fn_022007f0
    cmp r0, #0
    mov r1, r8, lsl #16
    mov r3, r1, asr #16
    mov r1, #0
    moveq r4, #3
    mov r0, r7, lsl #24
    str r1, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    mov r0, r0, asr #24
    mov r2, r4
    mov r1, r11
    bl native_fn_0204a448
    b ov001_021fde38_L23c
ov001_021fde38_L21c:
    ldr r3, [r6, #0x4]
    mov r1, #1
    add r3, r3, r5
    mov r3, r3, lsl #16
    mov r0, r8
    mov r2, r1
    mov r3, r3, lsr #16
    bl native_fn_0204a04c
ov001_021fde38_L23c:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    ldrh r1, [r6, #12]
    cmp r1, r0, asr #24
    bgt ov001_021fde38_L38
ov001_021fde38_L254:
    mov r0, r6
    mov r1, #1
    bl native_fn_02049604
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
