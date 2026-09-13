/*
 * QuarkRefer.c
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
#include "QuarkRefer_dt.h"

/* Block signals (default storage) */
B_QuarkRefer_T QuarkRefer_B;

/* Continuous states */
X_QuarkRefer_T QuarkRefer_X;

/* Block states (default storage) */
DW_QuarkRefer_T QuarkRefer_DW;

/* Real-time model */
RT_MODEL_QuarkRefer_T QuarkRefer_M_;
RT_MODEL_QuarkRefer_T *const QuarkRefer_M = &QuarkRefer_M_;
static void rate_scheduler(void);

/*
 *   This function updates active task flag for each subrate.
 * The function is called at model base rate, hence the
 * generated code self-manages all its subrates.
 */
static void rate_scheduler(void)
{
  /* Compute which subrates run during the next base time step.  Subrates
   * are an integer multiple of the base rate counter.  Therefore, the subtask
   * counter is reset when it reaches its limit (zero means run).
   */
  (QuarkRefer_M->Timing.TaskCounters.TID[2])++;
  if ((QuarkRefer_M->Timing.TaskCounters.TID[2]) > 4) {/* Sample time: [0.02s, 0.0s] */
    QuarkRefer_M->Timing.TaskCounters.TID[2] = 0;
  }
}

/*
 * This function updates continuous states using the ODE3 fixed-step
 * solver algorithm
 */
static void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si )
{
  /* Solver Matrices */
  static const real_T rt_ODE3_A[3] = {
    1.0/2.0, 3.0/4.0, 1.0
  };

  static const real_T rt_ODE3_B[3][3] = {
    { 1.0/2.0, 0.0, 0.0 },

    { 0.0, 3.0/4.0, 0.0 },

    { 2.0/9.0, 1.0/3.0, 4.0/9.0 }
  };

  time_T t = rtsiGetT(si);
  time_T tnew = rtsiGetSolverStopTime(si);
  time_T h = rtsiGetStepSize(si);
  real_T *x = rtsiGetContStates(si);
  ODE3_IntgData *id = (ODE3_IntgData *)rtsiGetSolverData(si);
  real_T *y = id->y;
  real_T *f0 = id->f[0];
  real_T *f1 = id->f[1];
  real_T *f2 = id->f[2];
  real_T hB[3];
  int_T i;
  int_T nXc = 3;
  rtsiSetSimTimeStep(si,MINOR_TIME_STEP);

  /* Save the state values at time t in y, we'll use x as ynew. */
  (void) memcpy(y, x,
                (uint_T)nXc*sizeof(real_T));

  /* Assumes that rtsiSetT and ModelOutputs are up-to-date */
  /* f0 = f(t,y) */
  rtsiSetdX(si, f0);
  QuarkRefer_derivatives();

  /* f(:,2) = feval(odefile, t + hA(1), y + f*hB(:,1), args(:)(*)); */
  hB[0] = h * rt_ODE3_B[0][0];
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[0]);
  rtsiSetdX(si, f1);
  QuarkRefer_step();
  QuarkRefer_derivatives();

  /* f(:,3) = feval(odefile, t + hA(2), y + f*hB(:,2), args(:)(*)); */
  for (i = 0; i <= 1; i++) {
    hB[i] = h * rt_ODE3_B[1][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[1]);
  rtsiSetdX(si, f2);
  QuarkRefer_step();
  QuarkRefer_derivatives();

  /* tnew = t + hA(3);
     ynew = y + f*hB(:,3); */
  for (i = 0; i <= 2; i++) {
    hB[i] = h * rt_ODE3_B[2][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2]);
  }

  rtsiSetT(si, tnew);
  rtsiSetSimTimeStep(si,MAJOR_TIME_STEP);
}

real_T rt_urand_Upu32_Yd_f_pw_snf(uint32_T *u)
{
  uint32_T lo;
  uint32_T hi;

  /* Uniform random number generator (random number between 0 and 1)

     #define IA      16807                      magic multiplier = 7^5
     #define IM      2147483647                 modulus = 2^31-1
     #define IQ      127773                     IM div IA
     #define IR      2836                       IM modulo IA
     #define S       4.656612875245797e-10      reciprocal of 2^31-1
     test = IA * (seed % IQ) - IR * (seed/IQ)
     seed = test < 0 ? (test + IM) : test
     return (seed*S)
   */
  lo = *u % 127773U * 16807U;
  hi = *u / 127773U * 2836U;
  if (lo < hi) {
    *u = 2147483647U - (hi - lo);
  } else {
    *u = lo - hi;
  }

  return (real_T)*u * 4.6566128752457969E-10;
}

real_T rt_powd_snf(real_T u0, real_T u1)
{
  real_T y;
  real_T tmp;
  real_T tmp_0;
  if (rtIsNaN(u0) || rtIsNaN(u1)) {
    y = (rtNaN);
  } else {
    tmp = fabs(u0);
    tmp_0 = fabs(u1);
    if (rtIsInf(u1)) {
      if (tmp == 1.0) {
        y = 1.0;
      } else if (tmp > 1.0) {
        if (u1 > 0.0) {
          y = (rtInf);
        } else {
          y = 0.0;
        }
      } else if (u1 > 0.0) {
        y = 0.0;
      } else {
        y = (rtInf);
      }
    } else if (tmp_0 == 0.0) {
      y = 1.0;
    } else if (tmp_0 == 1.0) {
      if (u1 > 0.0) {
        y = u0;
      } else {
        y = 1.0 / u0;
      }
    } else if (u1 == 2.0) {
      y = u0 * u0;
    } else if ((u1 == 0.5) && (u0 >= 0.0)) {
      y = sqrt(u0);
    } else if ((u0 < 0.0) && (u1 > floor(u1))) {
      y = (rtNaN);
    } else {
      y = pow(u0, u1);
    }
  }

  return y;
}

