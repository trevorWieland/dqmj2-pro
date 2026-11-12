/* ov000 row 0x0220e20c: 452 bytes.
 *
 * What it does: 113 instructions; 10 call(s) to 0x0220d7b8, 0x0220dfa4, 0x0220a2a4, +7 more; loops (back edge at +0x0c); returns through pop {r4, r5, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x14 -> +0x3c
 *   branch +0x20 -> +0x3c
 *   branch +0x44 -> +0x6c
 *   branch +0x74 -> +0xd4
 *   branch +0x90 -> +0xb0
 *   branch +0xdc -> +0x130
 *   branch +0x138 -> +0x194
 *   branch +0x15c -> +0x170
 *   branch +0x19c -> +0x1b8
 *   test +0x10 cmp r0, #0
 *   test +0x1c cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x40 cmp r0, #50
 *   test +0x70 cmp r0, #52
 *   test +0x84 cmp r5, #0
 *   test +0xb0 cmp r5, #20
 *   test +0xd8 cmp r0, #54
 *   test +0x134 cmp r0, #56
 *   test +0x150 cmp r5, #31
 *   test +0x170 cmp r5, #20
 *   test +0x198 cmp r0, #58
 *   4 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220e20c; the literal pool and
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

extern void native_fn_0220d7b8(void);
extern void native_fn_0220dfa4(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_02042c0c(void);
extern void native_fn_021e60a8(void);
extern void native_fn_021e07b8(void);
extern void native_fn_020420c4(void);


asm u32 native_ov000_0220e20c (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    mov r4, r0
    bl native_fn_0220d7b8
    cmp r0, #0
    beq ov000_0220e20c_L3c
    ldrb r0, [r4, #0x279]
    cmp r0, #0
    bne ov000_0220e20c_L3c
    mov r0, r4
    bl native_fn_0220dfa4
    cmp r0, #0
    strgeb r0, [r4, #0x290]
    movge r0, #50
    strgeb r0, [r4, #0x279]
ov000_0220e20c_L3c:
    ldrb r0, [r4, #0x279]
    cmp r0, #50
    bne ov000_0220e20c_L6c
    mov r1, #0
    mov r0, r4
    mov r2, r1
    bl native_fn_0220a2a4
    add r0, r4, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #52
    strb r0, [r4, #0x279]
ov000_0220e20c_L6c:
    ldrb r0, [r4, #0x279]
    cmp r0, #52
    bne ov000_0220e20c_Ld4
    add r0, r4, #512
    ldrsh r0, [r0, #122]
    rsb r5, r0, #31
    cmp r5, #0
    movle r0, #54
    strleb r0, [r4, #0x279]
    ble ov000_0220e20c_Lb0
    mov r0, r4
    and r1, r5, #255
    bl native_fn_02042c0c
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #2
    strh r1, [r0, #122]
ov000_0220e20c_Lb0:
    cmp r5, #20
    movlt r0, #1
    ldrb r1, [r4, #0x2c2]
    movge r0, #0
    and r0, r0, #255
    and r0, r0, #15
    bic r1, r1, #15
    orr r0, r1, r0
    strb r0, [r4, #0x2c2]
ov000_0220e20c_Ld4:
    ldrb r0, [r4, #0x279]
    cmp r0, #54
    bne ov000_0220e20c_L130
    ldrb r0, [r4, #0x290]
    add r1, sp, #0
    bl native_fn_021e60a8
    add r12, sp, #0
    add r3, r4, #112
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r3, r4, #272
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #0
    bl native_fn_021e07b8
    mov r1, r0
    mov r0, r4
    bl native_fn_020420c4
    add r0, r4, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #56
    strb r0, [r4, #0x279]
ov000_0220e20c_L130:
    ldrb r0, [r4, #0x279]
    cmp r0, #56
    bne ov000_0220e20c_L194
    add r0, r4, #512
    ldrsh r5, [r0, #122]
    mov r0, r4
    and r1, r5, #255
    bl native_fn_02042c0c
    cmp r5, #31
    movge r0, #58
    strgeb r0, [r4, #0x279]
    bge ov000_0220e20c_L170
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #2
    strh r1, [r0, #122]
ov000_0220e20c_L170:
    cmp r5, #20
    movlt r0, #1
    ldrb r1, [r4, #0x2c2]
    movge r0, #0
    and r0, r0, #255
    and r0, r0, #15
    bic r1, r1, #15
    orr r0, r1, r0
    strb r0, [r4, #0x2c2]
ov000_0220e20c_L194:
    ldrb r0, [r4, #0x279]
    cmp r0, #58
    bne ov000_0220e20c_L1b8
    mov r0, r4
    mov r1, #2
    mov r2, #0
    bl native_fn_0220a2a4
    mov r0, #0
    strb r0, [r4, #0x279]
ov000_0220e20c_L1b8:
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
