/* ov001 row 0x021fd858: 336 bytes.
 *
 * What it does: 83 instructions; 13 call(s) to 0x02202360, 0x021fd994, 0x02049ad0, +10 more; loops (back edge at +0x40); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (83 instructions, 13 calls, 13 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0x14c -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x1c -> +0x13c
 *   branch +0x50 -> +0x60
 *   branch +0x5c -> +0x74
 *   branch +0xbc -> +0x118
 *   branch +0xc0 -> +0x118
 *   branch +0xc4 -> +0xd8
 *   branch +0xc8 -> +0x118
 *   branch +0xcc -> +0x108
 *   branch +0xd0 -> +0xf8
 *   branch +0xd4 -> +0xe8
 *   branch +0xe4 -> +0x118
 *   branch +0xf4 -> +0x118
 *   branch +0x104 -> +0x118
 *   back edge +0x138 -> +0x30
 *   test +0x18 cmp r0, #0
 *   test +0x48 cmp r9, #5
 *   test +0x64 cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xb4 cmp r9, #5
 *   test +0xdc cmp r0, #0
 *   test +0xec cmp r0, #0
 *   test +0xfc cmp r0, #0
 *   test +0x10c cmp r0, #0
 *   test +0x134 cmp r1, r0, asr #24
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd858; the literal pool and
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
extern void native_fn_022021fc(void);
extern void native_fn_0204a04c(void);
extern void native_fn_02085270(void);
extern void native_fn_02085418(void);
extern void native_fn_02202f98(void);
extern void native_fn_02202fe4(void);
extern void native_fn_02202fb4(void);
extern void native_fn_021fbe88(void);
extern void native_fn_020852c8(void);
extern void native_fn_02049604(void);


asm u32 native_ov001_021fd858 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r0, #0
    bl ov001_table_f0_entry_02202360
    mov r7, r0
    ldrh r0, [r7, #12]
    mov r9, #0
    cmp r0, #0
    ble ov001_021fd858_L13c
    ldr r4, =0x02239c10
    mov r10, #9
    mov r11, r9
    mov r5, #1
ov001_021fd858_L30:
    mov r8, r5
    add r0, r9, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    cmp r9, #5
    ldr r6, [r0, #0x4]
    beq ov001_021fd858_L60
    ldr r0, [r7, #0x4]
    add r0, r0, r9
    b ov001_021fd858_L74
ov001_021fd858_L60:
    bl native_fn_022021fc
    cmp r0, #0
    ldrne r0, [r7, #0x4]
    addne r0, r0, r9
    moveq r0, r10
ov001_021fd858_L74:
    mov r0, r0, lsl #16
    mov r1, #1
    mov r3, r0, lsr #16
    mov r0, r6
    mov r2, r1
    bl native_fn_0204a04c
    add r0, r6, #60
    mov r1, r11
    mov r2, #4
    bl native_fn_02085270
    mov r0, r6
    mov r1, #3
    bl native_fn_02085418
    ldrb r0, [r4]
    cmp r0, #0
    movne r8, #3
    cmp r9, #5
    addls pc, pc, r9, lsl #2
    b ov001_021fd858_L118
    b ov001_021fd858_L118
    b ov001_021fd858_Ld8
    b ov001_021fd858_L118
    b ov001_021fd858_L108
    b ov001_021fd858_Lf8
    b ov001_021fd858_Le8
ov001_021fd858_Ld8:
    bl native_fn_02202f98
    cmp r0, #0
    moveq r8, #3
    b ov001_021fd858_L118
ov001_021fd858_Le8:
    bl native_fn_02202fe4
    cmp r0, #0
    moveq r8, #3
    b ov001_021fd858_L118
ov001_021fd858_Lf8:
    bl native_fn_02202fb4
    cmp r0, #0
    moveq r8, #3
    b ov001_021fd858_L118
ov001_021fd858_L108:
    bl native_fn_021fbe88
    cmp r0, #0
    str r0, [r4, #0x4c]
    movne r8, #3
ov001_021fd858_L118:
    mov r0, r6
    mov r1, r8
    bl native_fn_020852c8
    add r0, r9, #1
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
    ldrh r1, [r7, #12]
    cmp r1, r0, asr #24
    bgt ov001_021fd858_L30
ov001_021fd858_L13c:
    mov r0, r7
    mov r1, #0
    bl native_fn_02049604
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
