/* ov006 row 0x021f9384: 220 bytes.
 *
 * What it does: 104 instructions; 13 call(s) to 0x021f530c, 0x021f26f0, 0x021f530c, +10 more; loops (back edge at +0x08); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd8 -> constant 0x0221c0e0 (image word 0x0221c0e0)
 *   branch +0x10 -> +0x1e
 *   branch +0x2a -> +0x42
 *   branch +0x34 -> +0x3c
 *   branch +0x46 -> +0x58
 *   branch +0x50 -> +0x58
 *   branch +0x66 -> +0x86
 *   branch +0x6a -> +0x78
 *   branch +0x6c -> +0x9a
 *   branch +0x70 -> +0x94
 *   branch +0x74 -> +0x94
 *   branch +0x76 -> +0xd2
 *   branch +0x7a -> +0x80
 *   branch +0x7c -> +0x94
 *   branch +0x7e -> +0xd2
 *   branch +0x82 -> +0x94
 *   branch +0x84 -> +0xd2
 *   branch +0x88 -> +0x8e
 *   branch +0x8a -> +0x9a
 *   branch +0x8c -> +0xd2
 *   branch +0x90 -> +0x9a
 *   branch +0x92 -> +0xd2
 *   branch +0x9e -> +0xcc
 *   branch +0xa8 -> +0xae
 *   branch +0xac -> +0xc4
 *   branch +0xb0 -> +0xb6
 *   branch +0xb4 -> +0xc4
 *   branch +0xb8 -> +0xbe
 *   branch +0xbc -> +0xc4
 *   back edge +0xca -> +0xa4
 *   test +0x0e cmp r0, #0x1
 *   test +0x28 cmp r0, #0x0
 *   test +0x32 cmp r0, #0x0
 *   test +0x44 cmp r0, #0x1
 *   test +0x4e cmp r0, #0x0
 *   test +0x64 cmp r0, #0x10
 *   test +0x68 cmp r0, #0xa
 *   test +0x6e cmp r0, #0xd
 *   test +0x72 cmp r0, #0x10
 *   test +0x78 cmp r0, #0x0
 *   test +0x80 cmp r0, #0x5
 *   test +0x86 cmp r0, #0x1a
 *   test +0x8e cmp r0, #0x20
 *   test +0x9c cmp r0, #0x0
 *   test +0xa6 cmp r1, #0x30
 *   test +0xaa cmp r1, #0x39
 *   test +0xae cmp r1, #0x41
 *   test +0xb2 cmp r1, #0x46
 *   test +0xb6 cmp r1, #0x61
 *   test +0xba cmp r1, #0x66
 *   test +0xc8 cmp r2, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9384; the literal pool and
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

extern void native_fn_021f530c(void);
extern void native_fn_021f26f0(void);
extern void native_fn_022045c8(void);


asm u32 native_ov006_021f9384 (register u32 a0)
{
    push {r3, lr}
    sub sp, #0x8
    add r0, sp, #0x4
    add r1, sp, #0x0
    bl native_fn_021f530c
    ldr r0, [sp]
    cmp r0, #0x1
    bne ov006_021f9384_L1e
    mov r0, #0x35
    add r1, r0, #0x0
    sub r1, #0x36
    mov r2, #0x0
    bl native_fn_021f26f0
ov006_021f9384_L1e:
    add r0, sp, #0x4
    add r1, sp, #0x0
    bl native_fn_021f530c
    ldr r0, [sp, #0x4]
    cmp r0, #0x0
    bne ov006_021f9384_L42
    ldr r0, =0x0221c0e0
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x8]
    cmp r0, #0x0
    beq ov006_021f9384_L3c
    add sp, #0x8
    mov r0, #0x1
    pop {r3, pc}
ov006_021f9384_L3c:
    add sp, #0x8
    mov r0, #0x0
    pop {r3, pc}
ov006_021f9384_L42:
    ldr r0, [sp]
    cmp r0, #0x1
    bne ov006_021f9384_L58
    ldr r0, =0x0221c0e0
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x8]
    cmp r0, #0x0
    bne ov006_021f9384_L58
    add sp, #0x8
    mov r0, #0x0
    pop {r3, pc}
ov006_021f9384_L58:
    ldr r0, =0x0221c0e0
    mov r1, #0x20
    ldr r0, [r0, #0]
    add r0, #0x8
    bl native_fn_022045c8
    cmp r0, #0x10
    bgt ov006_021f9384_L86
    cmp r0, #0xa
    blt ov006_021f9384_L78
    beq ov006_021f9384_L9a
    cmp r0, #0xd
    beq ov006_021f9384_L94
    cmp r0, #0x10
    beq ov006_021f9384_L94
    b ov006_021f9384_Ld2
ov006_021f9384_L78:
    cmp r0, #0x0
    bgt ov006_021f9384_L80
    beq ov006_021f9384_L94
    b ov006_021f9384_Ld2
ov006_021f9384_L80:
    cmp r0, #0x5
    beq ov006_021f9384_L94
    b ov006_021f9384_Ld2
ov006_021f9384_L86:
    cmp r0, #0x1a
    bgt ov006_021f9384_L8e
    beq ov006_021f9384_L9a
    b ov006_021f9384_Ld2
ov006_021f9384_L8e:
    cmp r0, #0x20
    beq ov006_021f9384_L9a
    b ov006_021f9384_Ld2
ov006_021f9384_L94:
    add sp, #0x8
    mov r0, #0x1
    pop {r3, pc}
ov006_021f9384_L9a:
    mov r2, #0x0
    cmp r0, #0x0
    ble ov006_021f9384_Lcc
    ldr r1, =0x0221c0e0
    ldr r3, [r1, #0]
ov006_021f9384_La4:
    ldrb r1, [r3, #0x8]
    cmp r1, #0x30
    blo ov006_021f9384_Lae
    cmp r1, #0x39
    bls ov006_021f9384_Lc4
ov006_021f9384_Lae:
    cmp r1, #0x41
    blo ov006_021f9384_Lb6
    cmp r1, #0x46
    bls ov006_021f9384_Lc4
ov006_021f9384_Lb6:
    cmp r1, #0x61
    blo ov006_021f9384_Lbe
    cmp r1, #0x66
    bls ov006_021f9384_Lc4
ov006_021f9384_Lbe:
    add sp, #0x8
    mov r0, #0x0
    pop {r3, pc}
ov006_021f9384_Lc4:
    add r2, r2, #0x1
    add r3, r3, #0x1
    cmp r2, r0
    blt ov006_021f9384_La4
ov006_021f9384_Lcc:
    add sp, #0x8
    mov r0, #0x1
    pop {r3, pc}
ov006_021f9384_Ld2:
    mov r0, #0x0
    add sp, #0x8
    pop {r3, pc}
}
