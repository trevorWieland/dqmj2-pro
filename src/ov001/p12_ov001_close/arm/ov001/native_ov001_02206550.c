/* ov001 row 0x02206550: 160 bytes.
 *
 * What it does: 39 instructions; 7 call(s) to 0x02213698, 0x020630b0, 0x020244c4, +4 more; loops (back edge at +0x3c); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (39 instructions, 7 calls, 0 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0x9c -> constant 0x40540000 (image word 0x40540000)
 *   test +0x40 cmp r7, r0
 *   test +0x50 cmp r5, #0
 *   test +0x58 cmp r6, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02206550; the literal pool and
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

extern void native_fn_02213698(void);
extern void native_fn_020630b0(void);
extern void native_fn_020244c4(void);
extern void native_fn_0202654c(void);
extern void native_fn_020243e0(void);


asm u32 native_ov001_02206550 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r5, [r0, #0x28]
    ldr r4, [r0, #0x40]
    mov r0, r5
    mov r7, r2
    mov r8, r1
    mov r6, r3
    bl native_fn_02213698
    add r1, r0, r7, lsl #2
    ldr r2, [r1, #-0x4]
    ldr r1, [r0, r7, lsl #2]
    ldr r0, [r5, #0x1e8]
    sub r5, r1, r2
    ldrb r0, [r0, #0xab]
    sub r8, r8, r2
    bl native_fn_020630b0
    cmp r7, r0
    moveq r0, #80
    streqb r0, [r4]
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    cmp r5, #0
    movlt r5, #0
    cmp r6, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    mov r0, r5
    bl native_fn_020244c4
    ldr r3, =0x40540000
    mov r2, #0
    bl native_fn_0202654c
    mov r5, r0
    mov r6, r1
    mov r0, r8
    bl native_fn_020244c4
    mov r2, r5
    mov r3, r6
    bl native_fn_0202654c
    bl native_fn_020243e0
    strb r0, [r4]
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
