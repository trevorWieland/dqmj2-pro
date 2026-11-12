/* ov001 row 0x02225164: 240 bytes.
 *
 * What it does: 60 instructions; 10 call(s) to 0x02008e0c, 0x021dbe68, 0x021dbe5c, +7 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 10 calls (60 instructions, 10 calls, 2 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x7c
 *   back edge +0x88 -> +0x2c
 *   branch +0xa4 -> +0xb4
 *   back edge +0xbc -> +0x9c
 *   branch +0xd0 -> +0xe4
 *   test +0x30 cmp r0, #0
 *   test +0x70 cmp r9, r0
 *   test +0x80 cmp r8, #3
 *   test +0xa0 cmp r1, #0
 *   test +0xac cmp r1, r9
 *   test +0xb8 cmp r4, #3
 *   test +0xcc cmp r4, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225164; the literal pool and
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
extern void native_fn_021dbe68(void);
extern void native_fn_021dbe5c(void);
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbd8c(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02225164 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    mov r10, r1
    add r1, sp, #4
    mov r2, #12
    str r0, [sp]
    mov r9, #0
    bl native_fn_02008e0c
    mov r8, r9
    add r11, sp, #16
    add r7, sp, #4
ov001_02225164_L2c:
    ldr r0, [r7, r8, lsl #2]
    cmp r0, #0
    beq ov001_02225164_L7c
    mov r0, r10
    bl native_fn_021dbe68
    mov r6, r0
    mov r0, r10
    bl native_fn_021dbe5c
    mov r5, r0
    mov r0, r10
    bl native_fn_021dbd3c
    mov r4, r0
    mov r0, r10
    bl native_fn_021dbd8c
    add r0, r4, r0
    add r0, r5, r0
    add r0, r6, r0
    cmp r9, r0
    str r0, [r11, r8, lsl #2]
    movlt r9, r0
ov001_02225164_L7c:
    add r8, r8, #1
    cmp r8, #3
    add r10, r10, #1088
    blt ov001_02225164_L2c
    mov r4, #0
    mov r0, r4
    add r2, sp, #16
    add r3, sp, #4
ov001_02225164_L9c:
    ldr r1, [r3, r4, lsl #2]
    cmp r1, #0
    beq ov001_02225164_Lb4
    ldr r1, [r2, r4, lsl #2]
    cmp r1, r9
    strlt r0, [r3, r4, lsl #2]
ov001_02225164_Lb4:
    add r4, r4, #1
    cmp r4, #3
    blt ov001_02225164_L9c
    add r0, sp, #4
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225164_Le4
    ldr r1, [sp]
    add r0, sp, #4
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225164_Le4:
    mov r0, r4
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
