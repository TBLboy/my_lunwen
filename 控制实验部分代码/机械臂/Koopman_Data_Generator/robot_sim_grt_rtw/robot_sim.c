/*
 * robot_sim.c
 *
 * Code generation for model "robot_sim".
 *
 * Model version              : 1.12
 * Simulink Coder version : 8.14 (R2018a) 06-Feb-2018
 * C source code generated on : Thu Nov  6 22:06:01 2025
 *
 * Target selection: grt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "robot_sim.h"
#include "robot_sim_private.h"

/* Block signals (default storage) */
B_robot_sim_T robot_sim_B;

/* Continuous states */
X_robot_sim_T robot_sim_X;

/* Block states (default storage) */
DW_robot_sim_T robot_sim_DW;

/* Real-time model */
RT_MODEL_robot_sim_T robot_sim_M_;
RT_MODEL_robot_sim_T *const robot_sim_M = &robot_sim_M_;

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
  robot_sim_derivatives();

  /* f(:,2) = feval(odefile, t + hA(1), y + f*hB(:,1), args(:)(*)); */
  hB[0] = h * rt_ODE3_B[0][0];
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[0]);
  rtsiSetdX(si, f1);
  robot_sim_step();
  robot_sim_derivatives();

  /* f(:,3) = feval(odefile, t + hA(2), y + f*hB(:,2), args(:)(*)); */
  for (i = 0; i <= 1; i++) {
    hB[i] = h * rt_ODE3_B[1][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[1]);
  rtsiSetdX(si, f2);
  robot_sim_step();
  robot_sim_derivatives();

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
void robot_sim_step(void)
{
  /* local block i/o variables */
  real_T rtb_Memory2[3];
  real_T rtb_Memory1[3];
  real_T rtb_Memory[3];
  real_T rtb_TmpSignalConversionAtMemory[3];
  real_T rtb_TmpSignalConversionAtToWork[6];
  real_T rtb_Gain3[3];
  if (rtmIsMajorTimeStep(robot_sim_M)) {
    /* set solver stop time */
    if (!(robot_sim_M->Timing.clockTick0+1)) {
      rtsiSetSolverStopTime(&robot_sim_M->solverInfo,
                            ((robot_sim_M->Timing.clockTickH0 + 1) *
        robot_sim_M->Timing.stepSize0 * 4294967296.0));
    } else {
      rtsiSetSolverStopTime(&robot_sim_M->solverInfo,
                            ((robot_sim_M->Timing.clockTick0 + 1) *
        robot_sim_M->Timing.stepSize0 + robot_sim_M->Timing.clockTickH0 *
        robot_sim_M->Timing.stepSize0 * 4294967296.0));
    }
  }                                    /* end MajorTimeStep */

  /* Update absolute time of base rate at minor time step */
  if (rtmIsMinorTimeStep(robot_sim_M)) {
    robot_sim_M->Timing.t[0] = rtsiGetT(&robot_sim_M->solverInfo);
  }

  {
    real_T (*lastU)[3];
    real_T lastTime;
    if (rtmIsMajorTimeStep(robot_sim_M)) {
      /* S-Function (memory_block): '<Root>/Memory2' */
      {
        rtb_Memory2[0] = robot_sim_DW.Memory2_Value[0];
        rtb_Memory2[1] = robot_sim_DW.Memory2_Value[1];
        rtb_Memory2[2] = robot_sim_DW.Memory2_Value[2];
      }

      /* S-Function (memory_block): '<Root>/Memory1' */
      {
        rtb_Memory1[0] = robot_sim_DW.Memory1_Value[0];
        rtb_Memory1[1] = robot_sim_DW.Memory1_Value[1];
        rtb_Memory1[2] = robot_sim_DW.Memory1_Value[2];
      }

      /* S-Function (memory_block): '<Root>/Memory' */
      {
        rtb_Memory[0] = robot_sim_DW.Memory_Value[0];
        rtb_Memory[1] = robot_sim_DW.Memory_Value[1];
        rtb_Memory[2] = robot_sim_DW.Memory_Value[2];
      }

      /* Sum: '<Root>/Sum' */
      rtb_Gain3[0] = (rtb_Memory2[0] + rtb_Memory1[0]) + rtb_Memory[0];

      /* Saturate: '<Root>/Saturation' */
      if (rtb_Gain3[0] > robot_sim_P.Saturation_UpperSat[0]) {
        robot_sim_B.Saturation[0] = robot_sim_P.Saturation_UpperSat[0];
      } else if (rtb_Gain3[0] < robot_sim_P.Saturation_LowerSat[0]) {
        robot_sim_B.Saturation[0] = robot_sim_P.Saturation_LowerSat[0];
      } else {
        robot_sim_B.Saturation[0] = rtb_Gain3[0];
      }

      /* Sum: '<Root>/Sum' */
      rtb_Gain3[1] = (rtb_Memory2[1] + rtb_Memory1[1]) + rtb_Memory[1];

      /* Saturate: '<Root>/Saturation' */
      if (rtb_Gain3[1] > robot_sim_P.Saturation_UpperSat[1]) {
        robot_sim_B.Saturation[1] = robot_sim_P.Saturation_UpperSat[1];
      } else if (rtb_Gain3[1] < robot_sim_P.Saturation_LowerSat[1]) {
        robot_sim_B.Saturation[1] = robot_sim_P.Saturation_LowerSat[1];
      } else {
        robot_sim_B.Saturation[1] = rtb_Gain3[1];
      }

      /* Sum: '<Root>/Sum' */
      rtb_Gain3[2] = (rtb_Memory2[2] + rtb_Memory1[2]) + rtb_Memory[2];

      /* Saturate: '<Root>/Saturation' */
      if (rtb_Gain3[2] > robot_sim_P.Saturation_UpperSat[2]) {
        robot_sim_B.Saturation[2] = robot_sim_P.Saturation_UpperSat[2];
      } else if (rtb_Gain3[2] < robot_sim_P.Saturation_LowerSat[2]) {
        robot_sim_B.Saturation[2] = robot_sim_P.Saturation_LowerSat[2];
      } else {
        robot_sim_B.Saturation[2] = rtb_Gain3[2];
      }
    }

    /* Gain: '<Root>/Gain' incorporates:
     *  TransferFcn: '<Root>/Transfer Fcn'
     */
    robot_sim_B.Gain = robot_sim_P.TransferFcn_C *
      robot_sim_X.TransferFcn_CSTATE * robot_sim_P.Gain_Gain;
    if (rtmIsMajorTimeStep(robot_sim_M)) {
      /* S-Function (phantom_block): '<S3>/Left Device' */

      /* S-Function Block: robot_sim/Subsystem/Left Device (phantom_block) */
      {
        t_error result = 0;
        result = phantom_read(robot_sim_DW.LeftDevice_Phantom,
                              &robot_sim_B.LeftDevice_o1,
                              &robot_sim_B.LeftDevice_o2[0],
                              &robot_sim_B.LeftDevice_o3[0], NULL,
                              &robot_sim_B.LeftDevice_o4);
        if (result < 0) {
          msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
            (_rt_error_message));
          rtmSetErrorStatus(robot_sim_M, _rt_error_message);
        }

        result = phantom_write(robot_sim_DW.LeftDevice_Phantom,
          &robot_sim_B.Saturation[0], NULL);
        if (result < 0) {
          msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
            (_rt_error_message));
          rtmSetErrorStatus(robot_sim_M, _rt_error_message);
        }
      }
    }

    /* Derivative: '<S3>/Derivative' */
    if ((robot_sim_DW.TimeStampA >= robot_sim_M->Timing.t[0]) &&
        (robot_sim_DW.TimeStampB >= robot_sim_M->Timing.t[0])) {
      robot_sim_B.Derivative[0] = 0.0;
      robot_sim_B.Derivative[1] = 0.0;
      robot_sim_B.Derivative[2] = 0.0;
    } else {
      lastTime = robot_sim_DW.TimeStampA;
      lastU = &robot_sim_DW.LastUAtTimeA;
      if (robot_sim_DW.TimeStampA < robot_sim_DW.TimeStampB) {
        if (robot_sim_DW.TimeStampB < robot_sim_M->Timing.t[0]) {
          lastTime = robot_sim_DW.TimeStampB;
          lastU = &robot_sim_DW.LastUAtTimeB;
        }
      } else {
        if (robot_sim_DW.TimeStampA >= robot_sim_M->Timing.t[0]) {
          lastTime = robot_sim_DW.TimeStampB;
          lastU = &robot_sim_DW.LastUAtTimeB;
        }
      }

      lastTime = robot_sim_M->Timing.t[0] - lastTime;
      robot_sim_B.Derivative[0] = (robot_sim_B.LeftDevice_o2[0] - (*lastU)[0]) /
        lastTime;
      robot_sim_B.Derivative[1] = (robot_sim_B.LeftDevice_o2[1] - (*lastU)[1]) /
        lastTime;
      robot_sim_B.Derivative[2] = (robot_sim_B.LeftDevice_o2[2] - (*lastU)[2]) /
        lastTime;
    }

    /* End of Derivative: '<S3>/Derivative' */

    /* MATLAB Function: '<Root>/MATLAB Function' */
    robot_sim_B.tau[0] = rt_powd_snf(fabs(robot_sim_B.LeftDevice_o2[0]) /
      1.0471975511965976, 5.0) * 0.5 * -robot_sim_B.LeftDevice_o2[0] + 0.01 *
      -robot_sim_B.Derivative[0];
    robot_sim_B.tau[1] = rt_powd_snf(fabs(robot_sim_B.LeftDevice_o2[1] - 0.895) /
      0.895, 5.0) * 0.5 * -(robot_sim_B.LeftDevice_o2[1] - 0.895) + 0.01 *
      -robot_sim_B.Derivative[1];
    robot_sim_B.tau[2] = rt_powd_snf(fabs(robot_sim_B.LeftDevice_o2[2] - -1.35) /
      1.1, 5.0) * 0.5 * -(robot_sim_B.LeftDevice_o2[2] - -1.35) + 0.01 *
      -robot_sim_B.Derivative[2];
    if (rtmIsMajorTimeStep(robot_sim_M)) {
    }

    /* Gain: '<Root>/Gain1' incorporates:
     *  TransferFcn: '<Root>/Transfer Fcn1'
     */
    robot_sim_B.Gain1 = robot_sim_P.TransferFcn1_C *
      robot_sim_X.TransferFcn1_CSTATE * robot_sim_P.Gain1_Gain;
    if (rtmIsMajorTimeStep(robot_sim_M)) {
    }

    /* Gain: '<Root>/Gain2' incorporates:
     *  TransferFcn: '<Root>/Transfer Fcn2'
     */
    robot_sim_B.Gain2 = robot_sim_P.TransferFcn2_C *
      robot_sim_X.TransferFcn2_CSTATE * robot_sim_P.Gain2_Gain;
    if (rtmIsMajorTimeStep(robot_sim_M)) {
      /* SignalConversion: '<Root>/TmpSignal ConversionAtTo WorkspaceInport1' */
      rtb_TmpSignalConversionAtToWork[0] = robot_sim_B.LeftDevice_o2[0];
      rtb_TmpSignalConversionAtToWork[1] = robot_sim_B.Derivative[0];
      rtb_TmpSignalConversionAtToWork[2] = robot_sim_B.LeftDevice_o2[1];
      rtb_TmpSignalConversionAtToWork[3] = robot_sim_B.Derivative[1];
      rtb_TmpSignalConversionAtToWork[4] = robot_sim_B.LeftDevice_o2[2];
      rtb_TmpSignalConversionAtToWork[5] = robot_sim_B.Derivative[2];

      /* ToWorkspace: '<Root>/To Workspace' */
      if (rtmIsMajorTimeStep(robot_sim_M)) {
        rt_UpdateLogVar((LogVar *)(LogVar*)
                        (robot_sim_DW.ToWorkspace_PWORK.LoggedData),
                        &rtb_TmpSignalConversionAtToWork[0], 0);
      }

      /* Gain: '<Root>/Gain3' */
      rtb_Gain3[0] = robot_sim_P.Gain3_Gain * robot_sim_B.Saturation[0];
      rtb_Gain3[1] = robot_sim_P.Gain3_Gain * robot_sim_B.Saturation[1];
      rtb_Gain3[2] = robot_sim_P.Gain3_Gain * robot_sim_B.Saturation[2];

      /* ToWorkspace: '<Root>/To Workspace1' */
      if (rtmIsMajorTimeStep(robot_sim_M)) {
        rt_UpdateLogVar((LogVar *)(LogVar*)
                        (robot_sim_DW.ToWorkspace1_PWORK.LoggedData),
                        &rtb_Gain3[0], 0);
      }

      /* MATLAB Function: '<Root>/MATLAB Function1' */
      robot_sim_B.tau_g[0] = 0.0;
      lastTime = cos(robot_sim_B.LeftDevice_o2[1] + robot_sim_B.LeftDevice_o2[2])
        * 0.050960000000000012;
      robot_sim_B.tau_g[1] = lastTime + 0.089180000000000009 * cos
        (robot_sim_B.LeftDevice_o2[1]);
      robot_sim_B.tau_g[2] = lastTime;

      /* SignalConversion: '<Root>/TmpSignal ConversionAtMemory2Inport1' */
      rtb_TmpSignalConversionAtMemory[0] = robot_sim_B.Gain;
      rtb_TmpSignalConversionAtMemory[1] = robot_sim_B.Gain1;
      rtb_TmpSignalConversionAtMemory[2] = robot_sim_B.Gain2;

      /* UniformRandomNumber: '<Root>/Uniform Random Number' */
      robot_sim_B.UniformRandomNumber =
        robot_sim_DW.UniformRandomNumber_NextOutput;

      /* UniformRandomNumber: '<Root>/Uniform Random Number1' */
      robot_sim_B.UniformRandomNumber1 =
        robot_sim_DW.UniformRandomNumber1_NextOutput;

      /* UniformRandomNumber: '<Root>/Uniform Random Number2' */
      robot_sim_B.UniformRandomNumber2 =
        robot_sim_DW.UniformRandomNumber2_NextOutput;
    }

    /* Clock: '<Root>/Clock' */
    robot_sim_B.Clock = robot_sim_M->Timing.t[0];
    if (rtmIsMajorTimeStep(robot_sim_M)) {
      /* ToWorkspace: '<Root>/To Workspace2' */
      if (rtmIsMajorTimeStep(robot_sim_M)) {
        rt_UpdateLogVar((LogVar *)(LogVar*)
                        (robot_sim_DW.ToWorkspace2_PWORK.LoggedData),
                        &robot_sim_B.Clock, 0);
      }
    }
  }

  if (rtmIsMajorTimeStep(robot_sim_M)) {
    /* Matfile logging */
    rt_UpdateTXYLogVars(robot_sim_M->rtwLogInfo, (robot_sim_M->Timing.t));
  }                                    /* end MajorTimeStep */

  if (rtmIsMajorTimeStep(robot_sim_M)) {
    real_T (*lastU)[3];
    if (rtmIsMajorTimeStep(robot_sim_M)) {
      /* Update for S-Function (memory_block): '<Root>/Memory2' */
      {
        robot_sim_DW.Memory2_Value[0] = rtb_TmpSignalConversionAtMemory[0];
        robot_sim_DW.Memory2_Value[1] = rtb_TmpSignalConversionAtMemory[1];
        robot_sim_DW.Memory2_Value[2] = rtb_TmpSignalConversionAtMemory[2];
      }

      /* Update for S-Function (memory_block): '<Root>/Memory1' */
      {
        robot_sim_DW.Memory1_Value[0] = robot_sim_B.tau[0];
        robot_sim_DW.Memory1_Value[1] = robot_sim_B.tau[1];
        robot_sim_DW.Memory1_Value[2] = robot_sim_B.tau[2];
      }

      /* Update for S-Function (memory_block): '<Root>/Memory' */
      {
        robot_sim_DW.Memory_Value[0] = robot_sim_B.tau_g[0];
        robot_sim_DW.Memory_Value[1] = robot_sim_B.tau_g[1];
        robot_sim_DW.Memory_Value[2] = robot_sim_B.tau_g[2];
      }
    }

    /* Update for Derivative: '<S3>/Derivative' */
    if (robot_sim_DW.TimeStampA == (rtInf)) {
      robot_sim_DW.TimeStampA = robot_sim_M->Timing.t[0];
      lastU = &robot_sim_DW.LastUAtTimeA;
    } else if (robot_sim_DW.TimeStampB == (rtInf)) {
      robot_sim_DW.TimeStampB = robot_sim_M->Timing.t[0];
      lastU = &robot_sim_DW.LastUAtTimeB;
    } else if (robot_sim_DW.TimeStampA < robot_sim_DW.TimeStampB) {
      robot_sim_DW.TimeStampA = robot_sim_M->Timing.t[0];
      lastU = &robot_sim_DW.LastUAtTimeA;
    } else {
      robot_sim_DW.TimeStampB = robot_sim_M->Timing.t[0];
      lastU = &robot_sim_DW.LastUAtTimeB;
    }

    (*lastU)[0] = robot_sim_B.LeftDevice_o2[0];
    (*lastU)[1] = robot_sim_B.LeftDevice_o2[1];
    (*lastU)[2] = robot_sim_B.LeftDevice_o2[2];

    /* End of Update for Derivative: '<S3>/Derivative' */
    if (rtmIsMajorTimeStep(robot_sim_M)) {
      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number' */
      robot_sim_DW.UniformRandomNumber_NextOutput =
        (robot_sim_P.UniformRandomNumber_Maximum -
         robot_sim_P.UniformRandomNumber_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
        (&robot_sim_DW.RandSeed) + robot_sim_P.UniformRandomNumber_Minimum;

      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number1' */
      robot_sim_DW.UniformRandomNumber1_NextOutput =
        (robot_sim_P.UniformRandomNumber1_Maximum -
         robot_sim_P.UniformRandomNumber1_Minimum) * rt_urand_Upu32_Yd_f_pw_snf(
        &robot_sim_DW.RandSeed_d) + robot_sim_P.UniformRandomNumber1_Minimum;

      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number2' */
      robot_sim_DW.UniformRandomNumber2_NextOutput =
        (robot_sim_P.UniformRandomNumber2_Maximum -
         robot_sim_P.UniformRandomNumber2_Minimum) * rt_urand_Upu32_Yd_f_pw_snf(
        &robot_sim_DW.RandSeed_e) + robot_sim_P.UniformRandomNumber2_Minimum;
    }
  }                                    /* end MajorTimeStep */

  if (rtmIsMajorTimeStep(robot_sim_M)) {
    /* signal main to stop simulation */
    {                                  /* Sample time: [0.0s, 0.0s] */
      if ((rtmGetTFinal(robot_sim_M)!=-1) &&
          !((rtmGetTFinal(robot_sim_M)-(((robot_sim_M->Timing.clockTick1+
               robot_sim_M->Timing.clockTickH1* 4294967296.0)) * 0.004)) >
            (((robot_sim_M->Timing.clockTick1+robot_sim_M->Timing.clockTickH1*
               4294967296.0)) * 0.004) * (DBL_EPSILON))) {
        rtmSetErrorStatus(robot_sim_M, "Simulation finished");
      }
    }

    rt_ertODEUpdateContinuousStates(&robot_sim_M->solverInfo);

    /* Update absolute time for base rate */
    /* The "clockTick0" counts the number of times the code of this task has
     * been executed. The absolute time is the multiplication of "clockTick0"
     * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
     * overflow during the application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick0 and the high bits
     * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
     */
    if (!(++robot_sim_M->Timing.clockTick0)) {
      ++robot_sim_M->Timing.clockTickH0;
    }

    robot_sim_M->Timing.t[0] = rtsiGetSolverStopTime(&robot_sim_M->solverInfo);

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
      robot_sim_M->Timing.clockTick1++;
      if (!robot_sim_M->Timing.clockTick1) {
        robot_sim_M->Timing.clockTickH1++;
      }
    }
  }                                    /* end MajorTimeStep */
}

