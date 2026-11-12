/* ov001 row 0x021f7d70: 828 bytes.
 *
 * What it does: 204 instructions; 24 call(s) to 0x0207afec, 0x0207afec, 0x0203d294, +21 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 24 calls (204 instructions, 24 calls, 20 branches, 19 back edges, 3 literal slots).
 *
 *   pool +0x330 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x334 -> constant 0x0223990c (image word 0x0223990c)
 *   pool +0x338 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x2c -> +0x88
 *   branch +0x84 -> +0x324
 *   branch +0x8c -> +0xf4
 *   branch +0xf0 -> +0x324
 *   branch +0xf8 -> +0x1fc
 *   branch +0x110 -> +0x324
 *   branch +0x120 -> +0x15c
 *   back edge +0x148 -> +0x128
 *   branch +0x158 -> +0x324
 *   branch +0x164 -> +0x1dc
 *   branch +0x184 -> +0x1e4
 *   branch +0x19c -> +0x1c8
 *   branch +0x1b0 -> +0x1c8
 *   back edge +0x1d4 -> +0x194
 *   branch +0x1d8 -> +0x1e4
 *   branch +0x1f8 -> +0x324
 *   branch +0x200 -> +0x238
 *   branch +0x218 -> +0x324
 *   branch +0x234 -> +0x324
 *   branch +0x23c -> +0x268
 *   branch +0x254 -> +0x324
 *   branch +0x264 -> +0x324
 *   branch +0x26c -> +0x324
 *   branch +0x278 -> +0x2b8
 *   branch +0x28c -> +0x2b8
 *   branch +0x2f0 -> +0x2fc
 *   back edge +0x308 -> +0x2dc
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, #0
 *   test +0x88 cmp r0, #5
 *   test +0x94 cmp r2, #0
 *   test +0xf4 cmp r0, #10
 *   test +0x10c cmp r0, #10
 *   test +0x11c cmp r1, r0
 *   test +0x144 cmp r0, #0
 *   test +0x160 cmp r1, #0
 *   test +0x198 cmp r0, #0
 *   test +0x1ac cmp r1, #0
 *   test +0x1d0 cmp r8, r0
 *   test +0x1fc cmp r0, #20
 *   test +0x214 cmp r0, #20
 *   test +0x238 cmp r0, #30
 *   test +0x250 cmp r0, #0
 *   test +0x268 cmp r0, #100
 *   test +0x274 cmp r0, #0
 *   test +0x288 cmp r0, #0
 *   test +0x2ec cmp r0, #0
 *   test +0x300 cmp r5, #3
 *   0 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f7d70; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_0203d294(void);
extern void native_fn_021f2304(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_021f39cc(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f2120(void);
extern void native_fn_0220f868(void);
extern void native_fn_021f2230(void);
extern void native_fn_0207b004(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021e2444(void);


asm u32 native_ov001_021f7d70 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #16
    ldr r0, =0x0223989c
    ldr r9, =0x0223989c
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    ldrb r0, [r9, #0x2f]
    moveq r4, #1
    movne r4, #0
    cmp r0, #0
    bne ov001_021f7d70_L88
    ldrh r0, [r9, #80]
    bl native_fn_0207afec
    mov r1, r9
    mov r4, r0
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldrsh r1, [r4, #26]
    ldrsh r0, [r0, #24]
    sub r0, r1, r0
    add r0, r0, #1
    bl native_fn_0203d294
    mov r1, r9
    mov r4, r0
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldrsh r2, [r0, #24]
    mov r0, r9
    mov r1, #5
    add r2, r4, r2
    strb r2, [r0, #0x14]
    strb r1, [r0, #0x2f]
    b ov001_021f7d70_L324
ov001_021f7d70_L88:
    cmp r0, #5
    bne ov001_021f7d70_Lf4
    ldrb r2, [r9, #0x10]
    cmp r2, #0
    ldreqb r0, [r9, #0x7]
    addeq r0, r0, #1
    ldrneb r0, [r9, #0x14]
    strb r0, [r9, #0x7]
    ldr r0, =0x0223989c
    ldrh r1, [r0, #80]
    ldr r0, [r0, #0x80]
    bl native_fn_021f2304
    mov r1, r0
    mov r0, r4
    bl ov001_side_slot_record_021db438
    ldr r3, =0x0223989c
    mov r1, r0
    ldrh r2, [r3, #80]
    ldr r0, [r3, #0x84]
    ldr r3, =0x0223990c
    bl native_fn_021f39cc
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x2f]
    mov r1, #0
    strb r1, [r0, #0x2d]
    b ov001_021f7d70_L324
ov001_021f7d70_Lf4:
    cmp r0, #10
    bne ov001_021f7d70_L1fc
    ldrb r0, [r9, #0x2d]
    add r1, r0, #1
    and r0, r1, #255
    strb r1, [r9, #0x2d]
    cmp r0, #10
    blo ov001_021f7d70_L324
    ldrb r1, [r9, #0x7]
    ldrb r0, [r9, #0x14]
    cmp r1, r0
    bhs ov001_021f7d70_L15c
    mov r5, #3
ov001_021f7d70_L128:
    mov r0, r5
    bl native_fn_0203d294
    mov r1, r0
    mov r0, r4
    bl ov001_side_slot_record_021db438
    str r0, [r9, #0x80]
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f7d70_L128
    ldr r0, =0x0223989c
    mov r1, #5
    strb r1, [r0, #0x2f]
    b ov001_021f7d70_L324
ov001_021f7d70_L15c:
    ldrsb r1, [r9, #43]
    cmp r1, #0
    ble ov001_021f7d70_L1dc
    add r7, sp, #4
    mov r8, #0
    str r8, [r7]
    str r8, [r7, #0x4]
    str r8, [r7, #0x8]
    mov r0, #1
    strb r0, [r9, #0x10]
    ble ov001_021f7d70_L1e4
    ldr r6, =0x022399b8
    mov r5, #176
    mov r4, r0
ov001_021f7d70_L194:
    ldr r0, [r9, #0x70]
    cmp r0, #0
    beq ov001_021f7d70_L1c8
    ldr r0, [r6, r8, lsl #2]
    ldrb r1, [r0, #0x31f]
    ldr r1, [r7, r1, lsl #2]
    cmp r1, #0
    bne ov001_021f7d70_L1c8
    mov r1, r5
    bl native_fn_021f2120
    ldr r0, [r6, r8, lsl #2]
    ldrb r0, [r0, #0x31f]
    str r4, [r7, r0, lsl #2]
ov001_021f7d70_L1c8:
    ldrsb r0, [r9, #43]
    add r8, r8, #1
    cmp r8, r0
    blt ov001_021f7d70_L194
    b ov001_021f7d70_L1e4
ov001_021f7d70_L1dc:
    mov r0, #0
    strb r0, [r9, #0x10]
ov001_021f7d70_L1e4:
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x2f]
    mov r1, #0
    strb r1, [r0, #0x2d]
    b ov001_021f7d70_L324
ov001_021f7d70_L1fc:
    cmp r0, #20
    bne ov001_021f7d70_L238
    ldrb r0, [r9, #0x2d]
    add r1, r0, #1
    and r0, r1, #255
    strb r1, [r9, #0x2d]
    cmp r0, #20
    blo ov001_021f7d70_L324
    mov r0, r4
    bl native_fn_0220f868
    mov r1, r9
    mov r2, #30
    strb r0, [r1, #0x2c]
    strb r2, [r1, #0x2f]
    b ov001_021f7d70_L324
ov001_021f7d70_L238:
    cmp r0, #30
    bne ov001_021f7d70_L268
    ldrb r1, [r9, #0x2c]
    mov r2, r4
    mov r0, #0
    bl native_fn_021f2230
    cmp r0, #0
    beq ov001_021f7d70_L324
    mov r0, r9
    mov r1, #100
    strb r1, [r0, #0x2f]
    b ov001_021f7d70_L324
ov001_021f7d70_L268:
    cmp r0, #100
    bne ov001_021f7d70_L324
    ldrb r0, [r9, #0x10]
    cmp r0, #0
    bne ov001_021f7d70_L2b8
    ldrh r0, [r9, #80]
    mov r1, #536870912
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f7d70_L2b8
    mov r0, r9
    ldr r0, [r0, #0x84]
    mov r2, #0
    str r2, [sp]
    add r2, r0, #512
    ldrsb r2, [r2, #52]
    mov r1, #8
    sub r3, r1, #9
    rsb r2, r2, #0
    bl native_fn_021dbf98
ov001_021f7d70_L2b8:
    ldr r2, =0x0223989c
    mov r0, r4
    ldr r3, [r2, #0x70]
    mov r1, #0
    strb r3, [r2, #0x10]
    bl ov001_side_slot_record_021db438
    ldr r4, =0x0223989c
    mov r6, r0
    mov r5, #0
ov001_021f7d70_L2dc:
    ldr r0, [r4, #0x84]
    add r0, r0, r5, lsl #1
    add r0, r0, #768
    ldrsh r0, [r0, #78]
    cmp r0, #0
    ble ov001_021f7d70_L2fc
    mov r0, r6
    bl native_fn_021e2444
ov001_021f7d70_L2fc:
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_021f7d70_L2dc
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x2f]
    strb r1, [r0, #0x7]
    mov r1, #14
    strb r1, [r0, #0x1b]
ov001_021f7d70_L324:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
