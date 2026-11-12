/* ov006 row 0x021ff0d0: 164 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x90 -> constant 0x0221c148 (image word 0x0221c148)
 *   pool +0x94 -> constant 0x000004f4 (image word 0x000004f4)
 *   pool +0x98 -> native_data_0220b9f0 (image word 0x0220b9f0)
 *   pool +0x9c -> constant 0x000004f5 (image word 0x000004f5)
 *   pool +0xa0 -> constant 0x000004f6 (image word 0x000004f6)
 *   back edge +0x1c -> +0x12
 *   branch +0x30 -> +0x38
 *   branch +0x36 -> +0x3c
 *   branch +0x50 -> +0x62
 *   branch +0x60 -> +0x6e
 *   branch +0x6c -> +0x78
 *   test +0x2e cmp r0, #0x0
 *   test +0x4e cmp r0, #0x0
 *   test +0x5e cmp r0, #0x0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff0d0; the literal pool and
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

extern u8 native_data_0220b9f0[];
extern void native_fn_0201b248(void);
extern void native_fn_020a4910(void);


asm u32 native_ov006_021ff0d0 (register u32 a0)
{
    push {r4, r5, r6, lr}
    ldr r1, =0x0221c148
    mov r2, #0x1
    ldr r5, [r1, #0]
    lsl r4, r0, #0x8
    lsl r2, r2, #0xa
    add r1, r5, r4
    add r6, r5, r2
    mov r3, #0xf0
ov006_021ff0d0_L12:
    ldrb r2, [r1, #0]
    add r1, r1, #0x1
    strb r2, [r6, #0]
    add r6, r6, #0x1
    sub r3, r3, #0x1
    bne ov006_021ff0d0_L12
    ldr r1, =0x000004f4
    mov r2, #0x4
    strb r0, [r5, r1]
    add r0, r5, r4
    ldr r1, =native_data_0220b9f0
    add r0, #0xc0
    blx native_fn_0201b248
    cmp r0, #0x0
    beq ov006_021ff0d0_L38
    mov r2, #0x0
    ldr r0, =0x0221c148
    b ov006_021ff0d0_L3c
ov006_021ff0d0_L38:
    ldr r0, =0x0221c148
    mov r2, #0x1
ov006_021ff0d0_L3c:
    ldr r1, [r0, #0]
    ldr r0, =0x000004f5
    strb r2, [r1, r0]
    add r0, r5, r4
    ldr r1, =native_data_0220b9f0
    add r0, #0xc8
    mov r2, #0x4
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_021ff0d0_L62
    add r0, r5, r4
    ldr r1, =native_data_0220b9f0
    add r0, #0xcc
    mov r2, #0x4
    blx native_fn_0201b248
    cmp r0, #0x0
    beq ov006_021ff0d0_L6e
ov006_021ff0d0_L62:
    ldr r0, =0x0221c148
    mov r2, #0x0
    ldr r1, [r0, #0]
    ldr r0, =0x000004f6
    strb r2, [r1, r0]
    b ov006_021ff0d0_L78
ov006_021ff0d0_L6e:
    ldr r0, =0x0221c148
    mov r2, #0x1
    ldr r1, [r0, #0]
    ldr r0, =0x000004f6
    strb r2, [r1, r0]
ov006_021ff0d0_L78:
    add r0, r5, r4
    ldr r1, =0x0221c148
    add r0, #0xd0
    ldr r2, [r1, #0]
    mov r1, #0x4f
    lsl r1, r1, #0x4
    ldrb r0, [r0, #0]
    add r1, r2, r1
    bl native_fn_020a4910
    pop {r4, r5, r6, pc}
    mov r8, r8
}
