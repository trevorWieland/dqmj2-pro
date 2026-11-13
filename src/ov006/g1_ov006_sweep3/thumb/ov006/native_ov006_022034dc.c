/* ov006 row 0x022034dc: 252 bytes.
 *
 * What it does: 103 instructions; 7 call(s) to 0x02203c08, 0x0203631c, 0x02003e88, +4 more; loops (back edge at +0x72); returns through pop {r4, r5, r6, r7, pc}; 8 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xdc -> constant 0x0221c184 (image word 0x0221c184)
 *   pool +0xe0 -> native_data_0220bb5a (image word 0x0220bb5a)
 *   pool +0xe4 -> native_data_0220bb58 (image word 0x0220bb58)
 *   pool +0xe8 -> constant 0x04001008 (image word 0x04001008)
 *   pool +0xec -> constant 0x04000008 (image word 0x04000008)
 *   pool +0xf0 -> native_data_0220bb54 (image word 0x0220bb54)
 *   pool +0xf4 -> native_fn_022035d8+1 (image word 0x022035d9)
 *   pool +0xf8 -> constant 0x0000067c (image word 0x0000067c)
 *   branch +0x32 -> +0x4e
 *   branch +0x4c -> +0x66
 *   branch +0x8c -> +0x94
 *   branch +0x92 -> +0x98
 *   test +0x30 cmp r5, #0x1
 *   test +0x8a cmp r5, #0x1
 *   0 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022034dc; the literal pool and
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

extern u8 native_data_0220bb5a[];
extern u8 native_data_0220bb58[];
extern void ov006_clear_buffer_02203c08(void);
extern void native_fn_0203631c(void);
extern void native_fn_02003e88(void);
extern void native_fn_02003e54(void);
extern u8 native_data_0220bb54[];
extern void native_fn_020363d0(void);
extern void native_fn_0220383c(void);
extern void native_fn_022035d8(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_022034dc (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    add r5, r0, #0x0
    ldr r0, =0x0221c184
    str r1, [sp, #0x10]
    ldr r1, [r0, #0]
    mov r0, #0x61
    lsl r0, r0, #0x4
    add r1, r1, r0
    mov r0, #0x30
    mul r0, r5
    add r4, r1, r0
    ldr r0, =native_data_0220bb5a
    lsl r1, r5, #0x2
    ldrh r6, [r0, r1]
    ldr r0, =native_data_0220bb58
    ldrh r7, [r0, r1]
    mov r1, #0x20
    add r0, r7, #0x0
    mul r0, r6
    lsl r0, r0, #0x5
    bl ov006_clear_buffer_02203c08
    str r0, [r4, #0x28]
    cmp r5, #0x1
    bne ov006_022034dc_L4e
    ldr r0, =0x04001008
    mov r1, #0x40
    ldrh r2, [r0, #0]
    bic r2, r1
    strh r2, [r0, #0]
    ldrh r2, [r0, #0]
    mov r1, #0x43
    and r2, r1
    mov r1, #0x3
    lsl r1, r1, #0xa
    orr r1, r2
    strh r1, [r0, #0]
    b ov006_022034dc_L66
ov006_022034dc_L4e:
    ldr r0, =0x04000008
    mov r1, #0x40
    ldrh r2, [r0, #0]
    bic r2, r1
    strh r2, [r0, #0]
    ldrh r2, [r0, #0]
    mov r1, #0x43
    and r2, r1
    mov r1, #0x3
    lsl r1, r1, #0xa
    orr r1, r2
    strh r1, [r0, #0]
ov006_022034dc_L66:
    mov r0, #0x4
    str r0, [sp]
    ldr r1, [r4, #0x28]
    add r0, r4, #0x0
    add r2, r7, #0x0
    add r3, r6, #0x0
    blx native_fn_0203631c
    ldr r0, =0x0221c184
    ldr r1, [r0, #0]
    ldr r0, [sp, #0x10]
    str r4, [r4, #0x18]
    lsl r0, r0, #0x3
    add r0, r1, r0
    str r0, [r4, #0x1c]
    mov r0, #0x1
    str r0, [r4, #0x20]
    str r0, [r4, #0x24]
    cmp r5, #0x1
    bne ov006_022034dc_L94
    blx native_fn_02003e88
    b ov006_022034dc_L98
ov006_022034dc_L94:
    blx native_fn_02003e54
ov006_022034dc_L98:
    mov r3, #0x0
    add r2, r0, #0x0
    str r3, [sp]
    mov r0, #0x20
    str r0, [sp, #0x4]
    ldr r0, =native_data_0220bb54
    lsl r1, r5, #0x1
    ldrh r0, [r0, r1]
    add r1, r7, #0x0
    str r0, [sp, #0x8]
    mov r0, #0xf
    str r0, [sp, #0xc]
    add r0, r2, #0x0
    add r2, r6, #0x0
    blx native_fn_020363d0
    add r0, r4, #0x0
    mov r1, #0x0
    bl native_fn_0220383c
    ldr r2, =0x0221c184
    ldr r1, =native_fn_022035d8+1
    ldr r3, [r2, #0]
    ldr r2, =0x0000067c
    mov r0, #0x1
    add r2, r3, r2
    add r2, r2, r5
    mov r3, #0xc8
    bl native_fn_0220490c
    str r0, [r4, #0x2c]
    add r0, r4, #0x0
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
}
