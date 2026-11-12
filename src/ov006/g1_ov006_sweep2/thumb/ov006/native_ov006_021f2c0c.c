/* ov006 row 0x021f2c0c: 120 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x60 -> constant 0x04000208 (image word 0x04000208)
 *   pool +0x64 -> constant 0x0221c058 (image word 0x0221c058)
 *   pool +0x68 -> native_data_0220b14c (image word 0x0220b14c)
 *   pool +0x6c -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x70 -> constant 0x00e50026 (image word 0x00e50026)
 *   pool +0x74 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   branch +0x14 -> +0x1c
 *   test +0x12 cmp r0, r1
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2c0c; the literal pool and
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

extern void native_fn_02012290(void);
extern void native_fn_020122b0(void);
extern u8 native_data_0220b14c[];
extern void native_fn_02202ff0(void);


asm u32 native_ov006_021f2c0c (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r0, =0x04000208
    mov r4, #0x0
    ldrh r5, [r0, #0]
    strh r4, [r0, #0]
    blx native_fn_02012290
    mov r1, #0x2
    lsl r1, r1, #0xe
    cmp r0, r1
    beq ov006_021f2c0c_L1c
    blx native_fn_020122b0
    add r4, r0, #0x0
ov006_021f2c0c_L1c:
    ldr r1, =0x04000208
    ldrh r0, [r1, #0]
    ldr r0, =0x0221c058
    strh r5, [r1, #0]
    ldr r2, [r0, #0]
    mov r1, #0x8
    ldrsb r1, [r2, r1]
    ldr r2, [r2, #0]
    mov r0, #0x0
    lsl r3, r1, #0x2
    ldr r1, =native_data_0220b14c
    add r1, r1, r3
    ldrb r1, [r4, r1]
    bl native_fn_02202ff0
    ldr r1, =0x0221c058
    ldr r0, [r1, #0]
    ldr r3, [r0, #0]
    ldr r0, =0xfe00ff00
    ldr r2, [r3, #0]
    and r2, r0
    ldr r0, =0x00e50026
    orr r0, r2
    str r0, [r3, #0]
    ldr r0, [r1, #0]
    ldr r2, [r0, #0]
    ldr r0, =0xfffff3ff
    ldrh r1, [r2, #0x4]
    and r1, r0
    mov r0, #0x2
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r2, #0x4]
    pop {r3, r4, r5, pc}
}
