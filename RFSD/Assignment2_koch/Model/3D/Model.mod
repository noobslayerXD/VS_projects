'# MWS Version: Version 2024.0 - Sep 01 2023 - ACIS 33.0.1 -

'# length = mm
'# frequency = MHz
'# time = ns
'# frequency range: fmin = 100 fmax = 1100
'# created = '[VERSION]2024.0|33.0.1|20230901[/VERSION]


'@ use template: Koch_fractal.cfg

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
'set the units
With Units
    .SetUnit "Length", "mm"
    .SetUnit "Frequency", "MHz"
    .SetUnit "Voltage", "V"
    .SetUnit "Resistance", "Ohm"
    .SetUnit "Inductance", "nH"
    .SetUnit "Temperature",  "degC"
    .SetUnit "Time", "ns"
    .SetUnit "Current", "A"
    .SetUnit "Conductance", "S"
    .SetUnit "Capacitance", "pF"
End With

ThermalSolver.AmbientTemperature "0"

'----------------------------------------------------------------------------

'set the frequency range
Solver.FrequencyRange "100", "1100"

'----------------------------------------------------------------------------

Plot.DrawBox True

With Background
     .Type "Normal"
     .Epsilon "1.0"
     .Mu "1.0"
     .XminSpace "0.0"
     .XmaxSpace "0.0"
     .YminSpace "0.0"
     .YmaxSpace "0.0"
     .ZminSpace "0.0"
     .ZmaxSpace "0.0"
End With

With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
End With

' optimize mesh settings for planar structures

With Mesh
     .MergeThinPECLayerFixpoints "True"
     .RatioLimit "20"
     .AutomeshRefineAtPecLines "True", "6"
     .FPBAAvoidNonRegUnite "True"
     .ConsiderSpaceForLowerMeshLimit "False"
     .MinimumStepNumber "5"
     .AnisotropicCurvatureRefinement "True"
     .AnisotropicCurvatureRefinementFSM "True"
End With

With MeshSettings
     .SetMeshType "Hex"
     .Set "RatioLimitGeometry", "20"
     .Set "EdgeRefinementOn", "1"
     .Set "EdgeRefinementRatio", "6"
End With

With MeshSettings
     .SetMeshType "HexTLM"
     .Set "RatioLimitGeometry", "20"
End With

With MeshSettings
     .SetMeshType "Tet"
     .Set "VolMeshGradation", "1.5"
     .Set "SrfMeshGradation", "1.5"
End With

' change mesh adaption scheme to energy
' 		(planar structures tend to store high energy
'     	 locally at edges rather than globally in volume)

MeshAdaption3D.SetAdaptionStrategy "Energy"

' switch on FD-TET setting for accurate farfields

FDSolver.ExtrudeOpenBC "True"

PostProcess1D.ActivateOperation "vswr", "true"
PostProcess1D.ActivateOperation "yz-matrices", "true"

With FarfieldPlot
	.ClearCuts ' lateral=phi, polar=theta
	.AddCut "lateral", "0", "1"
	.AddCut "lateral", "90", "1"
	.AddCut "polar", "90", "1"
End With

'----------------------------------------------------------------------------

With MeshSettings
     .SetMeshType "Hex"
     .Set "Version", 1%
End With

With Mesh
     .MeshType "PBA"
End With

'set the solver type
ChangeSolverType("HF Time Domain")

'----------------------------------------------------------------------------

