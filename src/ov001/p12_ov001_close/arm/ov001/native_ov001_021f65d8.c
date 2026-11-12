/* ov001 row 0x021f65d8: 672 bytes.
 *
 * What it does: 167 instructions; 17 call(s) to 0x0207afec, 0x021db438, 0x021db438, +14 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 17 calls (167 instructions, 17 calls, 23 branches, 13 back edges, 1 literal slot).
 *
 *   pool +0x29c -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x30 -> +0x9c
 *   branch +0x40 -> +0x54
 *   branch +0x50 -> +0x70
 *   branch +0x58 -> +0x84
 *   branch +0x6c -> +0x84
 *   branch +0x80 -> +0x94
 *   branch +0x98 -> +0xa0
 *   branch +0xac -> +0x24c
 *   branch +0xbc -> +0x23c
 *   branch +0x114 -> +0x1ec
 *   branch +0x13c -> +0x154
 *   branch +0x144 -> +0x15c
 *   branch +0x14c -> +0x164
 *   branch +0x150 -> +0x178
 *   branch +0x158 -> +0x178
 *   branch +0x160 -> +0x178
 *   branch +0x190 -> +0x1e0
 *   branch +0x1a4 -> +0x1e0
 *   branch +0x1ac -> +0x1d4
 *   branch +0x1c0 -> +0x1d4
 *   branch +0x1d0 -> +0x1e0
 *   back edge +0x1e8 -> +0x180
 *   branch +0x1f4 -> +0x210
 *   branch +0x20c -> +0x23c
 *   branch +0x218 -> +0x23c
 *   back edge +0x248 -> +0xb0
 *   branch +0x25c -> +0x274
 *   test +0x2c cmp r10, #0
 *   test +0x3c cmp r2, #0
 *   test +0x54 cmp r2, #1
 *   test +0x68 cmp r0, #1
 *   test +0xa0 cmp r11, #0
 *   test +0xa8 cmpgt r11, #0
 *   test +0xb8 cmp r0, #0
 *   test +0x110 cmp r0, #0
 *   test +0x128 cmp r0, #0
 *   test +0x134 cmp r9, #58
 *   test +0x140 cmp r9, #169
 *   test +0x148 cmp r9, #171
 *   test +0x18c tst r7, r0
 *   test +0x1a0 cmp r0, r4
 *   test +0x1a8 cmp r9, #169
 *   test +0x1bc cmp r0, #0
 *   test +0x1cc cmp r0, #0
 *   test +0x1e4 cmp r6, #60
 *   test +0x1f0 cmp r0, #0
 *   test +0x214 cmp r0, #0
 *   test +0x240 cmp r5, r11
 *   test +0x250 cmp r0, #0
 *   test +0x27c cmp r0, #0
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f65d8; the literal pool and
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
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021e2a48(void);
extern void native_fn_021e048c(void);
extern void native_fn_021d8dec(void);
extern void native_fn_021dc940(void);
extern void native_fn_021ee7b0(void);
extern void native_fn_021f949c(void);


asm u32 native_ov001_021f65d8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #60
    str r0, [sp, #0x1c]
    mov r0, #0
    str r0, [sp, #0x24]
    mov r9, r2
    mov r10, r1
    ldr r1, [sp, #0x24]
    mov r0, r9
    str r1, [sp, #0x20]
    bl native_fn_0207afec
    cmp r10, #0
    bne ov001_021f65d8_L9c
    ldr r1, [sp, #0x1c]
    ldrb r2, [r1, #0x31e]
    cmp r2, #0
    bne ov001_021f65d8_L54
    ldrh r1, [r0, #8]
    mov r1, r1, lsl #24
    movs r1, r1, lsr #28
    beq ov001_021f65d8_L70
ov001_021f65d8_L54:
    cmp r2, #1
    bne ov001_021f65d8_L84
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_021f65d8_L84
ov001_021f65d8_L70:
    mov r0, #0
    mov r1, r0
    bl ov001_side_slot_record_021db438
    mov r10, r0
    b ov001_021f65d8_L94
ov001_021f65d8_L84:
    mov r0, #1
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r10, r0
ov001_021f65d8_L94:
    mov r11, #3
    b ov001_021f65d8_La0
ov001_021f65d8_L9c:
    mov r11, #1
ov001_021f65d8_La0:
    cmp r11, #0
    mov r5, #0
    cmpgt r11, #0
    ble ov001_021f65d8_L24c
ov001_021f65d8_Lb0:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f65d8_L23c
    mov r2, #0
    add r1, sp, #40
    str r2, [sp]
    str r1, [sp, #0x4]
    add r0, sp, #56
    str r0, [sp, #0x8]
    str r2, [sp, #0xc]
    add r1, sp, #48
    str r1, [sp, #0x10]
    add r0, sp, #52
    str r0, [sp, #0x14]
    add r1, sp, #44
    str r1, [sp, #0x18]
    ldr r0, =0x0223989c
    ldr r1, [sp, #0x1c]
    ldrb r3, [r0, #0x10]
    mov r0, r9
    mov r2, r10
    bl native_fn_021e1a60
    ldr r0, [sp, #0x34]
    cmp r0, #0
    beq ov001_021f65d8_L1ec
    ldr r0, =0x0223989c
    mov r7, #0
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r0, #8
    movne r0, #16
    cmp r9, #58
    and r0, r0, #255
    beq ov001_021f65d8_L154
    cmp r9, #169
    beq ov001_021f65d8_L15c
    cmp r9, #171
    beq ov001_021f65d8_L164
    b ov001_021f65d8_L178
ov001_021f65d8_L154:
    mov r7, #8
    b ov001_021f65d8_L178
ov001_021f65d8_L15c:
    mov r7, #1
    b ov001_021f65d8_L178
ov001_021f65d8_L164:
    mvn r0, r0
    and r0, r0, #255
    mov r7, #4
    bl native_fn_021e2a48
    bl native_fn_021e048c
ov001_021f65d8_L178:
    mov r6, #0
    mvn r4, #1
ov001_021f65d8_L180:
    mov r0, r6
    bl native_fn_021d8dec
    ldrb r0, [r0, #0x3]
    tst r7, r0
    beq ov001_021f65d8_L1e0
    add r8, r10, r6
    add r0, r8, #512
    ldrsb r0, [r0, #104]
    cmp r0, r4
    beq ov001_021f65d8_L1e0
    cmp r9, #169
    bne ov001_021f65d8_L1d4
    mov r0, r6
    bl native_fn_021d8dec
    ldrsb r0, [r0]
    cmp r0, #0
    bge ov001_021f65d8_L1d4
    add r0, r8, #512
    ldrsb r0, [r0, #44]
    cmp r0, #0
    bge ov001_021f65d8_L1e0
ov001_021f65d8_L1d4:
    mov r0, r10
    mov r1, r6
    bl native_fn_021dc940
ov001_021f65d8_L1e0:
    add r6, r6, #1
    cmp r6, #60
    blt ov001_021f65d8_L180
ov001_021f65d8_L1ec:
    ldr r0, [sp, #0x38]
    cmp r0, #0
    beq ov001_021f65d8_L210
    ldrh r2, [sp, #40]
    add r1, r10, #768
    mov r0, #1
    str r0, [sp, #0x24]
    strh r2, [r1, #74]
    b ov001_021f65d8_L23c
ov001_021f65d8_L210:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    bne ov001_021f65d8_L23c
    mov r1, #0
    mov r0, r10
    sub r2, r1, #1
    mov r3, #1
    str r1, [sp]
    bl native_fn_021ee7b0
    mov r0, #1
    str r0, [sp, #0x20]
ov001_021f65d8_L23c:
    add r5, r5, #1
    cmp r5, r11
    add r10, r10, #1088
    blt ov001_021f65d8_Lb0
ov001_021f65d8_L24c:
    ldr r0, [sp, #0x24]
    cmp r0, #0
    ldrle r0, =0x0223989c
    movle r1, #0
    ble ov001_021f65d8_L274
    mov r0, #243
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, =0x0223989c
    mov r1, #1
ov001_021f65d8_L274:
    strb r1, [r0, #0x10]
    ldr r0, [sp, #0x20]
    cmp r0, #0
    addeq sp, sp, #60
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #242
    mov r1, #1
    bl native_fn_021f949c
    add sp, sp, #60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
