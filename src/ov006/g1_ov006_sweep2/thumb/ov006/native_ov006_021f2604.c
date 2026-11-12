/* ov006 row 0x021f2604: 80 bytes.
 *
 * What it does: Writes 2 blocks of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x48 -> native_data_0221c008 (image word 0x0221c008)
 *   pool +0x4c -> native_data2_0221c008 (image word 0x0221c008)
 *   branch +0x12 -> +0x1a
 *   branch +0x26 -> +0x2c
 *   back edge +0x32 -> +0x20
 *   test +0x10 cmp r1, #0x0
 *   test +0x24 cmp r0, #0x0
 *   test +0x30 cmp r4, #0x2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2604; the literal pool and
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

extern void native_fn_02204974(void);
extern u8 native_data_0221c008[];
extern void native_fn_02202d64(void);
extern u8 native_data2_0221c008[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f2604 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r1, r0, #0x0
    mov r0, #0x0
    bl native_fn_02204974
    ldr r0, =native_data_0221c008
    ldr r0, [r0, #0]
    ldr r1, [r0, #0x10]
    cmp r1, #0x0
    beq ov006_021f2604_L1a
    mov r0, #0x0
    bl native_fn_02204974
ov006_021f2604_L1a:
    mov r4, #0x0
    ldr r6, =native_data_0221c008
    add r5, r4, #0x0
ov006_021f2604_L20:
    ldr r0, [r6, #0]
    ldr r0, [r0, r5]
    cmp r0, #0x0
    beq ov006_021f2604_L2c
    bl native_fn_02202d64
ov006_021f2604_L2c:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x2
    blt ov006_021f2604_L20
    ldr r0, =native_data_0221c008
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x8]
    bl native_fn_02202d64
    ldr r0, =native_data2_0221c008
    bl native_fn_02203c20
    pop {r4, r5, r6, pc}
    mov r8, r8
}
