/* ov001 row 0x02219ed0: 112 bytes.
 *
 * What it does: 26 instructions; 4 call(s) to 0x021dbd24, 0x021dbcbc, 0x02219d8c, +1 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (26 instructions, 4 calls, 2 branches, 4 back edges, 2 literal slots).
 *
 *   pool +0x68 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x6c -> constant 0x000002ee (image word 0x000002ee)
 *   branch +0x34 -> +0x60
 *   branch +0x44 -> +0x60
 *   test +0x30 cmp r4, r3
 *   test +0x40 cmp r0, #0
 *   test +0x54 cmp r0, r1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219ed0; the literal pool and
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

extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_02219d8c(void);
extern void ov001_record_field_1f2_021dbd30(void);


asm u32 native_ov001_02219ed0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldr r5, [r6]
    mov r0, r5
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, r5
    bl native_fn_021dbcbc
    ldr r2, =0x66666667
    mov r1, r0, lsr #31
    smull r0, r3, r2, r0
    add r3, r1, r3, asr #1
    cmp r4, r3
    bge ov001_02219ed0_L60
    mov r0, r6
    bl native_fn_02219d8c
    cmp r0, #0
    bne ov001_02219ed0_L60
    mov r0, r5
    bl ov001_record_field_1f2_021dbd30
    ldr r1, =0x000002ee
    cmp r0, r1
    movge r0, #1
    ldmgeia sp!, {r4, r5, r6, pc}
ov001_02219ed0_L60:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
