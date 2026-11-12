/* ov001 row 0x022034e0: 80 bytes.
 *
 * What it does: 18 instructions; 3 call(s) to 0x0206b324, 0x0206b35c, 0x022023c4; loops (back edge at +0x30); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (18 instructions, 4 calls, 1 branch, 3 back edges, 2 literal slots).
 *
 *   pool +0x48 -> constant 0x0223d8ec (image word 0x0223d8ec)
 *   pool +0x4c -> native_data_0222f000 (image word 0x0222f000)
 *   branch +0x28 -> +0x40
 *   test +0x24 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022034e0; the literal pool and
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

extern u8 native_data_0222f000[];
extern void native_fn_0206b324(void);
extern void native_fn_0206b35c(void);
extern void native_fn_022023c4(void);


asm u32 native_ov001_022034e0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x0223d8ec
    ldr r1, =native_data_0222f000
    ldrsb r0, [r0, #8]
    ldr r0, [r1, r0, lsl #2]
    blx r0
    ldr r1, =0x0223d8ec
    mov r4, r0
    ldrsb r0, [r1, #1]
    cmp r0, #0
    beq ov001_022034e0_L40
    mov r0, #1
    bl native_fn_0206b324
    bl native_fn_0206b35c
    mov r0, #8
    bl native_fn_022023c4
ov001_022034e0_L40:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
