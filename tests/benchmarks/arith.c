#include "runtime.h"





int
main(void)
{
    int i;
    int n;
    int t;
    int pygen_0_tagF_temp;
    int pygen_1_tagF_temp;
    int pygen_0_compF_temp;
    int pygen_2_tagF_temp;
    int pygen_1_compF_temp;
    int pygen_0_projF_temp;
    int pygen_1_projF_temp;
    int pygen_2_compF_temp;
    int pygen_0_injF_temp;
    int pygen_1_ifexF_temp;
    int pygen_3_tagF_temp;
    int pygen_3_compF_temp;
    int pygen_2_projF_temp;
    int pygen_3_projF_temp;
    int pygen_4_compF_temp;
    int pygen_1_injF_temp;
    int pygen_0_ifexF_temp;
    int pygen_4_projF_temp;
    int pygen_5_projF_temp;
    int pygen_0_callF_temp;
    int pygen_2_injF_temp;
    int pygen_3_ifexF_temp;
    int pygen_4_tagF_temp;
    int pygen_5_compF_temp;
    int pygen_6_projF_temp;
    int pygen_7_projF_temp;
    int pygen_6_compF_temp;
    int pygen_3_injF_temp;
    int pygen_2_ifexF_temp;
    int pygen_8_projF_temp;
    int pygen_9_projF_temp;
    int pygen_7_compF_temp;
    int pygen_4_injF_temp;
    int pygen_2_let_temp;
    int pygen_5_tagF_temp;
    int pygen_8_compF_temp;
    int pygen_10_projF_temp;
    int pygen_9_compF_temp;
    int pygen_5_ifexF_temp;
    int pygen_6_tagF_temp;
    int pygen_10_compF_temp;
    int pygen_11_projF_temp;
    int pygen_11_compF_temp;
    int pygen_4_ifexF_temp;
    int pygen_1_callF_temp;
    int pygen_7_tagF_temp;
    int pygen_12_compF_temp;
    int pygen_12_projF_temp;
    int pygen_13_projF_temp;
    int pygen_0_addF_temp;
    int pygen_5_injF_temp;
    int pygen_7_ifexF_temp;
    int pygen_8_tagF_temp;
    int pygen_13_compF_temp;
    int pygen_14_projF_temp;
    int pygen_15_projF_temp;
    int pygen_1_addF_temp;
    int pygen_6_injF_temp;
    int pygen_6_ifexF_temp;
    int pygen_16_projF_temp;
    int pygen_17_projF_temp;
    int pygen_2_callF_temp;
    int pygen_7_injF_temp;
    int pygen_18_projF_temp;
    int pygen_0_usubF_temp;
    int pygen_8_injF_temp;
    int pygen_0_let_temp;
    int pygen_9_tagF_temp;
    int pygen_14_compF_temp;
    int pygen_19_projF_temp;
    int pygen_20_projF_temp;
    int pygen_2_addF_temp;
    int pygen_9_injF_temp;
    int pygen_9_ifexF_temp;
    int pygen_10_tagF_temp;
    int pygen_15_compF_temp;
    int pygen_21_projF_temp;
    int pygen_22_projF_temp;
    int pygen_3_addF_temp;
    int pygen_10_injF_temp;
    int pygen_8_ifexF_temp;
    int pygen_23_projF_temp;
    int pygen_24_projF_temp;
    int pygen_3_callF_temp;
    int pygen_11_injF_temp;
    int pygen_12_injF_temp;
    int pygen_1_let_temp;
    int pygen_11_tagF_temp;
    int pygen_16_compF_temp;
    int pygen_25_projF_temp;
    int pygen_26_projF_temp;
    int pygen_4_addF_temp;
    int pygen_13_injF_temp;
    int pygen_11_ifexF_temp;
    int pygen_12_tagF_temp;
    int pygen_17_compF_temp;
    int pygen_27_projF_temp;
    int pygen_28_projF_temp;
    int pygen_5_addF_temp;
    int pygen_14_injF_temp;
    int pygen_10_ifexF_temp;
    int pygen_29_projF_temp;
    int pygen_30_projF_temp;
    int pygen_4_callF_temp;
    int pygen_15_injF_temp;
    i = inject_int(0);
    n = input_int();
    t = inject_int(0);
    pygen_0_tagF_temp = tag(i);
    pygen_1_tagF_temp = tag(n);
    pygen_0_compF_temp = (pygen_0_tagF_temp == pygen_1_tagF_temp);
    if (pygen_0_compF_temp) {
        pygen_2_tagF_temp = tag(i);
        pygen_1_compF_temp = (pygen_2_tagF_temp == 0);
        if (pygen_1_compF_temp) {
            pygen_0_projF_temp = project_int(i);
            pygen_1_projF_temp = project_int(n);
            pygen_2_compF_temp = (pygen_0_projF_temp != pygen_1_projF_temp);
            pygen_0_injF_temp = inject_bool(pygen_2_compF_temp);
            pygen_1_ifexF_temp = pygen_0_injF_temp;
        } else {
            pygen_3_tagF_temp = tag(i);
            pygen_3_compF_temp = (pygen_3_tagF_temp == 1);
            if (pygen_3_compF_temp) {
                pygen_2_projF_temp = project_bool(i);
                pygen_3_projF_temp = project_bool(n);
                pygen_4_compF_temp = (pygen_2_projF_temp != pygen_3_projF_temp);
                pygen_1_injF_temp = inject_bool(pygen_4_compF_temp);
                pygen_0_ifexF_temp = pygen_1_injF_temp;
            } else {
                pygen_4_projF_temp = project_big(i);
                pygen_5_projF_temp = project_big(n);
                pygen_0_callF_temp = not_equal(pygen_4_projF_temp, pygen_5_projF_temp);
                pygen_2_injF_temp = inject_bool(pygen_0_callF_temp);
                pygen_0_ifexF_temp = pygen_2_injF_temp;
            }
            pygen_1_ifexF_temp = pygen_0_ifexF_temp;
        }
        pygen_3_ifexF_temp = pygen_1_ifexF_temp;
    } else {
        pygen_4_tagF_temp = tag(i);
        pygen_5_compF_temp = (pygen_4_tagF_temp == 0);
        if (pygen_5_compF_temp) {
            pygen_6_projF_temp = project_int(i);
            pygen_7_projF_temp = project_bool(n);
            pygen_6_compF_temp = (pygen_6_projF_temp != pygen_7_projF_temp);
            pygen_3_injF_temp = inject_bool(pygen_6_compF_temp);
            pygen_2_ifexF_temp = pygen_3_injF_temp;
        } else {
            pygen_8_projF_temp = project_bool(i);
            pygen_9_projF_temp = project_int(n);
            pygen_7_compF_temp = (pygen_8_projF_temp != pygen_9_projF_temp);
            pygen_4_injF_temp = inject_bool(pygen_7_compF_temp);
            pygen_2_ifexF_temp = pygen_4_injF_temp;
        }
        pygen_3_ifexF_temp = pygen_2_ifexF_temp;
    }
    pygen_2_let_temp = pygen_3_ifexF_temp;
    pygen_5_tagF_temp = tag(pygen_2_let_temp);
    pygen_8_compF_temp = (pygen_5_tagF_temp == 0);
    if (pygen_8_compF_temp) {
        pygen_10_projF_temp = project_int(pygen_2_let_temp);
        pygen_9_compF_temp = (0 != pygen_10_projF_temp);
        pygen_5_ifexF_temp = pygen_9_compF_temp;
    } else {
        pygen_6_tagF_temp = tag(pygen_2_let_temp);
        pygen_10_compF_temp = (pygen_6_tagF_temp == 1);
        if (pygen_10_compF_temp) {
            pygen_11_projF_temp = project_bool(pygen_2_let_temp);
            pygen_11_compF_temp = (0 != pygen_11_projF_temp);
            pygen_4_ifexF_temp = pygen_11_compF_temp;
        } else {
            pygen_1_callF_temp = is_true(pygen_2_let_temp);
            pygen_4_ifexF_temp = pygen_1_callF_temp;
        }
        pygen_5_ifexF_temp = pygen_4_ifexF_temp;
    }
    while (pygen_5_ifexF_temp) {
        pygen_7_tagF_temp = tag(t);
        pygen_12_compF_temp = (pygen_7_tagF_temp == 0);
        if (pygen_12_compF_temp) {
            pygen_12_projF_temp = project_int(t);
            pygen_13_projF_temp = project_int(i);
            pygen_0_addF_temp = (pygen_12_projF_temp + pygen_13_projF_temp);
            pygen_5_injF_temp = inject_int(pygen_0_addF_temp);
            pygen_7_ifexF_temp = pygen_5_injF_temp;
        } else {
            pygen_8_tagF_temp = tag(t);
            pygen_13_compF_temp = (pygen_8_tagF_temp == 1);
            if (pygen_13_compF_temp) {
                pygen_14_projF_temp = project_bool(t);
                pygen_15_projF_temp = project_bool(i);
                pygen_1_addF_temp = (pygen_14_projF_temp + pygen_15_projF_temp);
                pygen_6_injF_temp = inject_int(pygen_1_addF_temp);
                pygen_6_ifexF_temp = pygen_6_injF_temp;
            } else {
                pygen_16_projF_temp = project_big(t);
                pygen_17_projF_temp = project_big(i);
                pygen_2_callF_temp = add(pygen_16_projF_temp, pygen_17_projF_temp);
                pygen_7_injF_temp = inject_big(pygen_2_callF_temp);
                pygen_6_ifexF_temp = pygen_7_injF_temp;
            }
            pygen_7_ifexF_temp = pygen_6_ifexF_temp;
        }
        t = pygen_7_ifexF_temp;
        pygen_18_projF_temp = project_int(i);
        pygen_0_usubF_temp = -(pygen_18_projF_temp);
        pygen_8_injF_temp = inject_int(pygen_0_usubF_temp);
        pygen_0_let_temp = pygen_8_injF_temp;
        pygen_9_tagF_temp = tag(pygen_0_let_temp);
        pygen_14_compF_temp = (pygen_9_tagF_temp == 0);
        if (pygen_14_compF_temp) {
            pygen_19_projF_temp = project_int(pygen_0_let_temp);
            pygen_20_projF_temp = project_int(t);
            pygen_2_addF_temp = (pygen_19_projF_temp + pygen_20_projF_temp);
            pygen_9_injF_temp = inject_int(pygen_2_addF_temp);
            pygen_9_ifexF_temp = pygen_9_injF_temp;
        } else {
            pygen_10_tagF_temp = tag(pygen_0_let_temp);
            pygen_15_compF_temp = (pygen_10_tagF_temp == 1);
            if (pygen_15_compF_temp) {
                pygen_21_projF_temp = project_bool(pygen_0_let_temp);
                pygen_22_projF_temp = project_bool(t);
                pygen_3_addF_temp = (pygen_21_projF_temp + pygen_22_projF_temp);
                pygen_10_injF_temp = inject_int(pygen_3_addF_temp);
                pygen_8_ifexF_temp = pygen_10_injF_temp;
            } else {
                pygen_23_projF_temp = project_big(pygen_0_let_temp);
                pygen_24_projF_temp = project_big(t);
                pygen_3_callF_temp = add(pygen_23_projF_temp, pygen_24_projF_temp);
                pygen_11_injF_temp = inject_big(pygen_3_callF_temp);
                pygen_8_ifexF_temp = pygen_11_injF_temp;
            }
            pygen_9_ifexF_temp = pygen_8_ifexF_temp;
        }
        t = pygen_9_ifexF_temp;
        pygen_12_injF_temp = inject_int(1);
        pygen_1_let_temp = pygen_12_injF_temp;
        pygen_11_tagF_temp = tag(i);
        pygen_16_compF_temp = (pygen_11_tagF_temp == 0);
        if (pygen_16_compF_temp) {
            pygen_25_projF_temp = project_int(i);
            pygen_26_projF_temp = project_int(pygen_1_let_temp);
            pygen_4_addF_temp = (pygen_25_projF_temp + pygen_26_projF_temp);
            pygen_13_injF_temp = inject_int(pygen_4_addF_temp);
            pygen_11_ifexF_temp = pygen_13_injF_temp;
        } else {
            pygen_12_tagF_temp = tag(i);
            pygen_17_compF_temp = (pygen_12_tagF_temp == 1);
            if (pygen_17_compF_temp) {
                pygen_27_projF_temp = project_bool(i);
                pygen_28_projF_temp = project_bool(pygen_1_let_temp);
                pygen_5_addF_temp = (pygen_27_projF_temp + pygen_28_projF_temp);
                pygen_14_injF_temp = inject_int(pygen_5_addF_temp);
                pygen_10_ifexF_temp = pygen_14_injF_temp;
            } else {
                pygen_29_projF_temp = project_big(i);
                pygen_30_projF_temp = project_big(pygen_1_let_temp);
                pygen_4_callF_temp = add(pygen_29_projF_temp, pygen_30_projF_temp);
                pygen_15_injF_temp = inject_big(pygen_4_callF_temp);
                pygen_10_ifexF_temp = pygen_15_injF_temp;
            }
            pygen_11_ifexF_temp = pygen_10_ifexF_temp;
        }
        i = pygen_11_ifexF_temp;
        pygen_0_tagF_temp = tag(i);
        pygen_1_tagF_temp = tag(n);
        pygen_0_compF_temp = (pygen_0_tagF_temp == pygen_1_tagF_temp);
        if (pygen_0_compF_temp) {
            pygen_2_tagF_temp = tag(i);
            pygen_1_compF_temp = (pygen_2_tagF_temp == 0);
            if (pygen_1_compF_temp) {
                pygen_0_projF_temp = project_int(i);
                pygen_1_projF_temp = project_int(n);
                pygen_2_compF_temp = (pygen_0_projF_temp != pygen_1_projF_temp);
                pygen_0_injF_temp = inject_bool(pygen_2_compF_temp);
                pygen_1_ifexF_temp = pygen_0_injF_temp;
            } else {
                pygen_3_tagF_temp = tag(i);
                pygen_3_compF_temp = (pygen_3_tagF_temp == 1);
                if (pygen_3_compF_temp) {
                    pygen_2_projF_temp = project_bool(i);
                    pygen_3_projF_temp = project_bool(n);
                    pygen_4_compF_temp = (pygen_2_projF_temp != pygen_3_projF_temp);
                    pygen_1_injF_temp = inject_bool(pygen_4_compF_temp);
                    pygen_0_ifexF_temp = pygen_1_injF_temp;
                } else {
                    pygen_4_projF_temp = project_big(i);
                    pygen_5_projF_temp = project_big(n);
                    pygen_0_callF_temp = not_equal(pygen_4_projF_temp, pygen_5_projF_temp);
                    pygen_2_injF_temp = inject_bool(pygen_0_callF_temp);
                    pygen_0_ifexF_temp = pygen_2_injF_temp;
                }
                pygen_1_ifexF_temp = pygen_0_ifexF_temp;
            }
            pygen_3_ifexF_temp = pygen_1_ifexF_temp;
        } else {
            pygen_4_tagF_temp = tag(i);
            pygen_5_compF_temp = (pygen_4_tagF_temp == 0);
            if (pygen_5_compF_temp) {
                pygen_6_projF_temp = project_int(i);
                pygen_7_projF_temp = project_bool(n);
                pygen_6_compF_temp = (pygen_6_projF_temp != pygen_7_projF_temp);
                pygen_3_injF_temp = inject_bool(pygen_6_compF_temp);
                pygen_2_ifexF_temp = pygen_3_injF_temp;
            } else {
                pygen_8_projF_temp = project_bool(i);
                pygen_9_projF_temp = project_int(n);
                pygen_7_compF_temp = (pygen_8_projF_temp != pygen_9_projF_temp);
                pygen_4_injF_temp = inject_bool(pygen_7_compF_temp);
                pygen_2_ifexF_temp = pygen_4_injF_temp;
            }
            pygen_3_ifexF_temp = pygen_2_ifexF_temp;
        }
        pygen_2_let_temp = pygen_3_ifexF_temp;
        pygen_5_tagF_temp = tag(pygen_2_let_temp);
        pygen_8_compF_temp = (pygen_5_tagF_temp == 0);
        if (pygen_8_compF_temp) {
            pygen_10_projF_temp = project_int(pygen_2_let_temp);
            pygen_9_compF_temp = (0 != pygen_10_projF_temp);
            pygen_5_ifexF_temp = pygen_9_compF_temp;
        } else {
            pygen_6_tagF_temp = tag(pygen_2_let_temp);
            pygen_10_compF_temp = (pygen_6_tagF_temp == 1);
            if (pygen_10_compF_temp) {
                pygen_11_projF_temp = project_bool(pygen_2_let_temp);
                pygen_11_compF_temp = (0 != pygen_11_projF_temp);
                pygen_4_ifexF_temp = pygen_11_compF_temp;
            } else {
                pygen_1_callF_temp = is_true(pygen_2_let_temp);
                pygen_4_ifexF_temp = pygen_1_callF_temp;
            }
            pygen_5_ifexF_temp = pygen_4_ifexF_temp;
        }
    }
    print_any(t);
}
