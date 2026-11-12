/* ov000 row 0x021e1038: 156 bytes.
 *
 * What it does: 37 instructions; 6 call(s) to 0x0202818c, 0x02028158, 0x02028158, +3 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x94 -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x98 -> constant 0x02232344 (image word 0x02232344)
 *   branch +0x38 -> +0x50
 *   branch +0x54 -> +0x8c
 *   branch +0x74 -> +0x8c
 *   test +0x34 cmp r0, #737280
 *   test +0x48 cmp r0, #737280
 *   test +0x50 cmp r4, #0
 *   test +0x70 cmp r0, #368640
 *   test +0x84 cmp r0, #245760
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e1038; the literal pool and
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

extern void native_fn_0202818c(void);
extern void native_fn_02028158(void);


asm u32 native_ov000_021e1038 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r2, =0x022322d4
    ldr r6, =0x02232344
    mov r8, r0
    mov r7, r1
    ldr r5, [r2, #0x8c]
    mov r0, r6
    mov r1, r8
    mov r4, #0
    bl native_fn_0202818c
    sub r0, r0, r5
    bl native_fn_02028158
    add r0, r0, #368640
    cmp r0, #737280
    bhs ov000_021e1038_L50
    sub r0, r5, r7
    bl native_fn_02028158
    add r0, r0, #368640
    cmp r0, #737280
    movlo r4, #1
ov000_021e1038_L50:
    cmp r4, #0
    bne ov000_021e1038_L8c
    mov r0, r8
    mov r1, r6
    bl native_fn_0202818c
    sub r0, r0, r5
    bl native_fn_02028158
    add r0, r0, #184320
    cmp r0, #368640
    bhs ov000_021e1038_L8c
    sub r0, r5, r7
    bl native_fn_02028158
    add r0, r0, #122880
    cmp r0, #245760
    movlo r4, #2
ov000_021e1038_L8c:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
