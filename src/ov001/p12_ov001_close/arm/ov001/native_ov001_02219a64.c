/* ov001 row 0x02219a64: 104 bytes.
 *
 * What it does: 26 instructions; 4 call(s) to 0x021db8d0, 0x021dbd30, 0x021dbcf0, +1 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: block load (26 instructions, 4 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x44
 *   branch +0x40 -> +0x60
 *   back edge +0x5c -> +0x0c
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmpne r1, r0
 *   test +0x3c cmp r4, r0
 *   test +0x44 cmp r6, #2
 *   test +0x54 cmp r6, #3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219a64; the literal pool and
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
extern void native_fn_021dbd30(void);
extern void native_fn_021dbcf0(void);


asm u32 native_ov001_02219a64 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldmia r0, {r5, r7}
    mov r6, #0
ov001_02219a64_Lc:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    ldrneb r1, [r5, #0x31f]
    ldrneb r0, [r7, #0x31f]
    cmpne r1, r0
    beq ov001_02219a64_L44
    mov r0, r7
    bl native_fn_021dbd30
    mov r4, r0
    mov r0, r7
    bl native_fn_021dbcf0
    cmp r4, r0
    bne ov001_02219a64_L60
ov001_02219a64_L44:
    cmp r6, #2
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_02219a64_Lc
ov001_02219a64_L60:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
