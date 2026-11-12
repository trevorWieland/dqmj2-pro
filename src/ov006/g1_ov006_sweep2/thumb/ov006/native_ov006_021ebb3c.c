/* ov006 row 0x021ebb3c: 240 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd4 -> constant 0x00000106 (image word 0x00000106)
 *   pool +0xd8 -> constant 0x0221a920 (image word 0x0221a920)
 *   pool +0xdc -> constant 0x0221a92c (image word 0x0221a92c)
 *   pool +0xe0 -> constant 0x00000116 (image word 0x00000116)
 *   pool +0xe4 -> constant 0x000005f8 (image word 0x000005f8)
 *   pool +0xe8 -> constant 0x02219b4c (image word 0x02219b4c)
 *   pool +0xec -> native_data_0220d3dc (image word 0x0220d3dc)
 *   branch +0x0a -> +0x50
 *   branch +0x12 -> +0x50
 *   branch +0x1a -> +0x50
 *   branch +0x22 -> +0x50
 *   branch +0x26 -> +0x50
 *   branch +0x2e -> +0x50
 *   branch +0x38 -> +0x50
 *   branch +0x3e -> +0x50
 *   branch +0x44 -> +0x50
 *   branch +0x4e -> +0x56
 *   branch +0x54 -> +0x58
 *   branch +0x5e -> +0x68
 *   branch +0x66 -> +0x6c
 *   branch +0x72 -> +0x84
 *   branch +0x90 -> +0xa2
 *   branch +0xc8 -> +0xce
 *   test +0x08 cmp r0, #0x0
 *   test +0x10 cmp r0, r1
 *   test +0x18 cmp r0, r1
 *   test +0x20 cmp r0, #0x0
 *   test +0x24 cmp r0, r1
 *   test +0x2c cmp r0, r1
 *   test +0x36 cmp r0, r1
 *   test +0x3c cmp r1, #0x0
 *   test +0x42 cmp r1, r0
 *   test +0x4c cmp r0, #0x0
 *   test +0x5c cmp r0, #0x0
 *   test +0x64 cmp r0, #0x0
 *   test +0x70 cmp r1, r0
 *   test +0x8c cmp r0, #0x0
 *   test +0xc6 cmp r0, r1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ebb3c; the literal pool and
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

extern void native_fn_021ec65c(void);
extern void native_fn_021ebb1c(void);
extern void native_fn_021eca04(void);
extern void native_fn_021ebc2c(void);
extern void native_fn_021ebb2c(void);
extern u8 native_data_0220d3dc[];
extern void native_fn_021edc48(void);


asm u32 native_ov006_021ebb3c (register u32 a0)
{
    push {r4, lr}
    ldr r2, =0x00000106
    add r4, r0, #0x0
    ldrsh r0, [r4, r2]
    cmp r0, #0x0
    beq ov006_021ebb3c_L50
    mov r1, #0x0
    mvn r1, r1
    cmp r0, r1
    blt ov006_021ebb3c_L50
    add r0, r2, #0x2
    ldrsh r0, [r4, r0]
    cmp r0, r1
    blt ov006_021ebb3c_L50
    add r0, r2, #0x4
    ldrsh r0, [r4, r0]
    cmp r0, #0x0
    beq ov006_021ebb3c_L50
    cmp r0, r1
    blt ov006_021ebb3c_L50
    add r0, r2, #0x6
    ldrsh r0, [r4, r0]
    cmp r0, r1
    blt ov006_021ebb3c_L50
    add r0, r2, #0x0
    add r0, #0x8
    ldrsh r0, [r4, r0]
    cmp r0, r1
    blt ov006_021ebb3c_L50
    ldrh r1, [r4, #0x4]
    cmp r1, #0x0
    beq ov006_021ebb3c_L50
    sub r0, r2, #0x6
    cmp r1, r0
    bhi ov006_021ebb3c_L50
    sub r0, r1, #0x1
    add r0, r4, r0
    ldrb r0, [r0, #0x6]
    cmp r0, #0x0
    beq ov006_021ebb3c_L56
ov006_021ebb3c_L50:
    mov r1, #0x0
    mvn r1, r1
    b ov006_021ebb3c_L58
ov006_021ebb3c_L56:
    mov r1, #0x0
ov006_021ebb3c_L58:
    ldr r0, =0x0221a920
    ldr r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021ebb3c_L68
    ldr r0, =0x0221a92c
    ldr r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021ebb3c_L6c
ov006_021ebb3c_L68:
    mov r1, #0x0
    mvn r1, r1
ov006_021ebb3c_L6c:
    mov r0, #0x0
    mvn r0, r0
    cmp r1, r0
    bne ov006_021ebb3c_L84
    ldr r0, =0x00000116
    mov r1, #0xf
    strb r1, [r4, r0]
    bl native_fn_021ec65c
    mov r0, #0x0
    mvn r0, r0
    pop {r4, pc}
ov006_021ebb3c_L84:
    ldr r0, =0x000005f8
    bl native_fn_021ebb1c
    ldr r1, =0x02219b4c
    cmp r0, #0x0
    str r0, [r1, #0x14]
    bne ov006_021ebb3c_La2
    ldr r0, =0x00000116
    mov r1, #0xf
    strb r1, [r4, r0]
    bl native_fn_021ec65c
    mov r0, #0x0
    mvn r0, r0
    pop {r4, pc}
ov006_021ebb3c_La2:
    mov r0, #0x0
    mvn r0, r0
    bl native_fn_021eca04
    add r0, r4, #0x0
    bl native_fn_021ebc2c
    add r4, r0, #0x0
    ldr r0, =0x02219b4c
    ldr r0, [r0, #0x14]
    bl native_fn_021ebb2c
    bl native_fn_021ec65c
    ldr r0, =native_data_0220d3dc
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    cmp r0, r1
    beq ov006_021ebb3c_Lce
    bl native_fn_021edc48
ov006_021ebb3c_Lce:
    add r0, r4, #0x0
    pop {r4, pc}
    mov r8, r8
}
