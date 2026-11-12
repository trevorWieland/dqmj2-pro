/* ov006 row 0x02203228: 184 bytes.
 *
 * What it does: 78 instructions; 7 call(s) to 0x02002480, 0x02004308, 0x02004308, +4 more; loops (back edge at +0x3a); returns through pop {r3, r4, r5, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xa8 -> native_data_0220bb48 (image word 0x0220bb48)
 *   pool +0xac -> constant 0x0221c180 (image word 0x0221c180)
 *   pool +0xb0 -> constant 0x04001050 (image word 0x04001050)
 *   pool +0xb4 -> constant 0x04000050 (image word 0x04000050)
 *   branch +0x4a -> +0x50
 *   branch +0x54 -> +0x58
 *   branch +0x5e -> +0x68
 *   branch +0x66 -> +0x6e
 *   branch +0x76 -> +0xa4
 *   branch +0x80 -> +0x8e
 *   branch +0x8c -> +0x98
 *   test +0x48 tst r2, r0
 *   test +0x52 tst r0, r2
 *   test +0x5c cmp r4, r0
 *   test +0x74 cmp r1, r0
 *   test +0x7c cmp r4, r0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02203228; the literal pool and
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

extern u8 native_data_0220bb48[];
extern void native_fn_02002480(void);
extern void native_fn_02004308(void);
extern void native_fn_02204974(void);


asm u32 native_ov006_02203228 (register u32 a0)
{
    push {r3, r4, r5, lr}
    sub sp, #0x8
    add r4, r1, #0x0
    ldr r1, =native_data_0220bb48
    add r5, r0, #0x0
    ldrb r2, [r1, #0x4]
    add r0, sp, #0x0
    strb r2, [r0, #0x4]
    ldrb r2, [r1, #0x5]
    strb r2, [r0, #0x5]
    ldrb r2, [r1, #0x6]
    strb r2, [r0, #0x6]
    ldrb r2, [r1, #0x7]
    strb r2, [r0, #0x7]
    ldrb r2, [r1, #0]
    strb r2, [r0, #0]
    ldrb r2, [r1, #0x1]
    strb r2, [r0, #0x1]
    ldrb r2, [r1, #0x2]
    strb r2, [r0, #0x2]
    ldrb r1, [r1, #0x3]
    strb r1, [r0, #0x3]
    mov r0, #0x4
    ldrsh r1, [r4, r0]
    add r1, r1, #0x1
    strh r1, [r4, #0x4]
    ldrsh r0, [r4, r0]
    ldrh r1, [r4, #0x6]
    lsl r0, r0, #0x4
    blx native_fn_02002480
    add r1, r0, #0x0
    ldrb r2, [r4, #0x8]
    add r0, sp, #0x4
    ldrb r0, [r0, r2]
    mov r2, #0x1
    tst r2, r0
    beq ov006_02203228_L50
    mov r2, #0x10
    sub r1, r2, r1
ov006_02203228_L50:
    mov r2, #0x10
    tst r0, r2
    beq ov006_02203228_L58
    neg r1, r1
ov006_02203228_L58:
    ldr r0, =0x0221c180
    ldr r0, [r0, #0]
    cmp r4, r0
    bne ov006_02203228_L68
    ldr r0, =0x04001050
    blx native_fn_02004308
    b ov006_02203228_L6e
ov006_02203228_L68:
    ldr r0, =0x04000050
    blx native_fn_02004308
ov006_02203228_L6e:
    mov r0, #0x4
    ldrsh r1, [r4, r0]
    ldrh r0, [r4, #0x6]
    cmp r1, r0
    blt ov006_02203228_La4
    ldr r0, =0x0221c180
    ldr r0, [r0, #0]
    cmp r4, r0
    add r1, sp, #0x0
    bne ov006_02203228_L8e
    ldrb r2, [r4, #0x8]
    ldr r0, =0x04001050
    ldrsb r1, [r1, r2]
    blx native_fn_02004308
    b ov006_02203228_L98
ov006_02203228_L8e:
    ldrb r2, [r4, #0x8]
    ldr r0, =0x04000050
    ldrsb r1, [r1, r2]
    blx native_fn_02004308
ov006_02203228_L98:
    mov r0, #0x0
    strb r0, [r4, #0x9]
    mov r0, #0x1
    add r1, r5, #0x0
    bl native_fn_02204974
ov006_02203228_La4:
    add sp, #0x8
    pop {r3, r4, r5, pc}
}
