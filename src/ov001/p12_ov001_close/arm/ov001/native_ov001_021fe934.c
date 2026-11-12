/* ov001 row 0x021fe934: 124 bytes.
 *
 * What it does: 28 instructions; 4 call(s) to 0x021fe6b8, 0x02065d00, 0x02065d14, +1 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (28 instructions, 4 calls, 0 branches, 4 back edges, 3 literal slots).
 *
 *   pool +0x70 -> native_data_0222ed88 (image word 0x0222ed88)
 *   pool +0x74 -> native_data_0222ed89 (image word 0x0222ed89)
 *   pool +0x78 -> native_data_0222ed8a (image word 0x0222ed8a)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fe934; the literal pool and
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

extern void native_fn_021fe6b8(void);
extern u8 native_data_0222ed88[];
extern u8 native_data_0222ed89[];
extern u8 native_data_0222ed8a[];
extern void native_fn_02065d00(void);
extern void native_fn_02065d14(void);
extern void native_fn_02045dc4(void);


asm u32 native_ov001_021fe934 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #8
    mov r6, r0
    mov r5, r1
    mov r4, r2
    bl native_fn_021fe6b8
    ldr r0, =native_data_0222ed88
    add r2, r6, r6, lsl #1
    ldrsb r6, [r0, r2]
    ldr r1, =native_data_0222ed89
    ldr r0, =native_data_0222ed8a
    ldrb r7, [r1, r2]
    ldrb r8, [r0, r2]
    mov r0, r6
    bl native_fn_02065d00
    and r9, r0, #255
    mov r0, r6
    bl native_fn_02065d14
    str r9, [sp]
    mov r1, r8
    mov r2, r5
    mov r3, r4
    and r0, r0, #255
    str r0, [sp, #0x4]
    mov r0, r7
    bl native_fn_02045dc4
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
