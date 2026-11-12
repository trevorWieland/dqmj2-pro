/* ov001 row 0x0221d3dc: 92 bytes.
 *
 * What it does: 23 instructions; 5 call(s) to 0x021dbd24, 0x021db8d0, 0x021dbd24, +2 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 5 calls (23 instructions, 5 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x38
 *   branch +0x34 -> +0x54
 *   back edge +0x50 -> +0x18
 *   test +0x20 cmp r0, #0
 *   test +0x30 cmp r5, r0
 *   test +0x38 cmp r4, #2
 *   test +0x48 cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221d3dc; the literal pool and
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

extern void native_fn_021dbd24(void);
extern void ov001_record_is_active_021db8d0(void);


asm u32 native_ov001_0221d3dc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r6, [r0, #0x8]
    ldr r0, [r0]
    bl native_fn_021dbd24
    mov r5, r0
    mov r4, #0
ov001_0221d3dc_L18:
    mov r0, r6
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221d3dc_L38
    mov r0, r6
    bl native_fn_021dbd24
    cmp r5, r0
    ble ov001_0221d3dc_L54
ov001_0221d3dc_L38:
    cmp r4, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r4, r4, #1
    cmp r4, #3
    add r6, r6, #1088
    blt ov001_0221d3dc_L18
ov001_0221d3dc_L54:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
