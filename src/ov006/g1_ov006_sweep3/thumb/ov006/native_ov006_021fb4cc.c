/* ov006 row 0x021fb4cc: 132 bytes.
 *
 * What it does: 54 instructions; 3 call(s) to 0x021fb506, 0x021f2948, 0x021f2948; loops (back edge at +0x14); returns through pop {r4, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x70 -> native_data_0220b720 (image word 0x0220b720)
 *   pool +0x74 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   pool +0x78 -> native_data_0220b7aa (image word 0x0220b7aa)
 *   pool +0x7c -> native_data_0220b7ae (image word 0x0220b7ae)
 *   pool +0x80 -> native_data_0220b7ac (image word 0x0220b7ac)
 *   back edge +0x14 -> +0x0a
 *   branch +0x20 -> +0x3a
 *   test +0x1e cmp r1, #0x3
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb4cc; the literal pool and
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

extern u8 native_data_0220b720[];
extern u8 native_data_0220b7aa[];
extern u8 native_data_0220b7ae[];
extern u8 native_data_0220b7ac[];
extern void native_fn_021f2948(void);


asm u32 native_ov006_021fb4cc (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x18
    ldr r3, =native_data_0220b720
    add r2, sp, #0x8
    mov r1, #0xe
ov006_021fb4cc_La:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021fb4cc_La
    ldr r0, =0x0221c0ec
    add r1, sp, #0x8
    ldrb r2, [r0, #0]
    ldrb r1, [r1, r2]
    cmp r1, #0x3
    blt ov006_021fb4cc_L3a
    lsl r4, r1, #0x3
    ldr r1, =native_data_0220b7aa
    ldr r2, =native_data_0220b7ae
    ldr r3, =native_data_0220b7ac
    ldrh r1, [r1, r4]
    ldrh r2, [r2, r4]
    ldrh r3, [r3, r4]
    mov r0, #0x3
    bl native_fn_021f2948
    add sp, #0x18
    pop {r4, pc}
ov006_021fb4cc_L3a:
    lsl r3, r1, #0x3
    ldr r1, =native_data_0220b7aa
    add r2, r1, r3
    ldrh r1, [r1, r3]
    add r3, sp, #0x0
    strh r1, [r3, #0]
    ldrh r1, [r2, #0x2]
    strh r1, [r3, #0x2]
    ldrh r1, [r2, #0x4]
    strh r1, [r3, #0x4]
    ldrh r1, [r2, #0x6]
    strh r1, [r3, #0x6]
    ldrb r1, [r0, #0x2]
    mov r0, #0x1d
    ldrh r2, [r3, #0x2]
    mul r0, r1
    add r0, r2, r0
    strh r0, [r3, #0x2]
    ldrh r1, [r3, #0]
    ldrh r2, [r3, #0x4]
    ldrh r3, [r3, #0x2]
    mov r0, #0x1
    bl native_fn_021f2948
    add sp, #0x18
    pop {r4, pc}
    mov r8, r8
}