/* Model step function */
void QuarkRefer_step(void)
{
  /* local block i/o variables */
  real_T rtb_Memory2[3];
  real_T rtb_Memory1[3];
  real_T rtb_Memory[3];
  real_T rtb_TmpSignalConversionAtMemory[3];
  real_T rtb_TmpSignalConversionAtMemo_g[3];
  real_T rtb_TmpSignalConversionAtMemo_m[3];
  if (rtmIsMajorTimeStep(QuarkRefer_M)) {
    /* set solver stop time */
    if (!(QuarkRefer_M->Timing.clockTick0+1)) {
      rtsiSetSolverStopTime(&QuarkRefer_M->solverInfo,
                            ((QuarkRefer_M->Timing.clockTickH0 + 1) *
        QuarkRefer_M->Timing.stepSize0 * 4294967296.0));
    } else {
      rtsiSetSolverStopTime(&QuarkRefer_M->solverInfo,
                            ((QuarkRefer_M->Timing.clockTick0 + 1) *
        QuarkRefer_M->Timing.stepSize0 + QuarkRefer_M->Timing.clockTickH0 *
        QuarkRefer_M->Timing.stepSize0 * 4294967296.0));
    }
  }                                    /* end MajorTimeStep */

  /* Update absolute time of base rate at minor time step */
  if (rtmIsMinorTimeStep(QuarkRefer_M)) {
    QuarkRefer_M->Timing.t[0] = rtsiGetT(&QuarkRefer_M->solverInfo);
  }

  {
    real_T (*lastU)[3];
    real_T lastTime;
    real_T rtb_Gain4;
    real_T rtb_tau_g_idx_1;
    real_T rtb_tau_g_idx_2;
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {
      /* S-Function (memory_block): '<Root>/Memory2' */
      {
        rtb_Memory2[0] = QuarkRefer_DW.Memory2_Value[0];
        rtb_Memory2[1] = QuarkRefer_DW.Memory2_Value[1];
        rtb_Memory2[2] = QuarkRefer_DW.Memory2_Value[2];
      }

      /* S-Function (memory_block): '<Root>/Memory1' */
      {
        rtb_Memory1[0] = QuarkRefer_DW.Memory1_Value[0];
        rtb_Memory1[1] = QuarkRefer_DW.Memory1_Value[1];
        rtb_Memory1[2] = QuarkRefer_DW.Memory1_Value[2];
      }

      /* S-Function (memory_block): '<Root>/Memory' */
      {
        rtb_Memory[0] = QuarkRefer_DW.Memory_Value[0];
        rtb_Memory[1] = QuarkRefer_DW.Memory_Value[1];
        rtb_Memory[2] = QuarkRefer_DW.Memory_Value[2];
      }

      /* Sum: '<Root>/Sum' */
      QuarkRefer_B.Sum[0] = (rtb_Memory2[0] + rtb_Memory1[0]) + rtb_Memory[0];

      /* Saturate: '<Root>/Saturation' */
      if (QuarkRefer_B.Sum[0] > QuarkRefer_P.Saturation_UpperSat[0]) {
        QuarkRefer_B.Saturation[0] = QuarkRefer_P.Saturation_UpperSat[0];
      } else if (QuarkRefer_B.Sum[0] < QuarkRefer_P.Saturation_LowerSat[0]) {
        QuarkRefer_B.Saturation[0] = QuarkRefer_P.Saturation_LowerSat[0];
      } else {
        QuarkRefer_B.Saturation[0] = QuarkRefer_B.Sum[0];
      }

      /* Sum: '<Root>/Sum' */
      QuarkRefer_B.Sum[1] = (rtb_Memory2[1] + rtb_Memory1[1]) + rtb_Memory[1];

      /* Saturate: '<Root>/Saturation' */
      if (QuarkRefer_B.Sum[1] > QuarkRefer_P.Saturation_UpperSat[1]) {
        QuarkRefer_B.Saturation[1] = QuarkRefer_P.Saturation_UpperSat[1];
      } else if (QuarkRefer_B.Sum[1] < QuarkRefer_P.Saturation_LowerSat[1]) {
        QuarkRefer_B.Saturation[1] = QuarkRefer_P.Saturation_LowerSat[1];
      } else {
        QuarkRefer_B.Saturation[1] = QuarkRefer_B.Sum[1];
      }

      /* Sum: '<Root>/Sum' */
      QuarkRefer_B.Sum[2] = (rtb_Memory2[2] + rtb_Memory1[2]) + rtb_Memory[2];

      /* Saturate: '<Root>/Saturation' */
      if (QuarkRefer_B.Sum[2] > QuarkRefer_P.Saturation_UpperSat[2]) {
        QuarkRefer_B.Saturation[2] = QuarkRefer_P.Saturation_UpperSat[2];
      } else if (QuarkRefer_B.Sum[2] < QuarkRefer_P.Saturation_LowerSat[2]) {
        QuarkRefer_B.Saturation[2] = QuarkRefer_P.Saturation_LowerSat[2];
      } else {
        QuarkRefer_B.Saturation[2] = QuarkRefer_B.Sum[2];
      }
    }

    /* Gain: '<Root>/Gain' incorporates:
     *  TransferFcn: '<Root>/Transfer Fcn'
     */
    QuarkRefer_B.Gain = QuarkRefer_P.TransferFcn_C *
      QuarkRefer_X.TransferFcn_CSTATE * QuarkRefer_P.Gain_Gain;
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {
      /* S-Function (phantom_block): '<S3>/Left Device' */

      /* S-Function Block: QuarkRefer/Subsystem/Left Device (phantom_block) */
      {
        t_error result = 0;
        result = phantom_read(QuarkRefer_DW.LeftDevice_Phantom,
                              &QuarkRefer_B.LeftDevice_o1,
                              &QuarkRefer_B.LeftDevice_o2[0],
                              &QuarkRefer_B.LeftDevice_o3[0], NULL,
                              &QuarkRefer_B.LeftDevice_o4);
        if (result < 0) {
          msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
            (_rt_error_message));
          rtmSetErrorStatus(QuarkRefer_M, _rt_error_message);
        }

        result = phantom_write(QuarkRefer_DW.LeftDevice_Phantom,
          &QuarkRefer_B.Saturation[0], NULL);
        if (result < 0) {
          msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
            (_rt_error_message));
          rtmSetErrorStatus(QuarkRefer_M, _rt_error_message);
        }
      }
    }

    /* Derivative: '<S3>/Derivative' */
    if ((QuarkRefer_DW.TimeStampA >= QuarkRefer_M->Timing.t[0]) &&
        (QuarkRefer_DW.TimeStampB >= QuarkRefer_M->Timing.t[0])) {
      QuarkRefer_B.Derivative[0] = 0.0;
      QuarkRefer_B.Derivative[1] = 0.0;
      QuarkRefer_B.Derivative[2] = 0.0;
    } else {
      lastTime = QuarkRefer_DW.TimeStampA;
      lastU = &QuarkRefer_DW.LastUAtTimeA;
      if (QuarkRefer_DW.TimeStampA < QuarkRefer_DW.TimeStampB) {
        if (QuarkRefer_DW.TimeStampB < QuarkRefer_M->Timing.t[0]) {
          lastTime = QuarkRefer_DW.TimeStampB;
          lastU = &QuarkRefer_DW.LastUAtTimeB;
        }
      } else {
        if (QuarkRefer_DW.TimeStampA >= QuarkRefer_M->Timing.t[0]) {
          lastTime = QuarkRefer_DW.TimeStampB;
          lastU = &QuarkRefer_DW.LastUAtTimeB;
        }
      }

      lastTime = QuarkRefer_M->Timing.t[0] - lastTime;
      QuarkRefer_B.Derivative[0] = (QuarkRefer_B.LeftDevice_o2[0] - (*lastU)[0])
        / lastTime;
      QuarkRefer_B.Derivative[1] = (QuarkRefer_B.LeftDevice_o2[1] - (*lastU)[1])
        / lastTime;
      QuarkRefer_B.Derivative[2] = (QuarkRefer_B.LeftDevice_o2[2] - (*lastU)[2])
        / lastTime;
    }

    /* End of Derivative: '<S3>/Derivative' */

    /* MATLAB Function: '<Root>/MATLAB Function' */
    /* MATLAB Function 'MATLAB Function': '<S1>:1' */
    /* '<S1>:1:3' */
    /* '<S1>:1:4' */
    /* '<S1>:1:8' */
    /* '<S1>:1:9' */
    /* '<S1>:1:20' */
    /* '<S1>:1:21' */
    /* '<S1>:1:22' */
    /* '<S1>:1:28' */
    /* '<S1>:1:29' */
    /* '<S1>:1:30' */
    /* '<S1>:1:40' */
    /* '<S1>:1:41' */
    /* '<S1>:1:42' */
    /* '<S1>:1:45' */
    /* '<S1>:1:46' */
    /* '<S1>:1:47' */
    /* '<S1>:1:50' */
    QuarkRefer_B.tau[0] = rt_powd_snf(fabs(QuarkRefer_B.LeftDevice_o2[0]) /
      1.0471975511965976, 4.0) * 0.5 * -QuarkRefer_B.LeftDevice_o2[0] + 0.01 *
      -QuarkRefer_B.Derivative[0];
    QuarkRefer_B.tau[1] = rt_powd_snf(fabs(QuarkRefer_B.LeftDevice_o2[1] - 1.135)
      / 0.865, 4.0) * 0.5 * -(QuarkRefer_B.LeftDevice_o2[1] - 1.135) + 0.01 *
      -QuarkRefer_B.Derivative[1];
    QuarkRefer_B.tau[2] = rt_powd_snf(fabs(QuarkRefer_B.LeftDevice_o2[2] - 0.905)
      / 1.045, 4.0) * 0.5 * -(QuarkRefer_B.LeftDevice_o2[2] - 0.905) + 0.01 *
      -QuarkRefer_B.Derivative[2];
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {
    }

    /* Gain: '<Root>/Gain1' incorporates:
     *  TransferFcn: '<Root>/Transfer Fcn1'
     */
    QuarkRefer_B.Gain1 = QuarkRefer_P.TransferFcn1_C *
      QuarkRefer_X.TransferFcn1_CSTATE * QuarkRefer_P.Gain1_Gain;
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {
    }

    /* Gain: '<Root>/Gain2' incorporates:
     *  TransferFcn: '<Root>/Transfer Fcn2'
     */
    QuarkRefer_B.Gain2 = QuarkRefer_P.TransferFcn2_C *
      QuarkRefer_X.TransferFcn2_CSTATE * QuarkRefer_P.Gain2_Gain;
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {
      /* SignalConversion: '<Root>/TmpSignal ConversionAtTo WorkspaceInport1' */
      QuarkRefer_B.TmpSignalConversionAtToWorkspac[0] =
        QuarkRefer_B.LeftDevice_o2[0];
      QuarkRefer_B.TmpSignalConversionAtToWorkspac[1] = QuarkRefer_B.Derivative
        [0];
      QuarkRefer_B.TmpSignalConversionAtToWorkspac[2] =
        QuarkRefer_B.LeftDevice_o2[1];
      QuarkRefer_B.TmpSignalConversionAtToWorkspac[3] = QuarkRefer_B.Derivative
        [1];
      QuarkRefer_B.TmpSignalConversionAtToWorkspac[4] =
        QuarkRefer_B.LeftDevice_o2[2];
      QuarkRefer_B.TmpSignalConversionAtToWorkspac[5] = QuarkRefer_B.Derivative
        [2];

      /* Gain: '<Root>/Gain3' */
      QuarkRefer_B.Gain3[0] = QuarkRefer_P.Gain3_Gain * QuarkRefer_B.Saturation
        [0];
      QuarkRefer_B.Gain3[1] = QuarkRefer_P.Gain3_Gain * QuarkRefer_B.Saturation
        [1];
      QuarkRefer_B.Gain3[2] = QuarkRefer_P.Gain3_Gain * QuarkRefer_B.Saturation
        [2];

      /* MATLAB Function: '<Root>/MATLAB Function1' */
      /* MATLAB Function 'MATLAB Function1': '<S2>:1' */
      /* '<S2>:1:10' */
      /* '<S2>:1:11' */
      /* '<S2>:1:16' */
      /* '<S2>:1:17' */
      /* '<S2>:1:24' */
      /* '<S2>:1:25' */
      /* '<S2>:1:26' */
      /* '<S2>:1:29' */
      rtb_tau_g_idx_2 = cos(QuarkRefer_B.LeftDevice_o2[1] +
                            QuarkRefer_B.LeftDevice_o2[2]) *
        0.050960000000000012;
      rtb_tau_g_idx_1 = rtb_tau_g_idx_2 + 0.089180000000000009 * cos
        (QuarkRefer_B.LeftDevice_o2[1]);

      /* Gain: '<Root>/Gain4' */
      rtb_Gain4 = QuarkRefer_P.Gain4_Gain * 0.0;
    }

    /* Gain: '<Root>/Gain5' */
    QuarkRefer_B.Gain5 = QuarkRefer_P.Gain5_Gain * QuarkRefer_B.tau[0];

    /* Gain: '<Root>/Gain6' */
    QuarkRefer_B.Gain6 = QuarkRefer_P.Gain6_Gain * QuarkRefer_B.tau[1];

    /* Gain: '<Root>/Gain7' */
    QuarkRefer_B.Gain7 = QuarkRefer_P.Gain7_Gain * QuarkRefer_B.tau[2];
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {
      /* SignalConversion: '<Root>/TmpSignal ConversionAtMemory1Inport1' */
      rtb_TmpSignalConversionAtMemory[0] = QuarkRefer_B.Gain5;
      rtb_TmpSignalConversionAtMemory[1] = QuarkRefer_B.Gain6;
      rtb_TmpSignalConversionAtMemory[2] = QuarkRefer_B.Gain7;

      /* SignalConversion: '<Root>/TmpSignal ConversionAtMemory2Inport1' */
      rtb_TmpSignalConversionAtMemo_g[0] = QuarkRefer_B.Gain;
      rtb_TmpSignalConversionAtMemo_g[1] = QuarkRefer_B.Gain1;
      rtb_TmpSignalConversionAtMemo_g[2] = QuarkRefer_B.Gain2;

      /* SignalConversion: '<Root>/TmpSignal ConversionAtMemoryInport1' incorporates:
       *  Gain: '<Root>/Gain8'
       *  Gain: '<Root>/Gain9'
       */
      rtb_TmpSignalConversionAtMemo_m[0] = rtb_Gain4;
      rtb_TmpSignalConversionAtMemo_m[1] = QuarkRefer_P.Gain8_Gain *
        rtb_tau_g_idx_1;
      rtb_TmpSignalConversionAtMemo_m[2] = QuarkRefer_P.Gain9_Gain *
        rtb_tau_g_idx_2;
    }

    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[2] == 0) {
      /* UniformRandomNumber: '<Root>/Uniform Random Number' */
      QuarkRefer_B.UniformRandomNumber =
        QuarkRefer_DW.UniformRandomNumber_NextOutput;

      /* UniformRandomNumber: '<Root>/Uniform Random Number1' */
      QuarkRefer_B.UniformRandomNumber1 =
        QuarkRefer_DW.UniformRandomNumber1_NextOutput;

      /* UniformRandomNumber: '<Root>/Uniform Random Number2' */
      QuarkRefer_B.UniformRandomNumber2 =
        QuarkRefer_DW.UniformRandomNumber2_NextOutput;
    }

    /* Clock: '<Root>/Clock' */
    QuarkRefer_B.Clock = QuarkRefer_M->Timing.t[0];
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {
    }
  }

  if (rtmIsMajorTimeStep(QuarkRefer_M)) {
    real_T (*lastU)[3];
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {
      /* Update for S-Function (memory_block): '<Root>/Memory2' */
      {
        QuarkRefer_DW.Memory2_Value[0] = rtb_TmpSignalConversionAtMemo_g[0];
        QuarkRefer_DW.Memory2_Value[1] = rtb_TmpSignalConversionAtMemo_g[1];
        QuarkRefer_DW.Memory2_Value[2] = rtb_TmpSignalConversionAtMemo_g[2];
      }

      /* Update for S-Function (memory_block): '<Root>/Memory1' */
      {
        QuarkRefer_DW.Memory1_Value[0] = rtb_TmpSignalConversionAtMemory[0];
        QuarkRefer_DW.Memory1_Value[1] = rtb_TmpSignalConversionAtMemory[1];
        QuarkRefer_DW.Memory1_Value[2] = rtb_TmpSignalConversionAtMemory[2];
      }

      /* Update for S-Function (memory_block): '<Root>/Memory' */
      {
        QuarkRefer_DW.Memory_Value[0] = rtb_TmpSignalConversionAtMemo_m[0];
        QuarkRefer_DW.Memory_Value[1] = rtb_TmpSignalConversionAtMemo_m[1];
        QuarkRefer_DW.Memory_Value[2] = rtb_TmpSignalConversionAtMemo_m[2];
      }
    }

    /* Update for Derivative: '<S3>/Derivative' */
    if (QuarkRefer_DW.TimeStampA == (rtInf)) {
      QuarkRefer_DW.TimeStampA = QuarkRefer_M->Timing.t[0];
      lastU = &QuarkRefer_DW.LastUAtTimeA;
    } else if (QuarkRefer_DW.TimeStampB == (rtInf)) {
      QuarkRefer_DW.TimeStampB = QuarkRefer_M->Timing.t[0];
      lastU = &QuarkRefer_DW.LastUAtTimeB;
    } else if (QuarkRefer_DW.TimeStampA < QuarkRefer_DW.TimeStampB) {
      QuarkRefer_DW.TimeStampA = QuarkRefer_M->Timing.t[0];
      lastU = &QuarkRefer_DW.LastUAtTimeA;
    } else {
      QuarkRefer_DW.TimeStampB = QuarkRefer_M->Timing.t[0];
      lastU = &QuarkRefer_DW.LastUAtTimeB;
    }

    (*lastU)[0] = QuarkRefer_B.LeftDevice_o2[0];
    (*lastU)[1] = QuarkRefer_B.LeftDevice_o2[1];
    (*lastU)[2] = QuarkRefer_B.LeftDevice_o2[2];

    /* End of Update for Derivative: '<S3>/Derivative' */
    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[2] == 0) {
      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number' */
      QuarkRefer_DW.UniformRandomNumber_NextOutput =
        (QuarkRefer_P.UniformRandomNumber_Maximum -
         QuarkRefer_P.UniformRandomNumber_Minimum) * rt_urand_Upu32_Yd_f_pw_snf(
        &QuarkRefer_DW.RandSeed) + QuarkRefer_P.UniformRandomNumber_Minimum;

      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number1' */
      QuarkRefer_DW.UniformRandomNumber1_NextOutput =
        (QuarkRefer_P.UniformRandomNumber1_Maximum -
         QuarkRefer_P.UniformRandomNumber1_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
        (&QuarkRefer_DW.RandSeed_o) + QuarkRefer_P.UniformRandomNumber1_Minimum;

      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number2' */
      QuarkRefer_DW.UniformRandomNumber2_NextOutput =
        (QuarkRefer_P.UniformRandomNumber2_Maximum -
         QuarkRefer_P.UniformRandomNumber2_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
        (&QuarkRefer_DW.RandSeed_g) + QuarkRefer_P.UniformRandomNumber2_Minimum;
    }

    /* External mode */
    rtExtModeUploadCheckTrigger(3);

    {                                  /* Sample time: [0.0s, 0.0s] */
      rtExtModeUpload(0, QuarkRefer_M->Timing.t[0]);
    }

    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[1] == 0) {/* Sample time: [0.004s, 0.0s] */
      rtExtModeUpload(1, (((QuarkRefer_M->Timing.clockTick1+
                            QuarkRefer_M->Timing.clockTickH1* 4294967296.0)) *
                          0.004));
    }

    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[2] == 0) {/* Sample time: [0.02s, 0.0s] */
      rtExtModeUpload(2, (((QuarkRefer_M->Timing.clockTick2+
                            QuarkRefer_M->Timing.clockTickH2* 4294967296.0)) *
                          0.02));
    }
  }                                    /* end MajorTimeStep */

  if (rtmIsMajorTimeStep(QuarkRefer_M)) {
    /* signal main to stop simulation */
    {                                  /* Sample time: [0.0s, 0.0s] */
      if ((rtmGetTFinal(QuarkRefer_M)!=-1) &&
          !((rtmGetTFinal(QuarkRefer_M)-(((QuarkRefer_M->Timing.clockTick1+
               QuarkRefer_M->Timing.clockTickH1* 4294967296.0)) * 0.004)) >
            (((QuarkRefer_M->Timing.clockTick1+QuarkRefer_M->Timing.clockTickH1*
               4294967296.0)) * 0.004) * (DBL_EPSILON))) {
        rtmSetErrorStatus(QuarkRefer_M, "Simulation finished");
      }

      if (rtmGetStopRequested(QuarkRefer_M)) {
        rtmSetErrorStatus(QuarkRefer_M, "Simulation finished");
      }
    }

    rt_ertODEUpdateContinuousStates(&QuarkRefer_M->solverInfo);

    /* Update absolute time for base rate */
    /* The "clockTick0" counts the number of times the code of this task has
     * been executed. The absolute time is the multiplication of "clockTick0"
     * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
     * overflow during the application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick0 and the high bits
     * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
     */
    if (!(++QuarkRefer_M->Timing.clockTick0)) {
      ++QuarkRefer_M->Timing.clockTickH0;
    }

    QuarkRefer_M->Timing.t[0] = rtsiGetSolverStopTime(&QuarkRefer_M->solverInfo);

    {
      /* Update absolute timer for sample time: [0.004s, 0.0s] */
      /* The "clockTick1" counts the number of times the code of this task has
       * been executed. The resolution of this integer timer is 0.004, which is the step size
       * of the task. Size of "clockTick1" ensures timer will not overflow during the
       * application lifespan selected.
       * Timer of this task consists of two 32 bit unsigned integers.
       * The two integers represent the low bits Timing.clockTick1 and the high bits
       * Timing.clockTickH1. When the low bit overflows to 0, the high bits increment.
       */
      QuarkRefer_M->Timing.clockTick1++;
      if (!QuarkRefer_M->Timing.clockTick1) {
        QuarkRefer_M->Timing.clockTickH1++;
      }
    }

    if (rtmIsMajorTimeStep(QuarkRefer_M) &&
        QuarkRefer_M->Timing.TaskCounters.TID[2] == 0) {
      /* Update absolute timer for sample time: [0.02s, 0.0s] */
      /* The "clockTick2" counts the number of times the code of this task has
       * been executed. The resolution of this integer timer is 0.02, which is the step size
       * of the task. Size of "clockTick2" ensures timer will not overflow during the
       * application lifespan selected.
       * Timer of this task consists of two 32 bit unsigned integers.
       * The two integers represent the low bits Timing.clockTick2 and the high bits
       * Timing.clockTickH2. When the low bit overflows to 0, the high bits increment.
       */
      QuarkRefer_M->Timing.clockTick2++;
      if (!QuarkRefer_M->Timing.clockTick2) {
        QuarkRefer_M->Timing.clockTickH2++;
      }
    }

    rate_scheduler();
  }                                    /* end MajorTimeStep */
}

