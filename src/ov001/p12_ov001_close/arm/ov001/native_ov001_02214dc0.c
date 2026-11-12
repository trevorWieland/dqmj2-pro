/* ov001 row 0x02214dc0: 104 bytes.
 *
 * What it does: 25 instructions; 4 call(s) to 0x0221495c, 0x02214968, 0x02214b6c, +1 more; loops (back edge at +0x30); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (25 instructions, 4 calls, 10 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0x64 -> constant 0x02242b94 (image word 0x02242b94)
 *   branch +0x18 -> +0x54
 *   branch +0x1c -> +0x30
 *   branch +0x20 -> +0x38
 *   branch +0x24 -> +0x54
 *   branch +0x28 -> +0x40
 *   branch +0x2c -> +0x48
 *   branch +0x34 -> +0x54
 *   branch +0x3c -> +0x54
 *   branch +0x44 -> +0x54
 *   back edge +0x58 -> +0x0c
 *   test +0x10 cmp r1, #4
 *   test +0x54 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02214dc0; the literal pool and
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

extern void native_fn_0221495c(void);
extern void native_fn_02214968(void);
extern void native_fn_02214b6c(void);
extern void native_fn_02214db4(void);


asm u32 native_ov001_02214dc0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, =0x02242b94
    mov r0, #1
ov001_02214dc0_Lc:
    ldrsb r1, [r4, #3]
    cmp r1, #4
    addls pc, pc, r1, lsl #2
    b ov001_02214dc0_L54
    b ov001_02214dc0_L30
    b ov001_02214dc0_L38
    b ov001_02214dc0_L54
    b ov001_02214dc0_L40
    b ov001_02214dc0_L48
ov001_02214dc0_L30:
    bl native_fn_0221495c
    b ov001_02214dc0_L54
ov001_02214dc0_L38:
    bl native_fn_02214968
    b ov001_02214dc0_L54
ov001_02214dc0_L40:
    bl native_fn_02214b6c
    b ov001_02214dc0_L54
ov001_02214dc0_L48:
    bl native_fn_02214db4
    mov r0, #1
    ldmia sp!, {r4, pc}
ov001_02214dc0_L54:
    cmp r0, #0
    bne ov001_02214dc0_Lc
    mov r0, #0
    ldmia sp!, {r4, pc}
}
