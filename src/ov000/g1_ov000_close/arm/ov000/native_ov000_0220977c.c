/* ov000 row 0x0220977c: 144 bytes.
 *
 * What it does: 33 instructions; 6 call(s) to 0x020c4938, 0x02008c58, 0x02046150, +3 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> constant 0x02238570 (image word 0x02238570)
 *   pool +0x88 -> constant 0x04001008 (image word 0x04001008)
 *   pool +0x8c -> constant 0x04001000 (image word 0x04001000)
 *   back edge +0x4c -> +0x30
 *   test +0x48 cmp r4, #4
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220977c; the literal pool and
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

extern void native_fn_020c4938(void);
extern void native_fn_02008c58(void);
extern void native_fn_02046150(void);
extern void native_fn_0221745c(void);
extern void native_fn_02048f3c(void);


asm u32 native_ov000_0220977c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_020c4938
    mov r5, r0
    ldr r1, =0x02238570
    mov r0, #0
    mov r2, #72
    bl native_fn_02008c58
    mov r0, #2
    mov r1, r0
    mov r2, r0
    bl native_fn_02046150
    mov r4, #0
ov000_0220977c_L30:
    ldr r1, [r5, r4, lsl #4]
    mov r0, r4
    bl native_fn_0221745c
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #4
    blt ov000_0220977c_L30
    ldr r3, =0x04001008
    mov r0, #0
    ldrh r2, [r3]
    mov r1, #1
    bic r2, r2, #3
    strh r2, [r3]
    bl native_fn_02048f3c
    ldr r1, =0x04001000
    ldr r0, [r1]
    bic r0, r0, #7936
    orr r0, r0, #4352
    str r0, [r1]
    ldmia sp!, {r3, r4, r5, pc}
}