/* Derivatives for root system: '<Root>' */
void QuarkRefer_derivatives(void)
{
  XDot_QuarkRefer_T *_rtXdot;
  _rtXdot = ((XDot_QuarkRefer_T *) QuarkRefer_M->derivs);

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn' */
  _rtXdot->TransferFcn_CSTATE = 0.0;
  _rtXdot->TransferFcn_CSTATE += QuarkRefer_P.TransferFcn_A *
    QuarkRefer_X.TransferFcn_CSTATE;
  _rtXdot->TransferFcn_CSTATE += QuarkRefer_B.UniformRandomNumber;

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn1' */
  _rtXdot->TransferFcn1_CSTATE = 0.0;
  _rtXdot->TransferFcn1_CSTATE += QuarkRefer_P.TransferFcn1_A *
    QuarkRefer_X.TransferFcn1_CSTATE;
  _rtXdot->TransferFcn1_CSTATE += QuarkRefer_B.UniformRandomNumber1;

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn2' */
  _rtXdot->TransferFcn2_CSTATE = 0.0;
  _rtXdot->TransferFcn2_CSTATE += QuarkRefer_P.TransferFcn2_A *
    QuarkRefer_X.TransferFcn2_CSTATE;
  _rtXdot->TransferFcn2_CSTATE += QuarkRefer_B.UniformRandomNumber2;
}

