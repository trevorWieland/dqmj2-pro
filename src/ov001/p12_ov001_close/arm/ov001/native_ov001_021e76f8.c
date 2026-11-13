/* ov001 row 0x021e76f8: 72 bytes.
 *
 * What it does: 17 instructions; 4 call(s) to 0x021db438, 0x021dbe5c, 0x0203d294, +1 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (17 instructions, 4 calls, 0 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0x44 -> constant 0x51eb851f (image word 0x51eb851f)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e76f8; the literal pool and
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

extern void ov001_side_slot_record_021db438(void);
extern void native_fn_021dbe5c(void);
extern void native_fn_0203d294(void);
extern void native_fn_0220f11c(void);


asm u32 native_ov001_021e76f8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl ov001_side_slot_record_021db438
    mov r5, r0
    bl native_fn_021dbe5c
    mov r4, r0
    mov r0, #51
    bl native_fn_0203d294
    add r0, r0, #50
    mul r12, r4, r0
    ldr r2, =0x51eb851f
    ldr r3, [r5, #0x1e8]
    smull r0, r1, r2, r12
    mov r0, r12, lsr #31
    add r1, r0, r1, asr #5
    add r0, r3, #70
    bl native_fn_0220f11c
    ldmia sp!, {r3, r4, r5, pc}
}
