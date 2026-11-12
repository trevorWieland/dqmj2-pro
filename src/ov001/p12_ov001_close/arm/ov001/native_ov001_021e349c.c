/* ov001 row 0x021e349c: 84 bytes.
 *
 * What it does: 19 instructions; 2 call(s) to 0x0203cac8, 0x0203caa4; loops (back edge at +0x34); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (19 instructions, 2 calls, 1 branch, 2 back edges, 2 literal slots).
 *
 *   pool +0x4c -> constant 0x02238ad4 (image word 0x02238ad4)
 *   pool +0x50 -> constant 0x02238bd4 (image word 0x02238bd4)
 *   branch +0x28 -> +0x38
 *   test +0x10 cmp r2, #0
 *   test +0x18 cmpne r2, #0
 *   test +0x24 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e349c; the literal pool and
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

extern void native_fn_0203cac8(void);
extern void native_fn_0203caa4(void);


asm u32 native_ov001_021e349c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, =0x02238ad4
    mov r0, #0
    ldrb r2, [r1, #0x1e8]
    cmp r2, #0
    ldrneb r2, [r1, #0x1e9]
    cmpne r2, #0
    ldmeqia sp!, {r3, pc}
    ldrb r0, [r1, #0x10c]
    cmp r0, #0
    beq ov001_021e349c_L38
    ldr r0, =0x02238bd4
    mov r1, #65
    bl native_fn_0203cac8
ov001_021e349c_L38:
    ldr r0, =0x02238ad4
    mov r1, #65
    bl native_fn_0203caa4
    mov r0, #1
    ldmia sp!, {r3, pc}
}
