/* ov001 row 0x02213a4c: 144 bytes.
 *
 * What it does: 34 instructions; 5 call(s) to 0x02065d88, 0x02065d88, 0x02213aac, +2 more; loops (back edge at +0x34); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (34 instructions, 5 calls, 1 branch, 4 back edges, 2 literal slots).
 *
 *   pool +0x88 -> constant 0x02242998 (image word 0x02242998)
 *   pool +0x8c -> constant 0x022429ac (image word 0x022429ac)
 *   branch +0x28 -> +0x74
 *   branch +0x4c -> +0x60
 *   back edge +0x70 -> +0x30
 *   back edge +0x80 -> +0x20
 *   test +0x10 cmp r0, #0
 *   test +0x24 cmp r6, r0
 *   test +0x48 cmp r7, r0
 *   test +0x6c cmp r6, r0
 *   test +0x78 cmp r5, r0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213a4c; the literal pool and
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

extern void native_fn_02065d88(void);


asm u32 native_ov001_02213a4c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldr r10, =0x02242998
    mov r5, #0
    ldrb r0, [r10, #0x2]
    cmp r0, #0
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    ldr r8, =0x022429ac
    mov r4, r8
ov001_02213a4c_L20:
    add r6, r5, #1
    cmp r6, r0
    bge ov001_02213a4c_L74
    add r9, r4, r6
ov001_02213a4c_L30:
    ldrb r0, [r8]
    bl native_fn_02065d88
    ldrh r7, [r0, #12]
    ldrb r0, [r9]
    bl native_fn_02065d88
    ldrh r0, [r0, #12]
    cmp r7, r0
    ble ov001_02213a4c_L60
    ldrb r1, [r8]
    ldrb r0, [r9]
    strb r0, [r8]
    strb r1, [r9]
ov001_02213a4c_L60:
    ldrb r0, [r10, #0x2]
    add r6, r6, #1
    add r9, r9, #1
    cmp r6, r0
    blt ov001_02213a4c_L30
ov001_02213a4c_L74:
    add r5, r5, #1
    cmp r5, r0
    add r8, r8, #1
    blt ov001_02213a4c_L20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
