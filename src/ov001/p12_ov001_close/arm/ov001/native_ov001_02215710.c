/* ov001 row 0x02215710: 80 bytes.
 *
 * What it does: 18 instructions; 4 call(s) to 0x02062b0c, 0x021e6744, 0x0203d0d8, +1 more; loops (back edge at +0x04); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (18 instructions, 4 calls, 0 branches, 4 back edges, 2 literal slots).
 *
 *   pool +0x48 -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x4c -> constant 0x02242ba0 (image word 0x02242ba0)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02215710; the literal pool and
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

extern void native_fn_02062b0c(void);
extern void native_fn_021e6744(void);
extern void native_fn_0203d0d8(void);
extern void native_fn_021d75d4(void);


asm u32 native_ov001_02215710 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02062b0c
    add r0, r0, r0, lsl #1
    add r0, r0, #99
    ldr r3, =0x51eb851f
    mov r1, r0, lsr #31
    smull r2, r0, r3, r0
    add r0, r1, r0, asr #5
    bl native_fn_021e6744
    mov r0, #3
    mov r1, #1
    bl native_fn_0203d0d8
    ldr r1, =0x02242ba0
    mov r0, #2
    str r0, [r1, #0x8]
    bl native_fn_021d75d4
    mov r0, #1
    ldmia sp!, {r3, pc}
}
