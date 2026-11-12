/* ov006 row 0x02201eb4: 160 bytes.
 *
 * What it does: 75 instructions; 1 call(s) to 0x02018604; loops (back edge at +0x56); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x98 -> constant 0x0221c16c (image word 0x0221c16c)
 *   pool +0x9c -> constant 0x00000a98 (image word 0x00000a98)
 *   branch +0x0e -> +0x20
 *   branch +0x12 -> +0x20
 *   branch +0x16 -> +0x20
 *   branch +0x1a -> +0x20
 *   branch +0x1e -> +0x36
 *   branch +0x38 -> +0x46
 *   branch +0x3c -> +0x46
 *   branch +0x40 -> +0x46
 *   branch +0x44 -> +0x72
 *   branch +0x48 -> +0x56
 *   branch +0x50 -> +0x56
 *   branch +0x7c -> +0x86
 *   branch +0x88 -> +0x92
 *   test +0x0c cmp r3, #0x1
 *   test +0x10 cmp r3, #0x14
 *   test +0x14 cmp r3, #0x17
 *   test +0x18 cmp r3, #0x1a
 *   test +0x1c cmp r3, #0x1d
 *   test +0x36 cmp r3, #0x4
 *   test +0x3a cmp r3, #0x5
 *   test +0x3e cmp r3, #0x6
 *   test +0x42 cmp r3, #0xd
 *   test +0x46 cmp r3, #0x4
 *   test +0x4e cmp r0, #0x6
 *   test +0x7a cmp r1, #0x1
 *   test +0x86 cmp r3, #0xc
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02201eb4; the literal pool and
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

extern void native_fn_02018604(void);


asm u32 native_ov006_02201eb4 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =0x0221c16c
    mov r2, #0xa9
    ldr r0, [r0, #0]
    lsl r2, r2, #0x4
    ldrb r3, [r0, r2]
    cmp r3, #0x1
    beq ov006_02201eb4_L20
    cmp r3, #0x14
    beq ov006_02201eb4_L20
    cmp r3, #0x17
    beq ov006_02201eb4_L20
    cmp r3, #0x1a
    beq ov006_02201eb4_L20
    cmp r3, #0x1d
    bne ov006_02201eb4_L36
ov006_02201eb4_L20:
    mov r1, #0xa9
    mov r2, #0x22
    lsl r1, r1, #0x4
    strb r2, [r0, r1]
    ldr r0, =0x0221c16c
    mov r2, #0x0
    ldr r0, [r0, #0]
    add r1, #0x1c
    strb r2, [r0, r1]
    mov r0, #0x1
    pop {r3, pc}
ov006_02201eb4_L36:
    cmp r3, #0x4
    beq ov006_02201eb4_L46
    cmp r3, #0x5
    beq ov006_02201eb4_L46
    cmp r3, #0x6
    beq ov006_02201eb4_L46
    cmp r3, #0xd
    bne ov006_02201eb4_L72
ov006_02201eb4_L46:
    cmp r3, #0x4
    bne ov006_02201eb4_L56
    ldr r1, =0x00000a98
    ldr r0, [r0, r1]
    cmp r0, #0x6
    bhs ov006_02201eb4_L56
    mov r0, #0x0
    pop {r3, pc}
ov006_02201eb4_L56:
    blx native_fn_02018604
    ldr r1, =0x0221c16c
    mov r0, #0xa9
    ldr r2, [r1, #0]
    mov r3, #0x10
    lsl r0, r0, #0x4
    strb r3, [r2, r0]
    ldr r1, [r1, #0]
    mov r2, #0x2
    add r0, #0x1c
    strb r2, [r1, r0]
    mov r0, #0x1
    pop {r3, pc}
ov006_02201eb4_L72:
    add r1, r3, #0x0
    add r1, #0xf7
    lsl r1, r1, #0x18
    lsr r1, r1, #0x18
    cmp r1, #0x1
    bhi ov006_02201eb4_L86
    mov r1, #0x20
    strb r1, [r0, r2]
    mov r0, #0x1
    pop {r3, pc}
ov006_02201eb4_L86:
    cmp r3, #0xc
    bne ov006_02201eb4_L92
    mov r1, #0x22
    strb r1, [r0, r2]
    mov r0, #0x1
    pop {r3, pc}
ov006_02201eb4_L92:
    mov r0, #0x0
    pop {r3, pc}
    mov r8, r8
}
