/* ov001 row 0x02214fb4: 92 bytes.
 *
 * What it does: 22 instructions; 3 call(s) to 0x02214e28, 0x02214e68, 0x02214fac; loops (back edge at +0x2c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (22 instructions, 3 calls, 7 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x58 -> constant 0x02242b94 (image word 0x02242b94)
 *   branch +0x14 -> +0x2c
 *   branch +0x1c -> +0x34
 *   branch +0x24 -> +0x3c
 *   branch +0x28 -> +0x48
 *   branch +0x30 -> +0x48
 *   branch +0x38 -> +0x48
 *   back edge +0x4c -> +0x0c
 *   test +0x10 cmp r1, #0
 *   test +0x18 cmp r1, #3
 *   test +0x20 cmp r1, #4
 *   test +0x48 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02214fb4; the literal pool and
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

extern void native_fn_02214e28(void);
extern void native_fn_02214e68(void);
extern void native_fn_02214fac(void);


asm u32 native_ov001_02214fb4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, =0x02242b94
    mov r0, #1
ov001_02214fb4_Lc:
    ldrsb r1, [r4, #3]
    cmp r1, #0
    beq ov001_02214fb4_L2c
    cmp r1, #3
    beq ov001_02214fb4_L34
    cmp r1, #4
    beq ov001_02214fb4_L3c
    b ov001_02214fb4_L48
ov001_02214fb4_L2c:
    bl native_fn_02214e28
    b ov001_02214fb4_L48
ov001_02214fb4_L34:
    bl native_fn_02214e68
    b ov001_02214fb4_L48
ov001_02214fb4_L3c:
    bl native_fn_02214fac
    mov r0, #1
    ldmia sp!, {r4, pc}
ov001_02214fb4_L48:
    cmp r0, #0
    bne ov001_02214fb4_Lc
    mov r0, #0
    ldmia sp!, {r4, pc}
}
