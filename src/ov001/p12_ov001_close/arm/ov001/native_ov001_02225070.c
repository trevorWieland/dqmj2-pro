/* ov001 row 0x02225070: 244 bytes.
 *
 * What it does: 61 instructions; 9 call(s) to 0x02008e0c, 0x021dbd24, 0x021dbe5c, +6 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 9 calls (61 instructions, 9 calls, 2 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x80
 *   back edge +0x8c -> +0x30
 *   branch +0xa8 -> +0xb8
 *   back edge +0xc0 -> +0xa0
 *   branch +0xd4 -> +0xe8
 *   test +0x34 cmp r0, #0
 *   test +0x74 cmp r1, r7
 *   test +0x84 cmp r6, #3
 *   test +0xa4 cmp r1, #0
 *   test +0xb0 cmp r1, r7
 *   test +0xbc cmp r4, #3
 *   test +0xd0 cmp r4, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225070; the literal pool and
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
extern void native_fn_021dbe5c(void);
extern void native_fn_02223f48(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02225070 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    mov r10, r1
    mov r9, r2
    add r1, sp, #4
    mov r2, #12
    str r0, [sp]
    mov r8, r3
    mov r7, #0
    bl native_fn_02008e0c
    mov r6, r7
    add r11, sp, #4
ov001_02225070_L30:
    ldr r0, [r11, r6, lsl #2]
    cmp r0, #0
    beq ov001_02225070_L80
    mov r0, r9
    bl native_fn_021dbd24
    mov r5, r0
    mov r0, r9
    bl native_fn_021dbe5c
    mov r4, r0
    mov r0, r10
    mov r1, r9
    mov r2, r8
    mov r3, #2
    bl native_fn_02223f48
    add r1, r5, r4, lsl #1
    sub r1, r1, r0
    add r0, sp, #16
    cmp r1, r7
    str r1, [r0, r6, lsl #2]
    movgt r7, r1
ov001_02225070_L80:
    add r6, r6, #1
    cmp r6, #3
    add r9, r9, #1088
    blt ov001_02225070_L30
    mov r4, #0
    mov r0, r4
    add r2, sp, #16
    add r3, sp, #4
ov001_02225070_La0:
    ldr r1, [r3, r4, lsl #2]
    cmp r1, #0
    beq ov001_02225070_Lb8
    ldr r1, [r2, r4, lsl #2]
    cmp r1, r7
    strlt r0, [r3, r4, lsl #2]
ov001_02225070_Lb8:
    add r4, r4, #1
    cmp r4, #3
    blt ov001_02225070_La0
    add r0, sp, #4
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225070_Le8
    ldr r1, [sp]
    add r0, sp, #4
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225070_Le8:
    mov r0, r4
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
