/*
 * Robot_Real.c
 *
 * Code generation for model "Robot_Real".
 *
 * Model version              : 1.12
 * Simulink Coder version : 8.14 (R2018a) 06-Feb-2018
 * C source code generated on : Fri Nov  7 13:04:05 2025
 *
 * Target selection: grt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "Robot_Real.h"
#include "Robot_Real_private.h"

/* Block signals (default storage) */
B_Robot_Real_T Robot_Real_B;

/* Continuous states */
X_Robot_Real_T Robot_Real_X;

/* Block states (default storage) */
DW_Robot_Real_T Robot_Real_DW;

/* Real-time model */
RT_MODEL_Robot_Real_T Robot_Real_M_;
RT_MODEL_Robot_Real_T *const Robot_Real_M = &Robot_Real_M_;

/* Simplified version of numjac.cpp, for use with RTW. */
void local_numjac( RTWSolverInfo *si, real_T *y, const real_T *Fty, real_T *fac,
                  real_T *dFdy )
{
  /* constants */
  real_T THRESH = 1e-6;
  real_T EPS = 2.2e-16;                /* utGetEps(); */
  real_T BL = pow(EPS, 0.75);
  real_T BU = pow(EPS, 0.25);
  real_T FACMIN = pow(EPS, 0.78);
  real_T FACMAX = 0.1;
  int_T nx = 3;
  real_T *x = rtsiGetContStates(si);
  real_T del;
  real_T difmax;
  real_T FdelRowmax;
  real_T temp;
  real_T Fdiff;
  real_T maybe;
  real_T xscale;
  real_T fscale;
  real_T *p;
  int_T rowmax;
  int_T i,j;
  if (x != y)
    (void) memcpy(x, y,
                  (uint_T)nx*sizeof(real_T));
  rtsiSetSolverComputingJacobian(si,true);
  for (p = dFdy, j = 0; j < nx; j++, p += nx) {
    /* Select an increment del for a difference approximation to
       column j of dFdy.  The vector fac accounts for experience
       gained in previous calls to numjac. */
    xscale = fabs(x[j]);
    if (xscale < THRESH)
      xscale = THRESH;
    temp = (x[j] + fac[j]*xscale);
    del = temp - y[j];
    while (del == 0.0) {
      if (fac[j] < FACMAX) {
        fac[j] *= 100.0;
        if (fac[j] > FACMAX)
          fac[j] = FACMAX;
        temp = (x[j] + fac[j]*xscale);
        del = temp - x[j];
      } else {
        del = THRESH;                  /* thresh is nonzero */
        break;
      }
    }

    /* Keep del pointing into region. */
    if (Fty[j] >= 0.0)
      del = fabs(del);
    else
      del = -fabs(del);

    /* Form a difference approximation to column j of dFdy. */
    temp = x[j];
    x[j] += del;
    Robot_Real_step();
    rtsiSetdX(si,p);
    Robot_Real_derivatives();
    x[j] = temp;
    difmax = 0.0;
    rowmax = 0;
    FdelRowmax = p[0];
    temp = 1.0 / del;
    for (i = 0; i < nx; i++) {
      Fdiff = p[i] - Fty[i];
      maybe = fabs(Fdiff);
      if (maybe > difmax) {
        difmax = maybe;
        rowmax = i;
        FdelRowmax = p[i];
      }

      p[i] = temp * Fdiff;
    }

    /* Adjust fac for next call to numjac. */
    if (((FdelRowmax != 0.0) && (Fty[rowmax] != 0.0)) || (difmax == 0.0)) {
      fscale = fabs(FdelRowmax);
      if (fscale < fabs(Fty[rowmax]))
        fscale = fabs(Fty[rowmax]);
      if (difmax <= BL*fscale) {
        /* The difference is small, so increase the increment. */
        fac[j] *= 10.0;
        if (fac[j] > FACMAX)
          fac[j] = FACMAX;
      } else if (difmax > BU*fscale) {
        /* The difference is large, so reduce the increment. */
        fac[j] *= 0.1;
        if (fac[j] < FACMIN)
          fac[j] = FACMIN;
      }
    }
  }

  rtsiSetSolverComputingJacobian(si,false);
}                                      /* end local_numjac */

/*
 * This function updates continuous states using the ODE14x fixed-step
 * solver algorithm
 */
