/* ov001 row 0x02207898: 160 bytes.
 *
 * What it does: 40 instructions; 6 call(s) to 0x022068a0, 0x02062a50, 0x02085270, +3 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 6 calls (40 instructions, 6 calls, 0 branches, 6 back edges, 0 literal slots).
 *
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02207898; the literal pool and
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

extern void native_fn_022068a0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02085270(void);
extern void native_fn_02060954(void);
extern void native_fn_02048034(void);
extern void native_fn_0204a574(void);


asm u32 native_ov001_02207898 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #16
    mov r5, r0
    mov r4, r1
    bl native_fn_022068a0
    add r0, r0, r5, lsl #5
    ldr r1, [r0, #0x1c]
    ldr r0, [r0, #0x24]
    ldr r1, [r1]
    ldrb r0, [r0, #0x31f]
    ldr r7, [r1, #0x4]
    bl native_fn_02062a50
    mov r6, r0
    add r2, sp, #12
    mov r1, #0
    add r0, r7, #60
    strh r1, [r2]
    strh r1, [r2, #2]
    mov r1, #16
    mov r2, #2
    bl native_fn_02085270
    mov r0, r4
    mov r1, #0
    bl native_fn_02060954
    mov r0, r6
    mov r1, #2
    bl native_fn_02048034
    mov r0, r5, lsl #1
    add r0, r0, #1
    mov r2, #1
    mov r0, r0, lsl #24
    str r2, [sp]
    str r2, [sp, #0x4]
    mov r0, r0, asr #24
    add r1, sp, #12
    mov r3, #3
    str r2, [sp, #0x8]
    bl native_fn_0204a574
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
