/* ov001 row 0x02224900: 248 bytes.
 *
 * What it does: 62 instructions; 12 call(s) to 0x02008e0c, 0x021dbd24, 0x021dbcbc, +9 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 12 calls (62 instructions, 12 calls, 2 branches, 11 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x64
 *   back edge +0x70 -> +0x30
 *   branch +0x8c -> +0xb8
 *   back edge +0xc4 -> +0x84
 *   branch +0xd8 -> +0xec
 *   test +0x34 cmp r0, #0
 *   test +0x5c cmp r0, r4
 *   test +0x68 cmp r9, #3
 *   test +0x88 cmp r0, #0
 *   test +0xb0 cmp r0, r4
 *   test +0xbc cmp r10, #3
 *   test +0xd4 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224900; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_02026144(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02224900 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r5, r1
    add r1, sp, #0
    mov r2, #12
    mov r11, r0
    mov r4, #100
    bl native_fn_02008e0c
    mov r10, r5
    mov r9, #0
    add r8, sp, #0
    mov r6, r4
ov001_02224900_L30:
    ldr r0, [r8, r9, lsl #2]
    cmp r0, #0
    beq ov001_02224900_L64
    mov r0, r10
    bl native_fn_021dbd24
    mov r7, r0
    mov r0, r10
    bl native_fn_021dbcbc
    mov r1, r0
    mul r0, r7, r6
    bl native_fn_02026144
    cmp r0, r4
    movlt r4, r0
ov001_02224900_L64:
    add r9, r9, #1
    cmp r9, #3
    add r10, r10, #1088
    blt ov001_02224900_L30
    mov r10, #0
    mov r7, r10
    add r9, sp, #0
    mov r6, #100
ov001_02224900_L84:
    ldr r0, [r9, r10, lsl #2]
    cmp r0, #0
    beq ov001_02224900_Lb8
    mov r0, r5
    bl native_fn_021dbd24
    mov r8, r0
    mov r0, r5
    bl native_fn_021dbcbc
    mov r1, r0
    mul r0, r8, r6
    bl native_fn_02026144
    cmp r0, r4
    strgt r7, [r9, r10, lsl #2]
ov001_02224900_Lb8:
    add r10, r10, #1
    cmp r10, #3
    add r5, r5, #1088
    blt ov001_02224900_L84
    add r0, sp, #0
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02224900_Lec
    add r0, sp, #0
    mov r1, r11
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224900_Lec:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
