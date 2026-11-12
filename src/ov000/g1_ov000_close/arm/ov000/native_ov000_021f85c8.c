/* ov000 row 0x021f85c8: 624 bytes.
 *
 * What it does: 155 instructions; 22 call(s) to 0x02215698, 0x021f86f8, 0x02062a50, +19 more; loops (back edge at +0x44); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x26c -> constant 0x02236f14 (image word 0x02236f14)
 *   branch +0x34 -> +0x130
 *   branch +0x7c -> +0x90
 *   branch +0x8c -> +0x9c
 *   branch +0xb4 -> +0xe4
 *   back edge +0xe0 -> +0xbc
 *   branch +0xe8 -> +0x100
 *   branch +0xf0 -> +0x108
 *   branch +0xfc -> +0x10c
 *   branch +0x104 -> +0x10c
 *   back edge +0x12c -> +0x40
 *   branch +0x188 -> +0x254
 *   branch +0x1c8 -> +0x1dc
 *   branch +0x1d8 -> +0x1e4
 *   branch +0x1f8 -> +0x210
 *   branch +0x20c -> +0x220
 *   branch +0x224 -> +0x23c
 *   branch +0x22c -> +0x244
 *   branch +0x238 -> +0x248
 *   branch +0x240 -> +0x248
 *   back edge +0x25c -> +0x15c
 *   test +0x30 cmp r0, #0
 *   test +0x5c cmp r1, #0
 *   test +0x64 cmpeq r1, r4
 *   test +0x6c cmp r0, #0
 *   test +0x74 cmp r7, #0
 *   test +0x78 cmpne r7, #1
 *   test +0x80 cmp r7, #2
 *   test +0xb0 cmp r0, #0
 *   test +0xdc cmp r5, r0
 *   test +0xe4 cmp r7, #0
 *   test +0xec cmp r7, #1
 *   test +0xf4 cmp r7, #2
 *   test +0x124 cmp r4, r0
 *   test +0x184 cmp r5, #127
 *   test +0x198 cmp r0, #1
 *   test +0x1a0 cmpeq r0, r7
 *   test +0x1b4 cmp r0, #0
 *   test +0x1c0 cmp r8, #0
 *   test +0x1c4 cmpne r8, #1
 *   test +0x1cc cmp r8, #2
 *   test +0x1ec cmp r8, #2
 *   test +0x220 cmp r10, #0
 *   test +0x228 cmp r10, #1
 *   test +0x230 cmp r10, #2
 *   test +0x258 cmp r7, #12
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f85c8; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_02062a50(void);
extern void native_fn_0206d23c(void);
extern void native_fn_0206d250(void);
extern void native_fn_020482b4(void);
extern void native_fn_0221744c(void);
extern void native_fn_0206d914(void);
extern void native_fn_021f95b0(void);
extern void native_fn_021f9614(void);
extern void native_fn_02217814(void);
extern void native_fn_0204820c(void);
extern void native_fn_0204afe0(void);
extern void native_fn_021f94d0(void);
extern void native_fn_02048308(void);


asm u32 native_ov000_021f85c8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    bl native_fn_02215698
    str r0, [sp, #0xc]
    add r0, r0, #1024
    ldrsb r0, [r0, #149]
    mov r4, #0
    str r0, [sp, #0x8]
    ldr r0, [sp, #0xc]
    ldrb r0, [r0, #0x491]
    str r0, [sp]
    ldr r0, [sp, #0x8]
    cmp r0, #0
    ble ov000_021f85c8_L130
    ldr r0, [sp, #0xc]
    add r10, r0, #160
ov000_021f85c8_L40:
    mov r0, r4
    bl native_fn_02062a50
    ldr r1, [sp, #0xc]
    ldrb r0, [r0, #0x33]
    add r1, r1, #1024
    ldrsb r1, [r1, #154]
    mov r7, #1
    cmp r1, #0
    ldreq r1, [sp]
    cmpeq r1, r4
    moveq r7, #0
    cmp r0, #0
    movne r7, #2
    cmp r7, #0
    cmpne r7, #1
    beq ov000_021f85c8_L90
    cmp r7, #2
    ldreq r0, =0x02236f14
    ldreq r9, [r0, #0x10]
    b ov000_021f85c8_L9c
ov000_021f85c8_L90:
    ldrsb r0, [r10, #6]
    bl native_fn_0206d23c
    ldr r9, [r0, #0x14]
ov000_021f85c8_L9c:
    ldrsb r1, [r10, #7]
    ldrsb r0, [r10, #6]
    mov r5, #0
    mov r8, r1, lsl #5
    bl native_fn_0206d250
    cmp r0, #0
    blt ov000_021f85c8_Le4
    mov r11, #32
ov000_021f85c8_Lbc:
    mov r0, r9
    mov r1, r8
    mov r2, r11
    bl native_fn_020482b4
    ldrsb r0, [r10, #6]
    add r5, r5, #1
    add r8, r8, #32
    bl native_fn_0206d250
    cmp r5, r0
    ble ov000_021f85c8_Lbc
ov000_021f85c8_Le4:
    cmp r7, #0
    beq ov000_021f85c8_L100
    cmp r7, #1
    beq ov000_021f85c8_L108
    cmp r7, #2
    moveq r6, #9
    b ov000_021f85c8_L10c
ov000_021f85c8_L100:
    mov r6, #6
    b ov000_021f85c8_L10c
ov000_021f85c8_L108:
    mov r6, #3
ov000_021f85c8_L10c:
    bl native_fn_0221744c
    ldrsb r1, [r10, #6]
    mov r2, r6
    bl native_fn_0206d914
    ldr r0, [sp, #0x8]
    add r4, r4, #1
    cmp r4, r0
    add r10, r10, #8
    blt ov000_021f85c8_L40
ov000_021f85c8_L130:
    ldr r0, [sp, #0xc]
    mov r7, #0
    add r0, r0, #1024
    str r0, [sp, #0x10]
    ldrsb r1, [r0, #144]
    ldrsb r0, [r0, #145]
    add r0, r1, r0, lsl #2
    and r0, r0, #255
    str r0, [sp, #0x4]
    ldr r0, [sp, #0xc]
    add r11, r0, #184
ov000_021f85c8_L15c:
    mov r8, #1
    and r0, r7, #255
    mov r10, r8
    bl native_fn_021f95b0
    mov r1, #80
    mul r4, r0, r1
    and r0, r7, #255
    bl native_fn_021f95b0
    bl native_fn_021f9614
    mov r5, r0
    cmp r5, #127
    beq ov000_021f85c8_L254
    ldr r0, [sp, #0x10]
    mov r6, #3
    ldrsb r0, [r0, #154]
    cmp r0, #1
    ldreq r0, [sp, #0x4]
    cmpeq r0, r7
    moveq r8, #0
    mov r0, r5
    moveq r10, r8
    bl native_fn_02217814
    cmp r0, #0
    moveq r8, #2
    moveq r10, r8
    cmp r8, #0
    cmpne r8, #1
    beq ov000_021f85c8_L1dc
    cmp r8, #2
    ldreq r0, =0x02236f14
    ldreq r9, [r0, #0x10]
    b ov000_021f85c8_L1e4
ov000_021f85c8_L1dc:
    ldr r0, =0x02236f14
    ldr r9, [r0, #0xc]
ov000_021f85c8_L1e4:
    and r0, r7, #255
    bl native_fn_021f95b0
    cmp r8, #2
    add r0, r0, #2
    mov r3, r0, lsl #5
    bne ov000_021f85c8_L210
    mov r1, r3
    mov r0, r9
    mov r2, #32
    bl native_fn_0204820c
    b ov000_021f85c8_L220
ov000_021f85c8_L210:
    mov r2, r5
    mov r0, r9
    mov r1, #1
    bl native_fn_0204afe0
ov000_021f85c8_L220:
    cmp r10, #0
    beq ov000_021f85c8_L23c
    cmp r10, #1
    beq ov000_021f85c8_L244
    cmp r10, #2
    moveq r6, #9
    b ov000_021f85c8_L248
ov000_021f85c8_L23c:
    mov r6, #6
    b ov000_021f85c8_L248
ov000_021f85c8_L244:
    mov r6, #3
ov000_021f85c8_L248:
    add r0, r11, r4
    mov r1, r6
    bl native_fn_021f94d0
ov000_021f85c8_L254:
    add r7, r7, #1
    cmp r7, #12
    blt ov000_021f85c8_L15c
    bl native_fn_02048308
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
