/* ov001 row 0x02220220: 332 bytes.
 *
 * What it does: 82 instructions; 13 call(s) to 0x021db8d0, 0x02220350, 0x0207b004, +10 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (82 instructions, 13 calls, 5 branches, 12 back edges, 1 literal slot).
 *
 *   pool +0x148 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x1c -> +0x130
 *   branch +0x2c -> +0xb8
 *   branch +0x38 -> +0x130
 *   branch +0x5c -> +0xa4
 *   back edge +0xb0 -> +0x44
 *   branch +0xb4 -> +0x130
 *   branch +0xdc -> +0x124
 *   back edge +0x12c -> +0xc0
 *   back edge +0x13c -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, #1
 *   test +0x34 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x98 cmp r1, r2
 *   test +0xac cmp r10, r0
 *   test +0xd8 cmp r0, #0
 *   test +0x118 cmp r1, r2
 *   test +0x128 cmp r10, #6
 *   test +0x134 cmp r11, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02220220; the literal pool and
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
extern void native_fn_0207b004(void);
extern void native_fn_021dbd24(void);
extern void native_fn_02218cf8(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_02220220 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r4, [r0]
    ldr r5, [r0, #0x8]
    mov r11, #0
ov001_02220220_L10:
    mov r0, r5
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02220220_L130
    ldrb r0, [r5, #0x322]
    mov r10, #0
    cmp r0, #1
    beq ov001_02220220_Lb8
    ldrb r0, [r5, #0x323]
    cmp r0, #0
    ble ov001_02220220_L130
    ldr r6, =0x66666667
    mov r9, #2097152
ov001_02220220_L44:
    add r0, r5, r10
    ldrb r7, [r0, #0x35e]
    mov r1, r9
    mov r0, r7
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_02220220_La4
    mov r0, r4
    bl native_fn_021dbd24
    mov r8, r0
    mov r0, r5
    mov r1, r4
    mov r2, r7
    bl native_fn_02218cf8
    mov r7, r0
    mov r0, r4
    bl native_fn_021dbcbc
    smull r1, r2, r6, r0
    mov r0, r0, lsr #31
    sub r1, r8, r7
    add r2, r0, r2, asr #1
    cmp r1, r2
    movle r0, #1
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02220220_La4:
    ldrb r0, [r5, #0x323]
    add r10, r10, #1
    cmp r10, r0
    blt ov001_02220220_L44
    b ov001_02220220_L130
ov001_02220220_Lb8:
    ldr r6, =0x66666667
    mov r9, #2097152
ov001_02220220_Lc0:
    ldr r0, [r5, #0x1e8]
    mov r1, r9
    add r0, r0, r10
    ldrb r7, [r0, #0x8]
    mov r0, r7
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_02220220_L124
    mov r0, r4
    bl native_fn_021dbd24
    mov r8, r0
    mov r0, r5
    mov r1, r4
    mov r2, r7
    bl native_fn_02218cf8
    mov r7, r0
    mov r0, r4
    bl native_fn_021dbcbc
    smull r1, r2, r6, r0
    mov r0, r0, lsr #31
    sub r1, r8, r7
    add r2, r0, r2, asr #1
    cmp r1, r2
    movle r0, #1
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02220220_L124:
    add r10, r10, #1
    cmp r10, #6
    blt ov001_02220220_Lc0
ov001_02220220_L130:
    add r11, r11, #1
    cmp r11, #3
    add r5, r5, #1088
    blt ov001_02220220_L10
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
