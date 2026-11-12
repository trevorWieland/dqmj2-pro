/* ov006 row 0x02207778: 324 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x12c -> native_data2_0221c6dc (image word 0x0221c6dc)
 *   pool +0x130 -> native_data_0220c88c (image word 0x0220c88c)
 *   pool +0x134 -> constant 0x0204594c (image word 0x0204594c)
 *   pool +0x138 -> constant 0x02045994 (image word 0x02045994)
 *   pool +0x13c -> constant 0x00000fff (image word 0x00000fff)
 *   pool +0x140 -> constant 0x0221c6e0 (image word 0x0221c6e0)
 *   branch +0x1c -> +0x120
 *   branch +0x30 -> +0x120
 *   back edge +0xb8 -> +0x9c
 *   back edge +0x110 -> +0x74
 *   test +0x18 cmpne r1, #0
 *   test +0x2c cmp r0, #0
 *   test +0x5c cmp r5, #0
 *   test +0xb0 cmp r12, #2
 *   test +0x108 cmp r5, #2
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02207778; the literal pool and
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

extern u8 native_data2_0221c6dc[];
extern void native_fn_0220774c(void);
extern u8 native_data_0220c88c[];
extern void native_fn_02048f6c(void);
extern void native_fn_02008e0c(void);


asm u32 native_ov006_02207778 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    movs r10, r0
    mov r5, r2
    mov r9, r3
    ldr r8, [sp, #0x30]
    cmpne r1, #0
    beq ov006_02207778_L120
    ldr r1, [r1]
    ldr r0, =native_data2_0221c6dc
    bl native_fn_0220774c
    cmp r0, #0
    beq ov006_02207778_L120
    ldr r0, =native_data2_0221c6dc
    ldr r2, =native_data_0220c88c
    ldr r1, [r0]
    add r0, r2, r5, lsl #2
    ldrb r1, [r1, r0]
    mov r0, r5
    mov r1, r1, lsl #12
    and r1, r1, #61440
    mov r4, r1, lsl #16
    bl native_fn_02048f6c
    cmp r5, #0
    ldreq r11, =0x0204594c
    mov r5, #0
    ldrne r11, =0x02045994
    str r0, [sp]
    mov r6, r5
ov006_02207778_L74:
    ldrb r0, [r10, #0x22]
    add r7, r8, r5
    ldr r2, [r10, #0x1c]
    mla r1, r0, r7, r9
    add r0, r2, r1
    mov r0, r0, lsl #16
    mov lr, r0, lsr #16
    ldr r0, =0x00000fff
    mov r12, #0
    add r1, sp, #4
ov006_02207778_L9c:
    and r2, lr, r0
    orr r3, r2, r4, lsr #16
    mov r2, r12, lsl #1
    strh r3, [r1, r2]
    add r12, r12, #1
    cmp r12, #2
    add lr, lr, #1
    blt ov006_02207778_L9c
    ldrb r2, [r10, #0x21]
    ldrb r3, [r10, #0x20]
    ldr r0, [sp]
    add r2, r2, r8
    add r3, r3, r9
    add r2, r5, r2
    add r2, r3, r2, lsl #5
    mov r3, #4
    blx r11
    ldrb r0, [r10, #0x22]
    ldr r2, [r10, #0x8]
    ldr r3, =0x0221c6e0
    mla r1, r0, r7, r9
    add r0, r3, r6
    ldr r3, [r2]
    mov r2, #64
    add r1, r3, r1, lsl #5
    bl native_fn_02008e0c
    add r5, r5, #1
    cmp r5, #2
    add r6, r6, #64
    blt ov006_02207778_L74
    add sp, sp, #8
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov006_02207778_L120:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
