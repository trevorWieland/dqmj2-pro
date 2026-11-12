/* ov006 row 0x021fd0a4: 120 bytes.
 *
 * What it does: 53 instructions; 4 call(s) to 0x021fe580, 0x021ff0bc, 0x021fd0f6, +1 more; no back edge; returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x70 -> native_data_0220b80c (image word 0x0220b80c)
 *   pool +0x74 -> constant 0x0221c10c (image word 0x0221c10c)
 *   branch +0x30 -> +0x6c
 *   branch +0x44 -> +0x6c
 *   branch +0x4e -> +0x52
 *   test +0x2e cmp r1, #0x3
 *   test +0x42 cmp r0, #0x3
 *   test +0x4c cmp r3, #0x2
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fd0a4; the literal pool and
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

extern u8 native_data_0220b80c[];
extern void native_fn_021fe580(void);
extern void native_fn_021ff0bc(void);
extern void native_fn_02202e50(void);


asm u32 native_ov006_021fd0a4 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    ldr r2, =native_data_0220b80c
    add r1, sp, #0x0
    ldrb r3, [r2, #0]
    add r0, sp, #0x4
    strb r3, [r1, #0x4]
    ldrb r3, [r2, #0x1]
    strb r3, [r1, #0x5]
    ldrb r3, [r2, #0x2]
    strb r3, [r1, #0x6]
    ldrb r3, [r2, #0x3]
    strb r3, [r1, #0x7]
    ldrb r3, [r2, #0x4]
    strb r3, [r1, #0]
    ldrb r3, [r2, #0x5]
    strb r3, [r1, #0x1]
    ldrb r3, [r2, #0x6]
    strb r3, [r1, #0x2]
    ldrb r2, [r2, #0x7]
    strb r2, [r1, #0x3]
    ldr r2, =0x0221c10c
    ldrb r1, [r2, #0]
    cmp r1, #0x3
    bhi ov006_021fd0a4_L6c
    ldrb r1, [r0, r1]
    ldr r0, [r2, #0x4]
    ldr r0, [r0, #0]
    add r2, r1, #0x0
    bl native_fn_021fe580
    ldr r0, =0x0221c10c
    ldrb r0, [r0, #0]
    cmp r0, #0x3
    beq ov006_021fd0a4_L6c
    bl native_fn_021ff0bc
    add r3, r0, #0x0
    cmp r3, #0x2
    ble ov006_021fd0a4_L52
    mov r3, #0x3
ov006_021fd0a4_L52:
    ldr r0, =0x0221c10c
    add r4, sp, #0x0
    ldr r1, [r0, #0x4]
    ldrb r0, [r0, #0]
    ldrb r3, [r4, r3]
    mov r2, #0x0
    lsl r0, r0, #0x2
    add r0, r1, r0
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    bl native_fn_02202e50
ov006_021fd0a4_L6c:
    add sp, #0x8
    pop {r4, pc}
}