'@ define material: Denim

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Material
     .Reset
     .Name "Denim"
     .Folder ""
     .Rho "0"
     .ThermalType "Normal"
     .ThermalConductivity "0"
     .SpecificHeat "0", "J/K/kg"
     .DynamicViscosity "0"
     .UseEmissivity "True"
     .Emissivity "0"
     .MetabolicRate "0.0"
     .VoxelConvection "0.0"
     .BloodFlow "0"
     .Absorptance "0"
     .MechanicsType "Unused"
     .IntrinsicCarrierDensity "0"
     .FrqType "all"
     .Type "Normal"
     .MaterialUnit "Frequency", "MHz"
     .MaterialUnit "Geometry", "mm"
     .MaterialUnit "Time", "ns"
     .MaterialUnit "Temperature", "degC"
     .Epsilon "1.6"
     .Mu "1"
     .Sigma "0.0"
     .TanD "0.025"
     .TanDFreq "450"
     .TanDGiven "True"
     .TanDModel "ConstTanD"
     .SetConstTanDStrategyEps "AutomaticOrder"
     .ConstTanDModelOrderEps "3"
     .DjordjevicSarkarUpperFreqEps "0"
     .SetElParametricConductivity "False"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .SigmaM "0"
     .TanDM "0.0"
     .TanDMFreq "0.0"
     .TanDMGiven "False"
     .TanDMModel "ConstTanD"
     .SetConstTanDStrategyMu "AutomaticOrder"
     .ConstTanDModelOrderMu "3"
     .DjordjevicSarkarUpperFreqMu "0"
     .SetMagParametricConductivity "False"
     .DispModelEps "None"
     .DispModelMu "None"
     .DispersiveFittingSchemeEps "Nth Order"
     .MaximalOrderNthModelFitEps "10"
     .ErrorLimitNthModelFitEps "0.1"
     .DispersiveFittingSchemeMu "Nth Order"
     .MaximalOrderNthModelFitMu "10"
     .ErrorLimitNthModelFitMu "0.1"
     .UseGeneralDispersionEps "False"
     .UseGeneralDispersionMu "False"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Colour "0", "1", "1" 
     .Wireframe "False" 
     .Reflection "False" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .Create
End With

'@ new component: component1

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Component.New "component1"

'@ define brick: component1:Substrate

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Brick
     .Reset 
     .Name "Substrate" 
     .Component "component1" 
     .Material "Denim" 
     .Xrange "-115", "115" 
     .Yrange "-10", "40" 
     .Zrange "-2.84", "0" 
     .Create
End With

'@ define curve polygon: curve1:polygon1

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Polygon 
     .Reset 
     .Name "polygon1" 
     .Curve "curve1" 
     .Point "0", "0" 
     .LineTo "9", "0" 
     .LineTo "15", "6" 
     .LineTo "21", "0" 
     .LineTo "33", "0" 
     .LineTo "40", "5" 
     .LineTo "35", "9" 
     .LineTo "43", "9" 
     .LineTo "48", "15" 
     .LineTo "53", "9" 
     .LineTo "61", "9" 
     .LineTo "55", "4" 
     .LineTo "59", "0" 
     .LineTo "71", "0" 
     .LineTo "79", "5" 
     .LineTo "86", "0" 
     .LineTo "95", "0" 
     .Create 
End With 


'@ transform curve: translate curve1

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Transform 
     .Reset 
     .Name "curve1" 
     .Vector "-0", "0", "0" 
     .UsePickedPoints "False" 
     .InvertPickedPoints "False" 
     .MultipleObjects "False" 
     .GroupObjects "False" 
     .Repetitions "2" 
     .MultipleSelection "False" 
     .Transform "Curve", "Translate" 
End With

'@ delete curve: curve1

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Curve.DeleteCurve "curve1"

'@ define brick: component1:wirePart

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Brick
     .Reset 
     .Name "wirePart" 
     .Component "component1" 
     .Material "PEC" 
     .Xrange "0.1", "25" 
     .Yrange "-1.875", "1.875" 
     .Zrange "2.84", "6.59" 
     .Create
End With

'@ delete shape: component1:wirePart

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Solid.Delete "component1:wirePart"

'@ import step file: C:\Users\jacob\Downloads\koch_dipole.step

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With STEP
     .Reset 
     .ScaleToUnit "0" 
     .FileName "*koch_dipole.step" 
     .Id "1" 
     .Version "11.0" 
     .ImportToActiveCoordinateSystem "True" 
     .Curves "True" 
     .ImportAttributes "True" 
     .ImportCurveAttributes "True" 
     .UpdateMaterialPropertiesFromMaterialLibrary "False" 
     .Read 
End With