static void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si )
{
  /* Solver Matrices */
  static int_T rt_ODE14x_N[4] = { 12, 8, 6, 4 };

  time_T t0 = rtsiGetT(si);
  time_T t1 = t0;
  time_T h = rtsiGetStepSize(si);
  real_T *x1 = rtsiGetContStates(si);
  int_T order = rtsiGetSolverExtrapolationOrder(si);
  int_T numIter = rtsiGetSolverNumberNewtonIterations(si);
  ODE14X_IntgData *id = (ODE14X_IntgData *)rtsiGetSolverData(si);
  real_T *x0 = id->x0;
  real_T *f0 = id->f0;
  real_T *x1start = id->x1start;
  real_T *f1 = id->f1;
  real_T *Delta = id->Delta;
  real_T *E = id->E;
  real_T *fac = id->fac;
  real_T *dfdx = id->DFDX;
  real_T *W = id->W;
  int_T *pivots = id->pivots;
  real_T *xtmp = id->xtmp;
  real_T *ztmp = id->ztmp;
  int_T *N = &(rt_ODE14x_N[0]);
  int_T i,j,k,iter;
  int_T nx = 3;
  rtsiSetSimTimeStep(si,MINOR_TIME_STEP);

  /* Save the state values at time t in y, we'll use x as ynew. */
  (void) memcpy(x0, x1,
                (uint_T)nx*sizeof(real_T));

  /* Assumes that rtsiSetT and ModelOutputs are up-to-date */

  /* f0 = f(t,y) */
  rtsiSetdX(si, f0);
  Robot_Real_derivatives();
  local_numjac(si,x0,f0,fac,dfdx );
  for (j = 0; j < order; j++) {
    real_T *p;
    real_T hN = h/N[j];

    /* Get the iteration matrix and solution at t0 */

    /* [L,U] = lu(M - hN*J) */
    (void) memcpy(W, dfdx,
                  (uint_T)nx*nx*sizeof(real_T));
    for (p = W, i = 0; i < nx*nx; i++, p++) {
      *p *= (-hN);
    }

    for (p = W, i = 0; i < nx; i++, p += (nx+1)) {
      *p += 1.0;
    }

    rt_lu_real(W, nx,
               pivots);

    /* First Newton's iteration at t0. */
    /* rhs = hN*f0 */
    for (i = 0; i < nx; i++) {
      Delta[i] = hN*f0[i];
    }

    /* Delta = (U \ (L \ rhs)) */
    rt_ForwardSubstitutionRR_Dbl(W, Delta,
      f1, nx,
      1, pivots,
      1);
    rt_BackwardSubstitutionRR_Dbl(W+nx*nx-1, f1+nx-1,
      Delta, nx,
      1, 0);

    /* ytmp = y0 + Delta
       ztmp = (ytmp-y0)/h
     */
    (void) memcpy(x1, x0,
                  (uint_T)nx*sizeof(real_T));
    for (i = 0; i < nx; i++) {
      x1[i] += Delta[i];
      ztmp[i] = Delta[i]/hN;
    }

    /* Additional Newton's iterations, if desired.
       for iter = 2:NewtIter
       rhs = hN*feval(odefun,tn,ytmp,extraArgs{:}) - M*(ytmp - yn);
       if statedepM   % only for state dep. Mdel ~= 0
       Mdel = M - feval(massfun,tn,ytmp);
       rhs = rhs + Mdel*ztmp*h;
       end
       Delta = ( U \ ( L \ rhs ) );
       ytmp = ytmp + Delta;
       ztmp = (ytmp - yn)/h
       end
     */
    rtsiSetT(si, t0);
    rtsiSetdX(si, f1);
    for (iter = 1; iter < numIter; iter++) {
      Robot_Real_step();
      Robot_Real_derivatives();
      for (i = 0; i < nx; i++) {
        Delta[i] = hN*f1[i];
        xtmp[i] = x1[i] - x0[i];
      }

      /* rhs = hN*f(tn,ytmp) - (ytmp-yn) */
      for (i = 0; i < nx; i++) {
        Delta[i] -= xtmp[i];
      }

      rt_ForwardSubstitutionRR_Dbl(W, Delta,
        f1, nx,
        1, pivots,
        1);
      rt_BackwardSubstitutionRR_Dbl(W+nx*nx-1, f1+nx-1,
        Delta, nx,
        1, 0);

      /* ytmp = ytmp + delta
         ztmp = (ytmp - yn)/h
       */
      for (i = 0; i < nx; i++) {
        x1[i] += Delta[i];
        ztmp[i] = (x1[i] - x0[i])/hN;
      }
    }

    /* Steps from t0+hN to t1 -- subintegration of N(j) steps for extrapolation
       ttmp = t0;
       for i = 2:N(j)
       ttmp = ttmp + hN
       ytmp0 = ytmp;
       for iter = 1:NewtIter
       rhs = (ytmp0 - ytmp) + hN*feval(odefun,ttmp,ytmp,extraArgs{:});
       Delta = ( U \ ( L \ rhs ) );
       ytmp = ytmp + Delta;
       end
       end
     */
    for (k = 1; k < N[j]; k++) {
      t1 = t0 + k*hN;
      (void) memcpy(x1start, x1,
                    (uint_T)nx*sizeof(real_T));
      rtsiSetT(si, t1);
      rtsiSetdX(si, f1);
      for (iter = 0; iter < numIter; iter++) {
        Robot_Real_step();
        Robot_Real_derivatives();
        if (iter == 0) {
          for (i = 0; i < nx; i++) {
            Delta[i] = hN*f1[i];
          }
        } else {
          for (i = 0; i < nx; i++) {
            Delta[i] = hN*f1[i];
            xtmp[i] = (x1[i]-x1start[i]);
          }

          /* rhs = hN*f(tn,ytmp) - M*(ytmp-yn) */
          for (i = 0; i < nx; i++) {
            Delta[i] -= xtmp[i];
          }
        }

        rt_ForwardSubstitutionRR_Dbl(W, Delta,
          f1, nx,
          1, pivots,
          1);
        rt_BackwardSubstitutionRR_Dbl(W+nx*nx-1, f1+nx-1,
          Delta, nx,
          1, 0);

        /* ytmp = ytmp + Delta
           ztmp = (ytmp - ytmp0)/h
         */
        for (i = 0; i < nx; i++) {
          x1[i] += Delta[i];
          ztmp[i] = (x1[i] - x1start[i])/hN;
        }
      }
    }

    /* Extrapolate to order j
       E(:,j) = ytmp
       for k = j:-1:2
       coef = N(k-1)/(N(j) - N(k-1))
       E(:,k-1) = E(:,k) + coef*( E(:,k) - E(:,k-1) )
       end
     */
    (void) memcpy(&(E[nx*j]), x1,
                  (uint_T)nx*sizeof(real_T));
    for (k = j; k > 0; k--) {
      real_T coef = (real_T)(N[k-1]) / (N[j]-N[k-1]);
      for (i = 0; i < nx; i++) {
        x1[i] = E[nx*k+i] + coef*(E[nx*k+i] - E[nx*(k-1)+i]);
      }

      (void) memcpy(&(E[nx*(k-1)]), x1,
                    (uint_T)nx*sizeof(real_T));
    }
  }

  /* x1 = E(:,1); */
  (void) memcpy(x1, E,
                (uint_T)nx*sizeof(real_T));

  /* t1 = t0 + h; */
  rtsiSetT(si,rtsiGetSolverStopTime(si));
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
void Robot_Real_step(void)
{
  /* local block i/o variables */
  real_T rtb_Memory2[3];
  real_T rtb_Memory1[3];
  real_T rtb_Memory[3];
  real_T rtb_TmpSignalConversionAtMemory[3];
  real_T rtb_TmpSignalConversionAtToWork[6];
  real_T rtb_Gain3[3];
  if (rtmIsMajorTimeStep(Robot_Real_M)) {
    /* set solver stop time */
    if (!(Robot_Real_M->Timing.clockTick0+1)) {
      rtsiSetSolverStopTime(&Robot_Real_M->solverInfo,
                            ((Robot_Real_M->Timing.clockTickH0 + 1) *
        Robot_Real_M->Timing.stepSize0 * 4294967296.0));
    } else {
      rtsiSetSolverStopTime(&Robot_Real_M->solverInfo,
                            ((Robot_Real_M->Timing.clockTick0 + 1) *
        Robot_Real_M->Timing.stepSize0 + Robot_Real_M->Timing.clockTickH0 *
        Robot_Real_M->Timing.stepSize0 * 4294967296.0));
    }
  }                                    /* end MajorTimeStep */

  /* Update absolute time of base rate at minor time step */
  if (rtmIsMinorTimeStep(Robot_Real_M)) {
    Robot_Real_M->Timing.t[0] = rtsiGetT(&Robot_Real_M->solverInfo);
  }

  {
    real_T (*lastU)[3];
    real_T lastTime;
    if (rtmIsMajorTimeStep(Robot_Real_M)) {
      /* S-Function (memory_block): '<Root>/Memory2' */
      {
        rtb_Memory2[0] = Robot_Real_DW.Memory2_Value[0];
        rtb_Memory2[1] = Robot_Real_DW.Memory2_Value[1];
        rtb_Memory2[2] = Robot_Real_DW.Memory2_Value[2];
      }

      /* S-Function (memory_block): '<Root>/Memory1' */
      {
        rtb_Memory1[0] = Robot_Real_DW.Memory1_Value[0];
        rtb_Memory1[1] = Robot_Real_DW.Memory1_Value[1];
        rtb_Memory1[2] = Robot_Real_DW.Memory1_Value[2];
      }

      /* S-Function (memory_block): '<Root>/Memory' */
      {
        rtb_Memory[0] = Robot_Real_DW.Memory_Value[0];
        rtb_Memory[1] = Robot_Real_DW.Memory_Value[1];
        rtb_Memory[2] = Robot_Real_DW.Memory_Value[2];
      }

      /* Sum: '<Root>/Sum' */
      rtb_Gain3[0] = (rtb_Memory2[0] + rtb_Memory1[0]) + rtb_Memory[0];

      /* Saturate: '<Root>/Saturation' */
      if (rtb_Gain3[0] > Robot_Real_P.Saturation_UpperSat[0]) {
        Robot_Real_B.Saturation[0] = Robot_Real_P.Saturation_UpperSat[0];
      } else if (rtb_Gain3[0] < Robot_Real_P.Saturation_LowerSat[0]) {
        Robot_Real_B.Saturation[0] = Robot_Real_P.Saturation_LowerSat[0];
      } else {
        Robot_Real_B.Saturation[0] = rtb_Gain3[0];
      }

      /* Sum: '<Root>/Sum' */
      rtb_Gain3[1] = (rtb_Memory2[1] + rtb_Memory1[1]) + rtb_Memory[1];

      /* Saturate: '<Root>/Saturation' */
      if (rtb_Gain3[1] > Robot_Real_P.Saturation_UpperSat[1]) {
        Robot_Real_B.Saturation[1] = Robot_Real_P.Saturation_UpperSat[1];
      } else if (rtb_Gain3[1] < Robot_Real_P.Saturation_LowerSat[1]) {
        Robot_Real_B.Saturation[1] = Robot_Real_P.Saturation_LowerSat[1];
      } else {
        Robot_Real_B.Saturation[1] = rtb_Gain3[1];
      }

      /* Sum: '<Root>/Sum' */
      rtb_Gain3[2] = (rtb_Memory2[2] + rtb_Memory1[2]) + rtb_Memory[2];

      /* Saturate: '<Root>/Saturation' */
      if (rtb_Gain3[2] > Robot_Real_P.Saturation_UpperSat[2]) {
        Robot_Real_B.Saturation[2] = Robot_Real_P.Saturation_UpperSat[2];
      } else if (rtb_Gain3[2] < Robot_Real_P.Saturation_LowerSat[2]) {
        Robot_Real_B.Saturation[2] = Robot_Real_P.Saturation_LowerSat[2];
      } else {
        Robot_Real_B.Saturation[2] = rtb_Gain3[2];
      }
    }

    /* TransferFcn: '<Root>/Transfer Fcn' */
    Robot_Real_B.TransferFcn = 0.0;
    Robot_Real_B.TransferFcn += Robot_Real_P.TransferFcn_C *
      Robot_Real_X.TransferFcn_CSTATE;

    /* Gain: '<Root>/Gain' */
    Robot_Real_B.Gain = Robot_Real_P.Gain_Gain * Robot_Real_B.TransferFcn;
    if (rtmIsMajorTimeStep(Robot_Real_M)) {
      /* S-Function (phantom_block): '<S3>/Left Device' */

      /* S-Function Block: Robot_Real/Subsystem/Left Device (phantom_block) */
      {
        t_error result = 0;
        result = phantom_read(Robot_Real_DW.LeftDevice_Phantom,
                              &Robot_Real_B.LeftDevice_o1,
                              &Robot_Real_B.LeftDevice_o2[0],
                              &Robot_Real_B.LeftDevice_o3[0], NULL,
                              &Robot_Real_B.LeftDevice_o4);
        if (result < 0) {
          msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
            (_rt_error_message));
          rtmSetErrorStatus(Robot_Real_M, _rt_error_message);
        }

        result = phantom_write(Robot_Real_DW.LeftDevice_Phantom,
          &Robot_Real_B.Saturation[0], NULL);
        if (result < 0) {
          msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
            (_rt_error_message));
          rtmSetErrorStatus(Robot_Real_M, _rt_error_message);
        }
      }
    }

    /* Derivative: '<S3>/Derivative' */
    if ((Robot_Real_DW.TimeStampA >= Robot_Real_M->Timing.t[0]) &&
        (Robot_Real_DW.TimeStampB >= Robot_Real_M->Timing.t[0])) {
      Robot_Real_B.Derivative[0] = 0.0;
      Robot_Real_B.Derivative[1] = 0.0;
      Robot_Real_B.Derivative[2] = 0.0;
    } else {
      lastTime = Robot_Real_DW.TimeStampA;
      lastU = &Robot_Real_DW.LastUAtTimeA;
      if (Robot_Real_DW.TimeStampA < Robot_Real_DW.TimeStampB) {
        if (Robot_Real_DW.TimeStampB < Robot_Real_M->Timing.t[0]) {
          lastTime = Robot_Real_DW.TimeStampB;
          lastU = &Robot_Real_DW.LastUAtTimeB;
        }
      } else {
        if (Robot_Real_DW.TimeStampA >= Robot_Real_M->Timing.t[0]) {
          lastTime = Robot_Real_DW.TimeStampB;
          lastU = &Robot_Real_DW.LastUAtTimeB;
        }
      }

      lastTime = Robot_Real_M->Timing.t[0] - lastTime;
      Robot_Real_B.Derivative[0] = (Robot_Real_B.LeftDevice_o2[0] - (*lastU)[0])
        / lastTime;
      Robot_Real_B.Derivative[1] = (Robot_Real_B.LeftDevice_o2[1] - (*lastU)[1])
        / lastTime;
      Robot_Real_B.Derivative[2] = (Robot_Real_B.LeftDevice_o2[2] - (*lastU)[2])
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
    Robot_Real_B.tau[0] = rt_powd_snf(fabs(Robot_Real_B.LeftDevice_o2[0]) /
      1.0471975511965976, 5.0) * 0.5 * -Robot_Real_B.LeftDevice_o2[0] + 0.01 *
      -Robot_Real_B.Derivative[0];
    Robot_Real_B.tau[1] = rt_powd_snf(fabs(Robot_Real_B.LeftDevice_o2[1] - 0.895)
      / 0.895, 5.0) * 0.5 * -(Robot_Real_B.LeftDevice_o2[1] - 0.895) + 0.01 *
      -Robot_Real_B.Derivative[1];
    Robot_Real_B.tau[2] = rt_powd_snf(fabs(Robot_Real_B.LeftDevice_o2[2] - -1.35)
      / 1.1, 5.0) * 0.5 * -(Robot_Real_B.LeftDevice_o2[2] - -1.35) + 0.01 *
      -Robot_Real_B.Derivative[2];
    if (rtmIsMajorTimeStep(Robot_Real_M)) {
    }

    /* TransferFcn: '<Root>/Transfer Fcn1' */
    Robot_Real_B.TransferFcn1 = 0.0;
    Robot_Real_B.TransferFcn1 += Robot_Real_P.TransferFcn1_C *
      Robot_Real_X.TransferFcn1_CSTATE;

    /* Gain: '<Root>/Gain1' */
    Robot_Real_B.Gain1 = Robot_Real_P.Gain1_Gain * Robot_Real_B.TransferFcn1;
    if (rtmIsMajorTimeStep(Robot_Real_M)) {
    }

    /* TransferFcn: '<Root>/Transfer Fcn2' */
    Robot_Real_B.TransferFcn2 = 0.0;
    Robot_Real_B.TransferFcn2 += Robot_Real_P.TransferFcn2_C *
      Robot_Real_X.TransferFcn2_CSTATE;

    /* Gain: '<Root>/Gain2' */
    Robot_Real_B.Gain2 = Robot_Real_P.Gain2_Gain * Robot_Real_B.TransferFcn2;
    if (rtmIsMajorTimeStep(Robot_Real_M)) {
      /* SignalConversion: '<Root>/TmpSignal ConversionAtTo WorkspaceInport1' */
      rtb_TmpSignalConversionAtToWork[0] = Robot_Real_B.LeftDevice_o2[0];
      rtb_TmpSignalConversionAtToWork[1] = Robot_Real_B.Derivative[0];
      rtb_TmpSignalConversionAtToWork[2] = Robot_Real_B.LeftDevice_o2[1];
      rtb_TmpSignalConversionAtToWork[3] = Robot_Real_B.Derivative[1];
      rtb_TmpSignalConversionAtToWork[4] = Robot_Real_B.LeftDevice_o2[2];
      rtb_TmpSignalConversionAtToWork[5] = Robot_Real_B.Derivative[2];

      /* ToWorkspace: '<Root>/To Workspace' */
      if (rtmIsMajorTimeStep(Robot_Real_M)) {
        rt_UpdateLogVar((LogVar *)(LogVar*)
                        (Robot_Real_DW.ToWorkspace_PWORK.LoggedData),
                        &rtb_TmpSignalConversionAtToWork[0], 0);
      }

      /* Gain: '<Root>/Gain3' */
      rtb_Gain3[0] = Robot_Real_P.Gain3_Gain * Robot_Real_B.Saturation[0];
      rtb_Gain3[1] = Robot_Real_P.Gain3_Gain * Robot_Real_B.Saturation[1];
      rtb_Gain3[2] = Robot_Real_P.Gain3_Gain * Robot_Real_B.Saturation[2];

      /* ToWorkspace: '<Root>/To Workspace1' */
      if (rtmIsMajorTimeStep(Robot_Real_M)) {
        rt_UpdateLogVar((LogVar *)(LogVar*)
                        (Robot_Real_DW.ToWorkspace1_PWORK.LoggedData),
                        &rtb_Gain3[0], 0);
      }

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
      Robot_Real_B.tau_g[0] = 0.0;
      lastTime = cos(Robot_Real_B.LeftDevice_o2[1] + Robot_Real_B.LeftDevice_o2
                     [2]) * 0.050960000000000012;
      Robot_Real_B.tau_g[1] = lastTime + 0.089180000000000009 * cos
        (Robot_Real_B.LeftDevice_o2[1]);
      Robot_Real_B.tau_g[2] = lastTime;

      /* SignalConversion: '<Root>/TmpSignal ConversionAtMemory2Inport1' */
      rtb_TmpSignalConversionAtMemory[0] = Robot_Real_B.Gain;
      rtb_TmpSignalConversionAtMemory[1] = Robot_Real_B.Gain1;
      rtb_TmpSignalConversionAtMemory[2] = Robot_Real_B.Gain2;

      /* UniformRandomNumber: '<Root>/Uniform Random Number' */
      Robot_Real_B.UniformRandomNumber =
        Robot_Real_DW.UniformRandomNumber_NextOutput;

      /* UniformRandomNumber: '<Root>/Uniform Random Number1' */
      Robot_Real_B.UniformRandomNumber1 =
        Robot_Real_DW.UniformRandomNumber1_NextOutput;

      /* UniformRandomNumber: '<Root>/Uniform Random Number2' */
      Robot_Real_B.UniformRandomNumber2 =
        Robot_Real_DW.UniformRandomNumber2_NextOutput;
    }

    /* Clock: '<Root>/Clock' */
    Robot_Real_B.Clock = Robot_Real_M->Timing.t[0];
    if (rtmIsMajorTimeStep(Robot_Real_M)) {
      /* ToWorkspace: '<Root>/To Workspace2' */
      if (rtmIsMajorTimeStep(Robot_Real_M)) {
        rt_UpdateLogVar((LogVar *)(LogVar*)
                        (Robot_Real_DW.ToWorkspace2_PWORK.LoggedData),
                        &Robot_Real_B.Clock, 0);
      }
    }
  }

  if (rtmIsMajorTimeStep(Robot_Real_M)) {
    /* Matfile logging */
    rt_UpdateTXYLogVars(Robot_Real_M->rtwLogInfo, (Robot_Real_M->Timing.t));
  }                                    /* end MajorTimeStep */

  if (rtmIsMajorTimeStep(Robot_Real_M)) {
    real_T (*lastU)[3];
    if (rtmIsMajorTimeStep(Robot_Real_M)) {
      /* Update for S-Function (memory_block): '<Root>/Memory2' */
      {
        Robot_Real_DW.Memory2_Value[0] = rtb_TmpSignalConversionAtMemory[0];
        Robot_Real_DW.Memory2_Value[1] = rtb_TmpSignalConversionAtMemory[1];
        Robot_Real_DW.Memory2_Value[2] = rtb_TmpSignalConversionAtMemory[2];
      }

      /* Update for S-Function (memory_block): '<Root>/Memory1' */
      {
        Robot_Real_DW.Memory1_Value[0] = Robot_Real_B.tau[0];
        Robot_Real_DW.Memory1_Value[1] = Robot_Real_B.tau[1];
        Robot_Real_DW.Memory1_Value[2] = Robot_Real_B.tau[2];
      }

      /* Update for S-Function (memory_block): '<Root>/Memory' */
      {
        Robot_Real_DW.Memory_Value[0] = Robot_Real_B.tau_g[0];
        Robot_Real_DW.Memory_Value[1] = Robot_Real_B.tau_g[1];
        Robot_Real_DW.Memory_Value[2] = Robot_Real_B.tau_g[2];
      }
    }

    /* Update for Derivative: '<S3>/Derivative' */
    if (Robot_Real_DW.TimeStampA == (rtInf)) {
      Robot_Real_DW.TimeStampA = Robot_Real_M->Timing.t[0];
      lastU = &Robot_Real_DW.LastUAtTimeA;
    } else if (Robot_Real_DW.TimeStampB == (rtInf)) {
      Robot_Real_DW.TimeStampB = Robot_Real_M->Timing.t[0];
      lastU = &Robot_Real_DW.LastUAtTimeB;
    } else if (Robot_Real_DW.TimeStampA < Robot_Real_DW.TimeStampB) {
      Robot_Real_DW.TimeStampA = Robot_Real_M->Timing.t[0];
      lastU = &Robot_Real_DW.LastUAtTimeA;
    } else {
      Robot_Real_DW.TimeStampB = Robot_Real_M->Timing.t[0];
      lastU = &Robot_Real_DW.LastUAtTimeB;
    }

    (*lastU)[0] = Robot_Real_B.LeftDevice_o2[0];
    (*lastU)[1] = Robot_Real_B.LeftDevice_o2[1];
    (*lastU)[2] = Robot_Real_B.LeftDevice_o2[2];

    /* End of Update for Derivative: '<S3>/Derivative' */
    if (rtmIsMajorTimeStep(Robot_Real_M)) {
      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number' */
      Robot_Real_DW.UniformRandomNumber_NextOutput =
        (Robot_Real_P.UniformRandomNumber_Maximum -
         Robot_Real_P.UniformRandomNumber_Minimum) * rt_urand_Upu32_Yd_f_pw_snf(
        &Robot_Real_DW.RandSeed) + Robot_Real_P.UniformRandomNumber_Minimum;

      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number1' */
      Robot_Real_DW.UniformRandomNumber1_NextOutput =
        (Robot_Real_P.UniformRandomNumber1_Maximum -
         Robot_Real_P.UniformRandomNumber1_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
        (&Robot_Real_DW.RandSeed_j) + Robot_Real_P.UniformRandomNumber1_Minimum;

      /* Update for UniformRandomNumber: '<Root>/Uniform Random Number2' */
      Robot_Real_DW.UniformRandomNumber2_NextOutput =
        (Robot_Real_P.UniformRandomNumber2_Maximum -
         Robot_Real_P.UniformRandomNumber2_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
        (&Robot_Real_DW.RandSeed_o) + Robot_Real_P.UniformRandomNumber2_Minimum;
    }
  }                                    /* end MajorTimeStep */

  if (rtmIsMajorTimeStep(Robot_Real_M)) {
    /* signal main to stop simulation */
    {                                  /* Sample time: [0.0s, 0.0s] */
      if ((rtmGetTFinal(Robot_Real_M)!=-1) &&
          !((rtmGetTFinal(Robot_Real_M)-(((Robot_Real_M->Timing.clockTick1+
               Robot_Real_M->Timing.clockTickH1* 4294967296.0)) * 0.05)) >
            (((Robot_Real_M->Timing.clockTick1+Robot_Real_M->Timing.clockTickH1*
               4294967296.0)) * 0.05) * (DBL_EPSILON))) {
        rtmSetErrorStatus(Robot_Real_M, "Simulation finished");
      }
    }

    rt_ertODEUpdateContinuousStates(&Robot_Real_M->solverInfo);

    /* Update absolute time for base rate */
    /* The "clockTick0" counts the number of times the code of this task has
     * been executed. The absolute time is the multiplication of "clockTick0"
     * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
     * overflow during the application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick0 and the high bits
     * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
     */
    if (!(++Robot_Real_M->Timing.clockTick0)) {
      ++Robot_Real_M->Timing.clockTickH0;
    }

    Robot_Real_M->Timing.t[0] = rtsiGetSolverStopTime(&Robot_Real_M->solverInfo);

    {
      /* Update absolute timer for sample time: [0.05s, 0.0s] */
      /* The "clockTick1" counts the number of times the code of this task has
       * been executed. The resolution of this integer timer is 0.05, which is the step size
       * of the task. Size of "clockTick1" ensures timer will not overflow during the
       * application lifespan selected.
       * Timer of this task consists of two 32 bit unsigned integers.
       * The two integers represent the low bits Timing.clockTick1 and the high bits
       * Timing.clockTickH1. When the low bit overflows to 0, the high bits increment.
       */
      Robot_Real_M->Timing.clockTick1++;
      if (!Robot_Real_M->Timing.clockTick1) {
        Robot_Real_M->Timing.clockTickH1++;
      }
    }
  }                                    /* end MajorTimeStep */
}

/* Derivatives for root system: '<Root>' */
void Robot_Real_derivatives(void)
{
  XDot_Robot_Real_T *_rtXdot;
  _rtXdot = ((XDot_Robot_Real_T *) Robot_Real_M->derivs);

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn' */
  _rtXdot->TransferFcn_CSTATE = 0.0;
  _rtXdot->TransferFcn_CSTATE += Robot_Real_P.TransferFcn_A *
    Robot_Real_X.TransferFcn_CSTATE;
  _rtXdot->TransferFcn_CSTATE += Robot_Real_B.UniformRandomNumber;

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn1' */
  _rtXdot->TransferFcn1_CSTATE = 0.0;
  _rtXdot->TransferFcn1_CSTATE += Robot_Real_P.TransferFcn1_A *
    Robot_Real_X.TransferFcn1_CSTATE;
  _rtXdot->TransferFcn1_CSTATE += Robot_Real_B.UniformRandomNumber1;

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn2' */
  _rtXdot->TransferFcn2_CSTATE = 0.0;
  _rtXdot->TransferFcn2_CSTATE += Robot_Real_P.TransferFcn2_A *
    Robot_Real_X.TransferFcn2_CSTATE;
  _rtXdot->TransferFcn2_CSTATE += Robot_Real_B.UniformRandomNumber2;
}

/* Model initialize function */
void Robot_Real_initialize(void)
{
  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* initialize real-time model */
  (void) memset((void *)Robot_Real_M, 0,
                sizeof(RT_MODEL_Robot_Real_T));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&Robot_Real_M->solverInfo,
                          &Robot_Real_M->Timing.simTimeStep);
    rtsiSetTPtr(&Robot_Real_M->solverInfo, &rtmGetTPtr(Robot_Real_M));
    rtsiSetStepSizePtr(&Robot_Real_M->solverInfo,
                       &Robot_Real_M->Timing.stepSize0);
    rtsiSetdXPtr(&Robot_Real_M->solverInfo, &Robot_Real_M->derivs);
    rtsiSetContStatesPtr(&Robot_Real_M->solverInfo, (real_T **)
                         &Robot_Real_M->contStates);
    rtsiSetNumContStatesPtr(&Robot_Real_M->solverInfo,
      &Robot_Real_M->Sizes.numContStates);
    rtsiSetNumPeriodicContStatesPtr(&Robot_Real_M->solverInfo,
      &Robot_Real_M->Sizes.numPeriodicContStates);
    rtsiSetPeriodicContStateIndicesPtr(&Robot_Real_M->solverInfo,
      &Robot_Real_M->periodicContStateIndices);
    rtsiSetPeriodicContStateRangesPtr(&Robot_Real_M->solverInfo,
      &Robot_Real_M->periodicContStateRanges);
    rtsiSetErrorStatusPtr(&Robot_Real_M->solverInfo, (&rtmGetErrorStatus
      (Robot_Real_M)));
    rtsiSetRTModelPtr(&Robot_Real_M->solverInfo, Robot_Real_M);
  }

  rtsiSetSimTimeStep(&Robot_Real_M->solverInfo, MAJOR_TIME_STEP);
  Robot_Real_M->intgData.x0 = Robot_Real_M->odeX0;
  Robot_Real_M->intgData.f0 = Robot_Real_M->odeF0;
  Robot_Real_M->intgData.x1start = Robot_Real_M->odeX1START;
  Robot_Real_M->intgData.f1 = Robot_Real_M->odeF1;
  Robot_Real_M->intgData.Delta = Robot_Real_M->odeDELTA;
  Robot_Real_M->intgData.E = Robot_Real_M->odeE;
  Robot_Real_M->intgData.fac = Robot_Real_M->odeFAC;

  /* initialize */
  {
    int_T i;
    real_T *f = Robot_Real_M->intgData.fac;
    for (i = 0; i < (int_T)(sizeof(Robot_Real_M->odeFAC)/sizeof(real_T)); i++) {
      f[i] = 1.5e-8;
    }
  }

  Robot_Real_M->intgData.DFDX = Robot_Real_M->odeDFDX;
  Robot_Real_M->intgData.W = Robot_Real_M->odeW;
  Robot_Real_M->intgData.pivots = Robot_Real_M->odePIVOTS;
  Robot_Real_M->intgData.xtmp = Robot_Real_M->odeXTMP;
  Robot_Real_M->intgData.ztmp = Robot_Real_M->odeZTMP;
  Robot_Real_M->intgData.isFirstStep = true;
  rtsiSetSolverExtrapolationOrder(&Robot_Real_M->solverInfo, 4);
  rtsiSetSolverNumberNewtonIterations(&Robot_Real_M->solverInfo, 1);
  Robot_Real_M->contStates = ((X_Robot_Real_T *) &Robot_Real_X);
  rtsiSetSolverData(&Robot_Real_M->solverInfo, (void *)&Robot_Real_M->intgData);
  rtsiSetSolverName(&Robot_Real_M->solverInfo,"ode14x");
  rtmSetTPtr(Robot_Real_M, &Robot_Real_M->Timing.tArray[0]);
  rtmSetTFinal(Robot_Real_M, 20.0);
  Robot_Real_M->Timing.stepSize0 = 0.05;

  /* Setup for data logging */
  {
    static RTWLogInfo rt_DataLoggingInfo;
    rt_DataLoggingInfo.loggingInterval = NULL;
    Robot_Real_M->rtwLogInfo = &rt_DataLoggingInfo;
  }

  /* Setup for data logging */
  {
    rtliSetLogXSignalInfo(Robot_Real_M->rtwLogInfo, (NULL));
    rtliSetLogXSignalPtrs(Robot_Real_M->rtwLogInfo, (NULL));
    rtliSetLogT(Robot_Real_M->rtwLogInfo, "tout");
    rtliSetLogX(Robot_Real_M->rtwLogInfo, "");
    rtliSetLogXFinal(Robot_Real_M->rtwLogInfo, "");
    rtliSetLogVarNameModifier(Robot_Real_M->rtwLogInfo, "rt_");
    rtliSetLogFormat(Robot_Real_M->rtwLogInfo, 4);
    rtliSetLogMaxRows(Robot_Real_M->rtwLogInfo, 0);
    rtliSetLogDecimation(Robot_Real_M->rtwLogInfo, 1);
    rtliSetLogY(Robot_Real_M->rtwLogInfo, "");
    rtliSetLogYSignalInfo(Robot_Real_M->rtwLogInfo, (NULL));
    rtliSetLogYSignalPtrs(Robot_Real_M->rtwLogInfo, (NULL));
  }

  /* block I/O */
  (void) memset(((void *) &Robot_Real_B), 0,
                sizeof(B_Robot_Real_T));

  /* states (continuous) */
  {
    (void) memset((void *)&Robot_Real_X, 0,
                  sizeof(X_Robot_Real_T));
  }

  /* states (dwork) */
  (void) memset((void *)&Robot_Real_DW, 0,
                sizeof(DW_Robot_Real_T));

  /* Matfile logging */
  rt_StartDataLoggingWithStartTime(Robot_Real_M->rtwLogInfo, 0.0, rtmGetTFinal
    (Robot_Real_M), Robot_Real_M->Timing.stepSize0, (&rtmGetErrorStatus
    (Robot_Real_M)));

  /* Start for S-Function (memory_block): '<Root>/Memory2' */
  {
    Robot_Real_DW.Memory2_Value[0] = (real_T)
      Robot_Real_P.Memory2_initial_condition;
    Robot_Real_DW.Memory2_Value[1] = (real_T)
      Robot_Real_P.Memory2_initial_condition;
    Robot_Real_DW.Memory2_Value[2] = (real_T)
      Robot_Real_P.Memory2_initial_condition;
    Robot_Real_DW.Memory2_ValueDims = 1;
  }

  /* Start for S-Function (memory_block): '<Root>/Memory1' */
  {
    Robot_Real_DW.Memory1_Value[0] = (real_T)
      Robot_Real_P.Memory1_initial_condition;
    Robot_Real_DW.Memory1_Value[1] = (real_T)
      Robot_Real_P.Memory1_initial_condition;
    Robot_Real_DW.Memory1_Value[2] = (real_T)
      Robot_Real_P.Memory1_initial_condition;
    Robot_Real_DW.Memory1_ValueDims = 1;
  }

  /* Start for S-Function (memory_block): '<Root>/Memory' */
  {
    Robot_Real_DW.Memory_Value[0] = (real_T)
      Robot_Real_P.Memory_initial_condition;
    Robot_Real_DW.Memory_Value[1] = (real_T)
      Robot_Real_P.Memory_initial_condition;
    Robot_Real_DW.Memory_Value[2] = (real_T)
      Robot_Real_P.Memory_initial_condition;
    Robot_Real_DW.Memory_ValueDims = 1;
  }

  /* Start for S-Function (phantom_block): '<S3>/Left Device' */

  /* S-Function Block: Robot_Real/Subsystem/Left Device (phantom_block) */
  {
    t_error result;

    /* Open and initialize the device. This also schedules the device callback function. */
    result = phantom_open_device(&Robot_Real_DW.LeftDevice_Phantom,
      "Default Device", PHANTOM_JOINT_ANGLES_OUTPUT, PHANTOM_JOINT_SPACE_INPUT,
      0, -1, 3, 6);
    if (result < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(Robot_Real_M, _rt_error_message);
    } else {
      /* Start the scheduler - *****TODO: change the rate to a parameter, just hardcoded at 1000Hz for now. */
      result = phantom_start_scheduler(Robot_Real_DW.LeftDevice_Phantom, 1000);
      if (result < 0) {
        phantom_close_device(Robot_Real_DW.LeftDevice_Phantom);
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Robot_Real_M, _rt_error_message);
      }
    }
  }

  /* Start for ToWorkspace: '<Root>/To Workspace' */
  {
    int_T dimensions[2] = { 6, 1 };

    Robot_Real_DW.ToWorkspace_PWORK.LoggedData = rt_CreateLogVar(
      Robot_Real_M->rtwLogInfo,
      0.0,
      rtmGetTFinal(Robot_Real_M),
      Robot_Real_M->Timing.stepSize0,
      (&rtmGetErrorStatus(Robot_Real_M)),
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
      0.05,
      1);
    if (Robot_Real_DW.ToWorkspace_PWORK.LoggedData == (NULL))
      return;
  }

  /* Start for ToWorkspace: '<Root>/To Workspace1' */
  {
    int_T dimensions[1] = { 3 };

    Robot_Real_DW.ToWorkspace1_PWORK.LoggedData = rt_CreateLogVar(
      Robot_Real_M->rtwLogInfo,
      0.0,
      rtmGetTFinal(Robot_Real_M),
      Robot_Real_M->Timing.stepSize0,
      (&rtmGetErrorStatus(Robot_Real_M)),
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
      0.05,
      1);
    if (Robot_Real_DW.ToWorkspace1_PWORK.LoggedData == (NULL))
      return;
  }

  /* Start for ToWorkspace: '<Root>/To Workspace2' */
  {
    int_T dimensions[1] = { 1 };

    Robot_Real_DW.ToWorkspace2_PWORK.LoggedData = rt_CreateLogVar(
      Robot_Real_M->rtwLogInfo,
      0.0,
      rtmGetTFinal(Robot_Real_M),
      Robot_Real_M->Timing.stepSize0,
      (&rtmGetErrorStatus(Robot_Real_M)),
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
      0.05,
      1);
    if (Robot_Real_DW.ToWorkspace2_PWORK.LoggedData == (NULL))
      return;
  }

  {
    uint32_T tseed;
    int32_T r;
    int32_T t;
    real_T tmp;

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn' */
    Robot_Real_X.TransferFcn_CSTATE = 0.0;

    /* InitializeConditions for Derivative: '<S3>/Derivative' */
    Robot_Real_DW.TimeStampA = (rtInf);
    Robot_Real_DW.TimeStampB = (rtInf);

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn1' */
    Robot_Real_X.TransferFcn1_CSTATE = 0.0;

    /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn2' */
    Robot_Real_X.TransferFcn2_CSTATE = 0.0;

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number' */
    tmp = floor(fabs(Robot_Real_P.seed1));
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

    Robot_Real_DW.RandSeed = tseed;
    Robot_Real_DW.UniformRandomNumber_NextOutput =
      (Robot_Real_P.UniformRandomNumber_Maximum -
       Robot_Real_P.UniformRandomNumber_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&Robot_Real_DW.RandSeed) + Robot_Real_P.UniformRandomNumber_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number' */

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number1' */
    tmp = floor(fabs(Robot_Real_P.seed2));
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

    Robot_Real_DW.RandSeed_j = tseed;
    Robot_Real_DW.UniformRandomNumber1_NextOutput =
      (Robot_Real_P.UniformRandomNumber1_Maximum -
       Robot_Real_P.UniformRandomNumber1_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&Robot_Real_DW.RandSeed_j) + Robot_Real_P.UniformRandomNumber1_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number1' */

    /* InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number2' */
    tmp = floor(fabs(Robot_Real_P.seed3));
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

    Robot_Real_DW.RandSeed_o = tseed;
    Robot_Real_DW.UniformRandomNumber2_NextOutput =
      (Robot_Real_P.UniformRandomNumber2_Maximum -
       Robot_Real_P.UniformRandomNumber2_Minimum) * rt_urand_Upu32_Yd_f_pw_snf
      (&Robot_Real_DW.RandSeed_o) + Robot_Real_P.UniformRandomNumber2_Minimum;

    /* End of InitializeConditions for UniformRandomNumber: '<Root>/Uniform Random Number2' */
  }
}

/* Model terminate function */
void Robot_Real_terminate(void)
{
  /* Terminate for S-Function (phantom_block): '<S3>/Left Device' */

  /* S-Function Block: Robot_Real/Subsystem/Left Device (phantom_block) */
  {
    t_error result;
    if ((result = phantom_stop_scheduler(Robot_Real_DW.LeftDevice_Phantom)) < 0)
    {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(Robot_Real_M, _rt_error_message);
    }

    if ((result = phantom_close_device(Robot_Real_DW.LeftDevice_Phantom)) < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(Robot_Real_M, _rt_error_message);
    }
  }
}
