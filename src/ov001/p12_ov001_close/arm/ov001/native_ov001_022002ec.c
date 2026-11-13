/* ov001 row 0x022002ec: 384 bytes.
 *
 * What it does: 94 instructions; 17 call(s) to 0x02049ae4, 0x02202360, 0x021fd82c, +14 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 17 calls (94 instructions, 17 calls, 17 branches, 15 back edges, 2 literal slots).
 *
 *   pool +0x178 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x17c -> native_data_0222ed34 (image word 0x0222ed34)
 *   branch +0x3c -> +0x130
 *   branch +0x40 -> +0x58
 *   branch +0x44 -> +0x88
 *   branch +0x48 -> +0xd8
 *   branch +0x4c -> +0x108
 *   branch +0x50 -> +0xb4
 *   branch +0x54 -> +0xf4
 *   branch +0x6c -> +0x7c
 *   branch +0x78 -> +0x130
 *   branch +0x84 -> +0x130
 *   branch +0xb0 -> +0x130
 *   branch +0xd4 -> +0x130
 *   branch +0xf0 -> +0x130
 *   branch +0x104 -> +0x130
 *   branch +0x118 -> +0x128
 *   branch +0x124 -> +0x130
 *   branch +0x138 -> +0x144
 *   test +0x34 cmp r0, #5
 *   test +0x64 cmp r0, #0
 *   test +0x10c cmp r0, #7
 *   test +0x134 cmp r1, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022002ec; the literal pool and
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

extern void native_fn_02049ae4(void);
extern void ov001_table_f0_entry_02202360(void);
extern void native_fn_021fd82c(void);
extern u8 native_data_0222ed34[];
extern void native_fn_021fe3d0(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_02213b4c(void);
extern void native_fn_020443ec(void);
extern void native_fn_020853c8(void);
extern void native_fn_02086b14(void);
extern void native_fn_021fea80(void);


asm u32 native_ov001_022002ec (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    bl native_fn_02049ae4
    ldr r1, =0x02239c10
    mov r5, r0
    ldrsb r0, [r1, #12]
    bl ov001_table_f0_entry_02202360
    mov r4, r0
    ldr r0, [r4]
    mov r0, r0, lsl #16
    mov r6, r0, lsr #16
    bl native_fn_021fd82c
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b ov001_022002ec_L130
    b ov001_022002ec_L58
    b ov001_022002ec_L88
    b ov001_022002ec_Ld8
    b ov001_022002ec_L108
    b ov001_022002ec_Lb4
    b ov001_022002ec_Lf4
ov001_022002ec_L58:
    ldr r0, =native_data_0222ed34
    mov r2, #7
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    mov r0, #1
    beq ov001_022002ec_L7c
    mov r1, #4
    bl native_fn_021fe3d0
    b ov001_022002ec_L130
ov001_022002ec_L7c:
    mov r1, r0
    bl native_fn_021fe3d0
    b ov001_022002ec_L130
ov001_022002ec_L88:
    ldrsb r1, [r4, #18]
    mov r0, #0
    bl ov001_side_slot_record_021db438
    mov r2, r0
    ldr r1, [r4]
    mov r0, #13
    add r1, r2, r1
    ldrb r2, [r1, #0x35e]
    mov r1, #0
    bl native_fn_021fe3d0
    b ov001_022002ec_L130
ov001_022002ec_Lb4:
    ldr r0, [r4]
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    bl native_fn_02213b4c
    mov r2, r0
    mov r0, #14
    mov r1, #0
    bl native_fn_021fe3d0
    b ov001_022002ec_L130
ov001_022002ec_Ld8:
    add r0, r6, #8
    mov r0, r0, lsl #16
    mov r2, r0, lsr #16
    mov r0, #0
    mov r1, #1
    bl native_fn_021fe3d0
    b ov001_022002ec_L130
ov001_022002ec_Lf4:
    mov r2, r6
    mov r0, #1
    mov r1, #4
    bl native_fn_021fe3d0
    b ov001_022002ec_L130
ov001_022002ec_L108:
    bl native_fn_020443ec
    cmp r0, #7
    mov r0, #1
    mov r1, #4
    bne ov001_022002ec_L128
    mov r2, #3
    bl native_fn_021fe3d0
    b ov001_022002ec_L130
ov001_022002ec_L128:
    mov r2, #2
    bl native_fn_021fe3d0
ov001_022002ec_L130:
    ldr r1, [r5]
    cmp r1, #0
    beq ov001_022002ec_L144
    ldr r0, [r5, #0x4]
    bl native_fn_020853c8
ov001_022002ec_L144:
    ldr r2, [r5, #0x4]
    mov r1, #10
    ldr r0, [r2, #0x18]
    orr r0, r0, #2
    str r0, [r2, #0x18]
    ldr r0, [r5, #0x4]
    bl native_fn_02086b14
    bl native_fn_021fea80
    ldr r0, =0x02239c10
    mov r1, #9
    strb r1, [r0, #0xa]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
}
