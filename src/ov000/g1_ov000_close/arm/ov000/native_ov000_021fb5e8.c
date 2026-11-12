/* ov000 row 0x021fb5e8: 512 bytes.
 *
 * What it does: 127 instructions; 13 call(s) to 0x021fb8f8, 0x021fb9a8, 0x021fb9a8, +10 more; loops (back edge at +0x9c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block load.
 *
 *   pool +0x1fc -> constant 0x02237170 (image word 0x02237170)
 *   branch +0xb4 -> +0x180
 *   branch +0xbc -> +0x108
 *   branch +0xd4 -> +0x170
 *   branch +0x104 -> +0x170
 *   branch +0x11c -> +0x170
 *   back edge +0x17c -> +0xb8
 *   branch +0x184 -> +0x1e4
 *   branch +0x18c -> +0x1b0
 *   branch +0x1ac -> +0x1cc
 *   test +0x10 cmp r5, #51
 *   test +0x1c cmpne r5, #50
 *   test +0x44 cmp r0, #255
 *   test +0xb8 cmp r8, #0
 *   test +0xd0 cmp r0, #0
 *   test +0xe0 cmp r1, r6
 *   test +0x118 cmp r0, #0
 *   test +0x14c cmp r1, r6
 *   test +0x178 cmp r4, r11
 *   test +0x180 cmp r7, #0
 *   test +0x188 cmp r8, #0
 *   test +0x1e4 cmp r7, #0
 *   1 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fb5e8; the literal pool and
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

extern void native_fn_021fb8f8(void);
extern void native_fn_021fb9a8(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_021fb97c(void);
extern void native_fn_02215d94(void);
extern void native_fn_0207c2b8(void);
extern void native_fn_0207c18c(void);


asm u32 native_ov000_021fb5e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r5, r0
    mov r0, #0
    cmp r5, #51
    str r0, [sp, #0xc]
    str r1, [sp]
    cmpne r5, #50
    mov r9, r2
    mov r8, r3
    mov r7, r0
    addne sp, sp, #16
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r5
    mov r1, r8
    bl native_fn_021fb8f8
    str r0, [sp, #0x8]
    cmp r0, #255
    addeq sp, sp, #16
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0x8]
    mov r1, #52
    mul r1, r0, r1
    str r1, [sp, #0x4]
    ldr r4, =0x02237170
    ldr r0, [sp, #0x4]
    mov r1, r5
    add r0, r4, r0
    bl native_fn_021fb9a8
    ldrsh r3, [r0, #2]
    ldr r0, [sp, #0x4]
    ldr r2, [sp, #0xc]
    mov r1, r5
    add r2, r2, r3
    add r0, r4, r0
    str r2, [sp, #0xc]
    bl native_fn_021fb9a8
    ldrsh r6, [r0]
    bl native_fn_02062aa0
    mov r4, r0
    bl native_fn_02062ad0
    add r0, r4, r0
    ands r11, r0, #255
    mov r4, #0
    beq ov000_021fb5e8_L180
ov000_021fb5e8_Lb8:
    cmp r8, #0
    beq ov000_021fb5e8_L108
    mov r0, #52
    mul r1, r4, r0
    ldrb r0, [r8, r1]
    add r2, r8, r1
    cmp r0, #0
    beq ov000_021fb5e8_L170
    ldmib r2, {r0, r1}
    sub r1, r1, r0
    cmp r1, r6
    movge r1, r6
    ldr r0, [r2, #0x4]
    add r7, r7, r1
    add r0, r0, r1
    str r0, [r2, #0x4]
    ldr r0, [r9]
    add r0, r0, r1
    str r0, [r9]
    b ov000_021fb5e8_L170
ov000_021fb5e8_L108:
    mov r0, r4
    bl native_fn_021fb97c
    mov r5, r0
    ldrb r0, [r5, #0x33]
    cmp r0, #0
    bne ov000_021fb5e8_L170
    mov r0, r4
    bl native_fn_02215d94
    mov r10, r0
    add r0, r5, #32
    mov r1, r10
    bl native_fn_0207c2b8
    mov r1, r10
    mov r10, r0
    add r0, r5, #32
    bl native_fn_0207c18c
    sub r1, r10, r0
    cmp r1, r6
    movge r1, r6
    ldrsh r0, [r5, #36]
    add r7, r7, r1
    add r0, r0, r1
    strh r0, [r5, #36]
    ldr r0, [r9]
    add r0, r0, r1
    str r0, [r9]
ov000_021fb5e8_L170:
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, r11
    blo ov000_021fb5e8_Lb8
ov000_021fb5e8_L180:
    cmp r7, #0
    ble ov000_021fb5e8_L1e4
    cmp r8, #0
    beq ov000_021fb5e8_L1b0
    ldr r0, [sp, #0x4]
    add r2, r8, #12
    ldr r1, [r2, r0]
    ldr r0, [sp, #0xc]
    sub r1, r1, r0
    ldr r0, [sp, #0x4]
    str r1, [r2, r0]
    b ov000_021fb5e8_L1cc
ov000_021fb5e8_L1b0:
    bl native_fn_02062aa0
    ldr r0, [sp, #0x8]
    bl native_fn_021fb97c
    ldrsh r2, [r0, #38]
    ldr r1, [sp, #0xc]
    sub r1, r2, r1
    strh r1, [r0, #38]
ov000_021fb5e8_L1cc:
    ldr r0, [sp]
    ldr r1, [r0]
    ldr r0, [sp, #0xc]
    add r1, r1, r0
    ldr r0, [sp]
    str r1, [r0]
ov000_021fb5e8_L1e4:
    cmp r7, #0
    movne r0, #1
    moveq r0, #0
    and r0, r0, #255
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
