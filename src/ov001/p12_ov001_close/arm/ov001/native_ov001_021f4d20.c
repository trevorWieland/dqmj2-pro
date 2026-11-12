/* ov001 row 0x021f4d20: 644 bytes.
 *
 * What it does: 160 instructions; 16 call(s) to 0x0207afec, 0x0207afec, 0x0207afec, +13 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 16 calls (160 instructions, 16 calls, 12 branches, 14 back edges, 1 literal slot).
 *
 *   pool +0x280 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x18 -> +0x7c
 *   branch +0x88 -> +0xf8
 *   back edge +0xb4 -> +0x90
 *   branch +0x104 -> +0x154
 *   branch +0x11c -> +0x154
 *   branch +0x140 -> +0x154
 *   branch +0x160 -> +0x180
 *   branch +0x18c -> +0x1a8
 *   branch +0x1b4 -> +0x1d8
 *   branch +0x1e4 -> +0x278
 *   branch +0x1f0 -> +0x230
 *   branch +0x204 -> +0x230
 *   branch +0x23c -> +0x248
 *   branch +0x264 -> +0x278
 *   test +0x10 cmp r1, #0
 *   test +0x84 cmp r0, #10
 *   test +0xb0 cmp r0, #0
 *   test +0x100 cmp r1, #20
 *   test +0x118 cmp r1, #10
 *   test +0x134 cmp r2, r1
 *   test +0x15c cmp r1, #30
 *   test +0x170 cmp r1, #20
 *   test +0x188 cmp r0, #40
 *   test +0x1b0 cmp r1, #50
 *   test +0x1c8 cmp r0, #0
 *   test +0x1e0 cmp r1, #100
 *   test +0x1ec cmp r1, #0
 *   test +0x200 cmp r0, #0
 *   test +0x238 cmp r1, #0
 *   test +0x258 cmp r1, #0
 *   0 block transfer(s), 22 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f4d20; the literal pool and
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
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f47b8(void);
extern void native_fn_0220f868(void);
extern void native_fn_021f2230(void);
extern void native_fn_0207b004(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021e2278(void);
extern void native_fn_021f4210(void);


asm u32 native_ov001_021f4d20 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x4]
    ldr r2, [r0, #0x84]
    cmp r1, #0
    ldrb r5, [r2, #0x31e]
    bne ov001_021f4d20_L7c
    ldrh r0, [r0, #80]
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    mov r4, r0
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    mov r6, r0
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldrsh r1, [r6, #26]
    ldrsh r0, [r0, #24]
    sub r0, r1, r0
    add r0, r0, #1
    bl native_fn_0203d294
    ldrsh r3, [r4, #24]
    ldr r1, =0x0223989c
    mov r2, #0
    add r0, r3, r0
    strb r0, [r1, #0x4b]
    strb r2, [r1, #0x4a]
    strb r2, [r1, #0x49]
    mov r0, #10
    strb r0, [r1, #0x4]
ov001_021f4d20_L7c:
    ldr r6, =0x0223989c
    ldrb r0, [r6, #0x4]
    cmp r0, #10
    bne ov001_021f4d20_Lf8
    mov r7, #3
ov001_021f4d20_L90:
    mov r0, r7
    bl native_fn_0203d294
    ldr r2, [r6, #0x84]
    mov r1, r0
    ldrb r0, [r2, #0x31e]
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f4d20_L90
    ldr r0, =0x0223989c
    mov r1, r4
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x84]
    bl native_fn_021f47b8
    ldr r1, =0x0223989c
    mov r3, #20
    ldrb r6, [r1, #0x49]
    mov r2, #0
    orr r0, r6, r0
    strb r0, [r1, #0x49]
    ldrb r0, [r4, #0x357]
    add r0, r0, #1
    strb r0, [r4, #0x357]
    strb r3, [r1, #0x4]
    strb r2, [r1, #0x1]
ov001_021f4d20_Lf8:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x4]
    cmp r1, #20
    bne ov001_021f4d20_L154
    ldrb r1, [r0, #0x1]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0x1]
    cmp r1, #10
    bls ov001_021f4d20_L154
    ldrb r1, [r0, #0x4a]
    add r2, r1, #1
    strb r2, [r0, #0x4a]
    ldrb r1, [r0, #0x4b]
    and r2, r2, #255
    cmp r2, r1
    movlo r1, #10
    strlob r1, [r0, #0x4]
    blo ov001_021f4d20_L154
    mov r1, #30
    strb r1, [r0, #0x4]
    mov r1, #0
    strb r1, [r0, #0x1]
ov001_021f4d20_L154:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x4]
    cmp r1, #30
    bne ov001_021f4d20_L180
    ldrb r1, [r0, #0x1]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #20
    strb r2, [r0, #0x1]
    movhi r1, #40
    strhib r1, [r0, #0x4]
ov001_021f4d20_L180:
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x4]
    cmp r0, #40
    bne ov001_021f4d20_L1a8
    mov r0, r5
    bl native_fn_0220f868
    ldr r1, =0x0223989c
    mov r2, #50
    strb r0, [r1, #0x4c]
    strb r2, [r1, #0x4]
ov001_021f4d20_L1a8:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x4]
    cmp r1, #50
    bne ov001_021f4d20_L1d8
    ldrb r1, [r0, #0x4c]
    mov r2, r5
    mov r0, #0
    bl native_fn_021f2230
    cmp r0, #0
    ldrne r0, =0x0223989c
    movne r1, #100
    strneb r1, [r0, #0x4]
ov001_021f4d20_L1d8:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x4]
    cmp r1, #100
    bne ov001_021f4d20_L278
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    bne ov001_021f4d20_L230
    ldrh r0, [r0, #80]
    mov r1, #536870912
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f4d20_L230
    ldr r0, =0x0223989c
    mov r1, #8
    ldr r0, [r0, #0x84]
    mov r2, #0
    str r2, [sp]
    add r2, r0, #512
    ldrsb r2, [r2, #52]
    sub r3, r1, #9
    rsb r2, r2, #0
    bl native_fn_021dbf98
ov001_021f4d20_L230:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x49]
    cmp r1, #0
    beq ov001_021f4d20_L248
    ldr r0, [r0, #0x84]
    bl native_fn_021e2278
ov001_021f4d20_L248:
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x4]
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    moveq r1, #27
    streqb r1, [r0, #0x1b]
    beq ov001_021f4d20_L278
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
    strb r1, [r0, #0x1b]
ov001_021f4d20_L278:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
