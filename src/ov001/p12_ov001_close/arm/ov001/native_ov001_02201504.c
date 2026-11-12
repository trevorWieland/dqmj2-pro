/* ov001 row 0x02201504: 548 bytes.
 *
 * What it does: 133 instructions; 22 call(s) to 0x02202360, 0x02049f24, 0x02049f30, +19 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 22 calls (133 instructions, 22 calls, 11 branches, 19 back edges, 4 literal slots).
 *
 *   pool +0x214 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x218 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x21c -> native_data_0222ed34 (image word 0x0222ed34)
 *   pool +0x220 -> constant 0x020dbc18 (image word 0x020dbc18)
 *   branch +0x44 -> +0x1fc
 *   branch +0x48 -> +0x60
 *   branch +0x4c -> +0xac
 *   branch +0x50 -> +0x1bc
 *   branch +0x54 -> +0x1fc
 *   branch +0x58 -> +0x13c
 *   branch +0x5c -> +0x1bc
 *   branch +0x6c -> +0x1fc
 *   branch +0xa8 -> +0x1fc
 *   branch +0xcc -> +0xf4
 *   branch +0x138 -> +0x1fc
 *   branch +0x1b8 -> +0x1fc
 *   test +0x3c cmp r0, #5
 *   test +0x68 cmp r0, #1
 *   test +0xc8 cmp r0, #8
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02201504; the literal pool and
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
extern void native_fn_02049f24(void);
extern void native_fn_02049f30(void);
extern u8 native_data_0222ed34[];
extern void native_fn_0205dc70(void);
extern void native_fn_02046af4(void);
extern void native_fn_02049f14(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_02060510(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02213b4c(void);
extern void native_fn_02065d88(void);
extern void native_fn_02066a6c(void);
extern void native_fn_0204b61c(void);


asm u32 native_ov001_02201504 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #8
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl ov001_table_f0_entry_02202360
    mov r4, r0
    ldr r1, [r4]
    ldr r0, [r4, #0x4]
    ldr r5, =0x021c9698
    sub r6, r1, r0
    bl native_fn_02049f24
    mov r7, r0
    bl native_fn_02049f30
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b ov001_02201504_L1fc
    b ov001_02201504_L60
    b ov001_02201504_Lac
    b ov001_02201504_L1bc
    b ov001_02201504_L1fc
    b ov001_02201504_L13c
    b ov001_02201504_L1bc
ov001_02201504_L60:
    ldr r0, =native_data_0222ed34
    ldrb r0, [r0, #0x2]
    cmp r0, #1
    bne ov001_02201504_L1fc
    mov r0, #1
    mov r1, #4
    mov r2, #8
    bl native_fn_0205dc70
    mov r1, r0
    mov r0, r5
    str r7, [sp]
    mov r5, #255
    mov r2, #28
    mov r3, #0
    str r5, [sp, #0x4]
    bl native_fn_02046af4
    mov r0, r7
    bl native_fn_02049f14
    b ov001_02201504_L1fc
ov001_02201504_Lac:
    ldrsb r1, [r4, #8]
    mov r8, #0
    mov r0, r8
    bl ov001_side_slot_record_021db438
    ldr r1, [r4]
    add r0, r0, r1
    ldrb r0, [r0, #0x35e]
    cmp r0, #8
    blo ov001_02201504_Lf4
    bl native_fn_02060510
    add r0, r0, #123
    add r2, r0, #256
    add r0, r8, #1
    ldr r1, =0x020dbc18
    mov r2, r2, lsl #1
    ldrh r1, [r1, r2]
    and r8, r0, #255
    strh r1, [r7]
ov001_02201504_Lf4:
    add r0, r6, #9
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    add r1, r7, r8, lsl #1
    str r1, [sp]
    mov r1, #255
    str r1, [sp, #0x4]
    ldr r1, [r0]
    mov r0, r5
    ldr r1, [r1, #0x4]
    mov r2, #28
    ldr r1, [r1, #0x68]
    mov r3, #0
    bl native_fn_02046af4
    mov r0, r7
    bl native_fn_02049f14
    b ov001_02201504_L1fc
ov001_02201504_L13c:
    ldr r0, [r4]
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    bl native_fn_02213b4c
    bl native_fn_02065d88
    ldrb r0, [r0, #0x24]
    bl native_fn_02066a6c
    add r1, r6, #9
    mov r1, r1, lsl #24
    add r0, r0, #123
    add r0, r0, #256
    mov r2, r0, lsl #1
    mov r0, r1, asr #24
    ldr r1, =0x020dbc18
    ldrh r1, [r1, r2]
    strh r1, [r7]
    bl native_fn_02049ad0
    mov r2, r0
    mov r0, r5
    add r1, r7, #2
    str r1, [sp]
    mov r1, #255
    str r1, [sp, #0x4]
    ldr r1, [r2]
    mov r2, #28
    ldr r1, [r1, #0x4]
    mov r3, #0
    ldr r1, [r1, #0x68]
    bl native_fn_02046af4
    mov r0, r7
    bl native_fn_02049f14
    b ov001_02201504_L1fc
ov001_02201504_L1bc:
    add r0, r6, #9
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    str r7, [sp]
    mov r1, #255
    str r1, [sp, #0x4]
    ldr r1, [r0]
    mov r0, r5
    ldr r1, [r1, #0x4]
    mov r2, #28
    ldr r1, [r1, #0x68]
    mov r3, #0
    bl native_fn_02046af4
    mov r0, r7
    bl native_fn_02049f14
ov001_02201504_L1fc:
    add r0, r4, #24
    mov r1, #0
    bl native_fn_0204b61c
    mov r0, #1
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
