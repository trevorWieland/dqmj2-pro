/* ov001 row 0x021fd544: 184 bytes.
 *
 * What it does: 45 instructions; 3 call(s) to 0x02202360, 0x02049604, 0x021fe4ac; loops (back edge at +0x40); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (45 instructions, 3 calls, 1 branch, 2 back edges, 1 literal slot).
 *
 *   pool +0xb4 -> constant 0x02239c10 (image word 0x02239c10)
 *   back edge +0xa8 -> +0x60
 *   test +0x4c cmp r6, #0
 *   test +0x9c cmp r6, r0, asr #24
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd544; the literal pool and
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

extern void native_fn_02202360(void);
extern void native_fn_02049604(void);
extern void native_fn_021fe4ac(void);


asm u32 native_ov001_021fd544 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    ldr r4, =0x02239c10
    mov r10, r0
    ldrsb r0, [r4, #12]
    mov r9, r1
    mov r8, r2
    mov r7, r3
    bl native_fn_02202360
    ldrb r3, [sp, #0x38]
    ldrb r1, [sp, #0x3c]
    mov r2, #0
    strh r3, [r0, #12]
    strh r1, [r0, #14]
    mov r1, #1
    str r2, [r0, #0x4]
    bl native_fn_02049604
    ldrb r6, [sp, #0x38]
    mov r5, #0
    cmp r6, #0
    addle sp, sp, #20
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r4, #1
    mov r11, r5
ov001_021fd544_L60:
    str r9, [sp]
    str r8, [sp, #0x4]
    add r0, r5, #1
    str r7, [sp, #0x8]
    mov r0, r0, lsl #24
    str r4, [sp, #0xc]
    mov r1, r11
    mov r2, #26
    mov r3, r10
    mov r0, r0, asr #24
    str r4, [sp, #0x10]
    bl native_fn_021fe4ac
    add r0, r5, #1
    mov r0, r0, lsl #24
    add r1, r9, r7
    cmp r6, r0, asr #24
    and r9, r1, #255
    mov r5, r0, asr #24
    bgt ov001_021fd544_L60
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
