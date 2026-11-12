/* ov006 row 0x021ea314: 72 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ea314; the literal pool and
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

extern void native_fn_021ea2d0(void);
extern void native_fn_02067af4(void);
extern void native_fn_021ea2ac(void);
extern void native_fn_021e7f08(void);
extern void native_fn_021e75ec(void);
extern void native_fn_021e7b64(void);


asm u32 native_ov006_021ea314 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl native_fn_021ea2d0
    mov r4, r0
    mov r0, r5
    bl native_fn_02067af4
    bl native_fn_021ea2ac
    add r1, r4, r4, lsl #2
    add r0, r0, r1
    add r2, r0, #10
    mov r0, #7
    mov r1, #9
    bl native_fn_021e7f08
    add r0, r5, #44
    bl native_fn_021e75ec
    add r0, r5, #44
    bl native_fn_021e7b64
    ldmia sp!, {r3, r4, r5, pc}
}
