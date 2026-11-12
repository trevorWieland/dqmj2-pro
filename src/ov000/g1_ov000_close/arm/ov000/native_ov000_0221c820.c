/* ov000 row 0x0221c820: 188 bytes.
 *
 * What it does: 46 instructions; 5 call(s) to 0x02008be0, 0x02087a48, 0x020877bc, +2 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb8 -> constant 0x020dbf18 (image word 0x020dbf18)
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221c820; the literal pool and
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

extern void native_fn_02008be0(void);
extern void native_fn_02087a48(void);
extern void native_fn_020877bc(void);
extern void native_fn_02086b14(void);


asm u32 native_ov000_0221c820 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #32
    mov r6, r1
    mov r7, r0
    mov r5, r2
    add r1, sp, #8
    mov r0, #0
    mov r2, #22
    mov r4, r3
    bl native_fn_02008be0
    ldr r0, =0x020dbf18
    mov r1, #58
    ldrh r0, [r0, #66]
    strh r1, [sp, #10]
    mov r1, #0
    strh r0, [sp, #8]
    strh r1, [sp, #12]
    mov r0, #1
    str r0, [sp]
    add r2, sp, #8
    str r2, [sp, #0x4]
    mov r0, r7
    mov r2, r5
    mov r3, r4
    bl native_fn_02087a48
    mov r0, r6
    add r1, sp, #8
    mov r2, #8
    mov r3, #7
    bl native_fn_020877bc
    add r0, r5, #8
    mov r0, r0, lsl #16
    mov r2, r0, asr #16
    mov r0, #1
    str r0, [sp]
    add r1, sp, #8
    str r1, [sp, #0x4]
    mov r3, r4
    mov r0, r7
    mov r1, #0
    bl native_fn_02087a48
    mov r0, r7
    mov r1, #0
    bl native_fn_02086b14
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
