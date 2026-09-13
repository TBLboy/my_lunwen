  function targMap = targDataMap(),

  ;%***********************
  ;% Create Parameter Map *
  ;%***********************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 1;
    sectIdxOffset = 0;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc paramMap
    ;%
    paramMap.nSections           = nTotSects;
    paramMap.sectIdxOffset       = sectIdxOffset;
      paramMap.sections(nTotSects) = dumSection; %prealloc
    paramMap.nTotData            = -1;
    
    ;%
    ;% Auto data (QuarkRefer_P)
    ;%
      section.nData     = 30;
      section.data(30)  = dumData; %prealloc
      
	  ;% QuarkRefer_P.seed1
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
	  ;% QuarkRefer_P.seed2
	  section.data(2).logicalSrcIdx = 1;
	  section.data(2).dtTransOffset = 1;
	
	  ;% QuarkRefer_P.seed3
	  section.data(3).logicalSrcIdx = 2;
	  section.data(3).dtTransOffset = 2;
	
	  ;% QuarkRefer_P.Memory2_initial_condition
	  section.data(4).logicalSrcIdx = 3;
	  section.data(4).dtTransOffset = 3;
	
	  ;% QuarkRefer_P.Memory1_initial_condition
	  section.data(5).logicalSrcIdx = 4;
	  section.data(5).dtTransOffset = 6;
	
	  ;% QuarkRefer_P.Memory_initial_condition
	  section.data(6).logicalSrcIdx = 5;
	  section.data(6).dtTransOffset = 7;
	
	  ;% QuarkRefer_P.Saturation_UpperSat
	  section.data(7).logicalSrcIdx = 6;
	  section.data(7).dtTransOffset = 10;
	
	  ;% QuarkRefer_P.Saturation_LowerSat
	  section.data(8).logicalSrcIdx = 7;
	  section.data(8).dtTransOffset = 13;
	
	  ;% QuarkRefer_P.TransferFcn_A
	  section.data(9).logicalSrcIdx = 8;
	  section.data(9).dtTransOffset = 16;
	
	  ;% QuarkRefer_P.TransferFcn_C
	  section.data(10).logicalSrcIdx = 9;
	  section.data(10).dtTransOffset = 17;
	
	  ;% QuarkRefer_P.Gain_Gain
	  section.data(11).logicalSrcIdx = 10;
	  section.data(11).dtTransOffset = 18;
	
	  ;% QuarkRefer_P.TransferFcn1_A
	  section.data(12).logicalSrcIdx = 11;
	  section.data(12).dtTransOffset = 19;
	
	  ;% QuarkRefer_P.TransferFcn1_C
	  section.data(13).logicalSrcIdx = 12;
	  section.data(13).dtTransOffset = 20;
	
	  ;% QuarkRefer_P.Gain1_Gain
	  section.data(14).logicalSrcIdx = 13;
	  section.data(14).dtTransOffset = 21;
	
	  ;% QuarkRefer_P.TransferFcn2_A
	  section.data(15).logicalSrcIdx = 14;
	  section.data(15).dtTransOffset = 22;
	
	  ;% QuarkRefer_P.TransferFcn2_C
	  section.data(16).logicalSrcIdx = 15;
	  section.data(16).dtTransOffset = 23;
	
	  ;% QuarkRefer_P.Gain2_Gain
	  section.data(17).logicalSrcIdx = 16;
	  section.data(17).dtTransOffset = 24;
	
	  ;% QuarkRefer_P.Gain3_Gain
	  section.data(18).logicalSrcIdx = 17;
	  section.data(18).dtTransOffset = 25;
	
	  ;% QuarkRefer_P.Gain4_Gain
	  section.data(19).logicalSrcIdx = 18;
	  section.data(19).dtTransOffset = 26;
	
	  ;% QuarkRefer_P.Gain5_Gain
	  section.data(20).logicalSrcIdx = 19;
	  section.data(20).dtTransOffset = 27;
	
	  ;% QuarkRefer_P.Gain6_Gain
	  section.data(21).logicalSrcIdx = 20;
	  section.data(21).dtTransOffset = 28;
	
	  ;% QuarkRefer_P.Gain7_Gain
	  section.data(22).logicalSrcIdx = 21;
	  section.data(22).dtTransOffset = 29;
	
	  ;% QuarkRefer_P.Gain8_Gain
	  section.data(23).logicalSrcIdx = 22;
	  section.data(23).dtTransOffset = 30;
	
	  ;% QuarkRefer_P.Gain9_Gain
	  section.data(24).logicalSrcIdx = 23;
	  section.data(24).dtTransOffset = 31;
	
	  ;% QuarkRefer_P.UniformRandomNumber_Minimum
	  section.data(25).logicalSrcIdx = 24;
	  section.data(25).dtTransOffset = 32;
	
	  ;% QuarkRefer_P.UniformRandomNumber_Maximum
	  section.data(26).logicalSrcIdx = 25;
	  section.data(26).dtTransOffset = 33;
	
	  ;% QuarkRefer_P.UniformRandomNumber1_Minimum
	  section.data(27).logicalSrcIdx = 26;
	  section.data(27).dtTransOffset = 34;
	
	  ;% QuarkRefer_P.UniformRandomNumber1_Maximum
	  section.data(28).logicalSrcIdx = 27;
	  section.data(28).dtTransOffset = 35;
	
	  ;% QuarkRefer_P.UniformRandomNumber2_Minimum
	  section.data(29).logicalSrcIdx = 28;
	  section.data(29).dtTransOffset = 36;
	
	  ;% QuarkRefer_P.UniformRandomNumber2_Maximum
	  section.data(30).logicalSrcIdx = 29;
	  section.data(30).dtTransOffset = 37;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(1) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (parameter)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    paramMap.nTotData = nTotData;
    


  ;%**************************
  ;% Create Block Output Map *
  ;%**************************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 2;
    sectIdxOffset = 0;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc sigMap
    ;%
    sigMap.nSections           = nTotSects;
    sigMap.sectIdxOffset       = sectIdxOffset;
      sigMap.sections(nTotSects) = dumSection; %prealloc
    sigMap.nTotData            = -1;
    
    ;%
    ;% Auto data (QuarkRefer_B)
    ;%
      section.nData     = 18;
      section.data(18)  = dumData; %prealloc
      
	  ;% QuarkRefer_B.Sum
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
	  ;% QuarkRefer_B.Saturation
	  section.data(2).logicalSrcIdx = 1;
	  section.data(2).dtTransOffset = 3;
	
	  ;% QuarkRefer_B.Gain
	  section.data(3).logicalSrcIdx = 2;
	  section.data(3).dtTransOffset = 6;
	
	  ;% QuarkRefer_B.LeftDevice_o2
	  section.data(4).logicalSrcIdx = 3;
	  section.data(4).dtTransOffset = 7;
	
	  ;% QuarkRefer_B.LeftDevice_o3
	  section.data(5).logicalSrcIdx = 4;
	  section.data(5).dtTransOffset = 10;
	
	  ;% QuarkRefer_B.Derivative
	  section.data(6).logicalSrcIdx = 5;
	  section.data(6).dtTransOffset = 13;
	
	  ;% QuarkRefer_B.Gain1
	  section.data(7).logicalSrcIdx = 6;
	  section.data(7).dtTransOffset = 16;
	
	  ;% QuarkRefer_B.Gain2
	  section.data(8).logicalSrcIdx = 7;
	  section.data(8).dtTransOffset = 17;
	
	  ;% QuarkRefer_B.TmpSignalConversionAtToWorkspac
	  section.data(9).logicalSrcIdx = 8;
	  section.data(9).dtTransOffset = 18;
	
	  ;% QuarkRefer_B.Gain3
	  section.data(10).logicalSrcIdx = 9;
	  section.data(10).dtTransOffset = 24;
	
	  ;% QuarkRefer_B.Gain5
	  section.data(11).logicalSrcIdx = 10;
	  section.data(11).dtTransOffset = 27;
	
	  ;% QuarkRefer_B.Gain6
	  section.data(12).logicalSrcIdx = 11;
	  section.data(12).dtTransOffset = 28;
	
	  ;% QuarkRefer_B.Gain7
	  section.data(13).logicalSrcIdx = 12;
	  section.data(13).dtTransOffset = 29;
	
	  ;% QuarkRefer_B.UniformRandomNumber
	  section.data(14).logicalSrcIdx = 13;
	  section.data(14).dtTransOffset = 30;
	
	  ;% QuarkRefer_B.UniformRandomNumber1
	  section.data(15).logicalSrcIdx = 14;
	  section.data(15).dtTransOffset = 31;
	
	  ;% QuarkRefer_B.UniformRandomNumber2
	  section.data(16).logicalSrcIdx = 15;
	  section.data(16).dtTransOffset = 32;
	
	  ;% QuarkRefer_B.Clock
	  section.data(17).logicalSrcIdx = 16;
	  section.data(17).dtTransOffset = 33;
	
	  ;% QuarkRefer_B.tau
	  section.data(18).logicalSrcIdx = 17;
	  section.data(18).dtTransOffset = 34;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(1) = section;
      clear section
      
      section.nData     = 2;
      section.data(2)  = dumData; %prealloc
      
	  ;% QuarkRefer_B.LeftDevice_o1
	  section.data(1).logicalSrcIdx = 18;
	  section.data(1).dtTransOffset = 0;
	
	  ;% QuarkRefer_B.LeftDevice_o4
	  section.data(2).logicalSrcIdx = 19;
	  section.data(2).dtTransOffset = 1;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(2) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (signal)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    sigMap.nTotData = nTotData;
    


  ;%*******************
  ;% Create DWork Map *
  ;%*******************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 5;
    sectIdxOffset = 2;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc dworkMap
    ;%
    dworkMap.nSections           = nTotSects;
    dworkMap.sectIdxOffset       = sectIdxOffset;
      dworkMap.sections(nTotSects) = dumSection; %prealloc
    dworkMap.nTotData            = -1;
    
    ;%
    ;% Auto data (QuarkRefer_DW)
    ;%
      section.nData     = 10;
      section.data(10)  = dumData; %prealloc
      
	  ;% QuarkRefer_DW.Memory2_Value
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
	  ;% QuarkRefer_DW.Memory1_Value
	  section.data(2).logicalSrcIdx = 1;
	  section.data(2).dtTransOffset = 3;
	
	  ;% QuarkRefer_DW.Memory_Value
	  section.data(3).logicalSrcIdx = 2;
	  section.data(3).dtTransOffset = 6;
	
	  ;% QuarkRefer_DW.TimeStampA
	  section.data(4).logicalSrcIdx = 3;
	  section.data(4).dtTransOffset = 9;
	
	  ;% QuarkRefer_DW.LastUAtTimeA
	  section.data(5).logicalSrcIdx = 4;
	  section.data(5).dtTransOffset = 10;
	
	  ;% QuarkRefer_DW.TimeStampB
	  section.data(6).logicalSrcIdx = 5;
	  section.data(6).dtTransOffset = 13;
	
	  ;% QuarkRefer_DW.LastUAtTimeB
	  section.data(7).logicalSrcIdx = 6;
	  section.data(7).dtTransOffset = 14;
	
	  ;% QuarkRefer_DW.UniformRandomNumber_NextOutput
	  section.data(8).logicalSrcIdx = 7;
	  section.data(8).dtTransOffset = 17;
	
	  ;% QuarkRefer_DW.UniformRandomNumber1_NextOutput
	  section.data(9).logicalSrcIdx = 8;
	  section.data(9).dtTransOffset = 18;
	
	  ;% QuarkRefer_DW.UniformRandomNumber2_NextOutput
	  section.data(10).logicalSrcIdx = 9;
	  section.data(10).dtTransOffset = 19;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(1) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% QuarkRefer_DW.LeftDevice_Phantom
	  section.data(1).logicalSrcIdx = 10;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(2) = section;
      clear section
      
      section.nData     = 28;
      section.data(28)  = dumData; %prealloc
      
	  ;% QuarkRefer_DW.Scope_PWORK.LoggedData
	  section.data(1).logicalSrcIdx = 11;
	  section.data(1).dtTransOffset = 0;
	
	  ;% QuarkRefer_DW.Scope1_PWORK.LoggedData
	  section.data(2).logicalSrcIdx = 12;
	  section.data(2).dtTransOffset = 1;
	
	  ;% QuarkRefer_DW.Scope10_PWORK.LoggedData
	  section.data(3).logicalSrcIdx = 13;
	  section.data(3).dtTransOffset = 2;
	
	  ;% QuarkRefer_DW.Scope11_PWORK.LoggedData
	  section.data(4).logicalSrcIdx = 14;
	  section.data(4).dtTransOffset = 3;
	
	  ;% QuarkRefer_DW.Scope12_PWORK.LoggedData
	  section.data(5).logicalSrcIdx = 15;
	  section.data(5).dtTransOffset = 4;
	
	  ;% QuarkRefer_DW.Scope13_PWORK.LoggedData
	  section.data(6).logicalSrcIdx = 16;
	  section.data(6).dtTransOffset = 5;
	
	  ;% QuarkRefer_DW.Scope14_PWORK.LoggedData
	  section.data(7).logicalSrcIdx = 17;
	  section.data(7).dtTransOffset = 6;
	
	  ;% QuarkRefer_DW.Scope15_PWORK.LoggedData
	  section.data(8).logicalSrcIdx = 18;
	  section.data(8).dtTransOffset = 7;
	
	  ;% QuarkRefer_DW.Scope16_PWORK.LoggedData
	  section.data(9).logicalSrcIdx = 19;
	  section.data(9).dtTransOffset = 8;
	
	  ;% QuarkRefer_DW.Scope17_PWORK.LoggedData
	  section.data(10).logicalSrcIdx = 20;
	  section.data(10).dtTransOffset = 9;
	
	  ;% QuarkRefer_DW.Scope2_PWORK.LoggedData
	  section.data(11).logicalSrcIdx = 21;
	  section.data(11).dtTransOffset = 10;
	
	  ;% QuarkRefer_DW.Scope3_PWORK.LoggedData
	  section.data(12).logicalSrcIdx = 22;
	  section.data(12).dtTransOffset = 11;
	
	  ;% QuarkRefer_DW.Scope4_PWORK.LoggedData
	  section.data(13).logicalSrcIdx = 23;
	  section.data(13).dtTransOffset = 12;
	
	  ;% QuarkRefer_DW.Scope5_PWORK.LoggedData
	  section.data(14).logicalSrcIdx = 24;
	  section.data(14).dtTransOffset = 13;
	
	  ;% QuarkRefer_DW.Scope6_PWORK.LoggedData
	  section.data(15).logicalSrcIdx = 25;
	  section.data(15).dtTransOffset = 14;
	
	  ;% QuarkRefer_DW.Scope7_PWORK.LoggedData
	  section.data(16).logicalSrcIdx = 26;
	  section.data(16).dtTransOffset = 15;
	
	  ;% QuarkRefer_DW.Scope8_PWORK.LoggedData
	  section.data(17).logicalSrcIdx = 27;
	  section.data(17).dtTransOffset = 16;
	
	  ;% QuarkRefer_DW.Scope9_PWORK.LoggedData
	  section.data(18).logicalSrcIdx = 28;
	  section.data(18).dtTransOffset = 17;
	
	  ;% QuarkRefer_DW.ToWorkspace_PWORK.LoggedData
	  section.data(19).logicalSrcIdx = 29;
	  section.data(19).dtTransOffset = 18;
	
	  ;% QuarkRefer_DW.ToWorkspace1_PWORK.LoggedData
	  section.data(20).logicalSrcIdx = 30;
	  section.data(20).dtTransOffset = 19;
	
	  ;% QuarkRefer_DW.Scope_PWORK_p.LoggedData
	  section.data(21).logicalSrcIdx = 31;
	  section.data(21).dtTransOffset = 20;
	
	  ;% QuarkRefer_DW.Scope1_PWORK_f.LoggedData
	  section.data(22).logicalSrcIdx = 32;
	  section.data(22).dtTransOffset = 21;
	
	  ;% QuarkRefer_DW.Scope2_PWORK_p.LoggedData
	  section.data(23).logicalSrcIdx = 33;
	  section.data(23).dtTransOffset = 22;
	
	  ;% QuarkRefer_DW.Scope3_PWORK_g.LoggedData
	  section.data(24).logicalSrcIdx = 34;
	  section.data(24).dtTransOffset = 23;
	
	  ;% QuarkRefer_DW.Scope4_PWORK_o.LoggedData
	  section.data(25).logicalSrcIdx = 35;
	  section.data(25).dtTransOffset = 24;
	
	  ;% QuarkRefer_DW.Scope5_PWORK_m.LoggedData
	  section.data(26).logicalSrcIdx = 36;
	  section.data(26).dtTransOffset = 25;
	
	  ;% QuarkRefer_DW.Scope6_PWORK_c.LoggedData
	  section.data(27).logicalSrcIdx = 37;
	  section.data(27).dtTransOffset = 26;
	
	  ;% QuarkRefer_DW.ToWorkspace2_PWORK.LoggedData
	  section.data(28).logicalSrcIdx = 38;
	  section.data(28).dtTransOffset = 27;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(3) = section;
      clear section
      
      section.nData     = 3;
      section.data(3)  = dumData; %prealloc
      
	  ;% QuarkRefer_DW.Memory2_ValueDims
	  section.data(1).logicalSrcIdx = 39;
	  section.data(1).dtTransOffset = 0;
	
	  ;% QuarkRefer_DW.Memory1_ValueDims
	  section.data(2).logicalSrcIdx = 40;
	  section.data(2).dtTransOffset = 1;
	
	  ;% QuarkRefer_DW.Memory_ValueDims
	  section.data(3).logicalSrcIdx = 41;
	  section.data(3).dtTransOffset = 2;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(4) = section;
      clear section
      
      section.nData     = 3;
      section.data(3)  = dumData; %prealloc
      
	  ;% QuarkRefer_DW.RandSeed
	  section.data(1).logicalSrcIdx = 42;
	  section.data(1).dtTransOffset = 0;
	
	  ;% QuarkRefer_DW.RandSeed_o
	  section.data(2).logicalSrcIdx = 43;
	  section.data(2).dtTransOffset = 1;
	
	  ;% QuarkRefer_DW.RandSeed_g
	  section.data(3).logicalSrcIdx = 44;
	  section.data(3).dtTransOffset = 2;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(5) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (dwork)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    dworkMap.nTotData = nTotData;
    


  ;%
  ;% Add individual maps to base struct.
  ;%

  targMap.paramMap  = paramMap;    
  targMap.signalMap = sigMap;
  targMap.dworkMap  = dworkMap;
  
  ;%
  ;% Add checksums to base struct.
  ;%


  targMap.checksum0 = 851540507;
  targMap.checksum1 = 3598186881;
  targMap.checksum2 = 642120379;
  targMap.checksum3 = 2771994871;

