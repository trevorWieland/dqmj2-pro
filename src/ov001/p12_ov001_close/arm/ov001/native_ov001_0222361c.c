/* ov001 row 0x0222361c: 252 bytes.
 *
 * What it does: 62 instructions; 9 call(s) to 0x021db8d0, 0x021dc1c0, 0x02218430, +6 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (62 instructions, 9 calls, 7 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0xf8 -> constant 0x80008000 (image word 0x80008000)
 *   branch +0x30 -> +0xd4
 *   branch +0x40 -> +0xd4
 *   branch +0x60 -> +0xd4
 *   branch +0x78 -> +0xc8
 *   branch +0x84 -> +0x9c
 *   branch +0x98 -> +0xc8
 *   branch +0xa4 -> +0xbc
 *   branch +0xb8 -> +0xc8
 *   back edge +0xd0 -> +0x68
 *   back edge +0xe8 -> +0x24
 *   test +0x2c cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x5c cmp r8, #0
 *   test +0x74 cmp r0, #0
 *   test +0x80 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0xa0 cmp r0, #0
 *   test +0xb4 cmp r0, #0
 *   test +0xcc cmp r10, r8
 *   test +0xe4 cmp r0, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222361c; the literal pool and
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
extern void native_fn_021dc1c0(void);
extern void native_fn_02218430(void);
extern void native_fn_0207b02c(void);
extern void native_fn_0207b004(void);


asm u32 native_ov001_0222361c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #204
    ldr r9, [r0, #0x8]
    mov r0, #0
    ldr r6, =0x80008000
    str r0, [sp]
    add r7, sp, #4
    mov r11, #67108864
    mov r5, #2
ov001_0222361c_L24:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0222361c_Ld4
    mov r0, r9
    bl native_fn_021dc1c0
    cmp r0, #0
    beq ov001_0222361c_Ld4
    mov r0, r9
    mov r1, r7
    mov r2, #200
    bl native_fn_02218430
    mov r8, r0
    mov r10, #0
    cmp r8, #0
    ble ov001_0222361c_Ld4
    add r4, r9, #512
ov001_0222361c_L68:
    ldr r0, [r7, r10, lsl #2]
    mov r1, r6
    bl native_fn_0207b02c
    cmp r0, #0
    beq ov001_0222361c_Lc8
    ldrsb r0, [r4, #60]
    cmp r0, #0
    beq ov001_0222361c_L9c
    ldr r0, [r7, r10, lsl #2]
    mov r1, r5
    bl native_fn_0207b004
    cmp r0, #0
    bne ov001_0222361c_Lc8
ov001_0222361c_L9c:
    ldrsb r0, [r4, #84]
    cmp r0, #0
    beq ov001_0222361c_Lbc
    ldr r0, [r7, r10, lsl #2]
    mov r1, r11
    bl native_fn_0207b004
    cmp r0, #0
    bne ov001_0222361c_Lc8
ov001_0222361c_Lbc:
    add sp, sp, #204
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_0222361c_Lc8:
    add r10, r10, #1
    cmp r10, r8
    blt ov001_0222361c_L68
ov001_0222361c_Ld4:
    ldr r0, [sp]
    add r9, r9, #1088
    add r0, r0, #1
    str r0, [sp]
    cmp r0, #3
    blt ov001_0222361c_L24
    mov r0, #1
    add sp, sp, #204
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
