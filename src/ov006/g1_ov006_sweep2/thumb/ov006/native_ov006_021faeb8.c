/* ov006 row 0x021faeb8: 168 bytes.
 *
 * What it does: Writes one block of 5 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x98 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   pool +0x9c -> native_data_0220b72e (image word 0x0220b72e)
 *   pool +0xa0 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0xa4 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   branch +0x28 -> +0x42
 *   branch +0x32 -> +0x3c
 *   branch +0x3a -> +0x42
 *   branch +0x4e -> +0x82
 *   test +0x26 cmp r0, #0x1
 *   test +0x30 cmp r0, #0x2
 *   test +0x4c cmp r1, #0x0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021faeb8; the literal pool and
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

extern void native_fn_021fb384(void);
extern u8 native_data_0220b72e[];
extern void native_fn_02202ff0(void);


asm u32 native_ov006_021faeb8 (register u32 a0)
{
    push {r3, r4, r5, r6, lr}
    sub sp, #0xc
    add r5, r0, #0x0
    add r6, r1, #0x0
    mov r1, #0xcc
    add r0, sp, #0x0
    strh r1, [r0, #0]
    mov r1, #0xc0
    strh r1, [r0, #0x2]
    strh r1, [r0, #0x4]
    mov r1, #0x8f
    strh r1, [r0, #0x6]
    strh r1, [r0, #0x8]
    ldr r0, =0x0221c0ec
    ldr r1, [r0, #0x8]
    lsl r0, r2, #0x2
    add r1, #0x18
    add r4, r1, r0
    sub r0, r5, #0x1
    cmp r0, #0x1
    bhi ov006_021faeb8_L42
    add r0, r2, #0x0
    bl native_fn_021fb384
    cmp r0, #0x2
    bne ov006_021faeb8_L3c
    ldr r0, =0x0221c0ec
    ldr r4, [r0, #0x8]
    add r4, #0x2c
    b ov006_021faeb8_L42
ov006_021faeb8_L3c:
    ldr r0, =0x0221c0ec
    ldr r4, [r0, #0x8]
    add r4, #0x30
ov006_021faeb8_L42:
    lsl r0, r5, #0x1
    add r1, r5, r0
    ldr r0, =native_data_0220b72e
    add r0, r0, r1
    ldrb r1, [r6, r0]
    cmp r1, #0x0
    beq ov006_021faeb8_L82
    ldr r2, [r4, #0]
    mov r0, #0x0
    bl native_fn_02202ff0
    add r1, sp, #0x0
    lsl r2, r5, #0x1
    ldrh r1, [r1, r2]
    ldr r0, [r4, #0]
    add sp, #0xc
    lsl r1, r1, #0x17
    lsr r3, r1, #0x7
    ldr r2, [r0, #0]
    ldr r1, =0xfe00ff00
    and r1, r2
    orr r1, r3
    str r1, [r0, #0]
    ldr r2, [r4, #0]
    ldr r0, =0xfffff3ff
    ldrh r1, [r2, #0x4]
    and r1, r0
    mov r0, #0x3
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r2, #0x4]
    pop {r3, r4, r5, r6, pc}
ov006_021faeb8_L82:
    ldr r2, [r4, #0]
    ldr r0, =0xfe00ff00
    ldr r1, [r2, #0]
    and r1, r0
    mov r0, #0x1
    lsl r0, r0, #0x18
    orr r0, r1
    str r0, [r2, #0]
    add sp, #0xc
    pop {r3, r4, r5, r6, pc}
    mov r8, r8
}
