/* ov001 row 0x022219a0: 152 bytes.
 *
 * What it does: 38 instructions; 8 call(s) to 0x02221a30, 0x021db8d0, 0x021dbd3c, +5 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 8 calls (38 instructions, 8 calls, 1 branch, 6 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x90
 *   branch +0x44 -> +0x80
 *   branch +0x60 -> +0x80
 *   back edge +0x8c -> +0x2c
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmp r0, #1
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmpne r1, r0
 *   test +0x5c cmp r5, r0
 *   test +0x74 cmp r0, #0
 *   test +0x84 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022219a0; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbd3c(void);
extern void native_fn_021e2c2c(void);
extern void native_fn_021e86cc(void);


asm u32 native_ov001_022219a0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r6, [r0]
    ldr r4, [r0, #0x4]
    add r0, r6, #512
    ldrsb r0, [r0, #52]
    cmp r0, #0
    movne r0, #1
    moveq r0, #0
    cmp r0, #1
    blt ov001_022219a0_L90
    mov r7, #0
ov001_022219a0_L2c:
    mov r0, r4
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    ldrneb r1, [r6, #0x31f]
    ldrneb r0, [r4, #0x31f]
    cmpne r1, r0
    beq ov001_022219a0_L80
    mov r0, r4
    bl native_fn_021dbd3c
    mov r5, r0
    mov r0, r6
    bl native_fn_021dbd3c
    cmp r5, r0
    blt ov001_022219a0_L80
    bl native_fn_021e2c2c
    ldrb r1, [r4, #0x31e]
    ldrb r2, [r4, #0x31f]
    bl native_fn_021e86cc
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
ov001_022219a0_L80:
    add r7, r7, #1
    cmp r7, #3
    add r4, r4, #1088
    blt ov001_022219a0_L2c
ov001_022219a0_L90:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
