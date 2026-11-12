/* ov001 row 0x02206c90: 800 bytes.
 *
 * What it does: 198 instructions; 27 call(s) to 0x022068a0, 0x0202a634, 0x0206d250, +24 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 27 calls (198 instructions, 27 calls, 20 branches, 21 back edges, 2 literal slots).
 *
 *   pool +0x318 -> native_data_0222f028 (image word 0x0222f028)
 *   pool +0x31c -> constant 0x00000ff7 (image word 0x00000ff7)
 *   branch +0x30 -> +0x308
 *   branch +0x34 -> +0x308
 *   branch +0x38 -> +0x54
 *   branch +0x3c -> +0x6c
 *   branch +0x40 -> +0x17c
 *   branch +0x44 -> +0x1f4
 *   branch +0x48 -> +0x28c
 *   branch +0x4c -> +0x2f4
 *   branch +0x50 -> +0x308
 *   branch +0x68 -> +0x308
 *   branch +0x1c0 -> +0x1dc
 *   branch +0x1d8 -> +0x308
 *   branch +0x1f0 -> +0x308
 *   branch +0x200 -> +0x308
 *   branch +0x210 -> +0x234
 *   branch +0x230 -> +0x280
 *   branch +0x258 -> +0x280
 *   branch +0x288 -> +0x308
 *   branch +0x298 -> +0x308
 *   branch +0x2c0 -> +0x2e8
 *   branch +0x2f0 -> +0x308
 *   test +0x28 cmp r1, #7
 *   test +0x5c cmp r1, r0
 *   test +0x1bc cmp r0, r1
 *   test +0x1d0 cmp r0, r1
 *   test +0x1fc tst r1, r0
 *   test +0x20c cmp r1, #0
 *   test +0x24c cmp r1, r0
 *   test +0x294 tst r1, r0
 *   test +0x2b4 cmp r1, r0
 *   test +0x2fc tst r1, r0
 *   0 block transfer(s), 20 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02206c90; the literal pool and
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

extern void native_fn_022068a0(void);
extern void native_fn_0202a634(void);
extern u8 native_data_0222f028[];
extern void native_fn_0206d250(void);
extern void native_fn_021fe4ac(void);
extern void native_fn_02049ffc(void);
extern void native_fn_022068ac(void);
extern void native_fn_022116c0(void);
extern void native_fn_02204250(void);
extern void native_fn_02206858(void);
extern void native_fn_0205fa4c(void);
extern void native_fn_02202320(void);
extern void native_fn_021fe6b8(void);
extern void native_fn_0206006c(void);
extern void native_fn_02207610(void);
extern void native_fn_022077fc(void);
extern void native_fn_020630b0(void);
extern void native_fn_02207898(void);
extern void native_fn_02045efc(void);


asm u32 native_ov001_02206c90 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #20
    mov r4, r0
    bl native_fn_022068a0
    mov r6, r0
    add r0, r6, r4, lsl #5
    ldr r5, [r0, #0x24]
    bl native_fn_0202a634
    add r2, r6, r4, lsl #5
    ldr r1, [r2, #0x2c]
    cmp r1, #7
    addls pc, pc, r1, lsl #2
    b ov001_02206c90_L308
    b ov001_02206c90_L308
    b ov001_02206c90_L54
    b ov001_02206c90_L6c
    b ov001_02206c90_L17c
    b ov001_02206c90_L1f4
    b ov001_02206c90_L28c
    b ov001_02206c90_L2f4
    b ov001_02206c90_L308
ov001_02206c90_L54:
    ldrb r1, [r2, #0x31]
    ldrb r0, [r2, #0x30]
    cmp r1, r0
    movhi r0, #2
    strhi r0, [r2, #0x2c]
    b ov001_02206c90_L308
ov001_02206c90_L6c:
    ldr r2, [r2, #0x28]
    ldr r0, =native_data_0222f028
    ldrb r1, [r2, #0x5]
    ldrb r3, [r0, #0xa]
    ldrsb r0, [r2, #12]
    mov r1, r1, asr #3
    add r5, r6, #28
    add r2, r3, #9
    sub r1, r1, #1
    add r7, r5, r4, lsl #5
    and r8, r2, #255
    and r9, r1, #255
    bl native_fn_0206d250
    add r0, r0, r0, lsl #2
    ldr r1, =native_data_0222f028
    mov r0, r0, asr #1
    and r0, r0, #255
    add r0, r9, r0
    and r3, r0, #255
    ldrb r2, [r1, #0xb]
    mov r0, r4, lsl #1
    add r0, r0, #1
    add r2, r3, r2
    and r2, r2, #255
    str r2, [sp]
    ldrb r2, [r1, #0xc]
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    str r2, [sp, #0x4]
    ldrb r3, [r1, #0xd]
    mov r2, #0
    mov r1, #1
    str r3, [sp, #0x8]
    str r2, [sp, #0xc]
    str r1, [sp, #0x10]
    mov r3, r8
    mov r1, #8
    mov r2, #31
    bl native_fn_021fe4ac
    str r0, [r5, r4, lsl #5]
    ldr r2, [r0]
    mov r0, #6
    ldr r1, [r2, #0x4]
    strb r0, [r7, #0x4]
    ldrb r0, [r1, #0x5f]
    strb r0, [r7, #0x5]
    ldr r0, [r2, #0x4]
    bl native_fn_02049ffc
    add r1, r6, r4, lsl #5
    mov r2, #3
    mov r0, #82
    str r2, [r1, #0x2c]
    bl native_fn_022068ac
    add r0, r6, r4, lsl #5
    ldr r0, [r0, #0x24]
    add r0, r0, #768
    ldrsb r0, [r0, #31]
    bl native_fn_022116c0
    bl native_fn_02204250
    mov r5, r0
    ldrsb r0, [r5, #9]
    bl native_fn_02204250
    mov r1, #0
    bl native_fn_02206858
    ldrsb r0, [r5, #9]
    bl native_fn_02204250
    mov r1, #0
    bl native_fn_0205fa4c
ov001_02206c90_L17c:
    add r0, r6, #28
    ldr r1, [r0, r4, lsl #5]
    add r5, r0, r4, lsl #5
    ldrsb r0, [r1, #5]
    ldr r1, [r1]
    ldr r7, [r1, #0x4]
    bl native_fn_02202320
    bl native_fn_021fe6b8
    ldrsb r1, [r5, #5]
    str r1, [sp]
    ldrsb r1, [r7, #28]
    ldrsb r2, [r7, #29]
    ldrsb r3, [r5, #4]
    bl native_fn_0206006c
    ldrsb r1, [r7, #94]
    ldrsb r0, [r5, #4]
    cmp r0, r1
    bge ov001_02206c90_L1dc
    add r0, r0, #4
    strb r0, [r5, #0x4]
    ldrsb r0, [r5, #4]
    cmp r0, r1
    strgtb r1, [r5, #0x4]
    b ov001_02206c90_L308
ov001_02206c90_L1dc:
    mov r0, r4
    bl native_fn_02207610
    add r0, r6, r4, lsl #5
    mov r1, #4
    str r1, [r0, #0x2c]
    b ov001_02206c90_L308
ov001_02206c90_L1f4:
    ldrh r1, [r0, #2]
    ldr r0, =0x00000ff7
    tst r1, r0
    beq ov001_02206c90_L308
    add r0, r5, #512
    ldrsh r1, [r0, #26]
    cmp r1, #0
    ble ov001_02206c90_L234
    mov r0, r4
    bl native_fn_022077fc
    add r1, r6, r4, lsl #5
    mov r2, #5
    mov r0, #82
    str r2, [r1, #0x2c]
    bl native_fn_022068ac
    b ov001_02206c90_L280
ov001_02206c90_L234:
    ldr r0, [r2, #0x24]
    ldr r0, [r0, #0x1e8]
    ldrb r0, [r0, #0xab]
    bl native_fn_020630b0
    add r2, r6, r4, lsl #5
    ldrb r1, [r2, #0x31]
    cmp r1, r0
    movne r0, #7
    strne r0, [r2, #0x2c]
    bne ov001_02206c90_L280
    ldr r1, [r5, #0x1e8]
    mov r0, r4
    ldrsh r1, [r1, #42]
    bl native_fn_02207898
    add r1, r6, r4, lsl #5
    mov r2, #6
    mov r0, #82
    str r2, [r1, #0x2c]
    bl native_fn_022068ac
ov001_02206c90_L280:
    mov r0, #1
    bl native_fn_02045efc
    b ov001_02206c90_L308
ov001_02206c90_L28c:
    ldrh r1, [r0, #2]
    ldr r0, =0x00000ff7
    tst r1, r0
    beq ov001_02206c90_L308
    ldr r0, [r2, #0x24]
    ldr r0, [r0, #0x1e8]
    ldrb r0, [r0, #0xab]
    bl native_fn_020630b0
    add r2, r6, r4, lsl #5
    ldrb r1, [r2, #0x31]
    cmp r1, r0
    movne r0, #7
    strne r0, [r2, #0x2c]
    bne ov001_02206c90_L2e8
    ldr r1, [r5, #0x1e8]
    mov r0, r4
    ldrsh r1, [r1, #42]
    bl native_fn_02207898
    add r1, r6, r4, lsl #5
    mov r2, #6
    mov r0, #82
    str r2, [r1, #0x2c]
    bl native_fn_022068ac
ov001_02206c90_L2e8:
    mov r0, #1
    bl native_fn_02045efc
    b ov001_02206c90_L308
ov001_02206c90_L2f4:
    ldrh r1, [r0, #2]
    ldr r0, =0x00000ff7
    tst r1, r0
    movne r0, #7
    strne r0, [r2, #0x2c]
ov001_02206c90_L308:
    add r0, r6, r4, lsl #5
    ldr r0, [r0, #0x2c]
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
