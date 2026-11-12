/* ov001 row 0x02213ce4: 196 bytes.
 *
 * What it does: 47 instructions; 8 call(s) to 0x02008d78, 0x02213bac, 0x02213bac, +5 more; loops (back edge at +0x10); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (47 instructions, 8 calls, 0 branches, 8 back edges, 2 literal slots).
 *
 *   pool +0xbc -> constant 0x02242ab4 (image word 0x02242ab4)
 *   pool +0xc0 -> constant 0x02242aac (image word 0x02242aac)
 *   test +0x9c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213ce4; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02213bac(void);
extern void native_fn_02213c78(void);


asm u32 native_ov001_02213ce4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02242ab4
    mov r1, #0
    mov r2, #156
    bl native_fn_02008d78
    mov r0, #8
    mov r1, #2
    mov r2, #6
    mov r3, #0
    bl native_fn_02213bac
    mov r3, r0
    mov r0, #16
    mov r1, #2
    mov r2, #9
    bl native_fn_02213bac
    mov r3, r0
    mov r0, #32
    mov r1, #2
    mov r2, #9
    bl native_fn_02213bac
    mov r2, r0
    mov r0, #1
    mov r1, #0
    bl native_fn_02213c78
    mov r1, #0
    mov r3, r0
    mov r0, #512
    mov r2, r1
    bl native_fn_02213bac
    mov r1, #0
    mov r3, r0
    mov r0, #8388608
    mov r2, r1
    bl native_fn_02213bac
    mov r3, r0
    mov r0, #16777216
    mov r1, #3
    mov r2, #78
    bl native_fn_02213bac
    cmp r0, #0
    ldrgt r0, =0x02242aac
    movgt r1, #1
    ldrle r0, =0x02242aac
    movle r1, #3
    strb r1, [r0, #0x1]
    mov r0, #0
    ldmia sp!, {r3, pc}
}
