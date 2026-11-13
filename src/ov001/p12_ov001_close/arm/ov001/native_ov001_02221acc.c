/* ov001 row 0x02221acc: 144 bytes.
 *
 * What it does: 36 instructions; 4 call(s) to 0x021db8d0, 0x021e2c2c, 0x021e86cc, +1 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 4 calls (36 instructions, 4 calls, 3 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x88
 *   branch +0x40 -> +0x78
 *   branch +0x58 -> +0x78
 *   back edge +0x84 -> +0x28
 *   test +0x18 cmp r2, r1
 *   test +0x30 cmp r0, #0
 *   test +0x3c cmpne r0, r7
 *   test +0x54 cmp r0, r8
 *   test +0x6c cmp r0, #0
 *   test +0x7c cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02221acc; the literal pool and
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
extern void native_fn_021e2c2c(void);
extern void native_fn_021e86cc(void);


asm u32 native_ov001_02221acc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r4, [r0]
    mvn r1, #0
    add r9, r4, #512
    ldrsb r2, [r9, #52]
    ldr r6, [r0, #0x4]
    cmp r2, r1
    bgt ov001_02221acc_L88
    mov r5, #0
    sub r8, r1, #4
ov001_02221acc_L28:
    mov r0, r6
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    ldrneb r7, [r6, #0x31f]
    ldrneb r0, [r4, #0x31f]
    cmpne r0, r7
    beq ov001_02221acc_L78
    add r0, r6, #512
    ldrsb r1, [r9, #52]
    ldrsb r0, [r0, #52]
    add r0, r1, r0
    cmp r0, r8
    bgt ov001_02221acc_L78
    bl native_fn_021e2c2c
    ldrb r1, [r6, #0x31e]
    mov r2, r7
    bl native_fn_021e86cc
    cmp r0, #0
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_02221acc_L78:
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_02221acc_L28
ov001_02221acc_L88:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
