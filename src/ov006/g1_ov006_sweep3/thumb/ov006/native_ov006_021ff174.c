/* ov006 row 0x021ff174: 176 bytes.
 *
 * What it does: 78 instructions; 8 call(s) to 0x02008d78, 0x02008d78, 0x02008e0c, +5 more; loops (back edge at +0x22); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xac -> constant 0x0221c148 (image word 0x0221c148)
 *   back edge +0x22 -> +0x18
 *   branch +0x2c -> +0x50
 *   branch +0x4e -> +0x7a
 *   branch +0x82 -> +0x92
 *   branch +0x90 -> +0xa0
 *   test +0x2a cmp r0, #0x0
 *   test +0x80 cmp r0, #0x0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff174; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02008e0c(void);
extern void native_fn_020a48e4(void);
extern void native_fn_021ff4d8(void);


asm u32 native_ov006_021ff174 (register u32 a0)
{
    push {r4, r5, r6, lr}
    ldr r0, =0x0221c148
    mov r6, #0x1
    ldr r5, [r0, #0]
    lsl r6, r6, #0xa
    add r0, r5, r6
    add r0, #0xf4
    ldrb r0, [r0, #0]
    add r3, r5, r6
    mov r1, #0xf0
    lsl r4, r0, #0x8
    add r2, r5, r4
ov006_021ff174_L18:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021ff174_L18
    add r0, r5, r6
    add r0, #0xf5
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021ff174_L50
    add r0, r5, r4
    add r0, #0xc0
    mov r1, #0x0
    mov r2, #0x4
    blx native_fn_02008d78
    add r0, r5, r4
    add r0, #0xc4
    mov r1, #0x0
    mov r2, #0x4
    blx native_fn_02008d78
    add r0, r5, r4
    mov r1, #0x0
    add r0, #0xd0
    strb r1, [r0, #0]
    b ov006_021ff174_L7a
ov006_021ff174_L50:
    add r0, r5, r6
    add r1, r5, r4
    add r0, #0xc0
    add r1, #0xc0
    mov r2, #0x4
    blx native_fn_02008e0c
    add r0, r5, r6
    add r1, r5, r4
    add r0, #0xc4
    add r1, #0xc4
    mov r2, #0x4
    blx native_fn_02008e0c
    add r0, r5, r6
    add r0, #0xf0
    bl native_fn_020a48e4
    add r1, r5, r4
    add r1, #0xd0
    strb r0, [r1, #0]
ov006_021ff174_L7a:
    add r0, r5, r6
    add r0, #0xf6
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021ff174_L92
    add r0, r5, r4
    add r0, #0xc8
    mov r1, #0x0
    mov r2, #0x8
    blx native_fn_02008d78
    b ov006_021ff174_La0
ov006_021ff174_L92:
    add r0, r5, r6
    add r1, r5, r4
    add r0, #0xc8
    add r1, #0xc8
    mov r2, #0x8
    blx native_fn_02008e0c
ov006_021ff174_La0:
    add r0, r5, r6
    add r0, #0xf4
    ldrb r0, [r0, #0]
    bl native_fn_021ff4d8
    pop {r4, r5, r6, pc}
}
