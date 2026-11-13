/* ov001 row 0x021f43bc: 1020 bytes.
 *
 * What it does: 249 instructions; 25 call(s) to 0x0207afec, 0x021f39cc, 0x0202ac08, +22 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill (249 instructions, 25 calls, 23 branches, 23 back edges, 6 literal slots).
 *
 *   pool +0x3e4 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x3e8 -> constant 0x02239910 (image word 0x02239910)
 *   pool +0x3ec -> constant 0x0223992c (image word 0x0223992c)
 *   pool +0x3f0 -> constant 0x00000119 (image word 0x00000119)
 *   pool +0x3f4 -> constant 0x0000010d (image word 0x0000010d)
 *   pool +0x3f8 -> constant 0x80002000 (image word 0x80002000)
 *   branch +0x3c -> +0x4c
 *   branch +0x48 -> +0x68
 *   branch +0x64 -> +0x6c
 *   branch +0x78 -> +0x8c
 *   branch +0x98 -> +0x1d8
 *   branch +0xc4 -> +0x148
 *   branch +0xdc -> +0x110
 *   branch +0x124 -> +0x148
 *   branch +0x134 -> +0x148
 *   branch +0x16c -> +0x1d0
 *   branch +0x1b0 -> +0x1bc
 *   back edge +0x1c8 -> +0x19c
 *   branch +0x1cc -> +0x1d8
 *   branch +0x1e4 -> +0x204
 *   branch +0x210 -> +0x230
 *   branch +0x23c -> +0x25c
 *   branch +0x268 -> +0x284
 *   branch +0x290 -> +0x2b4
 *   branch +0x2c0 -> +0x3d8
 *   branch +0x2f0 -> +0x3d0
 *   branch +0x304 -> +0x3d0
 *   branch +0x310 -> +0x3c8
 *   branch +0x344 -> +0x3a4
 *   branch +0x394 -> +0x3a4
 *   back edge +0x3b0 -> +0x338
 *   branch +0x3c4 -> +0x3d0
 *   test +0x14 cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   test +0x74 cmp r1, #0
 *   test +0x94 cmp r1, #5
 *   test +0xc0 cmp r0, #0
 *   test +0xd8 cmp r0, #0
 *   test +0x120 cmp r0, #0
 *   test +0x130 cmp r1, #0
 *   test +0x168 cmp r6, #0
 *   test +0x170 cmp r4, #0
 *   test +0x1ac cmp r0, #0
 *   test +0x1c0 cmp r4, #3
 *   test +0x1e0 cmp r1, #7
 *   test +0x1f4 cmp r1, #15
 *   test +0x20c cmp r1, #10
 *   test +0x220 cmp r0, #0
 *   test +0x238 cmp r1, #15
 *   test +0x24c cmp r1, #40
 *   test +0x264 cmp r0, #40
 *   test +0x28c cmp r1, #50
 *   test +0x2a4 cmp r0, #0
 *   test +0x2bc cmp r0, #100
 *   test +0x2e4 tst r2, #16777216
 *   test +0x2f8 cmp r2, #0
 *   test +0x30c cmp r2, #0
 *   test +0x340 cmp r0, #0
 *   test +0x390 cmp r0, r11
 *   test +0x3a8 cmp r10, #3
 *   1 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f43bc; the literal pool and
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
extern void native_fn_021f39cc(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021f2120(void);
extern void native_fn_0207b02c(void);
extern void native_fn_021f2408(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_021e2444(void);
extern void native_fn_021f433c(void);
extern void native_fn_0220f868(void);
extern void native_fn_021f2230(void);
extern void native_fn_021f42b8(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f2304(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021dc940(void);
extern void native_fn_021f4210(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021f43bc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #32
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    ldr r0, =0x0223989c
    moveq r7, #1
    ldrh r0, [r0, #80]
    movne r7, #0
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    mov r5, r0
    ldrb r0, [r1, #0x10]
    cmp r0, #0
    beq ov001_021f43bc_L4c
    ldrb r0, [r1, #0x13]
    cmp r0, #0
    beq ov001_021f43bc_L68
ov001_021f43bc_L4c:
    ldrh r0, [r5, #8]
    mov r0, r0, lsl #16
    movs r0, r0, lsr #28
    ldreq r0, =0x0223989c
    ldreq r8, [r0, #0x80]
    movne r8, #0
    b ov001_021f43bc_L6c
ov001_021f43bc_L68:
    ldr r8, [r1, #0x80]
ov001_021f43bc_L6c:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x16]
    cmp r1, #0
    bne ov001_021f43bc_L8c
    mov r1, #0
    strb r1, [r0, #0x1a]
    mov r1, #5
    strb r1, [r0, #0x16]
ov001_021f43bc_L8c:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x16]
    cmp r1, #5
    bne ov001_021f43bc_L1d8
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x84]
    ldr r3, =0x02239910
    mov r1, r8
    mov r6, #0
    bl native_fn_021f39cc
    ldr r1, =0x0223989c
    mov r4, r0
    ldrb r0, [r1, #0x1a]
    cmp r0, #0
    bne ov001_021f43bc_L148
    ldr r0, =0x0223992c
    bl native_fn_0202ac08
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x74]
    cmp r0, #0
    beq ov001_021f43bc_L110
    mov r0, r8
    mov r1, #176
    bl native_fn_021f2120
    mov r0, r8
    mov r1, #249
    bl native_fn_021f2120
    ldr r1, =0x00000119
    mov r0, r8
    bl native_fn_021f2120
    ldr r1, =0x0000010d
    mov r0, r8
    bl native_fn_021f2120
ov001_021f43bc_L110:
    ldr r0, =0x0223989c
    ldr r1, =0x80002000
    ldrh r0, [r0, #80]
    bl native_fn_0207b02c
    cmp r0, #0
    beq ov001_021f43bc_L148
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    bne ov001_021f43bc_L148
    ldrb r1, [r0, #0x1a]
    mov r6, #1
    add r1, r1, #1
    strb r1, [r0, #0x1a]
ov001_021f43bc_L148:
    ldr r1, =0x0223989c
    mov r0, r8
    ldrh r2, [r1, #80]
    mov r1, r7
    bl native_fn_021f2408
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0xa]
    cmp r6, #0
    bne ov001_021f43bc_L1d0
    cmp r4, #0
    movne r3, #10
    ldr r2, =0x0223989c
    moveq r3, #15
    mov r0, r7
    mov r1, #0
    strb r3, [r2, #0x16]
    bl ov001_side_slot_record_021db438
    ldr r9, =0x0223989c
    mov r6, r0
    mov r4, #0
ov001_021f43bc_L19c:
    ldr r0, [r9, #0x84]
    add r0, r0, r4, lsl #1
    add r0, r0, #768
    ldrsh r0, [r0, #78]
    cmp r0, #0
    ble ov001_021f43bc_L1bc
    mov r0, r6
    bl native_fn_021e2444
ov001_021f43bc_L1bc:
    add r4, r4, #1
    cmp r4, #3
    add r6, r6, #1088
    blt ov001_021f43bc_L19c
    b ov001_021f43bc_L1d8
ov001_021f43bc_L1d0:
    mov r1, #7
    strb r1, [r0, #0x16]
ov001_021f43bc_L1d8:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x16]
    cmp r1, #7
    bne ov001_021f43bc_L204
    ldrb r1, [r0, #0xa]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #15
    strb r2, [r0, #0xa]
    movhi r1, #5
    strhib r1, [r0, #0x16]
ov001_021f43bc_L204:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x16]
    cmp r1, #10
    bne ov001_021f43bc_L230
    ldr r0, [r0, #0x84]
    mov r1, r8
    bl native_fn_021f433c
    cmp r0, #0
    ldrne r0, =0x0223989c
    movne r1, #40
    strneb r1, [r0, #0x16]
ov001_021f43bc_L230:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x16]
    cmp r1, #15
    bne ov001_021f43bc_L25c
    ldrb r1, [r0, #0xa]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #40
    strb r2, [r0, #0xa]
    movhi r1, #40
    strhib r1, [r0, #0x16]
ov001_021f43bc_L25c:
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x16]
    cmp r0, #40
    bne ov001_021f43bc_L284
    mov r0, r7
    bl native_fn_0220f868
    ldr r1, =0x0223989c
    mov r2, #50
    strb r0, [r1, #0x36]
    strb r2, [r1, #0x16]
ov001_021f43bc_L284:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x16]
    cmp r1, #50
    bne ov001_021f43bc_L2b4
    ldrb r1, [r0, #0x36]
    mov r0, r8
    mov r2, r7
    bl native_fn_021f2230
    cmp r0, #0
    ldrne r0, =0x0223989c
    movne r1, #100
    strneb r1, [r0, #0x16]
ov001_021f43bc_L2b4:
    ldr r1, =0x0223989c
    ldrb r0, [r1, #0x16]
    cmp r0, #100
    bne ov001_021f43bc_L3d8
    ldr r2, [r1, #0x74]
    mov r0, r8
    strb r2, [r1, #0x10]
    bl native_fn_021f42b8
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x16]
    ldr r2, [r5]
    tst r2, #16777216
    movne r1, #14
    strneb r1, [r0, #0x1b]
    bne ov001_021f43bc_L3d0
    ldrb r2, [r5, #0x21]
    cmp r2, #0
    movne r1, #15
    strneb r1, [r0, #0x1b]
    bne ov001_021f43bc_L3d0
    ldrb r2, [r0, #0x10]
    cmp r2, #0
    beq ov001_021f43bc_L3c8
    ldrb r0, [r0, #0x11]
    bl ov001_side_slot_record_021db438
    mov r9, r0
    mov r10, #0
    ldr r4, =0x0223989c
    ldr r11, =0x00000119
    mov r7, r9
    mov r6, r10
    add r5, sp, #28
ov001_021f43bc_L338:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f43bc_L3a4
    ldrh r1, [r4, #80]
    mov r0, r7
    mov r2, #0
    bl native_fn_021f2304
    str r6, [sp]
    stmib sp, {r5, r6}
    str r6, [sp, #0xc]
    str r6, [sp, #0x10]
    str r6, [sp, #0x14]
    str r6, [sp, #0x18]
    add r0, r0, r0, lsl #4
    add r8, r9, r0, lsl #6
    ldrh r0, [r4, #80]
    ldr r1, [r4, #0x84]
    mov r2, r8
    mov r3, r6
    bl native_fn_021e1a60
    ldrh r0, [sp, #28]
    cmp r0, r11
    bne ov001_021f43bc_L3a4
    mov r0, r8
    mov r1, #27
    bl native_fn_021dc940
ov001_021f43bc_L3a4:
    add r10, r10, #1
    cmp r10, #3
    add r7, r7, #1088
    blt ov001_021f43bc_L338
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
    strb r1, [r0, #0x1b]
    b ov001_021f43bc_L3d0
ov001_021f43bc_L3c8:
    mov r1, #27
    strb r1, [r0, #0x1b]
ov001_021f43bc_L3d0:
    ldr r0, =0x0223992c
    bl native_fn_0202ac4c
ov001_021f43bc_L3d8:
    mov r0, #0
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
