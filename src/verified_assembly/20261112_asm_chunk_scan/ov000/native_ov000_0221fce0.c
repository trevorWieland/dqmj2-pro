/* ov000 row 0x0221fce0: 624 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (one load, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x264 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x268 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x26c -> constant 0x022463f6 (image word 0x022463f6)
 *   branch +0x54 -> +0x160
 *   branch +0x78 -> +0x12c
 *   branch +0xb0 -> +0xe8
 *   branch +0xbc -> +0xe0
 *   branch +0xdc -> +0xe8
 *   branch +0xe4 -> +0xec
 *   branch +0x130 -> +0x148
 *   back edge +0x150 -> +0x68
 *   back edge +0x198 -> +0x18c
 *   branch +0x1b0 -> +0x248
 *   branch +0x20c -> +0x228
 *   branch +0x214 -> +0x220
 *   branch +0x21c -> +0x250
 *   branch +0x224 -> +0x250
 *   branch +0x22c -> +0x23c
 *   branch +0x238 -> +0x250
 *   branch +0x244 -> +0x250
 *   test +0x44 cmp r0, #0
 *   test +0x50 cmpeq r1, r0
 *   test +0x70 cmp r8, r4
 *   test +0xac cmp r1, #10
 *   test +0xb8 cmp r0, #2
 *   test +0xd8 cmp r0, #2
 *   test +0x12c cmp r8, r4
 *   test +0x14c cmp r7, #6
 *   test +0x1ac cmp r1, #0
 *   test +0x208 cmp r0, #0
 *   test +0x210 cmp r3, #0
 *   test +0x228 cmp r3, #0
 *   9 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221fce0; the literal pool and
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

extern void native_fn_0221f6e8(void);
extern void native_fn_0207cd98(void);
extern void native_fn_02062a10(void);
extern void native_fn_02046af4(void);
extern void native_fn_020449d4(void);
extern void native_fn_0221f5fc(void);
extern void native_fn_0221f7d4(void);
extern void native_fn_0221cac8(void);
extern void native_fn_0221cae0(void);
extern void native_fn_0221d048(void);


asm u32 native_ov000_0221fce0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #76
    ldr r1, =0x022463b0
    mov r11, r0
    ldr r1, [r1, #0xc]
    ldr r0, [r11]
    and r1, r1, #255
    bl native_fn_0221f6e8
    ldr r1, =0x022463b0
    str r0, [sp, #0x8]
    ldr r1, [r1, #0xc]
    ldr r0, [r11, #0x4]
    and r1, r1, #255
    bl native_fn_0221f6e8
    ldr r1, =0x022463b0
    mov r8, r0
    ldrb r0, [r1, #0x1]
    cmp r0, #0
    ldreq r1, [r1, #0x8]
    ldreq r0, [r11, #0x4]
    cmpeq r1, r0
    beq ov000_0221fce0_L160
    ldr r5, =0x022463b0
    mov r7, #0
    add r6, sp, #12
    mvn r4, #0
ov000_0221fce0_L68:
    mov r0, r8
    bl native_fn_0207cd98
    cmp r8, r4
    mov r10, r0
    beq ov000_0221fce0_L12c
    bl native_fn_02062a10
    str r6, [sp]
    mov r1, #255
    str r1, [sp, #0x4]
    mov r1, r0
    ldr r0, =0x021c9698
    mov r2, #18
    mov r3, #8
    bl native_fn_02046af4
    mov r0, r10
    bl native_fn_02062a10
    ldrb r1, [r0, #0x30]
    cmp r1, #10
    blo ov000_0221fce0_Le8
    ldrb r0, [r0, #0x1b]
    cmp r0, #2
    bne ov000_0221fce0_Le0
    ldr r0, [r5, #0xc]
    ldr r2, [r5, #0x1c]
    rsb r1, r0, #1
    mov r0, #132
    mla r0, r1, r0, r2
    ldrb r0, [r0, #0x1b]
    cmp r0, #2
    beq ov000_0221fce0_Le8
ov000_0221fce0_Le0:
    mov r9, #1
    b ov000_0221fce0_Lec
ov000_0221fce0_Le8:
    mov r9, #3
ov000_0221fce0_Lec:
    mov r0, r10
    bl native_fn_02062a10
    ldrsh r0, [r0, #24]
    bl native_fn_020449d4
    mov r1, #0
    stmia sp, {r1, r9}
    ldrh r1, [r0, #4]
    add r0, r7, #20
    mov r0, r0, lsl #24
    mov r1, r1, lsl #24
    mov r1, r1, lsr #28
    and r2, r1, #255
    mov r0, r0, asr #24
    mov r1, r6
    mov r3, #12
    bl native_fn_0221f5fc
ov000_0221fce0_L12c:
    cmp r8, r4
    beq ov000_0221fce0_L148
    mov r0, r8
    ldr r1, [r5, #0xc]
    and r1, r1, #255
    bl native_fn_0221f7d4
    mov r8, r0
ov000_0221fce0_L148:
    add r7, r7, #1
    cmp r7, #6
    blt ov000_0221fce0_L68
    ldr r0, =0x022463b0
    mov r1, #0
    strb r1, [r0, #0x1]
ov000_0221fce0_L160:
    ldr r1, =0x022463b0
    ldr r0, [sp, #0x8]
    ldr r4, [r1, #0xc]
    bl native_fn_0207cd98
    bl native_fn_02062a10
    ldr r2, =0x022463b0
    mov r1, #132
    ldr r2, [r2, #0x1c]
    mov r7, r0
    mla r6, r4, r1, r2
    mov r5, #8
ov000_0221fce0_L18c:
    ldmia r7!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    subs r5, r5, #1
    bne ov000_0221fce0_L18c
    ldr r1, [r7]
    ldr r0, =0x022463b0
    str r1, [r6]
    ldrb r1, [r0, #0x4]
    cmp r1, #0
    bne ov000_0221fce0_L248
    ldr r0, [sp, #0x8]
    bl native_fn_0207cd98
    bl native_fn_02062a10
    ldr r2, =0x022463f6
    mov r1, #20
    mla r2, r4, r1, r2
    mov r1, r0
    str r2, [sp]
    mov r4, #255
    ldr r0, =0x021c9698
    mov r2, #18
    mov r3, #24
    str r4, [sp, #0x4]
    bl native_fn_02046af4
    ldr r1, =0x022463b0
    mov r0, #132
    ldr r3, [r1, #0xc]
    ldr r2, [r1, #0x1c]
    rsb r1, r3, #1
    mla r0, r1, r0, r2
    ldr r0, [r0, #0x14]
    cmp r0, #0
    beq ov000_0221fce0_L228
    cmp r3, #0
    bne ov000_0221fce0_L220
    bl native_fn_0221cac8
    b ov000_0221fce0_L250
ov000_0221fce0_L220:
    bl native_fn_0221cae0
    b ov000_0221fce0_L250
ov000_0221fce0_L228:
    cmp r3, #0
    bne ov000_0221fce0_L23c
    mov r0, #10
    bl native_fn_0221d048
    b ov000_0221fce0_L250
ov000_0221fce0_L23c:
    mov r0, #11
    bl native_fn_0221d048
    b ov000_0221fce0_L250
ov000_0221fce0_L248:
    mov r1, #0
    strb r1, [r0, #0x4]
ov000_0221fce0_L250:
    ldr r1, [r11, #0x4]
    ldr r0, =0x022463b0
    str r1, [r0, #0x8]
    add sp, sp, #76
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
