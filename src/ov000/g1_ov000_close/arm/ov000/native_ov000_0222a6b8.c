/* ov000 row 0x0222a6b8: 160 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x02001950, 0x020019b0, 0x02001a88, +2 more; loops (back edge at +0x10); returns through pop {r3, r4, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x8c -> constant 0x020edf98 (image word 0x020edf98)
 *   pool +0x90 -> constant 0x02247568 (image word 0x02247568)
 *   pool +0x94 -> constant 0xfffff333 (image word 0xfffff333)
 *   pool +0x98 -> constant 0x00001ccd (image word 0x00001ccd)
 *   pool +0x9c -> constant 0x020edf90 (image word 0x020edf90)
 *   test +0x20 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222a6b8; the literal pool and
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

extern void native_fn_02001950(void);
extern void native_fn_020019b0(void);
extern void native_fn_02001a88(void);
extern void native_fn_02001bac(void);
extern void native_fn_02008ca4(void);


asm u32 native_ov000_0222a6b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #132
    add r0, sp, #68
    ldr r4, =0x020edf98
    bl native_fn_02001950
    ldr r0, =0x02247568
    mov r2, #0
    ldrb r0, [r0]
    cmp r0, #0
    ldrne r3, =0xfffff333
    add r0, sp, #68
    ldreq r3, =0x00001ccd
    mov r1, r0
    str r2, [sp]
    bl native_fn_020019b0
    add r0, sp, #68
    mov r2, #4096
    mov r1, r0
    mov r3, #8192
    str r2, [sp]
    bl native_fn_02001a88
    add r1, sp, #68
    add r2, sp, #4
    mov r0, r4
    bl native_fn_02001bac
    ldr r1, =0x020edf98
    add r0, sp, #4
    mov r2, #64
    bl native_fn_02008ca4
    ldr r0, =0x020edf90
    ldr r1, [r0, #0xfc]
    bic r1, r1, #80
    str r1, [r0, #0xfc]
    add sp, sp, #132
    ldmia sp!, {r3, r4, pc}
}
