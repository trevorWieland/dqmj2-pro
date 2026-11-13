/* ov001 row 0x0220085c: 108 bytes.
 *
 * What it does: 27 instructions; 6 call(s) to 0x02065d88, 0x021db530, 0x022008c0, +3 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 6 calls (27 instructions, 6 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x64
 *   branch +0x54 -> +0x64
 *   back edge +0x60 -> +0x38
 *   test +0x14 cmp r0, #1
 *   test +0x2c cmp r6, #0
 *   test +0x4c cmp r0, #0
 *   test +0x5c cmp r5, r6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220085c; the literal pool and
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
extern void ov001_mode_byte_021db530(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_0220d66c(void);


asm u32 native_ov001_0220085c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r4, #0
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2f]
    cmp r0, #1
    moveq r7, #1
    movne r7, r4
    mov r0, r7
    bl ov001_mode_byte_021db530
    mov r6, r0
    cmp r6, #0
    mov r5, #0
    ble ov001_0220085c_L64
ov001_0220085c_L38:
    mov r0, r7
    mov r1, r5
    bl ov001_side_slot_record_021db438
    mov r1, r8
    bl native_fn_0220d66c
    cmp r0, #0
    movne r4, #1
    bne ov001_0220085c_L64
    add r5, r5, #1
    cmp r5, r6
    blt ov001_0220085c_L38
ov001_0220085c_L64:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
