/*
 * QuarkRefer_data.c
 *
 * Code generation for model "QuarkRefer".
 *
 * Model version              : 1.35
 * Simulink Coder version : 8.14 (R2018a) 06-Feb-2018
 * C source code generated on : Sun Nov  9 21:16:39 2025
 *
 * Target selection: quarc_win64.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "QuarkRefer.h"
#include "QuarkRefer_private.h"

/* Block parameters (default storage) */
P_QuarkRefer_T QuarkRefer_P = {
  /* Variable: seed1
   * Referenced by: '<Root>/Uniform Random Number'
   */
  917193.6638298101,

  /* Variable: seed2
   * Referenced by: '<Root>/Uniform Random Number1'
   */
  285839.01882037357,

  /* Variable: seed3
   * Referenced by: '<Root>/Uniform Random Number2'
   */
  757200.22911072127,

  /* Mask Parameter: Memory2_initial_condition
   * Referenced by: '<Root>/Memory2'
   */
  { 0.0, 0.0, 0.0 },

  /* Mask Parameter: Memory1_initial_condition
   * Referenced by: '<Root>/Memory1'
   */
  0.0,

  /* Mask Parameter: Memory_initial_condition
   * Referenced by: '<Root>/Memory'
   */
  { 0.0, 0.0, 0.0 },

  /* Expression: [0.3 0.29 0.2]
   * Referenced by: '<Root>/Saturation'
   */
  { 0.3, 0.29, 0.2 },

  /* Expression: [-0.3 -0.29 -0.2]
   * Referenced by: '<Root>/Saturation'
   */
  { -0.3, -0.29, -0.2 },

  /* Computed Parameter: TransferFcn_A
   * Referenced by: '<Root>/Transfer Fcn'
   */
  -10.0,

  /* Computed Parameter: TransferFcn_C
   * Referenced by: '<Root>/Transfer Fcn'
   */
  10.0,

  /* Expression: 1.6
   * Referenced by: '<Root>/Gain'
   */
  1.6,

  /* Computed Parameter: TransferFcn1_A
   * Referenced by: '<Root>/Transfer Fcn1'
   */
  -10.0,

  /* Computed Parameter: TransferFcn1_C
   * Referenced by: '<Root>/Transfer Fcn1'
   */
  10.0,

  /* Expression: 1.6
   * Referenced by: '<Root>/Gain1'
   */
  1.6,

  /* Computed Parameter: TransferFcn2_A
   * Referenced by: '<Root>/Transfer Fcn2'
   */
  -10.0,

  /* Computed Parameter: TransferFcn2_C
   * Referenced by: '<Root>/Transfer Fcn2'
   */
  10.0,

  /* Expression: 1.5
   * Referenced by: '<Root>/Gain2'
   */
  1.5,

  /* Expression: 20
   * Referenced by: '<Root>/Gain3'
   */
  20.0,

  /* Expression: 1
   * Referenced by: '<Root>/Gain4'
   */
  1.0,

  /* Expression: 1
   * Referenced by: '<Root>/Gain5'
   */
  1.0,

  /* Expression: 1
   * Referenced by: '<Root>/Gain6'
   */
  1.0,

  /* Expression: 0.5
   * Referenced by: '<Root>/Gain7'
   */
  0.5,

  /* Expression: 1
   * Referenced by: '<Root>/Gain8'
   */
  1.0,

  /* Expression: 1
   * Referenced by: '<Root>/Gain9'
   */
  1.0,

  /* Expression: -0.3
   * Referenced by: '<Root>/Uniform Random Number'
   */
  -0.3,

  /* Expression: 0.3
   * Referenced by: '<Root>/Uniform Random Number'
   */
  0.3,

  /* Expression: -0.3
   * Referenced by: '<Root>/Uniform Random Number1'
   */
  -0.3,

  /* Expression: 0.3
   * Referenced by: '<Root>/Uniform Random Number1'
   */
  0.3,

  /* Expression: -0.2
   * Referenced by: '<Root>/Uniform Random Number2'
   */
  -0.2,

  /* Expression: 0.2
   * Referenced by: '<Root>/Uniform Random Number2'
   */
  0.2
};
