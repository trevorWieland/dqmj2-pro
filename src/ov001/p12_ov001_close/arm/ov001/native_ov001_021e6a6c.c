/* ov001 row 0x021e6a6c: 748 bytes.
 *
 * What it does: 187 instructions; 28 call(s) to 0x021db8d0, 0x021dc108, 0x0207b674, +25 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (187 instructions, 28 calls, 30 branches, 14 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x2bc
 *   branch +0x34 -> +0x2bc
 *   branch +0x44 -> +0x8c
 *   branch +0x5c -> +0x84
 *   branch +0x70 -> +0x200
 *   branch +0x80 -> +0x200
 *   branch +0x88 -> +0x200
 *   branch +0xa0 -> +0x1bc
 *   branch +0xb4 -> +0x120
 *   branch +0xb8 -> +0xcc
 *   branch +0xbc -> +0xe0
 *   branch +0xc0 -> +0xf4
 *   branch +0xc4 -> +0x108
 *   branch +0xc8 -> +0x11c
 *   branch +0xdc -> +0x120
 *   branch +0xf0 -> +0x120
 *   branch +0x104 -> +0x120
 *   branch +0x118 -> +0x120
 *   branch +0x128 -> +0x1ac
 *   branch +0x164 -> +0x1ac
 *   branch +0x178 -> +0x190
 *   branch +0x18c -> +0x1ac
 *   branch +0x190 -> +0x1ac
 *   branch +0x198 -> +0x1ac
 *   back edge +0x1b8 -> +0xa8
 *   branch +0x1c0 -> +0x1f0
 *   branch +0x1ec -> +0x200
 *   branch +0x220 -> +0x240
 *   branch +0x23c -> +0x248
 *   branch +0x244 -> +0x258
 *   branch +0x270 -> +0x2ac
 *   branch +0x280 -> +0x298
 *   branch +0x294 -> +0x2b0
 *   branch +0x2a8 -> +0x2b0
 *   branch +0x2b8 -> +0x2c8
 *   test +0x20 cmp r0, #0
 *   test +0x30 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x68 cmp r0, #5
 *   test +0x74 cmp r0, #7
 *   test +0x98 cmp r0, #0
 *   test +0xac cmp r0, #4
 *   test +0x120 cmp r6, #0
 *   test +0x160 cmp r6, #0
 *   test +0x174 cmp r6, r5
 *   test +0x194 cmp r4, #100
 *   test +0x1b4 cmp r7, r0
 *   test +0x1bc cmp r4, #0
 *   test +0x238 cmp r0, #2
 *   test +0x24c cmp r0, #0
 *   test +0x26c cmp r0, #2
 *   test +0x278 cmp r0, r6
 *   1 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e6a6c; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dc108(void);
extern void native_fn_0207b674(void);
extern void native_fn_0203d294(void);
extern void native_fn_022180e0(void);
extern void native_fn_0220ee24(void);
extern void native_fn_021e6764(void);
extern void native_fn_021e68bc(void);
extern void native_fn_0207afec(void);
extern void native_fn_021e686c(void);


asm u32 native_ov001_021e6a6c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #424
    mov r9, r0
    str r1, [sp, #0x8]
    str r2, [sp, #0xc]
    str r3, [sp, #0x10]
    ldr r11, [sp, #0x1d8]
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021e6a6c_L2bc
    mov r0, r9
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_021e6a6c_L2bc
    add r0, r9, #512
    ldrsb r0, [r0, #55]
    cmp r0, #0
    beq ov001_021e6a6c_L8c
    ldr r1, [r9, #0x1e8]
    mov r0, #64
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    bgt ov001_021e6a6c_L84
    mov r0, #8
    bl native_fn_0203d294
    cmp r0, #5
    movlt r4, #203
    blt ov001_021e6a6c_L200
    cmp r0, #7
    movlt r4, #204
    movge r4, #205
    b ov001_021e6a6c_L200
ov001_021e6a6c_L84:
    mov r4, #217
    b ov001_021e6a6c_L200
ov001_021e6a6c_L8c:
    ldrb r0, [r9, #0x323]
    mov r4, #0
    mov r7, r4
    cmp r0, #0
    mvn r5, #0
    ble ov001_021e6a6c_L1bc
    str r5, [sp, #0x14]
ov001_021e6a6c_La8:
    ldrb r0, [r9, #0x1fe]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b ov001_021e6a6c_L120
    b ov001_021e6a6c_Lcc
    b ov001_021e6a6c_Le0
    b ov001_021e6a6c_Lf4
    b ov001_021e6a6c_L108
    b ov001_021e6a6c_L11c
ov001_021e6a6c_Lcc:
    add r0, r9, r7
    ldrb r0, [r0, #0x35e]
    bl native_fn_022180e0
    ldrb r6, [r0]
    b ov001_021e6a6c_L120
ov001_021e6a6c_Le0:
    add r0, r9, r7
    ldrb r0, [r0, #0x35e]
    bl native_fn_022180e0
    ldrb r6, [r0, #0x1]
    b ov001_021e6a6c_L120
ov001_021e6a6c_Lf4:
    add r0, r9, r7
    ldrb r0, [r0, #0x35e]
    bl native_fn_022180e0
    ldrb r6, [r0, #0x2]
    b ov001_021e6a6c_L120
ov001_021e6a6c_L108:
    add r0, r9, r7
    ldrb r0, [r0, #0x35e]
    bl native_fn_022180e0
    ldrb r6, [r0, #0x3]
    b ov001_021e6a6c_L120
ov001_021e6a6c_L11c:
    mov r6, #0
ov001_021e6a6c_L120:
    cmp r6, #0
    ldreq r6, [sp, #0x14]
    beq ov001_021e6a6c_L1ac
    mov r0, #0
    bl native_fn_0220ee24
    stmia sp, {r6, r11}
    add r8, r9, r7
    mov r10, r0
    ldrb r3, [r8, #0x35e]
    ldr r1, [sp, #0x8]
    ldr r2, [sp, #0xc]
    mov r0, r9
    bl native_fn_021e6764
    mov r6, r0
    mov r0, r10
    bl native_fn_0220ee24
    cmp r6, #0
    blt ov001_021e6a6c_L1ac
    mov r0, #50
    bl native_fn_0203d294
    add r6, r6, r0
    cmp r6, r5
    ble ov001_021e6a6c_L190
    ldrb r0, [r8, #0x35e]
    mov r4, #1
    mov r5, r6
    str r0, [sp, #0x18]
    b ov001_021e6a6c_L1ac
ov001_021e6a6c_L190:
    bne ov001_021e6a6c_L1ac
    cmp r4, #100
    bge ov001_021e6a6c_L1ac
    ldrb r1, [r8, #0x35e]
    add r0, sp, #24
    str r1, [r0, r4, lsl #2]
    add r4, r4, #1
ov001_021e6a6c_L1ac:
    add r7, r7, #1
    ldrb r0, [r9, #0x323]
    cmp r7, r0
    blt ov001_021e6a6c_La8
ov001_021e6a6c_L1bc:
    cmp r4, #0
    bne ov001_021e6a6c_L1f0
    mov r0, #0
    bl native_fn_0220ee24
    mov r5, r0
    ldr r1, [sp, #0xc]
    mov r0, r9
    mov r2, r11
    bl native_fn_021e68bc
    mov r4, r0
    mov r0, r5
    bl native_fn_0220ee24
    b ov001_021e6a6c_L200
ov001_021e6a6c_L1f0:
    mov r0, r4
    bl native_fn_0203d294
    add r1, sp, #24
    ldr r4, [r1, r0, lsl #2]
ov001_021e6a6c_L200:
    mov r0, #0
    bl native_fn_0220ee24
    mov r5, r0
    mov r0, r4
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    beq ov001_021e6a6c_L240
    mov r0, r4
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #2
    bne ov001_021e6a6c_L248
ov001_021e6a6c_L240:
    ldrb r6, [r9, #0x31e]
    b ov001_021e6a6c_L258
ov001_021e6a6c_L248:
    ldrb r0, [r9, #0x31e]
    cmp r0, #0
    moveq r6, #1
    movne r6, #0
ov001_021e6a6c_L258:
    mov r0, r4
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #2
    beq ov001_021e6a6c_L2ac
    ldrb r0, [r9, #0x31e]
    cmp r0, r6
    mov r0, r9
    bne ov001_021e6a6c_L298
    ldr r1, [sp, #0x8]
    mov r2, r4
    bl native_fn_021e686c
    mov r7, r0
    b ov001_021e6a6c_L2b0
ov001_021e6a6c_L298:
    ldr r1, [sp, #0xc]
    mov r2, r4
    bl native_fn_021e686c
    mov r7, r0
    b ov001_021e6a6c_L2b0
ov001_021e6a6c_L2ac:
    ldrb r7, [r9, #0x31f]
ov001_021e6a6c_L2b0:
    mov r0, r5
    bl native_fn_0220ee24
    b ov001_021e6a6c_L2c8
ov001_021e6a6c_L2bc:
    ldrb r6, [r9, #0x31e]
    mov r4, #6
    mov r7, #0
ov001_021e6a6c_L2c8:
    ldr r0, [sp, #0x10]
    ldr r1, [sp, #0x1d0]
    strh r4, [r0]
    ldr r0, [sp, #0x1d4]
    strb r6, [r1]
    strb r7, [r0]
    mov r0, #1
    add sp, sp, #424
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
