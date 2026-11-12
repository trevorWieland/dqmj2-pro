/* ov006 row 0x021fec44: 320 bytes.
 *
 * What it does: 147 instructions; 13 call(s) to 0x020072d0, 0x0201b248, 0x021fec8e, +10 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x134 -> constant 0x0221c144 (image word 0x0221c144)
 *   pool +0x138 -> native_data_0220b9a4 (image word 0x0220b9a4)
 *   pool +0x13c -> native_data_0220b9a0 (image word 0x0220b9a0)
 *   branch +0x2a -> +0x2e
 *   branch +0x2c -> +0x130
 *   branch +0x3c -> +0x114
 *   branch +0x42 -> +0x114
 *   branch +0x58 -> +0x62
 *   back edge +0x60 -> +0x4a
 *   branch +0x64 -> +0x88
 *   branch +0x7a -> +0x84
 *   back edge +0x82 -> +0x6c
 *   branch +0x86 -> +0x130
 *   branch +0xb8 -> +0xc2
 *   branch +0xc0 -> +0x114
 *   branch +0xda -> +0x114
 *   branch +0xe2 -> +0xec
 *   branch +0xea -> +0x114
 *   branch +0xee -> +0x10c
 *   branch +0xf4 -> +0x10c
 *   branch +0x102 -> +0x10c
 *   branch +0x10a -> +0x114
 *   back edge +0x112 -> +0xde
 *   back edge +0x12e -> +0x34
 *   test +0x28 cmp r0, #0x0
 *   test +0x3a cmp r0, #0x0
 *   test +0x40 cmp r0, #0x0
 *   test +0x56 cmp r0, #0x0
 *   test +0x5e cmp r4, #0x14
 *   test +0x62 cmp r4, #0x14
 *   test +0x78 cmp r0, #0x0
 *   test +0x80 cmp r4, #0x14
 *   test +0x84 cmp r4, #0x14
 *   test +0xb6 tst r0, r1
 *   test +0xd8 cmp r6, #0x0
 *   test +0xe0 cmp r0, #0x30
 *   test +0xec cmp r0, #0xdd
 *   test +0xf2 cmp r0, #0x4
 *   test +0x100 cmp r0, #0x0
 *   test +0x110 cmp r4, r6
 *   test +0x12c cmp r0, r1
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fec44; the literal pool and
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

extern void native_fn_020072d0(void);
extern void native_fn_0201b248(void);
extern u8 native_data_0220b9a4[];
extern void native_fn_02008e0c(void);
extern void native_fn_02012464(void);
extern u8 native_data_0220b9a0[];


asm u32 native_ov006_021fec44 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x98
    str r0, [sp]
    ldr r0, =0x0221c144
    ldr r1, [r0, #0]
    mov r0, #0x13
    lsl r0, r0, #0x8
    add r0, r1, r0
    str r0, [sp, #0x10]
    mov r0, #0xf
    lsl r0, r0, #0x8
    add r0, r1, r0
    mov r1, #0x1
    lsl r1, r1, #0xa
    blx native_fn_020072d0
    mov r0, #0x0
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldrh r0, [r0, #0xe]
    cmp r0, #0x0
    bgt ov006_021fec44_L2e
    b ov006_021fec44_L130
ov006_021fec44_L2e:
    ldr r0, [sp]
    str r0, [sp, #0x8]
    str r0, [sp, #0x4]
ov006_021fec44_L34:
    ldr r0, [sp, #0x8]
    ldr r6, [r0, #0x10]
    ldrb r0, [r6, #0xc]
    cmp r0, #0x0
    beq ov006_021fec44_L114
    ldrh r0, [r6, #0x3c]
    cmp r0, #0x0
    bne ov006_021fec44_L114
    ldr r5, [sp, #0x10]
    mov r4, #0x0
    mov r7, #0x6
ov006_021fec44_L4a:
    add r1, r5, #0x0
    add r0, r6, #0x4
    add r1, #0x20
    add r2, r7, #0x0
    blx native_fn_0201b248
    cmp r0, #0x0
    beq ov006_021fec44_L62
    add r4, r4, #0x1
    add r5, #0x2a
    cmp r4, #0x14
    blt ov006_021fec44_L4a
ov006_021fec44_L62:
    cmp r4, #0x14
    bne ov006_021fec44_L88
    ldr r5, [sp, #0x10]
    ldr r7, =native_data_0220b9a4
    mov r4, #0x0
ov006_021fec44_L6c:
    add r0, r5, #0x0
    add r0, #0x20
    add r1, r7, #0x0
    mov r2, #0x6
    blx native_fn_0201b248
    cmp r0, #0x0
    beq ov006_021fec44_L84
    add r4, r4, #0x1
    add r5, #0x2a
    cmp r4, #0x14
    blt ov006_021fec44_L6c
ov006_021fec44_L84:
    cmp r4, #0x14
    beq ov006_021fec44_L130
ov006_021fec44_L88:
    mov r0, #0x2a
    add r1, r4, #0x0
    mul r1, r0
    ldr r0, [sp, #0x10]
    mov r2, #0x6
    add r7, r0, r1
    add r1, r7, #0x0
    add r0, r6, #0x4
    add r1, #0x20
    blx native_fn_02008e0c
    add r0, r6, #0x0
    add r0, #0xc
    add r1, r7, #0x0
    mov r2, #0x20
    blx native_fn_02008e0c
    ldr r0, [sp, #0x4]
    add r0, #0x50
    ldrh r0, [r0, #0]
    strh r0, [r7, #0x26]
    ldrh r1, [r6, #0x2c]
    mov r0, #0x10
    tst r0, r1
    bne ov006_021fec44_Lc2
    mov r0, #0x0
    add r7, #0x28
    strb r0, [r7, #0]
    b ov006_021fec44_L114
ov006_021fec44_Lc2:
    add r0, r7, #0x0
    mov r1, #0x1
    add r0, #0x28
    strb r1, [r0, #0]
    add r0, sp, #0x14
    add r1, r6, #0x0
    blx native_fn_02012464
    add r0, sp, #0x14
    ldrb r6, [r0, #0]
    mov r4, #0x0
    cmp r6, #0x0
    ble ov006_021fec44_L114
    add r5, sp, #0x14
ov006_021fec44_Lde:
    ldrb r0, [r5, #0x4]
    cmp r0, #0x30
    bne ov006_021fec44_Lec
    mov r0, #0x2
    add r7, #0x28
    strb r0, [r7, #0]
    b ov006_021fec44_L114
ov006_021fec44_Lec:
    cmp r0, #0xdd
    bne ov006_021fec44_L10c
    ldrb r0, [r5, #0x5]
    cmp r0, #0x4
    blo ov006_021fec44_L10c
    ldr r0, [r5, #0x8]
    ldr r1, =native_data_0220b9a0
    mov r2, #0x4
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_021fec44_L10c
    mov r0, #0x2
    add r7, #0x28
    strb r0, [r7, #0]
    b ov006_021fec44_L114
ov006_021fec44_L10c:
    add r4, r4, #0x1
    add r5, #0x8
    cmp r4, r6
    blt ov006_021fec44_Lde
ov006_021fec44_L114:
    ldr r0, [sp, #0x8]
    add r0, r0, #0x4
    str r0, [sp, #0x8]
    ldr r0, [sp, #0x4]
    add r0, r0, #0x2
    str r0, [sp, #0x4]
    ldr r0, [sp, #0xc]
    add r0, r0, #0x1
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldrh r1, [r0, #0xe]
    ldr r0, [sp, #0xc]
    cmp r0, r1
    blt ov006_021fec44_L34
ov006_021fec44_L130:
    add sp, #0x98
    pop {r3, r4, r5, r6, r7, pc}
}
