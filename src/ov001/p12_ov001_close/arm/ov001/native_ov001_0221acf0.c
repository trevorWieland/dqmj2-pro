/* ov001 row 0x0221acf0: 104 bytes.
 *
 * What it does: 26 instructions; 5 call(s) to 0x021db8d0, 0x021dbd24, 0x021dbcbc, +2 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 5 calls (26 instructions, 5 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x44
 *   branch +0x40 -> +0x60
 *   back edge +0x5c -> +0x0c
 *   test +0x14 cmp r0, #0
 *   test +0x3c cmp r4, r0, asr #2
 *   test +0x44 cmp r5, #2
 *   test +0x54 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221acf0; the literal pool and
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
extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_0221acf0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r6, [r0, #0x4]
    mov r5, #0
ov001_0221acf0_Lc:
    mov r0, r6
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221acf0_L44
    mov r0, r6
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, r6
    bl native_fn_021dbcbc
    add r1, r0, r0, lsl #1
    mov r0, r1, asr #1
    add r0, r1, r0, lsr #30
    cmp r4, r0, asr #2
    ble ov001_0221acf0_L60
ov001_0221acf0_L44:
    cmp r5, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_0221acf0_Lc
ov001_0221acf0_L60:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
