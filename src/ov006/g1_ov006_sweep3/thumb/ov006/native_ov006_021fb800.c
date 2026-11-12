/* ov006 row 0x021fb800: 108 bytes.
 *
 * What it does: 50 instructions; 1 call(s) to 0x021fb820; loops (back edge at +0x5c); returns through bx lr; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x64 -> native_data_0220b704 (image word 0x0220b704)
 *   pool +0x68 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   branch +0x24 -> +0x56
 *   branch +0x34 -> +0x46
 *   back edge +0x5c -> +0x20
 *   test +0x22 cmp r3, r2
 *   test +0x32 tst r1, r0
 *   test +0x5a cmp r0, #0x4
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb800; the literal pool and
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

extern u8 native_data_0220b704[];


asm u32 native_ov006_021fb800 (register u32 a0)
{
    push {r3}
    sub sp, #0x4
    ldr r2, =native_data_0220b704
    add r0, sp, #0x0
    ldrb r3, [r2, #0]
    add r1, sp, #0x0
    strb r3, [r0, #0]
    ldrb r3, [r2, #0x1]
    strb r3, [r0, #0x1]
    ldrb r3, [r2, #0x2]
    ldrb r2, [r2, #0x3]
    strb r3, [r0, #0x2]
    strb r2, [r0, #0x3]
    ldr r2, =0x0221c0ec
    mov r0, #0x0
    ldrb r3, [r2, #0]
ov006_021fb800_L20:
    ldrb r2, [r1, #0]
    cmp r3, r2
    bne ov006_021fb800_L56
    ldr r2, =0x0221c0ec
    mov r3, #0x14
    ldr r1, [r2, #0x8]
    add r1, r1, r0
    strb r3, [r1, #0x4]
    mov r1, #0x1
    tst r1, r0
    beq ov006_021fb800_L46
    ldr r1, [r2, #0x8]
    sub r0, r0, #0x1
    mov r3, #0x0
    add r0, r1, r0
    add sp, #0x4
    strb r3, [r0, #0x4]
    pop {r3}
    bx lr
ov006_021fb800_L46:
    ldr r1, [r2, #0x8]
    add r0, r0, #0x1
    mov r3, #0x0
    add r0, r1, r0
    add sp, #0x4
    strb r3, [r0, #0x4]
    pop {r3}
    bx lr
ov006_021fb800_L56:
    add r0, r0, #0x1
    add r1, r1, #0x1
    cmp r0, #0x4
    blt ov006_021fb800_L20
    add sp, #0x4
    pop {r3}
    bx lr
}
