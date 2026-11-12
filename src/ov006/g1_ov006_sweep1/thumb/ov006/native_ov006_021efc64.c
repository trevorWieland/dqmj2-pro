/* ov006 row 0x021efc64: 252 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xec -> native_data_0220d540 (image word 0x0220d540)
 *   pool +0xf0 -> constant 0x0221af80 (image word 0x0221af80)
 *   pool +0xf4 -> constant 0x0221af78 (image word 0x0221af78)
 *   pool +0xf8 -> native_data_0220d480 (image word 0x0220d480)
 *   branch +0x72 -> +0x94
 *   branch +0x92 -> +0xb2
 *   branch +0xd0 -> +0xe4
 *   test +0x70 cmp r0, #0x0
 *   test +0xce cmp r0, #0x0
 *   0 block transfer(s), 35 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021efc64; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220d540[];
extern void native_fn_021efc58(void);
extern void native_fn_0201b248(void);
extern u8 native_data_0220d480[];
extern void native_fn_021f1f74(void);


asm u32 native_ov006_021efc64 (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0x4c
    ldr r1, =native_data_0220d540
    add r4, r0, #0x0
    ldrb r0, [r1, #0]
    add r2, r4, #0x0
    add r2, #0xc
    strb r0, [r4, #0xc]
    ldrb r0, [r1, #0x1]
    strb r0, [r2, #0x1]
    ldrb r0, [r1, #0x2]
    strb r0, [r2, #0x2]
    ldrb r0, [r1, #0x3]
    add r1, sp, #0x4
    add r1, #0x2
    strb r0, [r2, #0x3]
    ldr r0, =0x0221af80
    ldrb r2, [r0, #0]
    strb r2, [r1, #0]
    ldrb r2, [r0, #0x1]
    strb r2, [r1, #0x1]
    ldrb r2, [r0, #0x2]
    strb r2, [r1, #0x2]
    ldrb r2, [r0, #0x3]
    strb r2, [r1, #0x3]
    ldrb r2, [r0, #0x4]
    ldrb r0, [r0, #0x5]
    strb r2, [r1, #0x4]
    strb r0, [r1, #0x5]
    add r1, sp, #0x0
    ldrb r2, [r1, #0x6]
    mov r0, #0xfd
    and r0, r2
    strb r0, [r1, #0x6]
    add r0, sp, #0x0
    bl native_fn_021efc58
    add r1, sp, #0x0
    ldrb r2, [r1, #0]
    ldr r0, =0x0221af78
    strb r2, [r0, #0]
    ldrb r2, [r1, #0x1]
    strb r2, [r0, #0x1]
    ldrb r2, [r1, #0x2]
    strb r2, [r0, #0x2]
    ldrb r2, [r1, #0x3]
    strb r2, [r0, #0x3]
    ldrb r2, [r1, #0x4]
    strb r2, [r0, #0x4]
    ldrb r2, [r1, #0x5]
    strb r2, [r0, #0x5]
    add r0, sp, #0x4
    add r0, #0x2
    mov r2, #0x6
    blx native_fn_0201b248
    cmp r0, #0x0
    bgt ov006_021efc64_L94
    add r1, sp, #0x0
    ldrb r0, [r1, #0]
    strb r0, [r4, #0]
    ldrb r0, [r1, #0x1]
    strb r0, [r4, #0x1]
    ldrb r0, [r1, #0x2]
    strb r0, [r4, #0x2]
    ldrb r0, [r1, #0x3]
    strb r0, [r4, #0x3]
    ldrb r0, [r1, #0x4]
    strb r0, [r4, #0x4]
    ldrb r0, [r1, #0x5]
    add r1, sp, #0x4
    add r1, #0x2
    strb r0, [r4, #0x5]
    b ov006_021efc64_Lb2
ov006_021efc64_L94:
    add r1, sp, #0x4
    add r1, #0x2
    ldrb r0, [r1, #0]
    strb r0, [r4, #0]
    ldrb r0, [r1, #0x1]
    strb r0, [r4, #0x1]
    ldrb r0, [r1, #0x2]
    strb r0, [r4, #0x2]
    ldrb r0, [r1, #0x3]
    strb r0, [r4, #0x3]
    ldrb r0, [r1, #0x4]
    strb r0, [r4, #0x4]
    ldrb r0, [r1, #0x5]
    add r1, sp, #0x0
    strb r0, [r4, #0x5]
ov006_021efc64_Lb2:
    ldrb r0, [r1, #0]
    strb r0, [r4, #0x6]
    ldrb r0, [r1, #0x1]
    strb r0, [r4, #0x7]
    ldrb r0, [r1, #0x2]
    strb r0, [r4, #0x8]
    ldrb r0, [r1, #0x3]
    strb r0, [r4, #0x9]
    ldrb r0, [r1, #0x4]
    strb r0, [r4, #0xa]
    ldrb r0, [r1, #0x5]
    strb r0, [r4, #0xb]
    ldr r0, =native_data_0220d480
    ldr r0, [r0, #0x4]
    cmp r0, #0x0
    beq ov006_021efc64_Le4
    add r0, sp, #0x2c
    add r1, sp, #0x0
    bl native_fn_021f1f74
    add r1, sp, #0x4
    add r0, sp, #0xc
    add r1, #0x2
    bl native_fn_021f1f74
ov006_021efc64_Le4:
    mov r0, #0x1
    add sp, #0x4c
    pop {r3, r4, pc}
    mov r8, r8
}
