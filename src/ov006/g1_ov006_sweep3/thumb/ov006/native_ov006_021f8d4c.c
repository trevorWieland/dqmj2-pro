/* ov006 row 0x021f8d4c: 208 bytes.
 *
 * What it does: 82 instructions; 14 call(s) to 0x02203c08, 0x021f530c, 0x021fefb8, +11 more; loops (back edge at +0x20); returns through pop {pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xc0 -> native_data_0220b65c (image word 0x0220b65c)
 *   pool +0xc4 -> constant 0x0221c0e0 (image word 0x0221c0e0)
 *   pool +0xc8 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0xcc -> native_fn_021f8e9c+1 (image word 0x021f8e9d)
 *   branch +0x28 -> +0x48
 *   branch +0x58 -> +0x68
 *   branch +0x66 -> +0x78
 *   test +0x26 cmp r0, #0x0
 *   test +0x56 cmp r0, #0x1
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8d4c; the literal pool and
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

extern u8 native_data_0220b65c[];
extern void ov006_clear_buffer_02203c08(void);
extern void native_fn_021f530c(void);
extern void native_fn_021fefb8(void);
extern void native_fn_022045c8(void);
extern void native_fn_021f8e1c(void);
extern void native_fn_021f2ad4(void);
extern void native_fn_021f26f0(void);
extern void native_fn_021f27fc(void);
extern void native_fn_022034dc(void);
extern void native_fn_0220303c(void);
extern void native_fn_021f9288(void);
extern void native_fn_021f91f4(void);
extern void native_fn_021f8e9c(void);
extern void ov006_main_loop_set_callback_021f52cc(void);


asm u32 native_ov006_021f8d4c (register u32 a0)
{
    push {lr}
    sub sp, #0xc
    ldr r1, =native_data_0220b65c
    add r0, sp, #0x0
    ldrb r2, [r1, #0]
    ldrb r1, [r1, #0x1]
    strb r2, [r0, #0]
    strb r1, [r0, #0x1]
    mov r0, #0x2c
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r1, =0x0221c0e0
    str r0, [r1, #0]
    add r0, sp, #0x8
    add r1, sp, #0x4
    bl native_fn_021f530c
    ldr r0, [sp, #0x8]
    cmp r0, #0x0
    bne ov006_021f8d4c_L48
    ldr r0, =0x0221c0e0
    ldr r0, [r0, #0]
    add r0, #0x8
    bl native_fn_021fefb8
    ldr r0, =0x0221c0e0
    mov r1, #0x20
    ldr r0, [r0, #0]
    add r0, #0x8
    bl native_fn_022045c8
    ldr r1, =0x0221c0e0
    ldr r1, [r1, #0]
    add r1, #0x29
    strb r0, [r1, #0]
ov006_021f8d4c_L48:
    bl native_fn_021f8e1c
    ldr r0, [sp, #0x8]
    add r0, #0x9
    bl native_fn_021f2ad4
    ldr r0, [sp, #0x4]
    cmp r0, #0x1
    bne ov006_021f8d4c_L68
    mov r0, #0x35
    add r1, r0, #0x0
    sub r1, #0x36
    mov r2, #0x0
    bl native_fn_021f26f0
    b ov006_021f8d4c_L78
ov006_021f8d4c_L68:
    ldr r1, [sp, #0x8]
    add r0, sp, #0x0
    ldrb r0, [r0, r1]
    mov r1, #0x0
    mvn r1, r1
    mov r2, #0x0
    bl native_fn_021f26f0
ov006_021f8d4c_L78:
    mov r0, #0x2
    bl native_fn_021f27fc
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_022034dc
    ldr r1, =0x0221c0e0
    ldr r1, [r1, #0]
    str r0, [r1, #0]
    mov r0, #0x0
    mov r1, #0x3e
    bl native_fn_0220303c
    ldr r1, =0x0221c0e0
    ldr r2, [r1, #0]
    str r0, [r2, #0x4]
    ldr r0, [r1, #0]
    ldr r2, [r0, #0x4]
    ldr r0, =0xfffff3ff
    ldrh r1, [r2, #0x4]
    and r1, r0
    mov r0, #0x3
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r2, #0x4]
    bl native_fn_021f9288
    bl native_fn_021f91f4
    ldr r0, =native_fn_021f8e9c+1
    bl ov006_main_loop_set_callback_021f52cc
    add sp, #0xc
    pop {pc}
    mov r8, r8
}
