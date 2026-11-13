/* ov001 row 0x0221be78: 88 bytes.
 *
 * What it does: 22 instructions; 3 call(s) to 0x021db8d0, 0x021dbd24, 0x0221be88; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 3 calls (22 instructions, 3 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x40
 *   back edge +0x4c -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x34 cmp r0, r1, asr #1
 *   test +0x44 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221be78; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbd24(void);


asm u32 native_ov001_0221be78 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r4, [r0]
    ldr r6, [r0, #0x8]
    mov r5, #0
ov001_0221be78_L10:
    mov r0, r6
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221be78_L40
    mov r0, r6
    bl native_fn_021dbd24
    ldrb r1, [r4, #0x1fc]
    add r1, r1, r1, lsl #1
    add r1, r1, r1, lsr #31
    cmp r0, r1, asr #1
    movle r0, #1
    ldmleia sp!, {r4, r5, r6, pc}
ov001_0221be78_L40:
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_0221be78_L10
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
