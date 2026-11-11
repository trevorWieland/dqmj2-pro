#ifndef P8_OV006_BLX_AUTH3_CONTEXT_H
#define P8_OV006_BLX_AUTH3_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;

/* Third batch of ov006 Thumb rows from the BLX backlog, after
   src/ov006/p7_ov006_blx_auth2. Every file is one function, compiled under the
   p004 profile (module ov006, mode thumb). Rows that call ARM code reach it
   through an R_ARM_THM_CALL that the original linker expanded to a BLX
   immediate; mwccarm always emits the BL placeholder, so the mode comes from
   the target: docs/authoring/2026-11-11-blx-mode-fix.md. */

#endif
