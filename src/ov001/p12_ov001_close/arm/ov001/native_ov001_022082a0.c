/* ov001 row 0x022082a0: 144 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x02207938, 0x02208304, 0x02045994, +2 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (35 instructions, 5 calls, 0 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x8c -> constant 0x000003ff (image word 0x000003ff)
 *   branch +0x40 -> +0x64
 *   back edge +0x70 -> +0x28
 *   back edge +0x80 -> +0x24
 *   test +0x3c cmp r0, #0
 *   test +0x6c cmp r8, #32
 *   test +0x7c cmp r9, #24
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022082a0; the literal pool and
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

extern void native_fn_02207938(void);
extern void native_fn_02045994(void);


asm u32 native_ov001_022082a0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #4
    bl native_fn_02207938
    mov r9, #0
    ldr r10, =0x000003ff
    mov r7, r0
    mov r5, #2
    add r4, sp, #0
    mov r6, r9
ov001_022082a0_L24:
    mov r8, r6
ov001_022082a0_L28:
    add r2, r8, r9, lsl #5
    ldr r1, [r7, #0x14]
    mov r0, r2, lsl #1
    ldrh r3, [r1, r0]
    and r0, r3, r10
    cmp r0, #0
    ble ov001_022082a0_L64
    ldr r1, [r7, #0x18]
    mov r0, r5
    sub r1, r1, #1
    add r12, r3, r1
    mov r1, r4
    mov r3, r5
    strh r12, [sp]
    bl native_fn_02045994
ov001_022082a0_L64:
    add r0, r8, #1
    and r8, r0, #255
    cmp r8, #32
    blo ov001_022082a0_L28
    add r0, r9, #1
    and r9, r0, #255
    cmp r9, #24
    blo ov001_022082a0_L24
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
