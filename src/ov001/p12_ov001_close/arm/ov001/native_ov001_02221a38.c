/* ov001 row 0x02221a38: 148 bytes.
 *
 * What it does: 37 instructions; 6 call(s) to 0x02221ac4, 0x021db8d0, 0x02218498, +3 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 6 calls (37 instructions, 6 calls, 2 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x8c
 *   branch +0x48 -> +0x7c
 *   branch +0x5c -> +0x7c
 *   back edge +0x88 -> +0x30
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmp r0, #1
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmpne r1, r0
 *   test +0x58 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0x80 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02221a38; the literal pool and
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
extern void native_fn_02218498(void);
extern void native_fn_021e2c2c(void);
extern void native_fn_021e86cc(void);


asm u32 native_ov001_02221a38 (register u32 a0)
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
    blt ov001_02221a38_L8c
    mov r7, #0
    mov r5, #2
ov001_02221a38_L30:
    mov r0, r4
    bl native_fn_021db8d0
    cmp r0, #0
    ldrneb r1, [r6, #0x31f]
    ldrneb r0, [r4, #0x31f]
    cmpne r1, r0
    beq ov001_02221a38_L7c
    mov r0, r4
    mov r1, r5
    bl native_fn_02218498
    cmp r0, #0
    beq ov001_02221a38_L7c
    bl native_fn_021e2c2c
    ldrb r1, [r4, #0x31e]
    ldrb r2, [r4, #0x31f]
    bl native_fn_021e86cc
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02221a38_L7c:
    add r7, r7, #1
    cmp r7, #3
    add r4, r4, #1088
    blt ov001_02221a38_L30
ov001_02221a38_L8c:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
