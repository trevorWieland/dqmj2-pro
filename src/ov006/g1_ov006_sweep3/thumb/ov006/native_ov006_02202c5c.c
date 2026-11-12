/* ov006 row 0x02202c5c: 264 bytes.
 *
 * What it does: 123 instructions; 8 call(s) to 0x02203114, 0x02005d50, 0x0220428c, +5 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x104 -> constant 0x0221c174 (image word 0x0221c174)
 *   branch +0x2c -> +0x92
 *   branch +0x48 -> +0x7c
 *   branch +0x66 -> +0x76
 *   branch +0x74 -> +0x7c
 *   back edge +0x7a -> +0x56
 *   branch +0x8a -> +0xf4
 *   branch +0x90 -> +0xf4
 *   branch +0xac -> +0xe0
 *   branch +0xca -> +0xda
 *   branch +0xd8 -> +0xe0
 *   back edge +0xde -> +0xba
 *   branch +0xee -> +0xf4
 *   test +0x2a cmp r5, #0x0
 *   test +0x46 cmp r4, r1
 *   test +0x64 cmp r2, r1
 *   test +0x78 cmp r5, r0
 *   test +0x88 cmp r4, r0
 *   test +0xaa cmp r4, r1
 *   test +0xc8 cmp r1, r0
 *   test +0xdc cmp r2, r5
 *   test +0xec cmp r4, r0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202c5c; the literal pool and
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

extern void native_fn_02203114(void);
extern void native_fn_02005d50(void);
extern void native_fn_0220428c(void);
extern void native_fn_02008430(void);
extern void native_fn_02005d20(void);


asm u32 native_ov006_02202c5c (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    str r1, [sp]
    add r4, r0, #0x0
    ldr r1, =0x0221c174
    mov r0, #0x8a
    lsl r0, r0, #0x2
    add r7, r4, #0x0
    mul r7, r0
    ldr r1, [r1, #0]
    sub r0, r0, #0x4
    add r1, r1, r7
    ldr r0, [r1, r0]
    add r5, r2, #0x0
    bl native_fn_02203114
    str r0, [sp, #0x8]
    mov r0, #0x1
    blx native_fn_02005d50
    str r0, [sp, #0x4]
    cmp r5, #0x0
    beq ov006_02202c5c_L92
    ldr r0, =0x0221c174
    mov r2, #0x8a
    ldr r0, [r0, #0]
    lsl r2, r2, #0x2
    add r1, r4, #0x0
    mul r1, r2
    add r3, r0, r1
    add r1, r2, #0x0
    sub r1, #0x28
    sub r2, #0x18
    add r4, r3, r1
    add r1, r3, r2
    cmp r4, r1
    beq ov006_02202c5c_L7c
    ldr r1, [sp]
    lsl r6, r1, #0x3
    add r1, r0, r7
    mov r0, #0x21
    lsl r0, r0, #0x4
    add r0, r1, r0
ov006_02202c5c_L56:
    ldrb r2, [r4, #0xc]
    ldr r5, [r4, #0x4]
    ldr r1, [r4, #0x8]
    lsl r2, r2, #0x3
    add r3, r1, r2
    ldr r1, [r5, #0x8]
    add r2, r3, r6
    cmp r2, r1
    bhi ov006_02202c5c_L76
    ldr r0, [sp, #0x8]
    ldr r1, [sp, #0x8]
    str r3, [r0, #0x8]
    add r0, r5, #0x0
    bl native_fn_0220428c
    b ov006_02202c5c_L7c
ov006_02202c5c_L76:
    add r4, r5, #0x0
    cmp r5, r0
    bne ov006_02202c5c_L56
ov006_02202c5c_L7c:
    ldr r0, =0x0221c174
    ldr r0, [r0, #0]
    add r1, r0, r7
    mov r0, #0x21
    lsl r0, r0, #0x4
    add r0, r1, r0
    cmp r4, r0
    bne ov006_02202c5c_Lf4
    blx native_fn_02008430
    b ov006_02202c5c_Lf4
ov006_02202c5c_L92:
    ldr r0, =0x0221c174
    mov r2, #0x8a
    ldr r0, [r0, #0]
    lsl r2, r2, #0x2
    add r1, r4, #0x0
    mul r1, r2
    add r3, r0, r1
    add r1, r2, #0x0
    sub r1, #0x18
    sub r2, #0x28
    add r4, r3, r1
    add r1, r3, r2
    cmp r4, r1
    beq ov006_02202c5c_Le0
    ldr r1, [sp]
    lsl r3, r1, #0x3
    add r1, r0, r7
    mov r0, #0x2
    lsl r0, r0, #0x8
    add r5, r1, r0
ov006_02202c5c_Lba:
    ldr r2, [r4, #0]
    ldr r0, [r4, #0x8]
    ldrb r6, [r2, #0xc]
    sub r1, r0, r3
    ldr r0, [r2, #0x8]
    lsl r6, r6, #0x3
    add r0, r0, r6
    cmp r1, r0
    blo ov006_02202c5c_Lda
    ldr r0, [sp, #0x8]
    str r1, [r0, #0x8]
    ldr r1, [sp, #0x8]
    add r0, r4, #0x0
    bl native_fn_0220428c
    b ov006_02202c5c_Le0
ov006_02202c5c_Lda:
    add r4, r2, #0x0
    cmp r2, r5
    bne ov006_02202c5c_Lba
ov006_02202c5c_Le0:
    ldr r0, =0x0221c174
    ldr r0, [r0, #0]
    add r1, r0, r7
    mov r0, #0x2
    lsl r0, r0, #0x8
    add r0, r1, r0
    cmp r4, r0
    bne ov006_02202c5c_Lf4
    blx native_fn_02008430
ov006_02202c5c_Lf4:
    ldr r0, [sp, #0x4]
    blx native_fn_02005d20
    ldr r1, [sp]
    ldr r0, [sp, #0x8]
    strb r1, [r0, #0xc]
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
}
