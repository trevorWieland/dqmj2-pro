/* ov006 row 0x021f8f4c: 300 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x11c -> constant 0x0000e01d (image word 0x0000e01d)
 *   pool +0x120 -> native_data9_0221c0e0 (image word 0x0221c0e0)
 *   pool +0x124 -> native_fn2_021f907c+1 (image word 0x021f907d)
 *   pool +0x128 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   branch +0x0a -> +0x22
 *   branch +0x0e -> +0x1c
 *   branch +0x10 -> +0x28
 *   branch +0x14 -> +0x6e
 *   branch +0x18 -> +0x86
 *   branch +0x1a -> +0xcc
 *   branch +0x1e -> +0x112
 *   branch +0x20 -> +0xcc
 *   branch +0x26 -> +0xcc
 *   branch +0x32 -> +0x112
 *   branch +0x60 -> +0x66
 *   branch +0x6c -> +0x112
 *   branch +0x8c -> +0xa0
 *   branch +0x9e -> +0xb0
 *   branch +0xd6 -> +0x112
 *   branch +0x10a -> +0x112
 *   test +0x08 cmp r4, #0x83
 *   test +0x0c cmp r4, #0x80
 *   test +0x12 cmp r4, #0x82
 *   test +0x16 cmp r4, #0x83
 *   test +0x1c cmp r4, #0x0
 *   test +0x24 cmp r4, r0
 *   test +0x30 cmp r0, #0x0
 *   test +0x5e cmp r1, #0x0
 *   test +0x8a cmp r0, #0x0
 *   test +0xd4 cmp r0, #0x20
 *   test +0x108 cmp r0, #0x20
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8f4c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 15 of 300 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021f2f18(void);
extern u8 native_data9_0221c0e0[];
extern void native_fn_021ff6d4(void);
extern void native_fn_021f2f28(void);
extern void native_fn_021f2f3c(void);
extern void native_fn2_021f907c(void);
extern void ov006_main_loop_set_callback_021f52cc(void);
extern void native_fn_021f9384(void);
extern void native_fn_021f91f4(void);
extern void native_fn_021f9288(void);


asm u32 native_ov006_021f8f4c (register u32 a0)
{
    push {r4, lr}
    bl native_fn_021f2f18
    add r4, r0, #0x0
    cmp r4, #0x83
    bgt ov006_021f8f4c_L22
    cmp r4, #0x80
    blt ov006_021f8f4c_L1c
    beq ov006_021f8f4c_L28
    cmp r4, #0x82
    beq ov006_021f8f4c_L6e
    cmp r4, #0x83
    beq ov006_021f8f4c_L86
    b ov006_021f8f4c_Lcc
ov006_021f8f4c_L1c:
    cmp r4, #0x0
    beq ov006_021f8f4c_L112
    b ov006_021f8f4c_Lcc
ov006_021f8f4c_L22:
    ldr r0, =0x0000e01d
    cmp r4, r0
    b ov006_021f8f4c_Lcc
ov006_021f8f4c_L28:
    ldr r0, =native_data9_0221c0e0
    ldr r0, [r0, #0]
    add r0, #0x29
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f8f4c_L112
    mov r0, #0x3
    bl native_fn_021ff6d4
    ldr r2, =native_data9_0221c0e0
    ldr r1, [r2, #0]
    add r0, r1, #0x0
    add r0, #0x29
    ldrb r0, [r0, #0]
    add r1, #0x29
    sub r0, r0, #0x1
    strb r0, [r1, #0]
    ldr r3, [r2, #0]
    mov r0, #0x0
    add r1, r3, #0x0
    add r1, #0x29
    ldrb r1, [r1, #0]
    add r1, r3, r1
    strb r0, [r1, #0x8]
    ldr r1, [r2, #0]
    add r1, #0x29
    ldrb r1, [r1, #0]
    cmp r1, #0x0
    bne ov006_021f8f4c_L66
    bl native_fn_021f2f28
ov006_021f8f4c_L66:
    mov r0, #0x1
    bl native_fn_021f2f3c
    b ov006_021f8f4c_L112
ov006_021f8f4c_L6e:
    mov r0, #0x7
    bl native_fn_021ff6d4
    ldr r0, =native_data9_0221c0e0
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r0, #0x2a
    strb r1, [r0, #0]
    ldr r0, =native_fn2_021f907c+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r4, pc}
ov006_021f8f4c_L86:
    bl native_fn_021f9384
    cmp r0, #0x0
    beq ov006_021f8f4c_La0
    mov r0, #0x6
    bl native_fn_021ff6d4
    ldr r0, =native_data9_0221c0e0
    mov r1, #0x1
    ldr r0, [r0, #0]
    add r0, #0x2a
    strb r1, [r0, #0]
    b ov006_021f8f4c_Lb0
ov006_021f8f4c_La0:
    ldr r0, =native_data9_0221c0e0
    mov r1, #0x2
    ldr r0, [r0, #0]
    add r0, #0x2a
    strb r1, [r0, #0]
    mov r0, #0x9
    bl native_fn_021ff6d4
ov006_021f8f4c_Lb0:
    ldr r0, =native_data9_0221c0e0
    ldr r0, [r0, #0]
    ldr r2, [r0, #0x4]
    ldr r0, =0xc1fffcff
    ldr r1, [r2, #0]
    and r1, r0
    mov r0, #0x2
    lsl r0, r0, #0x8
    orr r0, r1
    str r0, [r2, #0]
    ldr r0, =native_fn2_021f907c+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r4, pc}
ov006_021f8f4c_Lcc:
    ldr r0, =native_data9_0221c0e0
    ldr r0, [r0, #0]
    add r0, #0x29
    ldrb r0, [r0, #0]
    cmp r0, #0x20
    beq ov006_021f8f4c_L112
    mov r0, #0x1
    bl native_fn_021ff6d4
    ldr r1, =native_data9_0221c0e0
    ldr r2, [r1, #0]
    add r0, r2, #0x0
    add r0, #0x29
    ldrb r0, [r0, #0]
    add r0, r2, r0
    strb r4, [r0, #0x8]
    ldr r1, [r1, #0]
    add r0, r1, #0x0
    add r0, #0x29
    ldrb r0, [r0, #0]
    add r1, #0x29
    add r0, r0, #0x1
    strb r0, [r1, #0]
    mov r0, #0x1
    bl native_fn_021f2f28
    ldr r0, =native_data9_0221c0e0
    ldr r0, [r0, #0]
    add r0, #0x29
    ldrb r0, [r0, #0]
    cmp r0, #0x20
    bne ov006_021f8f4c_L112
    mov r0, #0x0
    bl native_fn_021f2f3c
ov006_021f8f4c_L112:
    bl native_fn_021f91f4
    bl native_fn_021f9288
    pop {r4, pc}
}