'@ define material: Arm_left

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Material 
     .Reset 
     .Name "Arm_left"
     .Folder ""
     .Rho "0"
     .ThermalType "Normal"
     .ThermalConductivity "0"
     .SpecificHeat "0", "J/K/kg"
     .DynamicViscosity "0"
     .UseEmissivity "True"
     .Emissivity "0"
     .MetabolicRate "0.0"
     .VoxelConvection "0.0"
     .BloodFlow "0"
     .Absorptance "0"
     .MechanicsType "Unused"
     .IntrinsicCarrierDensity "0"
     .FrqType "all"
     .Type "Pec"
     .MaterialUnit "Frequency", "MHz"
     .MaterialUnit "Geometry", "mm"
     .MaterialUnit "Time", "s"
     .Epsilon "1.0"
     .Mu "1.0"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Colour "0.85", "0.55", "0.2" 
     .Wireframe "False" 
     .Reflection "False" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .Create
End With

'@ define material colour: Arm_left

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Material 
     .Name "Arm_left"
     .Folder ""
     .Colour "0.85", "0.55", "0.2" 
     .Wireframe "False" 
     .Reflection "False" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .ChangeColour 
End With

'@ define discrete port: 1

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With DiscretePort 
     .Reset 
     .PortNumber "1" 
     .Type "SParameter"
     .Label ""
     .Folder ""
     .Impedance "50.0"
     .Voltage "1.0"
     .Current "1.0"
     .Monitor "True"
     .Radius "0.0"
     .SetP1 "False", "-1", "0.0", "0.0"
     .SetP2 "False", "1", "0.0", "0.0"
     .InvertDirection "False"
     .LocalCoordinates "False"
     .Wire ""
     .Position "end1"
     .Create 
End With

'@ define time domain solver parameters

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Mesh.SetCreator "High Frequency" 

With Solver 
     .Method "Hexahedral"
     .CalculationType "TD-S"
     .StimulationPort "All"
     .StimulationMode "All"
     .SteadyStateLimit "-40"
     .MeshAdaption "False"
     .AutoNormImpedance "False"
     .NormingImpedance "50"
     .CalculateModesOnly "False"
     .SParaSymmetry "False"
     .StoreTDResultsInCache  "False"
     .RunDiscretizerOnly "False"
     .FullDeembedding "False"
     .SuperimposePLWExcitation "False"
     .UseSensitivityAnalysis "False"
End With

'@ set PBA version

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Discretizer.PBAVersion "2023090124"

'@ define farfield monitor: farfield (f=450)

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor 
     .Reset 
     .Name "farfield (f=450)" 
     .Domain "Frequency" 
     .FieldType "Farfield" 
     .MonitorValue "450" 
     .ExportFarfieldSource "False" 
     .UseSubvolume "False" 
     .Coordinates "Structure" 
     .SetSubvolume "-115", "115", "-10", "40", "0", "2.84" 
     .SetSubvolumeOffset "10", "10", "10", "10", "10", "10" 
     .SetSubvolumeInflateWithOffset "False" 
     .SetSubvolumeOffsetType "FractionOfWavelength" 
     .EnableNearfieldCalculation "True" 
     .Create 
End With

