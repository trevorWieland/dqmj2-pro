/* main row 0x020a85dc: 56 bytes.
 *
 * What it does: calls 2 helpers; 2 loads, 6 stores; 3 branches; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x12 -> +0x16
 *   branch +0x26 -> +0x32
 *   branch +0x30 -> +0x32
 *   test +0x10 cmp r5, #0
 *   test +0x24 cmp r1, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a85dc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020a927c(void);


asm u32 native_main_020a85dc (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r6, r0, #0
    mov r0, #0x18
    add r5, r1, #0
    add r7, r2, #0
    bl native_fn_020a927c
    add r4, r0, #0
    cmp r5, #0
    bne main_020a85dc_L16
    mov r5, #8
main_020a85dc_L16:
    mov r0, #0
    str r0, [r4, #0]
    str r5, [r4, #4]
    str r6, [r4, #8]
    str r5, [r4, #0xc]
    str r7, [r4, #0x10]
    ldr r1, [r4, #4]
    cmp r1, #0
    beq main_020a85dc_L32
    ldr r0, [r4, #8]
    mul r0, r1
    bl native_fn_020a927c
    b main_020a85dc_L32
main_020a85dc_L32:
    str r0, [r4, #0x14]
    add r0, r4, #0
    pop {r3, r4, r5, r6, r7, pc}
}
