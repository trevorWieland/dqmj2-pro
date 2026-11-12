/* ov001 row 0x022197dc: 156 bytes.
 *
 * What it does: 38 instructions; 7 call(s) to 0x021db8d0, 0x021dbe5c, 0x02219828, +4 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (38 instructions, 7 calls, 1 branch, 6 back edges, 1 literal slot).
 *
 *   pool +0x98 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x28 -> +0x4c
 *   branch +0x38 -> +0x4c
 *   back edge +0x58 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, r8
 *   test +0x50 cmp r7, #3
 *   test +0x88 cmp r4, r3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022197dc; the literal pool and
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
extern void native_fn_021dbe5c(void);


asm u32 native_ov001_022197dc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r4, [r0, #0x8]
    mov r6, #0
    ldr r5, [r0]
    mov r8, r6
    mov r7, r6
    mov r9, r4
ov001_022197dc_L1c:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022197dc_L4c
    mov r0, r9
    bl native_fn_021dbe5c
    cmp r0, r8
    ble ov001_022197dc_L4c
    mov r0, r9
    bl native_fn_021dbe5c
    mov r8, r0
    mov r6, r7
ov001_022197dc_L4c:
    add r7, r7, #1
    cmp r7, #3
    add r9, r9, #1088
    blt ov001_022197dc_L1c
    add r0, r6, r6, lsl #4
    add r0, r4, r0, lsl #6
    bl native_fn_021dbe5c
    mov r4, r0
    mov r0, r5
    bl native_fn_021dbe5c
    mov r1, r0, lsl #2
    ldr r2, =0x66666667
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #2
    cmp r4, r3
    movlt r0, #1
    movge r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
