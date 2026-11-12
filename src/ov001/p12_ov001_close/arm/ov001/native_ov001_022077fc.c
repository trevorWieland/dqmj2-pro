/* ov001 row 0x022077fc: 156 bytes.
 *
 * What it does: 39 instructions; 5 call(s) to 0x022068a0, 0x02049ffc, 0x02085270, +2 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 5 calls (39 instructions, 5 calls, 0 branches, 5 back edges, 0 literal slots).
 *
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022077fc; the literal pool and
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
extern void native_fn_02049ffc(void);
extern void native_fn_02085270(void);
extern void native_fn_02048094(void);
extern void native_fn_0204a574(void);


asm u32 native_ov001_022077fc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #16
    mov r5, r0
    mov r4, r1
    bl native_fn_022068a0
    add r0, r0, r5, lsl #5
    ldr r0, [r0, #0x1c]
    add r2, sp, #12
    ldr r0, [r0]
    mov r1, #0
    ldr r6, [r0, #0x4]
    mov r0, r6
    strh r1, [r2]
    strh r1, [r2, #2]
    bl native_fn_02049ffc
    add r0, r6, #60
    mov r1, #16
    mov r2, #2
    bl native_fn_02085270
    mov r0, r4
    mov r1, #0
    bl native_fn_02048094
    mov r0, r5, lsl #1
    mov r1, #0
    add r0, r0, #1
    mov r0, r0, lsl #24
    str r1, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r1, [sp, #0x8]
    mov r0, r0, asr #24
    add r1, sp, #12
    mov r3, #3
    bl native_fn_0204a574
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, pc}
}
