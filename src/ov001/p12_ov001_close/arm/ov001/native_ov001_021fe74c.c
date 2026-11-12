/* ov001 row 0x021fe74c: 280 bytes.
 *
 * What it does: 69 instructions; 20 call(s) to 0x02202360, 0x021fe54c, 0x021fe54c, +17 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 20 calls (69 instructions, 20 calls, 6 branches, 14 back edges, 1 literal slot).
 *
 *   pool +0x114 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x1c -> +0x34
 *   branch +0x20 -> +0xa4
 *   branch +0x24 -> +0xa4
 *   branch +0x28 -> +0xa4
 *   branch +0x2c -> +0xa4
 *   branch +0x30 -> +0xa4
 *   test +0x10 cmp r5, #5
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fe74c; the literal pool and
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

extern void native_fn_02202360(void);
extern void native_fn_021fe54c(void);
extern void native_fn_022042c4(void);
extern void native_fn_021fe9b0(void);
extern void native_fn_022023c4(void);


asm u32 native_ov001_021fe74c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl native_fn_02202360
    mov r4, r0
    cmp r5, #5
    addls pc, pc, r5, lsl #2
    ldmia sp!, {r3, r4, r5, pc}
    b ov001_021fe74c_L34
    b ov001_021fe74c_La4
    b ov001_021fe74c_La4
    b ov001_021fe74c_La4
    b ov001_021fe74c_La4
    b ov001_021fe74c_La4
ov001_021fe74c_L34:
    mov r0, r5
    mov r1, #30
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #127
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #27
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #26
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #32
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #33
    bl native_fn_021fe54c
    add r0, r4, #24
    bl native_fn_022042c4
    bl native_fn_021fe9b0
    mov r0, r5
    mov r1, #127
    bl native_fn_021fe54c
    ldr r0, =0x02239c10
    mov r1, #4
    strb r1, [r0, #0xe]
    ldmia sp!, {r3, r4, r5, pc}
ov001_021fe74c_La4:
    mov r0, r5
    mov r1, #30
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #21
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #22
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #127
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #31
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #32
    bl native_fn_021fe54c
    mov r0, r5
    mov r1, #33
    bl native_fn_021fe54c
    add r0, r4, #168
    bl native_fn_022042c4
    add r0, r4, #24
    bl native_fn_022042c4
    mov r0, #143
    bl native_fn_022023c4
    ldmia sp!, {r3, r4, r5, pc}
}
