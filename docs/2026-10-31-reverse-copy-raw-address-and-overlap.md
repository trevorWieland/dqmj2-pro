# Reverse copy, raw address and overlap - 2026-10-31

Thumb02094240/44 is a new ordinary-C candidate. Replay `python match_mechanics_save_20261031_lane_reverse_copy.py`. Normal and parent-directory Python `-I -S` runs reproduce canonical SHA92eb4765aa55f65ef1b7b0e7ce0418b750bfe36a7981cfa46deaa5093d70001b. The actual compiler path/hash/complete flags are static inputs. Full compiler/MWLD/native bytes match; current object/link provenance is separate from source/native identity. Registration/module/ROM acceptance belongs to the integrator.

The earlier u16 source pointer advanced by two elements where native advances two bytes. The preferred C uses one element. It also represents the running output address as u32 and groups the unsigned count-minus-one offset explicitly. Thus nonpositive-count modular returns and an even-count return one byte before destination do not require constructing before-object C pointers or overflowing signed count-minus-one. A first ungrouped raw-address hypothesis was40/44;the natural grouped offset recovered44/44. Byte stores use unsigned character views.

Each positive-count pair loads a halfword,writes its low byte backward,loads that same halfword again,and writes its high byte at the preceding output address. Repeated reads are retained because overlap can change the second value. An odd tail performs a complete halfword read but writes only its low byte. Nonoverlap gives byte reversal;overlap follows this measured sequence rather than a memmove guarantee.

RawR0 is the final running address. Nonpositive signed counts perform no data access and return destination+count-1 modulo2^32,including null/unbacked raw addresses. Even positive counts return destination-1;odd counts return destination. No output-length or success meaning is assigned.

The714 pairs yield1,428 actual returns with zero providers. Lengths0..33/64/65/127/128/129,six overlapping/separate layouts,three data patterns and extreme nonpositive counts are covered. An independent ordered-read/write model compares all1,024 arena bytes and rawR0. Every run uses fresh state,actual Thumb return,SP/callee-saved checks and all22 own instructions. Odd lengths still require one extra backed source byte for the final halfword. Six original/source unaligned,null or unbacked stops are excluded without post-fault state or game/import claims.

Two full compiled wrong-C bodies restore the two-element step or omit the odd tail. Their1,428 pairs yield2,856 real returns,837 independent final-state rejections and591 positives. There are1,008 separate access-trace differences. Full evidence is deterministic gzip.

Original ROM/save,application and accepted sources remain untouched. No original typedef,lifetime,ordinary scene,semantic serialized field,bank-selection or chronology inference follows from this kernel.