'@ farfield plot options

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With FarfieldPlot 
     .Plottype "3D" 
     .Vary "angle2" 
     .Theta "90" 
     .Phi "90" 
     .Step "5" 
     .Step2 "5" 
     .SetLockSteps "True" 
     .SetPlotRangeOnly "False" 
     .SetThetaStart "0" 
     .SetThetaEnd "180" 
     .SetPhiStart "0" 
     .SetPhiEnd "360" 
     .SetTheta360 "False" 
     .SymmetricRange "False" 
     .SetTimeDomainFF "False" 
     .SetFrequency "450" 
     .SetTime "0" 
     .SetColorByValue "True" 
     .DrawStepLines "False" 
     .DrawIsoLongitudeLatitudeLines "False" 
     .ShowStructure "False" 
     .ShowStructureProfile "False" 
     .SetStructureTransparent "False" 
     .SetFarfieldTransparent "False" 
     .AspectRatio "Free" 
     .ShowGridlines "True" 
     .InvertAxes "False", "False" 
     .SetSpecials "enablepolarextralines" 
     .SetPlotMode "Directivity" 
     .Distance "1" 
     .UseFarfieldApproximation "True" 
     .IncludeUnitCellSidewalls "True" 
     .SetScaleLinear "False" 
     .SetLogRange "40" 
     .SetLogNorm "0" 
     .DBUnit "0" 
     .SetMaxReferenceMode "abs" 
     .EnableFixPlotMaximum "False" 
     .SetFixPlotMaximumValue "1.0" 
     .SetInverseAxialRatio "False" 
     .SetAxesType "user" 
     .SetAntennaType "unknown" 
     .Phistart "1.000000e+00", "0.000000e+00", "0.000000e+00" 
     .Thetastart "0.000000e+00", "0.000000e+00", "1.000000e+00" 
     .PolarizationVector "0.000000e+00", "1.000000e+00", "0.000000e+00" 
     .SetCoordinateSystemType "spherical" 
     .SetAutomaticCoordinateSystem "True" 
     .SetPolarizationType "Linear" 
     .SlantAngle 0.000000e+00 
     .Origin "bbox" 
     .Userorigin "0.000000e+00", "0.000000e+00", "0.000000e+00" 
     .SetUserDecouplingPlane "False" 
     .UseDecouplingPlane "False" 
     .DecouplingPlaneAxis "X" 
     .DecouplingPlanePosition "0.000000e+00" 
     .LossyGround "False" 
     .GroundEpsilon "1" 
     .GroundKappa "0" 
     .EnablePhaseCenterCalculation "False" 
     .SetPhaseCenterAngularLimit "3.000000e+01" 
     .SetPhaseCenterComponent "boresight" 
     .SetPhaseCenterPlane "both" 
     .ShowPhaseCenter "True" 
     .ClearCuts 
     .AddCut "lateral", "0", "1"  
     .AddCut "lateral", "90", "1"  
     .AddCut "polar", "90", "1"  

     .StoreSettings
End With

'@ define brick: Koch_dipole/Arm_right:GND

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Brick
     .Reset 
     .Name "GND" 
     .Component "Koch_dipole/Arm_right" 
     .Material "Denim" 
     .Xrange "-100", "100" 
     .Yrange "-20", "20" 
     .Zrange "-2.875", "2.84" 
     .Create
End With

'@ define brick: Koch_dipole/Arm_right:GND1

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Brick
     .Reset 
     .Name "GND1" 
     .Component "Koch_dipole/Arm_right" 
     .Material "Denim" 
     .Xrange "-100", "100" 
     .Yrange "-10", "10" 
     .Zrange "-2.875", "-2.84" 
     .Create
End With

'@ boolean insert shapes: Koch_dipole/Arm_right:GND, Koch_dipole/Arm_right:GND1

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Solid.Insert "Koch_dipole/Arm_right:GND", "Koch_dipole/Arm_right:GND1"

'@ delete shape: Koch_dipole/Arm_right:GND

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Solid.Delete "Koch_dipole/Arm_right:GND"

'@ delete shape: Koch_dipole/Arm_right:GND1

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Solid.Delete "Koch_dipole/Arm_right:GND1"

'@ define brick: component1:GND

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Brick
     .Reset 
     .Name "GND" 
     .Component "component1" 
     .Material "PEC" 
     .Xrange "-115", "115" 
     .Yrange "-10", "40" 
     .Zrange "-2.875", "-2.84" 
     .Create
End With

'@ delete shape: component1:GND

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Solid.Delete "component1:GND"

'@ clear picks

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Pick.ClearAllPicks

'@ pick end point

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Pick.PickEndpointFromId "Koch_dipole/Arm_left:Arm_left", "65"

'@ pick end point

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Pick.PickEndpointFromId "Koch_dipole/Arm_right:Arm_right", "33"

'@ define distance dimension

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Dimension
    .Reset
    .CreationType "picks"
    .SetType "Distance"
    .SetID "0"
    .SetOrientation "Smart Mode"
    .SetDistance "-20.053677"
    .SetViewVector "-0.055555", "-0.060766", "-0.996605"
    .SetConnectedElement1 "Koch_dipole/Arm_left:Arm_left"
    .SetConnectedElement2 "Koch_dipole/Arm_right:Arm_right"
    .Create
End With

Pick.ClearAllPicks

