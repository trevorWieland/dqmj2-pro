/* ov001 row 0x021daf48: 108 bytes.
 *
 * What it does: 27 instructions; 4 call(s) to 0x021db8d0, 0x021dafa4, 0x0205d8bc, +1 more; loops (back edge at +0x58); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 4 calls (27 instructions, 4 calls, 2 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x14 -> +0x38
 *   branch +0x24 -> +0x38
 *   branch +0x4c -> +0x5c
 *   back edge +0x64 -> +0x3c
 *   test +0x0c cmp r0, #0
 *   test +0x1c cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x60 cmp r5, #19
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021daf48; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_0205d8bc(void);


asm u32 native_ov001_021daf48 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r4, r0
    bl native_fn_021db8d0
    cmp r0, #0
    moveq r6, #0
    beq ov001_021daf48_L38
    ldrb r0, [r4, #0x31d]
    cmp r0, #0
    moveq r6, #0
    beq ov001_021daf48_L38
    ldrb r0, [r4, #0x160]
    cmp r0, #0
    moveq r6, #0
    movne r6, #1
ov001_021daf48_L38:
    mov r5, #0
ov001_021daf48_L3c:
    add r0, r4, r5
    add r0, r0, #768
    ldrsb r0, [r0, #218]
    cmp r0, #0
    ble ov001_021daf48_L5c
    mov r1, r6
    sub r0, r0, #1
    bl native_fn_0205d8bc
ov001_021daf48_L5c:
    add r5, r5, #1
    cmp r5, #19
    blt ov001_021daf48_L3c
    ldmia sp!, {r4, r5, r6, pc}
}
