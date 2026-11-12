/* ov006 row 0x021f4e14: 164 bytes.
 *
 * What it does: 66 instructions; 6 call(s) to 0x02203c08, 0x02008be0, 0x02008e0c, +3 more; loops (back edge at +0x1c); returns through pop {r4, r5, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x90 -> constant 0x0221c064 (image word 0x0221c064)
 *   pool +0x94 -> native_data_0220b528 (image word 0x0220b528)
 *   pool +0x98 -> constant 0x00000106 (image word 0x00000106)
 *   pool +0x9c -> native_fn_021f4f30+1 (image word 0x021f4f31)
 *   pool +0xa0 -> native_fn_021f4f3c+1 (image word 0x021f4f3d)
 *   back edge +0x4c -> +0x42
 *   branch +0x86 -> +0x8c
 *   test +0x84 cmp r0, #0x0
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4e14; the literal pool and
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

extern void ov006_clear_buffer_02203c08(void);
extern void native_fn_02008be0(void);
extern u8 native_data_0220b528[];
extern void native_fn_02008e0c(void);
extern void native_fn_020081fc(void);
extern void native_fn_021f4f30(void);
extern void native_fn_021f4f3c(void);
extern void native_fn_021ede50(void);
extern void native_fn_02008430(void);


asm u32 native_ov006_021f4e14 (register u32 a0)
{
    push {r4, r5, lr}
    sub sp, #0x104
    mov r0, #0x9b
    lsl r0, r0, #0x2
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r1, =0x0221c064
    mov r2, #0x41
    str r0, [r1, #0x4]
    mov r0, #0x0
    strb r0, [r1, #0]
    add r1, sp, #0x0
    lsl r2, r2, #0x2
    blx native_fn_02008be0
    mov r1, #0x50
    add r0, sp, #0x0
    strb r1, [r0, #0]
    mov r2, #0xc
    strh r2, [r0, #0x2]
    ldr r0, =native_data_0220b528
    add r1, sp, #0x4
    blx native_fn_02008e0c
    ldr r0, =0x0221c064
    mov r2, #0x3
    ldr r1, [r0, #0x4]
    add r3, sp, #0x0
    strh r2, [r1, #0]
    ldr r4, [r0, #0x4]
    mov r1, #0x82
    add r2, r4, #0x2
ov006_021f4e14_L42:
    ldrh r0, [r3, #0]
    add r3, r3, #0x2
    strh r0, [r2, #0]
    add r2, r2, #0x2
    sub r1, r1, #0x1
    bne ov006_021f4e14_L42
    ldr r0, =0x00000106
    mov r3, #0x1
    strh r3, [r4, r0]
    ldr r1, =0x0221c064
    sub r2, r3, #0x2
    ldr r5, [r1, #0x4]
    add r4, r0, #0x2
    strh r2, [r5, r4]
    ldr r5, [r1, #0x4]
    add r4, r0, #0x4
    strh r3, [r5, r4]
    ldr r4, [r1, #0x4]
    add r3, r0, #0x6
    strh r2, [r4, r3]
    add r3, r0, #0x0
    ldr r4, [r1, #0x4]
    add r3, #0x8
    strh r2, [r4, r3]
    ldr r1, [r1, #0x4]
    add r0, #0xa
    add r0, r1, r0
    blx native_fn_020081fc
    ldr r0, =native_fn_021f4f30+1
    ldr r1, =native_fn_021f4f3c+1
    bl native_fn_021ede50
    cmp r0, #0x0
    beq ov006_021f4e14_L8c
    blx native_fn_02008430
ov006_021f4e14_L8c:
    add sp, #0x104
    pop {r4, r5, pc}
}