/* Derivatives for root system: '<Root>' */
void robot_sim_derivatives(void)
{
  XDot_robot_sim_T *_rtXdot;
  _rtXdot = ((XDot_robot_sim_T *) robot_sim_M->derivs);

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn' */
  _rtXdot->TransferFcn_CSTATE = 0.0;
  _rtXdot->TransferFcn_CSTATE += robot_sim_P.TransferFcn_A *
    robot_sim_X.TransferFcn_CSTATE;
  _rtXdot->TransferFcn_CSTATE += robot_sim_B.UniformRandomNumber;

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn1' */
  _rtXdot->TransferFcn1_CSTATE = 0.0;
  _rtXdot->TransferFcn1_CSTATE += robot_sim_P.TransferFcn1_A *
    robot_sim_X.TransferFcn1_CSTATE;
  _rtXdot->TransferFcn1_CSTATE += robot_sim_B.UniformRandomNumber1;

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn2' */
  _rtXdot->TransferFcn2_CSTATE = 0.0;
  _rtXdot->TransferFcn2_CSTATE += robot_sim_P.TransferFcn2_A *
    robot_sim_X.TransferFcn2_CSTATE;
  _rtXdot->TransferFcn2_CSTATE += robot_sim_B.UniformRandomNumber2;
}

/* Model initialize function */
void robot_sim_initialize(void)
{
  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* initialize real-time model */
  (void) memset((void *)robot_sim_M, 0,
                sizeof(RT_MODEL_robot_sim_T));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&robot_sim_M->solverInfo,
                          &robot_sim_M->Timing.simTimeStep);
    rtsiSetTPtr(&robot_sim_M->solverInfo, &rtmGetTPtr(robot_sim_M));
    rtsiSetStepSizePtr(&robot_sim_M->solverInfo, &robot_sim_M->Timing.stepSize0);
    rtsiSetdXPtr(&robot_sim_M->solverInfo, &robot_sim_M->derivs);
    rtsiSetContStatesPtr(&robot_sim_M->solverInfo, (real_T **)
                         &robot_sim_M->contStates);
    rtsiSetNumContStatesPtr(&robot_sim_M->solverInfo,
      &robot_sim_M->Sizes.numContStates);
    rtsiSetNumPeriodicContStatesPtr(&robot_sim_M->solverInfo,
      &robot_sim_M->Sizes.numPeriodicContStates);
    rtsiSetPeriodicContStateIndicesPtr(&robot_sim_M->solverInfo,
      &robot_sim_M->periodicContStateIndices);
    rtsiSetPeriodicContStateRangesPtr(&robot_sim_M->solverInfo,
      &robot_sim_M->periodicContStateRanges);
    rtsiSetErrorStatusPtr(&robot_sim_M->solverInfo, (&rtmGetErrorStatus
      (robot_sim_M)));
    rtsiSetRTModelPtr(&robot_sim_M->solverInfo, robot_sim_M);
  }

  rtsiSetSimTimeStep(&robot_sim_M->solverInfo, MAJOR_TIME_STEP);
  robot_sim_M->intgData.y = robot_sim_M->odeY;
  robot_sim_M->intgData.f[0] = robot_sim_M->odeF[0];
  robot_sim_M->intgData.f[1] = robot_sim_M->odeF[1];
  robot_sim_M->intgData.f[2] = robot_sim_M->odeF[2];
  robot_sim_M->contStates = ((X_robot_sim_T *) &robot_sim_X);
  rtsiSetSolverData(&robot_sim_M->solverInfo, (void *)&robot_sim_M->intgData);
  rtsiSetSolverName(&robot_sim_M->solverInfo,"ode3");
  rtmSetTPtr(robot_sim_M, &robot_sim_M->Timing.tArray[0]);
  rtmSetTFinal(robot_sim_M, 100.0);
  robot_sim_M->Timing.stepSize0 = 0.004;

  /* Setup for data logging */
  {
    static RTWLogInfo rt_DataLoggingInfo;
    rt_DataLoggingInfo.loggingInterval = NULL;
    robot_sim_M->rtwLogInfo = &rt_DataLoggingInfo;
  }

  /* Setup for data logging */
  {
    rtliSetLogXSignalInfo(robot_sim_M->rtwLogInfo, (NULL));
    rtliSetLogXSignalPtrs(robot_sim_M->rtwLogInfo, (NULL));
    rtliSetLogT(robot_sim_M->rtwLogInfo, "tout");
    rtliSetLogX(robot_sim_M->rtwLogInfo, "");
    rtliSetLogXFinal(robot_sim_M->rtwLogInfo, "");
    rtliSetLogVarNameModifier(robot_sim_M->rtwLogInfo, "rt_");
    rtliSetLogFormat(robot_sim_M->rtwLogInfo, 4);
    rtliSetLogMaxRows(robot_sim_M->rtwLogInfo, 0);
    rtliSetLogDecimation(robot_sim_M->rtwLogInfo, 1);
    rtliSetLogY(robot_sim_M->rtwLogInfo, "");
    rtliSetLogYSignalInfo(robot_sim_M->rtwLogInfo, (NULL));
    rtliSetLogYSignalPtrs(robot_sim_M->rtwLogInfo, (NULL));
  }

  /* block I/O */
  (void) memset(((void *) &robot_sim_B), 0,
                sizeof(B_robot_sim_T));

  /* states (continuous) */
  {
    (void) memset((void *)&robot_sim_X, 0,
                  sizeof(X_robot_sim_T));
  }

  /* states (dwork) */
  (void) memset((void *)&robot_sim_DW, 0,
                sizeof(DW_robot_sim_T));

  /* Matfile logging */
  rt_StartDataLoggingWithStartTime(robot_sim_M->rtwLogInfo, 0.0, rtmGetTFinal
    (robot_sim_M), robot_sim_M->Timing.stepSize0, (&rtmGetErrorStatus
    (robot_sim_M)));

  /* Start for S-Function (memory_block): '<Root>/Memory2' */
  {
    robot_sim_DW.Memory2_Value[0] = (real_T)
      robot_sim_P.Memory2_initial_condition;
    robot_sim_DW.Memory2_Value[1] = (real_T)
      robot_sim_P.Memory2_initial_condition;
    robot_sim_DW.Memory2_Value[2] = (real_T)
      robot_sim_P.Memory2_initial_condition;
    robot_sim_DW.Memory2_ValueDims = 1;
  }

  /* Start for S-Function (memory_block): '<Root>/Memory1' */
  {
    robot_sim_DW.Memory1_Value[0] = (real_T)
      robot_sim_P.Memory1_initial_condition;
    robot_sim_DW.Memory1_Value[1] = (real_T)
      robot_sim_P.Memory1_initial_condition;
    robot_sim_DW.Memory1_Value[2] = (real_T)
      robot_sim_P.Memory1_initial_condition;
    robot_sim_DW.Memory1_ValueDims = 1;
  }

  /* Start for S-Function (memory_block): '<Root>/Memory' */
  {
    robot_sim_DW.Memory_Value[0] = (real_T) robot_sim_P.Memory_initial_condition;
    robot_sim_DW.Memory_Value[1] = (real_T) robot_sim_P.Memory_initial_condition;
    robot_sim_DW.Memory_Value[2] = (real_T) robot_sim_P.Memory_initial_condition;
    robot_sim_DW.Memory_ValueDims = 1;
  }

  /* Start for S-Function (phantom_block): '<S3>/Left Device' */

  /* S-Function Block: robot_sim/Subsystem/Left Device (phantom_block) */
  {
    t_error result;

    /* Open and initialize the device. This also schedules the device callback function. */
    result = phantom_open_device(&robot_sim_DW.LeftDevice_Phantom,
      "Default Device", PHANTOM_JOINT_ANGLES_OUTPUT, PHANTOM_JOINT_SPACE_INPUT,
      0, -1, 3, 6);
    if (result < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(robot_sim_M, _rt_error_message);
    } else {
      /* Start the scheduler - *****TODO: change the rate to a parameter, just hardcoded at 1000Hz for now. */
      result = phantom_start_scheduler(robot_sim_DW.LeftDevice_Phantom, 1000);
      if (result < 0) {
        phantom_close_device(robot_sim_DW.LeftDevice_Phantom);
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(robot_sim_M, _rt_error_message);
      }
    }
  }

  /* Start for ToWorkspace: '<Root>/To Workspace' */
  {
    int_T dimensions[2] = { 6, 1 };

    robot_sim_DW.ToWorkspace_PWORK.LoggedData = rt_CreateLogVar(
      robot_sim_M->rtwLogInfo,
      0.0,
      rtmGetTFinal(robot_sim_M),
      robot_sim_M->Timing.stepSize0,
      (&rtmGetErrorStatus(robot_sim_M)),
      "q",
      SS_DOUBLE,
      0,
      0,
      0,
      6,
      2,
      dimensions,
      NO_LOGVALDIMS,
      (NULL),
      (NULL),
      0,
      1,
      0.004,
      1);
    if (robot_sim_DW.ToWorkspace_PWORK.LoggedData == (NULL))
      return;
  }

  /* Start for ToWorkspace: '<Root>/To Workspace1' */
  {
    int_T dimensions[1] = { 3 };

    robot_sim_DW.ToWorkspace1_PWORK.LoggedData = rt_CreateLogVar(
      robot_sim_M->rtwLogInfo,
      0.0,
      rtmGetTFinal(robot_sim_M),
      robot_sim_M->Timing.stepSize0,
      (&rtmGetErrorStatus(robot_sim_M)),
      "tau",
      SS_DOUBLE,
      0,
      0,
      0,
      3,
      1,
      dimensions,
      NO_LOGVALDIMS,
      (NULL),
      (NULL),
      0,
      1,
      0.004,
      1);
    if (robot_sim_DW.ToWorkspace1_PWORK.LoggedData == (NULL))
      return;
  }

  /* Start for ToWorkspace: '<Root>/To Workspace2' */
  {
    int_T dimensions[1] = { 1 };

    robot_sim_DW.ToWorkspace2_PWORK.LoggedData = rt_CreateLogVar(
      robot_sim_M->rtwLogInfo,
      0.0,
      rtmGetTFinal(robot_sim_M),
      robot_sim_M->Timing.stepSize0,
      (&rtmGetErrorStatus(robot_sim_M)),
      "t",
      SS_DOUBLE,
      0,
      0,
      0,
      1,
      1,
      dimensions,
      NO_LOGVALDIMS,
      (NULL),
      (NULL),
      0,
      1,
      0.004,
      1);
    if (robot_sim_DW.ToWorkspace2_PWORK.LoggedData == (NULL))
      return;
  }

  {
    uint32_T tseed;
    int32_T r;
    int32_T t;
    real_T tmp;

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn' */
    robot_sim_X.TransferFcn_CSTATE = 0.0;

    /* InitializeConditions for Derivative: '<S3>/Derivative' */
    robot_sim_DW.TimeStampA = (rtInf);
    robot_sim_DW.TimeStampB = (rtInf);

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn1' */
    robot_sim_X.TransferFcn1_CSTATE = 0.0;

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn2' */
    robot_sim_X.TransferFcn2_CSTATE = 0.0;

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number' */
    tmp = floor(fabs(robot_sim_P.seed1));
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

    robot_sim_DW.RandSeed = tseed;
    robot_sim_DW.UniformRandomNumber_NextOutput =
      (robot_sim_P.UniformRandomNumber_Maximum -
       robot_sim_P.UniformRandomNumber_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&robot_sim_DW.RandSeed) + robot_sim_P.UniformRandomNumber_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number' */

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number1' */
    tmp = floor(fabs(robot_sim_P.seed2));
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

    robot_sim_DW.RandSeed_d = tseed;
    robot_sim_DW.UniformRandomNumber1_NextOutput =
      (robot_sim_P.UniformRandomNumber1_Maximum -
       robot_sim_P.UniformRandomNumber1_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&robot_sim_DW.RandSeed_d) + robot_sim_P.UniformRandomNumber1_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number1' */

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number2' */
    tmp = floor(fabs(robot_sim_P.seed3));
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

    robot_sim_DW.RandSeed_e = tseed;
    robot_sim_DW.UniformRandomNumber2_NextOutput =
      (robot_sim_P.UniformRandomNumber2_Maximum -
       robot_sim_P.UniformRandomNumber2_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&robot_sim_DW.RandSeed_e) + robot_sim_P.UniformRandomNumber2_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number2' */
  }
}

/* Model terminate function */
void robot_sim_terminate(void)
{
  /* Terminate for S-Function (phantom_block): '<S3>/Left Device' */

  /* S-Function Block: robot_sim/Subsystem/Left Device (phantom_block) */
  {
    t_error result;
    if ((result = phantom_stop_scheduler(robot_sim_DW.LeftDevice_Phantom)) < 0)
    {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(robot_sim_M, _rt_error_message);
    }

    if ((result = phantom_close_device(robot_sim_DW.LeftDevice_Phantom)) < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(robot_sim_M, _rt_error_message);
    }
  }
}
