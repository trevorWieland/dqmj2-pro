/* ov006 row 0x021fcfa0: 232 bytes.
 *
 * What it does: 93 instructions; 15 call(s) to 0x02200574, 0x021ff6d4, 0x021ff440, +12 more; loops (back edge at +0xd0); returns through pop {r3, r4, r5, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd8 -> constant 0x0221c10c (image word 0x0221c10c)
 *   pool +0xdc -> native_data_0220b82a (image word 0x0220b82a)
 *   pool +0xe0 -> native_data_0220b82c (image word 0x0220b82c)
 *   pool +0xe4 -> native_fn_021fd088+1 (image word 0x021fd089)
 *   branch +0x0e -> +0x7c
 *   branch +0x12 -> +0xd4
 *   branch +0x7a -> +0xca
 *   test +0x0c cmp r0, #0x0
 *   test +0x10 cmp r0, #0x1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fcfa0; the literal pool and
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

extern void native_fn_02200574(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_021ff440(void);
extern void native_fn_02202dc0(void);
extern void native_fn_02202ff0(void);
extern u8 native_data_0220b82a[];
extern u8 native_data_0220b82c[];
extern void native_fn_02202eb0(void);
extern void native_fn_02202f54(void);
extern void native_fn_02202d64(void);
extern void native_fn_02200548(void);
extern void native_fn_021fd088(void);
extern void ov006_main_loop_set_callback_021f52cc(void);


asm u32 native_ov006_021fcfa0 (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r0, =0x0221c10c
    ldrb r0, [r0, #0]
    sub r5, r0, #0x4
    bl native_fn_02200574
    cmp r0, #0x0
    beq ov006_021fcfa0_L7c
    cmp r0, #0x1
    bne ov006_021fcfa0_Ld4
    mov r0, #0xe
    bl native_fn_021ff6d4
    add r0, r5, #0x0
    bl native_fn_021ff440
    ldr r0, =0x0221c10c
    lsl r4, r5, #0x2
    ldr r0, [r0, #0x4]
    mov r1, #0x0
    add r0, r0, r4
    ldr r0, [r0, #0x4]
    bl native_fn_02202dc0
    add r2, r0, #0x0
    mov r0, #0x0
    mov r1, #0x56
    bl native_fn_02202ff0
    ldr r0, =0x0221c10c
    ldr r2, =native_data_0220b82a
    ldr r0, [r0, #0x4]
    ldr r3, =native_data_0220b82c
    add r0, r0, r4
    mov r1, #0x0
    ldrh r2, [r2, r4]
    ldrh r3, [r3, r4]
    ldr r0, [r0, #0x4]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =0x0221c10c
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    add r0, r0, r4
    ldr r0, [r0, #0x4]
    mov r2, #0x3
    bl native_fn_02202f54
    ldr r0, =0x0221c10c
    ldr r0, [r0, #0x4]
    add r0, r0, r4
    ldr r0, [r0, #0x10]
    bl native_fn_02202d64
    ldr r0, =0x0221c10c
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r0, r0, r4
    str r1, [r0, #0x10]
    b ov006_021fcfa0_Lca
ov006_021fcfa0_L7c:
    mov r0, #0x7
    bl native_fn_021ff6d4
    ldr r0, =0x0221c10c
    lsl r4, r5, #0x2
    ldr r0, [r0, #0x4]
    mov r1, #0x0
    add r0, r0, r4
    ldr r0, [r0, #0x10]
    bl native_fn_02202dc0
    add r2, r0, #0x0
    mov r0, #0x0
    mov r1, #0x11
    bl native_fn_02202ff0
    add r0, r5, #0x3
    lsl r3, r0, #0x2
    ldr r0, =0x0221c10c
    ldr r2, =native_data_0220b82a
    ldr r0, [r0, #0x4]
    mov r1, #0x0
    add r0, r0, r4
    ldr r5, =native_data_0220b82c
    ldrh r2, [r2, r3]
    ldrh r3, [r5, r3]
    ldr r0, [r0, #0x10]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =0x0221c10c
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    add r0, r0, r4
    ldr r0, [r0, #0x10]
    mov r2, #0x3
    bl native_fn_02202f54
ov006_021fcfa0_Lca:
    bl native_fn_02200548
    ldr r0, =native_fn_021fd088+1
    bl ov006_main_loop_set_callback_021f52cc
ov006_021fcfa0_Ld4:
    pop {r3, r4, r5, pc}
    mov r8, r8
}
