/* ov006 row 0x021f4404: 76 bytes.
 *
 * What it does: 29 instructions; 6 call(s) to 0x02202f98, 0x021f442e, 0x021f4944, +3 more; no back edge; returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x44 -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0x48 -> native_fn_021f4450+1 (image word 0x021f4451)
 *   branch +0x1e -> +0x2a
 *   test +0x1c cmp r1, #0xaa
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4404; the literal pool and
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

extern void native_fn_02202f98(void);
extern void native_fn_021f4944(void);
extern void native_fn_021f4b50(void);
extern void native_fn_021f4450(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f4404 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r2, sp, #0x4
    ldr r0, [r0, #0x40]
    add r3, sp, #0x0
    bl native_fn_02202f98
    ldr r1, [sp]
    sub r1, #0xc
    str r1, [sp]
    cmp r1, #0xaa
    ble ov006_021f4404_L2a
    mov r0, #0x4
    bl native_fn_021f4944
    add sp, #0x8
    pop {r4, pc}
ov006_021f4404_L2a:
    mov r0, #0x4
    mov r1, #0xaa
    bl native_fn_021f4944
    bl native_fn_021f4b50
    ldr r1, =native_fn_021f4450+1
    add r0, r4, #0x0
    bl native_fn_02204970
    add sp, #0x8
    pop {r4, pc}
    mov r8, r8
}
