/* ov001 row 0x021f69a0: 844 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x33c -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x340 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x344 -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x348 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x40 -> +0x58
 *   branch +0x70 -> +0x2dc
 *   branch +0x88 -> +0x2cc
 *   branch +0x100 -> +0x114
 *   branch +0x168 -> +0x270
 *   branch +0x174 -> +0x254
 *   branch +0x188 -> +0x1f0
 *   branch +0x194 -> +0x1a8
 *   branch +0x1a4 -> +0x1c0
 *   branch +0x1ec -> +0x208
 *   branch +0x250 -> +0x270
 *   branch +0x278 -> +0x2a8
 *   branch +0x2a4 -> +0x2cc
 *   branch +0x2b0 -> +0x2cc
 *   back edge +0x2d8 -> +0x7c
 *   branch +0x2e8 -> +0x2f8
 *   branch +0x2f4 -> +0x300
 *   test +0x18 cmp r0, #0
 *   test +0x34 cmp r1, #0
 *   test +0x6c cmp r11, #0
 *   test +0x84 cmp r0, #0
 *   test +0xe8 cmp r9, r0
 *   test +0xfc cmp r0, #0
 *   test +0x108 cmp r0, #1
 *   test +0x164 cmp r0, #0
 *   test +0x170 cmp r0, #0
 *   test +0x180 cmp r0, #0
 *   test +0x190 cmp r1, #1
 *   test +0x274 cmp r0, #0
 *   test +0x2ac cmp r0, #0
 *   test +0x2d4 cmp r10, r11
 *   test +0x2e4 cmp r0, #0
 *   test +0x304 cmp r0, #0
 *   27 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f69a0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f2304(void);
extern void native_fn_0203d294(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02026144(void);
extern void native_fn_020655d8(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021f0eb4(void);
extern void native_fn_021db788(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f2464(void);
extern void native_fn_0220f600(void);
extern void native_fn_022024d4(void);
extern void native_fn_021ee7b0(void);
extern void native_fn_021f949c(void);


asm u32 native_ov001_021f69a0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #64
    ldr r1, =0x0223989c
    mov r6, r0
    ldr r0, [r1, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r0, #1
    streq r0, [sp, #0x1c]
    movne r0, #0
    strne r0, [sp, #0x1c]
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    ldrne r5, [r0, #0x80]
    movne r11, #1
    bne ov001_021f69a0_L58
    ldr r0, [sp, #0x1c]
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r5, r0
    mov r11, #3
ov001_021f69a0_L58:
    mov r0, #0
    str r0, [sp, #0x24]
    str r0, [sp, #0x20]
    mov r10, r0
    str r0, [r6]
    cmp r11, #0
    ble ov001_021f69a0_L2dc
    ldr r7, =0x0223989c
    mvn r8, #0
ov001_021f69a0_L7c:
    mov r0, r5
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f69a0_L2cc
    ldrh r1, [r7, #80]
    ldrb r2, [r7, #0x10]
    mov r0, r5
    bl native_fn_021f2304
    mov r1, r0
    ldr r0, [sp, #0x1c]
    bl ov001_side_slot_record_021db438
    mov r4, r0
    mov r0, #100
    bl native_fn_0203d294
    mov r9, r0
    ldr r0, [r4, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    ldr r12, [r7, #0x5c]
    ldr r2, =0x88888889
    mov r1, r0
    smull r3, r0, r2, r12
    add r0, r12, r0
    mov r2, r12, lsr #31
    add r0, r2, r0, asr #4
    add r0, r0, #25
    bl native_fn_02026144
    cmp r9, r0
    movlt r0, #1
    movge r0, #0
    str r0, [sp, #0x3c]
    bl native_fn_020655d8
    cmp r0, #0
    beq ov001_021f69a0_L114
    ldrb r0, [r4, #0x31e]
    cmp r0, #1
    moveq r0, #0
    streq r0, [sp, #0x3c]
ov001_021f69a0_L114:
    add r0, sp, #60
    str r0, [sp]
    add r0, sp, #40
    str r0, [sp, #0x4]
    add r0, sp, #52
    str r0, [sp, #0x8]
    add r0, r4, #844
    str r0, [sp, #0xc]
    add r0, sp, #48
    str r0, [sp, #0x10]
    add r0, sp, #56
    str r0, [sp, #0x14]
    add r0, sp, #44
    str r0, [sp, #0x18]
    ldrb r3, [r7, #0x10]
    ldr r1, [r7, #0x84]
    mov r0, #46
    mov r2, r4
    bl native_fn_021e1a60
    ldr r0, [sp, #0x38]
    cmp r0, #0
    beq ov001_021f69a0_L270
    ldr r0, [sp, #0x3c]
    cmp r0, #0
    beq ov001_021f69a0_L254
    mov r0, #2
    bl native_fn_0203d294
    cmp r0, #0
    add r0, r4, #256
    bne ov001_021f69a0_L1f0
    ldrsh r1, [r0, #240]
    cmp r1, #1
    bne ov001_021f69a0_L1a8
    mov r0, #1
    str r0, [r6]
    mov r9, r0
    b ov001_021f69a0_L1c0
ov001_021f69a0_L1a8:
    mov r0, #99
    smulbb r2, r1, r0
    ldr r0, =0x51eb851f
    smull r1, r9, r0, r2
    mov r0, r2, lsr #31
    add r9, r0, r9, asr #5
ov001_021f69a0_L1c0:
    mov r0, #0
    str r0, [sp]
    ldrh r2, [r7, #80]
    mov r0, r4
    mov r1, r9
    mov r3, #1
    bl native_fn_021ee78c
    ldrh r2, [r7, #80]
    mov r0, r4
    mov r1, r9
    bl native_fn_021f0eb4
    b ov001_021f69a0_L208
ov001_021f69a0_L1f0:
    ldrsh r9, [r0, #240]
    mov r0, r4
    mov r1, #0
    bl native_fn_021db788
    mov r0, #1
    str r0, [r6]
ov001_021f69a0_L208:
    mov r0, r4
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
    ldrh r0, [r7, #80]
    bl native_fn_021f2464
    str r0, [sp]
    ldrh r2, [r7, #80]
    ldr r0, [r7, #0x84]
    mov r1, r4
    mov r3, #0
    bl native_fn_0220f600
    ldrb r0, [r4, #0x31e]
    ldrb r1, [r4, #0x31f]
    mov r2, r9
    bl native_fn_022024d4
    mov r0, #1
    str r0, [sp, #0x24]
    b ov001_021f69a0_L270
ov001_021f69a0_L254:
    mov r0, #0
    str r0, [sp]
    mov r0, r4
    mov r1, #0
    mov r2, r8
    mov r3, #1
    bl native_fn_021ee7b0
ov001_021f69a0_L270:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    beq ov001_021f69a0_L2a8
    ldrh r2, [sp, #40]
    add r1, r4, #768
    mov r0, #1
    strh r2, [r1, #74]
    ldrsb r1, [r7, #43]
    str r0, [sp, #0x20]
    add r0, r1, #1
    strb r0, [r7, #0x2b]
    ldr r0, =0x022399b8
    str r4, [r0, r1, lsl #2]
    b ov001_021f69a0_L2cc
ov001_021f69a0_L2a8:
    ldr r0, [sp, #0x38]
    cmp r0, #0
    bne ov001_021f69a0_L2cc
    mov r1, #0
    mov r0, r4
    mov r2, r8
    mov r3, #1
    str r1, [sp]
    bl native_fn_021ee7b0
ov001_021f69a0_L2cc:
    add r5, r5, #1088
    add r10, r10, #1
    cmp r10, r11
    blt ov001_021f69a0_L7c
ov001_021f69a0_L2dc:
    ldr r0, [sp, #0x24]
    mov r1, #1
    cmp r0, #0
    beq ov001_021f69a0_L2f8
    mov r0, #238
    bl native_fn_021f949c
    b ov001_021f69a0_L300
ov001_021f69a0_L2f8:
    mov r0, #242
    bl native_fn_021f949c
ov001_021f69a0_L300:
    ldr r0, [sp, #0x20]
    cmp r0, #0
    ldreq r0, =0x0223989c
    moveq r1, #0
    streqb r1, [r0, #0x10]
    addeq sp, sp, #64
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #243
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, =0x0223989c
    mov r1, #1
    strb r1, [r0, #0x10]
    add sp, sp, #64
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
