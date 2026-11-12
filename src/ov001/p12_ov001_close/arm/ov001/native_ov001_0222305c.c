/* ov001 row 0x0222305c: 208 bytes.
 *
 * What it does: 52 instructions; 8 call(s) to 0x021db8d0, 0x021dc1c0, 0x02218430, +5 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 8 calls (52 instructions, 8 calls, 4 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x2c -> +0xb4
 *   branch +0x3c -> +0xb4
 *   branch +0x4c -> +0xb4
 *   branch +0x6c -> +0xb4
 *   branch +0x80 -> +0xa8
 *   back edge +0xb0 -> +0x70
 *   back edge +0xc0 -> +0x20
 *   test +0x28 cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x68 cmp r9, #0
 *   test +0x7c cmp r0, #0
 *   test +0x98 cmp r0, #1
 *   test +0xac cmp r8, r9
 *   test +0xb8 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222305c; the literal pool and
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
extern void native_fn_0207b004(void);
extern void native_fn_0207afec(void);


asm u32 native_ov001_0222305c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #200
    mov r7, #0
    ldr r10, [r0, #0x8]
    add r6, sp, #0
    mov r4, #67108864
    mov r5, #200
    mov r11, r7
ov001_0222305c_L20:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0222305c_Lb4
    add r0, r10, #512
    ldrsb r0, [r0, #84]
    cmp r0, #0
    bne ov001_0222305c_Lb4
    mov r0, r10
    bl native_fn_021dc1c0
    cmp r0, #0
    beq ov001_0222305c_Lb4
    mov r0, r10
    mov r1, r6
    mov r2, r5
    bl native_fn_02218430
    mov r9, r0
    mov r8, r11
    cmp r9, #0
    ble ov001_0222305c_Lb4
ov001_0222305c_L70:
    ldr r0, [r6, r8, lsl #2]
    mov r1, r4
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_0222305c_La8
    ldr r0, [r6, r8, lsl #2]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    addeq sp, sp, #200
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_0222305c_La8:
    add r8, r8, #1
    cmp r8, r9
    blt ov001_0222305c_L70
ov001_0222305c_Lb4:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_0222305c_L20
    mov r0, #1
    add sp, sp, #200
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
