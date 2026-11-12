/* ov001 row 0x0221c928: 104 bytes.
 *
 * What it does: 26 instructions; 3 call(s) to 0x021db8d0, 0x02218524, 0x0221c938; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 3 calls (26 instructions, 3 calls, 3 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x44
 *   branch +0x2c -> +0x44
 *   branch +0x40 -> +0x60
 *   back edge +0x5c -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x44 cmp r5, #2
 *   test +0x54 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221c928; the literal pool and
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
extern void native_fn_02218524(void);


asm u32 native_ov001_0221c928 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r6, [r0, #0x8]
    mov r5, #0
    mov r4, #8
ov001_0221c928_L10:
    mov r0, r6
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221c928_L44
    add r0, r6, #512
    ldrsb r0, [r0, #62]
    cmp r0, #0
    bne ov001_0221c928_L44
    mov r0, r6
    mov r1, r4
    bl native_fn_02218524
    cmp r0, #0
    bne ov001_0221c928_L60
ov001_0221c928_L44:
    cmp r5, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_0221c928_L10
ov001_0221c928_L60:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
