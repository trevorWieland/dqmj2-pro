/* ov006 row 0x021f8868: 212 bytes.
 *
 * What it does: 99 instructions; 10 call(s) to 0x022045c8, 0x02008d78, 0x021f88d0, +7 more; loops (back edge at +0x3e); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd0 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   branch +0x30 -> +0xcc
 *   branch +0x34 -> +0x38
 *   branch +0x44 -> +0x4a
 *   branch +0x48 -> +0x4c
 *   branch +0x50 -> +0x68
 *   back edge +0x66 -> +0x58
 *   branch +0x84 -> +0xcc
 *   branch +0x96 -> +0xb0
 *   back edge +0xae -> +0x9e
 *   test +0x2e cmp r6, r0
 *   test +0x32 cmp r4, #0x10
 *   test +0x42 cmp r4, #0x10
 *   test +0x4e cmp r3, #0x0
 *   test +0x64 cmp r0, r3
 *   test +0x82 cmp r4, #0x10
 *   test +0x94 cmp r4, #0x0
 *   test +0xac cmp r2, r4
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8868; the literal pool and
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

extern void native_fn_022045c8(void);
extern void native_fn_02008d78(void);
extern void native_fn_0220374c(void);


asm u32 native_ov006_021f8868 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x34
    add r6, r0, #0x0
    mov r0, #0x2a
    add r5, r6, #0x0
    mul r5, r0
    ldr r0, =0x0221c0d8
    str r1, [sp, #0xc]
    ldr r0, [r0, #0x4]
    mov r1, #0x20
    ldr r0, [r0, #0]
    add r0, r0, r5
    bl native_fn_022045c8
    add r4, r0, #0x0
    ldr r0, [sp, #0xc]
    mov r1, #0x1c
    add r7, r0, #0x0
    ldr r0, =0x0221c0d8
    mul r7, r1
    ldr r0, [r0, #0x4]
    add r0, #0x51
    ldrb r0, [r0, #0]
    cmp r6, r0
    bge ov006_021f8868_Lcc
    cmp r4, #0x10
    bgt ov006_021f8868_L38
    add r7, r7, #0x6
ov006_021f8868_L38:
    add r0, sp, #0x10
    mov r1, #0x0
    mov r2, #0x22
    blx native_fn_02008d78
    cmp r4, #0x10
    bgt ov006_021f8868_L4a
    add r3, r4, #0x0
    b ov006_021f8868_L4c
ov006_021f8868_L4a:
    mov r3, #0x10
ov006_021f8868_L4c:
    mov r0, #0x0
    cmp r3, #0x0
    ble ov006_021f8868_L68
    ldr r2, =0x0221c0d8
    add r1, sp, #0x10
    ldr r2, [r2, #0x4]
ov006_021f8868_L58:
    ldr r6, [r2, #0]
    add r6, r5, r6
    ldrb r6, [r0, r6]
    add r0, r0, #0x1
    strh r6, [r1, #0]
    add r1, r1, #0x2
    cmp r0, r3
    blt ov006_021f8868_L58
ov006_021f8868_L68:
    mov r1, #0xa
    str r1, [sp]
    add r0, sp, #0x10
    str r0, [sp, #0x4]
    mov r0, #0x1
    str r0, [sp, #0x8]
    ldr r0, =0x0221c0d8
    add r2, r7, #0x0
    ldr r0, [r0, #0x4]
    mov r3, #0x2
    ldr r0, [r0, #0xc]
    bl native_fn_0220374c
    cmp r4, #0x10
    ble ov006_021f8868_Lcc
    add r0, sp, #0x10
    mov r1, #0x0
    mov r2, #0x22
    blx native_fn_02008d78
    sub r4, #0x10
    mov r2, #0x0
    cmp r4, #0x0
    ble ov006_021f8868_Lb0
    ldr r1, =0x0221c0d8
    add r0, sp, #0x10
    ldr r1, [r1, #0x4]
ov006_021f8868_L9e:
    ldr r3, [r1, #0]
    add r3, r5, r3
    add r3, r2, r3
    ldrb r3, [r3, #0x10]
    add r2, r2, #0x1
    strh r3, [r0, #0]
    add r0, r0, #0x2
    cmp r2, r4
    blt ov006_021f8868_L9e
ov006_021f8868_Lb0:
    mov r1, #0xa
    str r1, [sp]
    add r0, sp, #0x10
    str r0, [sp, #0x4]
    mov r0, #0x1
    str r0, [sp, #0x8]
    ldr r0, =0x0221c0d8
    add r7, #0xc
    ldr r0, [r0, #0x4]
    add r2, r7, #0x0
    ldr r0, [r0, #0xc]
    mov r3, #0x2
    bl native_fn_0220374c
ov006_021f8868_Lcc:
    add sp, #0x34
    pop {r4, r5, r6, r7, pc}
}
