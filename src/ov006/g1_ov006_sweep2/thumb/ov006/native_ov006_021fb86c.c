/* ov006 row 0x021fb86c: 124 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x0e -> +0x14
 *   branch +0x1c -> +0x3a
 *   branch +0x28 -> +0x3a
 *   branch +0x34 -> +0x3a
 *   branch +0x42 -> +0x78
 *   branch +0x4e -> +0x54
 *   branch +0x5e -> +0x64
 *   branch +0x72 -> +0x78
 *   test +0x0c cmp r0, #0x0
 *   test +0x1a cmp r0, #0x0
 *   test +0x26 cmp r0, #0x0
 *   test +0x32 cmp r0, #0x0
 *   test +0x40 cmp r0, #0x0
 *   test +0x4c cmp r0, #0x0
 *   test +0x5c cmp r0, #0x0
 *   test +0x70 cmp r0, #0x0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb86c; the literal pool and
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

extern void native_fn_021fedc8(void);
extern void native_fn_020a4990(void);
extern void native_fn_020a4950(void);


asm u32 native_ov006_021fb86c (register u32 a0)
{
    push {r4, lr}
    bl native_fn_021fedc8
    add r4, r0, #0x0
    add r0, #0x40
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021fb86c_L14
    mov r0, #0x0
    pop {r4, pc}
ov006_021fb86c_L14:
    add r0, r4, #0x0
    add r0, #0xf6
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021fb86c_L3a
    add r0, r4, #0x0
    add r0, #0xc8
    bl native_fn_020a4990
    cmp r0, #0x0
    bne ov006_021fb86c_L3a
    add r0, r4, #0x0
    add r0, #0xcc
    bl native_fn_020a4990
    cmp r0, #0x0
    bne ov006_021fb86c_L3a
    mov r0, #0x0
    pop {r4, pc}
ov006_021fb86c_L3a:
    add r0, r4, #0x0
    add r0, #0xf5
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021fb86c_L78
    add r0, r4, #0x0
    add r0, #0xc0
    bl native_fn_020a4990
    cmp r0, #0x0
    bne ov006_021fb86c_L54
    mov r0, #0x0
    pop {r4, pc}
ov006_021fb86c_L54:
    add r0, r4, #0x0
    add r0, #0xc4
    bl native_fn_020a4990
    cmp r0, #0x0
    bne ov006_021fb86c_L64
    mov r0, #0x0
    pop {r4, pc}
ov006_021fb86c_L64:
    add r0, r4, #0x0
    add r4, #0xf0
    add r0, #0xc0
    add r1, r4, #0x0
    bl native_fn_020a4950
    cmp r0, #0x0
    bne ov006_021fb86c_L78
    mov r0, #0x0
    pop {r4, pc}
ov006_021fb86c_L78:
    mov r0, #0x1
    pop {r4, pc}
}
