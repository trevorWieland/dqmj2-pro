/* ov001 row 0x022213f0: 224 bytes.
 *
 * What it does: 55 instructions; 9 call(s) to 0x021db8d0, 0x02218430, 0x022214a8, +6 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (55 instructions, 9 calls, 2 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0xdc -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x2c -> +0xb8
 *   branch +0x4c -> +0xb8
 *   branch +0x60 -> +0xac
 *   back edge +0xb4 -> +0x50
 *   back edge +0xcc -> +0x20
 *   test +0x28 cmp r0, #0
 *   test +0x48 cmp r9, #0
 *   test +0x5c cmp r0, #0
 *   test +0x9c cmp r3, r2
 *   test +0xb0 cmp r8, r9
 *   test +0xc8 cmp r0, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022213f0; the literal pool and
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
extern void native_fn_02218430(void);
extern void native_fn_0207b004(void);
extern void native_fn_021dbd24(void);
extern void native_fn_02218cf8(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_022213f0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #204
    ldr r7, [r0]
    ldr r10, [r0, #0x8]
    mov r0, #0
    ldr r11, =0x66666667
    str r0, [sp]
    add r6, sp, #4
ov001_022213f0_L20:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022213f0_Lb8
    mov r0, r10
    mov r1, r6
    mov r2, #200
    bl native_fn_02218430
    mov r9, r0
    mov r8, #0
    cmp r9, #0
    ble ov001_022213f0_Lb8
ov001_022213f0_L50:
    ldr r0, [r6, r8, lsl #2]
    mov r1, #64
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_022213f0_Lac
    mov r0, r7
    bl native_fn_021dbd24
    mov r5, r0
    ldr r2, [r6, r8, lsl #2]
    mov r0, r10
    mov r1, r7
    bl native_fn_02218cf8
    mov r4, r0
    mov r0, r7
    bl native_fn_021dbcbc
    smull r1, r2, r11, r0
    mov r0, r0, lsr #31
    sub r3, r5, r4
    add r2, r0, r2, asr #1
    cmp r3, r2
    addle sp, sp, #204
    movle r0, #1
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_022213f0_Lac:
    add r8, r8, #1
    cmp r8, r9
    blt ov001_022213f0_L50
ov001_022213f0_Lb8:
    ldr r0, [sp]
    add r10, r10, #1088
    add r0, r0, #1
    str r0, [sp]
    cmp r0, #3
    blt ov001_022213f0_L20
    mov r0, #0
    add sp, sp, #204
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
