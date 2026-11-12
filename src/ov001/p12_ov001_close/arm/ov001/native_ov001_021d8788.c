/* ov001 row 0x021d8788: 160 bytes.
 *
 * What it does: 38 instructions; 9 call(s) to 0x021d8ce0, 0x0201d6b8, 0x0201d444, +6 more; loops (back edge at +0x14); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (38 instructions, 9 calls, 2 branches, 8 back edges, 2 literal slots).
 *
 *   pool +0x98 -> native_data_0222e978 (image word 0x0222e978)
 *   pool +0x9c -> constant 0x004e4353 (image word 0x004e4353)
 *   branch +0x40 -> +0x8c
 *   branch +0x50 -> +0x74
 *   test +0x4c cmp r1, r0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d8788; the literal pool and
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

extern void native_fn_021d8ce0(void);
extern void native_fn_0201d6b8(void);
extern u8 native_data_0222e978[];
extern void native_fn_0201d444(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_021d85d4(void);
extern void native_fn_021d8640(void);
extern void native_fn_021d86cc(void);
extern void native_fn_021d873c(void);
extern void native_fn_0203cf9c(void);


asm u32 native_ov001_021d8788 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #64
    bl native_fn_021d8ce0
    mov r1, r0
    add r0, sp, #32
    bl native_fn_0201d6b8
    mov r3, #0
    ldr r1, =native_data_0222e978
    add r0, sp, #0
    add r2, sp, #32
    strb r3, [sp, #0x26]
    bl native_fn_0201d444
    add r0, sp, #0
    mov r1, #1
    bl native_fn_0203cc2c
    movs r4, r0
    beq ov001_021d8788_L8c
    ldr r1, [r4]
    ldr r0, =0x004e4353
    cmp r1, r0
    bne ov001_021d8788_L74
    add r0, r4, #4
    bl native_fn_021d85d4
    add r0, r4, #68
    bl native_fn_021d8640
    add r0, r4, #116
    bl native_fn_021d86cc
    add r0, r4, #136
    bl native_fn_021d873c
ov001_021d8788_L74:
    mov r1, r4
    mov r0, #1
    bl native_fn_0203cf9c
    add sp, sp, #64
    mov r0, #1
    ldmia sp!, {r4, pc}
ov001_021d8788_L8c:
    mov r0, #0
    add sp, sp, #64
    ldmia sp!, {r4, pc}
}
