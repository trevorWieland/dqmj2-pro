/* ov001 row 0x021fff38: 524 bytes.
 *
 * What it does: 129 instructions; 22 call(s) to 0x0202a634, 0x02202360, 0x02049618, +19 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 22 calls (129 instructions, 22 calls, 18 branches, 7 back edges, 2 literal slots).
 *
 *   pool +0x204 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x208 -> constant 0x00000201 (image word 0x00000201)
 *   branch +0x38 -> +0x48
 *   branch +0x4c -> +0x18c
 *   branch +0x50 -> +0xd8
 *   branch +0x58 -> +0xb0
 *   branch +0x70 -> +0x94
 *   branch +0x90 -> +0x158
 *   branch +0xac -> +0x158
 *   branch +0xd4 -> +0x158
 *   branch +0xdc -> +0x134
 *   branch +0xf4 -> +0x118
 *   branch +0x114 -> +0x158
 *   branch +0x130 -> +0x158
 *   branch +0x188 -> +0x1f8
 *   branch +0x194 -> +0x1b0
 *   branch +0x1ac -> +0x1f8
 *   branch +0x1b8 -> +0x1f4
 *   branch +0x1d8 -> +0x1e8
 *   branch +0x1e4 -> +0x1f8
 *   branch +0x1f0 -> +0x1f8
 *   test +0x34 cmp r0, #0
 *   test +0x48 cmp r7, #0
 *   test +0x54 cmp r5, #0
 *   test +0x64 cmp r0, #0
 *   test +0xd8 cmp r5, #0
 *   test +0xe8 cmp r0, #0
 *   test +0x160 cmp r5, #0
 *   test +0x190 tst r1, #2
 *   test +0x1b4 tst r1, r0
 *   test +0x1bc cmp r5, #0
 *   test +0x1d0 cmp r6, #1
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fff38; the literal pool and
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

extern void native_fn_0202a634(void);
extern void ov001_table_f0_entry_02202360(void);
extern void native_fn_02049618(void);
extern void native_fn_02203418(void);
extern void native_fn_022011c0(void);
extern void native_fn_022029a8(void);
extern void native_fn_022028fc(void);
extern void native_fn_02202a68(void);
extern void native_fn_0220294c(void);
extern void native_fn_022023c4(void);
extern void native_fn_02204470(void);
extern void native_fn_021feeb4(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_021f949c(void);
extern void native_fn_022008c8(void);
extern void native_fn_02201438(void);


asm u32 native_ov001_021fff38 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #8
    bl native_fn_0202a634
    ldr r1, =0x02239c10
    mov r8, r0
    ldrsb r0, [r1, #12]
    mov r6, #0
    bl ov001_table_f0_entry_02202360
    mov r4, r0
    ldrb r5, [r4, #0x14]
    bl native_fn_02049618
    mov r7, r0
    bl native_fn_02203418
    cmp r0, #0
    beq ov001_021fff38_L48
    bl native_fn_022011c0
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov001_021fff38_L48:
    cmp r7, #0
    beq ov001_021fff38_L18c
    ble ov001_021fff38_Ld8
    cmp r5, #0
    bne ov001_021fff38_Lb0
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #7]
    cmp r0, #0
    mov r0, #1
    str r0, [sp]
    beq ov001_021fff38_L94
    str r0, [sp, #0x4]
    ldrsb r2, [r4, #8]
    ldrb r3, [r4, #0x9]
    mov r0, r4
    mov r1, r6
    bl native_fn_022029a8
    strb r0, [r4, #0x8]
    b ov001_021fff38_L158
ov001_021fff38_L94:
    ldrsb r2, [r4, #8]
    ldrb r3, [r4, #0x9]
    mov r0, r4
    mov r1, r6
    bl native_fn_022028fc
    strb r0, [r4, #0x8]
    b ov001_021fff38_L158
ov001_021fff38_Lb0:
    mov r1, #1
    str r1, [sp]
    mov r0, r6
    str r0, [sp, #0x4]
    ldrsb r2, [r4, #10]
    ldrb r3, [r4, #0xb]
    mov r0, r4
    bl native_fn_022029a8
    strb r0, [r4, #0xa]
    b ov001_021fff38_L158
ov001_021fff38_Ld8:
    cmp r5, #0
    bne ov001_021fff38_L134
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #7]
    cmp r0, #0
    mov r0, #1
    str r0, [sp]
    beq ov001_021fff38_L118
    str r0, [sp, #0x4]
    ldrsb r2, [r4, #8]
    ldrb r3, [r4, #0x9]
    mov r0, r4
    mov r1, r6
    bl native_fn_02202a68
    strb r0, [r4, #0x8]
    b ov001_021fff38_L158
ov001_021fff38_L118:
    ldrsb r2, [r4, #8]
    ldrb r3, [r4, #0x9]
    mov r0, r4
    mov r1, r6
    bl native_fn_0220294c
    strb r0, [r4, #0x8]
    b ov001_021fff38_L158
ov001_021fff38_L134:
    mov r1, #1
    str r1, [sp]
    mov r0, r6
    str r0, [sp, #0x4]
    ldrsb r2, [r4, #10]
    ldrb r3, [r4, #0xb]
    mov r0, r4
    bl native_fn_02202a68
    strb r0, [r4, #0xa]
ov001_021fff38_L158:
    mov r0, #133
    bl native_fn_022023c4
    cmp r5, #0
    ldreqsb r2, [r4, #8]
    ldrb r1, [r4, #0x14]
    add r0, r4, #168
    ldrnesb r2, [r4, #10]
    bl native_fn_02204470
    bl native_fn_021feeb4
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    b ov001_021fff38_L1f8
ov001_021fff38_L18c:
    ldrh r1, [r8, #2]
    tst r1, #2
    beq ov001_021fff38_L1b0
    bl native_fn_022011c0
    mov r6, r0
    mov r0, #83
    mov r1, #1
    bl native_fn_021f949c
    b ov001_021fff38_L1f8
ov001_021fff38_L1b0:
    ldr r0, =0x00000201
    tst r1, r0
    beq ov001_021fff38_L1f4
    cmp r5, #0
    ldreqsb r0, [r4, #8]
    ldrnesb r0, [r4, #10]
    bl native_fn_022008c8
    mov r6, r0
    cmp r6, #1
    mov r1, #1
    bne ov001_021fff38_L1e8
    mov r0, #82
    bl native_fn_021f949c
    b ov001_021fff38_L1f8
ov001_021fff38_L1e8:
    mov r0, #84
    bl native_fn_021f949c
    b ov001_021fff38_L1f8
ov001_021fff38_L1f4:
    bl native_fn_02201438
ov001_021fff38_L1f8:
    mov r0, r6
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
