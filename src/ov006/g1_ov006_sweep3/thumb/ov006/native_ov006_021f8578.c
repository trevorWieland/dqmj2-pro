/* ov006 row 0x021f8578: 188 bytes.
 *
 * What it does: 76 instructions; 12 call(s) to 0x021f2390, 0x021ff6d4, 0x021ff6d4, +9 more; loops (back edge at +0x16); returns through pop {r3, r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xb0 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   pool +0xb4 -> native_fn_021f8d0c+1 (image word 0x021f8d0d)
 *   pool +0xb8 -> native_fn_021f8634+1 (image word 0x021f8635)
 *   branch +0x0c -> +0xaa
 *   branch +0x14 -> +0xaa
 *   branch +0x1c -> +0x26
 *   branch +0x20 -> +0x2e
 *   branch +0x2c -> +0xa4
 *   branch +0x34 -> +0x4a
 *   branch +0x48 -> +0xa4
 *   branch +0x68 -> +0x92
 *   test +0x0a cmp r0, #0x0
 *   test +0x12 cmp r0, #0x0
 *   test +0x1a cmp r0, #0x0
 *   test +0x1e cmp r0, #0x1
 *   test +0x32 cmp r1, #0x4
 *   test +0x66 cmp r2, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8578; the literal pool and
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

extern void native_fn_021f2390(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_021f8cec(void);
extern void native_fn_02002480(void);
extern void native_fn_021fe6e8(void);
extern void native_fn_021f23f4(void);
extern void native_fn_02200344(void);
extern void native_fn_021f8d0c(void);
extern void native_fn_021f52cc(void);
extern void native_fn_021f8634(void);


asm u32 native_ov006_021f8578 (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0x4
    ldr r0, =0x0221c0d8
    ldr r1, [r0, #0x4]
    ldr r0, [r1, #0x38]
    cmp r0, #0x0
    bne ov006_021f8578_Laa
    add r1, #0x57
    ldrb r0, [r1, #0]
    cmp r0, #0x0
    bne ov006_021f8578_Laa
    bl native_fn_021f2390
    cmp r0, #0x0
    beq ov006_021f8578_L26
    cmp r0, #0x1
    beq ov006_021f8578_L2e
    add sp, #0x4
    pop {r3, r4, pc}
ov006_021f8578_L26:
    mov r0, #0x7
    bl native_fn_021ff6d4
    b ov006_021f8578_La4
ov006_021f8578_L2e:
    ldr r0, =0x0221c0d8
    ldrb r1, [r0, #0]
    cmp r1, #0x4
    bne ov006_021f8578_L4a
    ldr r0, [r0, #0x4]
    mov r1, #0x1
    add r0, #0x54
    strb r1, [r0, #0]
    mov r0, #0x6
    bl native_fn_021ff6d4
    bl native_fn_021f8cec
    b ov006_021f8578_La4
ov006_021f8578_L4a:
    ldrh r0, [r0, #0x2]
    mov r1, #0x1c
    blx native_fn_02002480
    ldr r3, =0x0221c0d8
    mov r2, #0x2a
    ldrb r1, [r3, #0]
    add r1, r1, r0
    ldr r0, [r3, #0x4]
    mul r2, r1
    ldr r4, [r0, #0]
    add r2, r4, r2
    add r2, #0x28
    ldrb r2, [r2, #0]
    cmp r2, #0x2
    bne ov006_021f8578_L92
    mov r0, #0x9
    bl native_fn_021ff6d4
    bl native_fn_021fe6e8
    bl native_fn_021f23f4
    mov r1, #0x1
    mov r0, #0x0
    str r0, [sp]
    mov r0, #0xe
    add r2, r1, #0x0
    sub r3, r1, #0x2
    bl native_fn_02200344
    ldr r0, =native_fn_021f8d0c+1
    bl native_fn_021f52cc
    add sp, #0x4
    pop {r3, r4, pc}
ov006_021f8578_L92:
    mov r2, #0x1
    add r0, #0x54
    strb r2, [r0, #0]
    ldr r0, [r3, #0x4]
    add r0, #0x52
    strb r1, [r0, #0]
    mov r0, #0x6
    bl native_fn_021ff6d4
ov006_021f8578_La4:
    ldr r0, =native_fn_021f8634+1
    bl native_fn_021f52cc
ov006_021f8578_Laa:
    add sp, #0x4
    pop {r3, r4, pc}
    mov r8, r8
}