/* Model initialize function */
void QuarkRefer_initialize(void)
{
  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* initialize real-time model */
  (void) memset((void *)QuarkRefer_M, 0,
                sizeof(RT_MODEL_QuarkRefer_T));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&QuarkRefer_M->solverInfo,
                          &QuarkRefer_M->Timing.simTimeStep);
    rtsiSetTPtr(&QuarkRefer_M->solverInfo, &rtmGetTPtr(QuarkRefer_M));
    rtsiSetStepSizePtr(&QuarkRefer_M->solverInfo,
                       &QuarkRefer_M->Timing.stepSize0);
    rtsiSetdXPtr(&QuarkRefer_M->solverInfo, &QuarkRefer_M->derivs);
    rtsiSetContStatesPtr(&QuarkRefer_M->solverInfo, (real_T **)
                         &QuarkRefer_M->contStates);
    rtsiSetNumContStatesPtr(&QuarkRefer_M->solverInfo,
      &QuarkRefer_M->Sizes.numContStates);
    rtsiSetNumPeriodicContStatesPtr(&QuarkRefer_M->solverInfo,
      &QuarkRefer_M->Sizes.numPeriodicContStates);
    rtsiSetPeriodicContStateIndicesPtr(&QuarkRefer_M->solverInfo,
      &QuarkRefer_M->periodicContStateIndices);
    rtsiSetPeriodicContStateRangesPtr(&QuarkRefer_M->solverInfo,
      &QuarkRefer_M->periodicContStateRanges);
    rtsiSetErrorStatusPtr(&QuarkRefer_M->solverInfo, (&rtmGetErrorStatus
      (QuarkRefer_M)));
    rtsiSetRTModelPtr(&QuarkRefer_M->solverInfo, QuarkRefer_M);
  }

  rtsiSetSimTimeStep(&QuarkRefer_M->solverInfo, MAJOR_TIME_STEP);
  QuarkRefer_M->intgData.y = QuarkRefer_M->odeY;
  QuarkRefer_M->intgData.f[0] = QuarkRefer_M->odeF[0];
  QuarkRefer_M->intgData.f[1] = QuarkRefer_M->odeF[1];
  QuarkRefer_M->intgData.f[2] = QuarkRefer_M->odeF[2];
  QuarkRefer_M->contStates = ((X_QuarkRefer_T *) &QuarkRefer_X);
  rtsiSetSolverData(&QuarkRefer_M->solverInfo, (void *)&QuarkRefer_M->intgData);
  rtsiSetSolverName(&QuarkRefer_M->solverInfo,"ode3");
  rtmSetTPtr(QuarkRefer_M, &QuarkRefer_M->Timing.tArray[0]);
  rtmSetTFinal(QuarkRefer_M, 20.0);
  QuarkRefer_M->Timing.stepSize0 = 0.004;

  /* External mode info */
  QuarkRefer_M->Sizes.checksums[0] = (851540507U);
  QuarkRefer_M->Sizes.checksums[1] = (3598186881U);
  QuarkRefer_M->Sizes.checksums[2] = (642120379U);
  QuarkRefer_M->Sizes.checksums[3] = (2771994871U);

  {
    static const sysRanDType rtAlwaysEnabled = SUBSYS_RAN_BC_ENABLE;
    static RTWExtModeInfo rt_ExtModeInfo;
    static const sysRanDType *systemRan[3];
    QuarkRefer_M->extModeInfo = (&rt_ExtModeInfo);
    rteiSetSubSystemActiveVectorAddresses(&rt_ExtModeInfo, systemRan);
    systemRan[0] = &rtAlwaysEnabled;
    systemRan[1] = &rtAlwaysEnabled;
    systemRan[2] = &rtAlwaysEnabled;
    rteiSetModelMappingInfoPtr(QuarkRefer_M->extModeInfo,
      &QuarkRefer_M->SpecialInfo.mappingInfo);
    rteiSetChecksumsPtr(QuarkRefer_M->extModeInfo, QuarkRefer_M->Sizes.checksums);
    rteiSetTPtr(QuarkRefer_M->extModeInfo, rtmGetTPtr(QuarkRefer_M));
  }

  /* block I/O */
  (void) memset(((void *) &QuarkRefer_B), 0,
                sizeof(B_QuarkRefer_T));

  {
    int32_T i;
    for (i = 0; i < 6; i++) {
      QuarkRefer_B.TmpSignalConversionAtToWorkspac[i] = 0.0;
    }

    QuarkRefer_B.Sum[0] = 0.0;
    QuarkRefer_B.Sum[1] = 0.0;
    QuarkRefer_B.Sum[2] = 0.0;
    QuarkRefer_B.Saturation[0] = 0.0;
    QuarkRefer_B.Saturation[1] = 0.0;
    QuarkRefer_B.Saturation[2] = 0.0;
    QuarkRefer_B.Gain = 0.0;
    QuarkRefer_B.LeftDevice_o2[0] = 0.0;
    QuarkRefer_B.LeftDevice_o2[1] = 0.0;
    QuarkRefer_B.LeftDevice_o2[2] = 0.0;
    QuarkRefer_B.LeftDevice_o3[0] = 0.0;
    QuarkRefer_B.LeftDevice_o3[1] = 0.0;
    QuarkRefer_B.LeftDevice_o3[2] = 0.0;
    QuarkRefer_B.Derivative[0] = 0.0;
    QuarkRefer_B.Derivative[1] = 0.0;
    QuarkRefer_B.Derivative[2] = 0.0;
    QuarkRefer_B.Gain1 = 0.0;
    QuarkRefer_B.Gain2 = 0.0;
    QuarkRefer_B.Gain3[0] = 0.0;
    QuarkRefer_B.Gain3[1] = 0.0;
    QuarkRefer_B.Gain3[2] = 0.0;
    QuarkRefer_B.Gain5 = 0.0;
    QuarkRefer_B.Gain6 = 0.0;
    QuarkRefer_B.Gain7 = 0.0;
    QuarkRefer_B.UniformRandomNumber = 0.0;
    QuarkRefer_B.UniformRandomNumber1 = 0.0;
    QuarkRefer_B.UniformRandomNumber2 = 0.0;
    QuarkRefer_B.Clock = 0.0;
    QuarkRefer_B.tau[0] = 0.0;
    QuarkRefer_B.tau[1] = 0.0;
    QuarkRefer_B.tau[2] = 0.0;
  }

  /* states (continuous) */
  {
    (void) memset((void *)&QuarkRefer_X, 0,
                  sizeof(X_QuarkRefer_T));
  }

  /* states (dwork) */
  (void) memset((void *)&QuarkRefer_DW, 0,
                sizeof(DW_QuarkRefer_T));
  QuarkRefer_DW.Memory2_Value[0] = 0.0;
  QuarkRefer_DW.Memory2_Value[1] = 0.0;
  QuarkRefer_DW.Memory2_Value[2] = 0.0;
  QuarkRefer_DW.Memory1_Value[0] = 0.0;
  QuarkRefer_DW.Memory1_Value[1] = 0.0;
  QuarkRefer_DW.Memory1_Value[2] = 0.0;
  QuarkRefer_DW.Memory_Value[0] = 0.0;
  QuarkRefer_DW.Memory_Value[1] = 0.0;
  QuarkRefer_DW.Memory_Value[2] = 0.0;
  QuarkRefer_DW.TimeStampA = 0.0;
  QuarkRefer_DW.LastUAtTimeA[0] = 0.0;
  QuarkRefer_DW.LastUAtTimeA[1] = 0.0;
  QuarkRefer_DW.LastUAtTimeA[2] = 0.0;
  QuarkRefer_DW.TimeStampB = 0.0;
  QuarkRefer_DW.LastUAtTimeB[0] = 0.0;
  QuarkRefer_DW.LastUAtTimeB[1] = 0.0;
  QuarkRefer_DW.LastUAtTimeB[2] = 0.0;
  QuarkRefer_DW.UniformRandomNumber_NextOutput = 0.0;
  QuarkRefer_DW.UniformRandomNumber1_NextOutput = 0.0;
  QuarkRefer_DW.UniformRandomNumber2_NextOutput = 0.0;

  /* data type transition information */
  {
    static DataTypeTransInfo dtInfo;
    (void) memset((char_T *) &dtInfo, 0,
                  sizeof(dtInfo));
    QuarkRefer_M->SpecialInfo.mappingInfo = (&dtInfo);
    dtInfo.numDataTypes = 15;
    dtInfo.dataTypeSizes = &rtDataTypeSizes[0];
    dtInfo.dataTypeNames = &rtDataTypeNames[0];

    /* Block I/O transition table */
    dtInfo.BTransTable = &rtBTransTable;

    /* Parameters transition table */
    dtInfo.PTransTable = &rtPTransTable;
  }

  /* Start for S-Function (memory_block): '<Root>/Memory2' */
  {
    QuarkRefer_DW.Memory2_Value[0] = (real_T)
      QuarkRefer_P.Memory2_initial_condition[0];
    QuarkRefer_DW.Memory2_Value[1] = (real_T)
      QuarkRefer_P.Memory2_initial_condition[1];
    QuarkRefer_DW.Memory2_Value[2] = (real_T)
      QuarkRefer_P.Memory2_initial_condition[2];
    QuarkRefer_DW.Memory2_ValueDims = 3;
  }

  /* Start for S-Function (memory_block): '<Root>/Memory1' */
  {
    QuarkRefer_DW.Memory1_Value[0] = (real_T)
      QuarkRefer_P.Memory1_initial_condition;
    QuarkRefer_DW.Memory1_Value[1] = (real_T)
      QuarkRefer_P.Memory1_initial_condition;
    QuarkRefer_DW.Memory1_Value[2] = (real_T)
      QuarkRefer_P.Memory1_initial_condition;
    QuarkRefer_DW.Memory1_ValueDims = 1;
  }

  /* Start for S-Function (memory_block): '<Root>/Memory' */
  {
    QuarkRefer_DW.Memory_Value[0] = (real_T)
      QuarkRefer_P.Memory_initial_condition[0];
    QuarkRefer_DW.Memory_Value[1] = (real_T)
      QuarkRefer_P.Memory_initial_condition[1];
    QuarkRefer_DW.Memory_Value[2] = (real_T)
      QuarkRefer_P.Memory_initial_condition[2];
    QuarkRefer_DW.Memory_ValueDims = 3;
  }

  /* Start for S-Function (phantom_block): '<S3>/Left Device' */

  /* S-Function Block: QuarkRefer/Subsystem/Left Device (phantom_block) */
  {
    t_error result;

    /* Open and initialize the device. This also schedules the device callback function. */
    result = phantom_open_device(&QuarkRefer_DW.LeftDevice_Phantom,
      "Default Device", PHANTOM_JOINT_ANGLES_OUTPUT, PHANTOM_JOINT_SPACE_INPUT,
      0, -1, 3, 6);
    if (result < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(QuarkRefer_M, _rt_error_message);
    } else {
      /* Start the scheduler - *****TODO: change the rate to a parameter, just hardcoded at 1000Hz for now. */
      result = phantom_start_scheduler(QuarkRefer_DW.LeftDevice_Phantom, 1000);
      if (result < 0) {
        phantom_close_device(QuarkRefer_DW.LeftDevice_Phantom);
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(QuarkRefer_M, _rt_error_message);
      }
    }
  }

  {
    uint32_T tseed;
    int32_T r;
    int32_T t;
    real_T tmp;

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn' */
    QuarkRefer_X.TransferFcn_CSTATE = 0.0;

    /* InitializeConditions for Derivative: '<S3>/Derivative' */
    QuarkRefer_DW.TimeStampA = (rtInf);
    QuarkRefer_DW.TimeStampB = (rtInf);

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn1' */
    QuarkRefer_X.TransferFcn1_CSTATE = 0.0;

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn2' */
    QuarkRefer_X.TransferFcn2_CSTATE = 0.0;

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number' */
    tmp = floor(fabs(QuarkRefer_P.seed1));
    if (rtIsNaN(tmp) || rtIsInf(tmp)) {
      tseed = 0U;
    } else {
      tseed = (uint32_T)fmod(tmp, 4.294967296E+9);
    }

    r = (int32_T)(tseed >> 16U);
    t = (int32_T)(tseed & 32768U);
    tseed = ((((tseed - ((uint32_T)r << 16U)) + t) << 16U) + t) + r;
    if (tseed < 1U) {
      tseed = 1144108930U;
    } else {
      if (tseed > 2147483646U) {
        tseed = 2147483646U;
      }
    }

    QuarkRefer_DW.RandSeed = tseed;
    QuarkRefer_DW.UniformRandomNumber_NextOutput =
      (QuarkRefer_P.UniformRandomNumber_Maximum -
       QuarkRefer_P.UniformRandomNumber_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&QuarkRefer_DW.RandSeed) + QuarkRefer_P.UniformRandomNumber_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number' */

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number1' */
    tmp = floor(fabs(QuarkRefer_P.seed2));
    if (rtIsNaN(tmp) || rtIsInf(tmp)) {
      tseed = 0U;
    } else {
      tseed = (uint32_T)fmod(tmp, 4.294967296E+9);
    }

    r = (int32_T)(tseed >> 16U);
    t = (int32_T)(tseed & 32768U);
    tseed = ((((tseed - ((uint32_T)r << 16U)) + t) << 16U) + t) + r;
    if (tseed < 1U) {
      tseed = 1144108930U;
    } else {
      if (tseed > 2147483646U) {
        tseed = 2147483646U;
      }
    }

    QuarkRefer_DW.RandSeed_o = tseed;
    QuarkRefer_DW.UniformRandomNumber1_NextOutput =
      (QuarkRefer_P.UniformRandomNumber1_Maximum -
       QuarkRefer_P.UniformRandomNumber1_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&QuarkRefer_DW.RandSeed_o) + QuarkRefer_P.UniformRandomNumber1_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number1' */

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number2' */
    tmp = floor(fabs(QuarkRefer_P.seed3));
    if (rtIsNaN(tmp) || rtIsInf(tmp)) {
      tseed = 0U;
    } else {
      tseed = (uint32_T)fmod(tmp, 4.294967296E+9);
    }

    r = (int32_T)(tseed >> 16U);
    t = (int32_T)(tseed & 32768U);
    tseed = ((((tseed - ((uint32_T)r << 16U)) + t) << 16U) + t) + r;
    if (tseed < 1U) {
      tseed = 1144108930U;
    } else {
      if (tseed > 2147483646U) {
        tseed = 2147483646U;
      }
    }

    QuarkRefer_DW.RandSeed_g = tseed;
    QuarkRefer_DW.UniformRandomNumber2_NextOutput =
      (QuarkRefer_P.UniformRandomNumber2_Maximum -
       QuarkRefer_P.UniformRandomNumber2_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&QuarkRefer_DW.RandSeed_g) + QuarkRefer_P.UniformRandomNumber2_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number2' */
  }
}

/* Model terminate function */
void QuarkRefer_terminate(void)
{
  /* Terminate for S-Function (phantom_block): '<S3>/Left Device' */

  /* S-Function Block: QuarkRefer/Subsystem/Left Device (phantom_block) */
  {
    t_error result;
    if ((result = phantom_stop_scheduler(QuarkRefer_DW.LeftDevice_Phantom)) < 0)
    {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(QuarkRefer_M, _rt_error_message);
    }

    if ((result = phantom_close_device(QuarkRefer_DW.LeftDevice_Phantom)) < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(QuarkRefer_M, _rt_error_message);
    }
  }
}
