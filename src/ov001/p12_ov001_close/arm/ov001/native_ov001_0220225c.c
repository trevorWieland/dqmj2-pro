/* ov001 row 0x0220225c: 160 bytes.
 *
 * What it does: 39 instructions; 7 call(s) to 0x021db530, 0x022022dc, 0x021e81d0, +4 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (39 instructions, 7 calls, 0 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0x9c -> constant 0x02239d04 (image word 0x02239d04)
 *   branch +0x18 -> +0x80
 *   back edge +0x7c -> +0x2c
 *   test +0x10 cmp r6, #0
 *   test +0x6c cmp r5, r6
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220225c; the literal pool and
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

extern void native_fn_021db530(void);
extern void native_fn_021e81d0(void);
extern void native_fn_021db438(void);
extern void native_fn_02203308(void);
extern void native_fn_0203d2dc(void);


asm u32 native_ov001_0220225c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r0, #0
    bl native_fn_021db530
    mov r6, r0
    cmp r6, #0
    mov r5, #0
    ble ov001_0220225c_L80
    ldr r7, =0x02239d04
    mov r4, r5
    mov r8, r7
    mov r9, r5
ov001_0220225c_L2c:
    mov r0, r4
    mov r1, r5
    bl native_fn_021e81d0
    ldrh r2, [r0]
    mov r1, r5
    strh r2, [r7, #4]
    ldrb r2, [r0, #0x2]
    strb r2, [r7, #0x6]
    ldrsb r2, [r0, #3]
    strb r2, [r7, #0x7]
    ldrb r2, [r0, #0x4]
    mov r0, r9
    strb r2, [r7, #0x8]
    bl native_fn_021db438
    ldrb r0, [r0, #0x1fe]
    add r5, r5, #1
    cmp r5, r6
    strb r0, [r8, #0x1]
    add r7, r7, #6
    add r8, r8, #1
    blt ov001_0220225c_L2c
ov001_0220225c_L80:
    mov r0, #0
    mov r1, r0
    bl native_fn_02203308
    bl native_fn_0203d2dc
    ldr r1, =0x02239d04
    str r0, [r1, #0x18]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
