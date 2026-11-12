/* ov006 row 0x02206080: 128 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> constant 0x0221c27c (image word 0x0221c27c)
 *   pool +0x74 -> constant 0x0221c418 (image word 0x0221c418)
 *   pool +0x78 -> native_data_0220e940 (image word 0x0220e940)
 *   pool +0x7c -> native_data2_0220e940 (image word 0x0220e940)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02206080; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021e6488(void);
extern void native_fn_02062a10(void);
extern void native_fn_02008e0c(void);
extern void native_fn_021eacf8(void);
extern void native_fn_021eb9a4(void);
extern void native_fn_021e71e4(void);
extern u8 native_data_0220e940[];
extern void native_fn_0207e97c(void);
extern u8 native_data2_0220e940[];
extern void native_fn_0207e720(void);
extern void native_fn_021e7a18(void);
extern void native_fn_0207e874(void);


asm u32 native_ov006_02206080 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_021e6488
    ldr r0, =0x0221c27c
    ldr r0, [r0, #0xc]
    bl native_fn_02062a10
    ldr r1, =0x0221c418
    mov r2, #132
    bl native_fn_02008e0c
    ldr r0, =0x0221c418
    bl native_fn_021eacf8
    mov r0, #12
    mov r1, #1
    mov r2, #0
    bl native_fn_021eb9a4
    bl native_fn_021e71e4
    ldr r1, =0x0221c418
    ldr r0, =native_data_0220e940
    ldrsh r2, [r1, #24]
    ldrb r1, [r1, #0x1b]
    strh r2, [r0, #2]
    strb r1, [r0, #0x5]
    bl native_fn_0207e97c
    ldr r0, =native_data2_0220e940
    bl native_fn_0207e720
    mov r0, #0
    bl native_fn_021e7a18
    bl native_fn_0207e874
    ldmia sp!, {r3, pc}
}
